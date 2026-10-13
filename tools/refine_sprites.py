"""
Turns the hand-drawn character sprites into a cleaner "digital" look so they
sit better on the painted backgrounds, without changing anyone's proportions,
face or hair.

For each character it reads the full-size drawing (game/images/*_original.png,
which stays untouched) and:

  1. separates the ink lines from the colour fills,
  2. traces every line, fits a smooth curve through it (this takes the shake
     out of long strokes but keeps them on the drawn path) and redraws it
     thinner, with even width and tapered ends. Fine details (eyes, eyebrows,
     noses, mouths, hair strands) are kept exactly as drawn,
  3. colours the lines with a dark shade of the colour next to them instead of
     pure black,
  4. adds two-tone cel shading and a soft rim light to each painted area, lit
     from the upper left (faces only get the soft shading, so they stay as
     drawn), and
  5. saves the in-game sprite (game/images/<name>.png), and the waist-up
     close-ups cut from it, at the same size and framing as before, so nothing
     in the scripts needs to change.

Needs numpy, scipy, scikit-image, opencv-python-headless and Pillow. Run from
the project root:

    python3 tools/refine_sprites.py            # every character
    python3 tools/refine_sprites.py gus emma   # just these
"""

import os
import sys

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from scipy.interpolate import splev, splprep
from skimage.morphology import skeletonize

IMAGES = os.path.join(os.path.dirname(__file__), "..", "game", "images")

## Working resolution. The originals are 8192 square; half of that is plenty.
WORK = 4096

## Which drawing makes which sprite, and the sprite's canvas size.
SPRITES = {
    "elena": ("Elena_original.png", 900),
    "emma": ("Emma_original.png", 1000),
    "gus": ("Gus_original.png", 1000),
    "zane": ("Zane_original.png", 1000),
}

## The waist-up close-ups are crops of the full drawings: which sprite, the
## crop box in the original's 8192 pixel space, and the close-up's canvas size.
CLOSEUPS = {
    "elenaclassroom": ("elena", (2460, 0, 6128, 3668), 900),
    "emmabus": ("emma", (2064, 0, 6272, 4208), 1000),
}

## Ink is anything this dark (0-255 luminance).
INK_LUMA = 32

## Ink more than this many times as thick as the drawing's usual lines is a
## filled black shape (hair, shoes), not a line.
SOLID_FACTOR = 1.6 / 2

## Lines thinner than this (working pixels) are details such as eyes, teeth
## and hair strands. They are kept exactly as drawn, only recoloured. So is
## every separate little drawing smaller than DETAIL_SIZE across: eyes,
## eyebrows, noses, mouths, buttons.
DETAIL_WIDTH = 9
DETAIL_SIZE = 260

## Lines get redrawn at this fraction of their drawn width (the outline round
## the whole character keeps a bit more)...
WIDTH_SCALE = 0.55
OUTLINE_SCALE = 0.72
## ...but never thinner than this many working pixels.
MIN_WIDTH = 4.0

## How far (as a fraction of the line width, plus a little) a smoothed line may
## drift from the drawn one. Bigger is straighter.
DRIFT = 0.30
DRIFT_MIN = 1.2

## Light direction: x right, y down, z towards the viewer.
LIGHT = np.array([-0.55, -0.65, 0.55])
LIGHT = LIGHT / np.linalg.norm(LIGHT)

## Shadow colour the fills are multiplied by, and how bright the rim light is.
SHADOW_TINT = np.array([0.82, 0.79, 0.90])
## Height (working pixels) the shading surface levels off at.
PLATEAU = 70.0
RIM_LIGHT = 0.10


def luma(rgb):
    return rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


## Step 1: lines and fills ####################################################

def split_ink(rgba):
    """
    Returns (ink, opaque). Ink is the line art; solid black areas (such as
    black hair or shoes) are treated as fills, not lines.
    """

    alpha = rgba[..., 3]
    opaque = alpha > 127
    ink = opaque & (luma(rgba[..., :3]) < INK_LUMA)
    # Some strokes were drawn with a textured brush and are full of pinholes.
    ink |= ndi.binary_closing(ink, structure=disk(2)) & opaque
    ink = ndi.binary_opening(ink, structure=disk(1))

    # Anything that survives opening with a disk wider than the thickest line
    # is a filled shape, not a line. How thick "thick" is depends on the
    # drawing, so measure the lines first.
    widths = ndi.distance_transform_edt(ink)[skeletonize(ink)] * 2.0
    radius = int(np.ceil(np.percentile(widths, 90) * SOLID_FACTOR))
    solid = ndi.binary_opening(ink, structure=disk(radius))
    lab, n = ndi.label(solid)
    if n:
        sizes = ndi.sum(solid, lab, range(1, n + 1))
        keep = np.zeros(n + 1, bool)
        keep[1:] = sizes > 1500
        # Heavy black lines bunched up on skin (fingers drawn over each
        # other) are still lines.
        ring = ndi.grey_dilation(lab, footprint=disk(radius)) * (opaque & ~ink)
        idx = np.arange(1, n + 1)
        ring_size = np.maximum(ndi.sum(ring > 0, ring, idx), 1)
        around = np.stack([ndi.sum(rgba[..., c].astype(float), ring, idx) / ring_size
                           for c in range(3)], 1)
        keep[1:] &= ~(is_skin(around) & (sizes < 15000))
        solid = keep[lab]
    # The thin black wedges between solid patches (say between shoelaces)
    # belong to the patch too.
    solid = ndi.binary_dilation(solid, structure=disk(radius * 3 // 2)) & ink

    return ink & ~solid, opaque


def label_fills(rgba, ink, opaque):
    """
    Splits everything that isn't ink into painted areas. Label 1 is the
    transparent outside, 2.. are areas enclosed by lines and 0 is not decided
    yet (ink, and the fringe round it).
    """

    fill = opaque & ~ink
    # Drop the anti-aliased fringe next to lines, which is muddied with black.
    fill &= ~ndi.binary_dilation(ink, iterations=2)
    lab, n = ndi.label(fill)
    lab = lab + 1
    lab[~fill] = 0
    lab[~opaque & ~ndi.binary_dilation(ink, iterations=2)] = 1

    # Tiny specks of fill (gaps in hatching and so on) are dropped as well.
    sizes = np.bincount(lab.ravel())
    lab[(sizes[lab] < 40) & (lab > 1)] = 0
    return lab


## Step 2: tracing and smoothing lines ########################################

NEIGHBOURS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def trace_paths(skel):
    """
    Breaks a one pixel skeleton into simple paths. Returns a list of
    (points, start_is_junction, end_is_junction, closed) and the junction
    pixels.
    """

    sk = skel.astype(np.uint8)
    count = ndi.convolve(sk, np.ones((3, 3), np.uint8), mode="constant") - sk
    count[~skel] = 0
    junction = skel & (count >= 3)
    body = skel & ~junction

    h, w = skel.shape
    jy, jx = np.nonzero(junction)
    jset = set(zip(jy.tolist(), jx.tolist()))

    visited = np.zeros_like(skel)
    paths = []

    by, bx = np.nonzero(body)
    bcount = ndi.convolve(body.astype(np.uint8), np.ones((3, 3), np.uint8), mode="constant") - body
    ends = body & (bcount <= 1)
    ey, ex = np.nonzero(ends)

    def walk(y, x):
        pts = [(y, x)]
        visited[y, x] = True
        while True:
            nxt = None
            for dy, dx in NEIGHBOURS:
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w:
                    if body[yy, xx] and not visited[yy, xx]:
                        nxt = (yy, xx)
                        break
            if nxt is None:
                break
            y, x = nxt
            visited[y, x] = True
            pts.append(nxt)
        return pts

    def junction_next_to(p):
        y, x = p
        for dy, dx in NEIGHBOURS:
            if (y + dy, x + dx) in jset:
                return (y + dy, x + dx)
        return None

    for y, x in zip(ey.tolist(), ex.tolist()):
        if visited[y, x]:
            continue
        pts = walk(y, x)
        js = junction_next_to(pts[0])
        je = junction_next_to(pts[-1])
        if js is not None:
            pts.insert(0, js)
        if je is not None and (len(pts) > 1 or js is None):
            pts.append(je)
        paths.append((np.array(pts, float), js is not None, je is not None, False))

    # What's left are closed loops with no ends.
    for y, x in zip(by.tolist(), bx.tolist()):
        if visited[y, x]:
            continue
        pts = walk(y, x)
        paths.append((np.array(pts, float), False, False, True))

    return paths, junction


def smooth_path(pts, widths, closed):
    """
    Fits a smoothing spline through a traced path, letting it drift a little
    from the drawn line so the shake disappears. Returns resampled points and
    widths.
    """

    n = len(pts)
    w = float(np.median(widths))
    tol = max(DRIFT_MIN, DRIFT * w)

    if n < 6:
        return pts, np.full(n, w)

    # Subsample long paths; a point every couple of pixels is enough.
    step = max(1, int(round(w / 6)))
    idx = np.arange(0, n, step)
    if idx[-1] != n - 1:
        idx = np.append(idx, n - 1)
    p = pts[idx]
    m = len(p)
    if m < 4:
        return pts, np.full(n, w)

    # Pin the ends so lines still meet where they did.
    weights = np.ones(m)
    if not closed:
        weights[0] = weights[-1] = 50.0

    try:
        if closed:
            p = np.vstack([p, p[:1]])
            weights = np.append(weights, 1.0)
            tck, _ = splprep([p[:, 1], p[:, 0]], w=weights, s=len(p) * tol * tol, per=1, k=3)
        else:
            tck, _ = splprep([p[:, 1], p[:, 0]], w=weights, s=m * tol * tol, k=3)
    except Exception:
        return pts, np.full(n, w)

    seg = np.sqrt((np.diff(pts, axis=0) ** 2).sum(1)).sum()
    k = max(8, int(seg / 1.5))
    u = np.linspace(0, 1, k)
    x, y = splev(u, tck)
    out = np.stack([y, x], 1)

    # Even width along the line, eased a little to follow the drawing.
    wi = np.interp(np.linspace(0, len(widths) - 1, k), np.arange(len(widths)), widths)
    wi = ndi.gaussian_filter1d(wi, max(2.0, k / 6), mode="nearest")
    wi = 0.5 * wi + 0.5 * w
    return out, wi


def render_lines(shape, strokes):
    """
    Draws the smoothed strokes as an anti-aliased coverage mask (0-1).
    strokes: list of (points[y, x], widths).
    """

    h, w = shape
    canvas = np.zeros((h, w), np.uint8)
    shift = 4
    scale = 1 << shift
    for pts, wid in strokes:
        if len(pts) == 1:
            r = int(round(wid[0] / 2 * scale))
            c = (int(pts[0, 1] * scale), int(pts[0, 0] * scale))
            cv2.circle(canvas, c, r, 255, -1, cv2.LINE_AA, shift)
            continue
        for i in range(len(pts) - 1):
            t = max(1, int(round((wid[i] + wid[i + 1]) / 2)))
            a = (int(pts[i, 1] * scale), int(pts[i, 0] * scale))
            b = (int(pts[i + 1, 1] * scale), int(pts[i + 1, 0] * scale))
            cv2.line(canvas, a, b, 255, t, cv2.LINE_AA, shift)
    return canvas.astype(np.float32) / 255.0


def taper(wid, start_free, end_free):
    """Narrows the free ends of a stroke, like a pen lifting off."""

    k = len(wid)
    if k < 3:
        return wid
    ramp = max(2, min(k // 3, int(wid.mean() * 3)))
    f = np.ones(k)
    r = np.linspace(0.25, 1.0, ramp)
    if start_free:
        f[:ramp] = np.minimum(f[:ramp], r)
    if end_free:
        f[-ramp:] = np.minimum(f[-ramp:], r[::-1])
    return wid * f


def side_labels(pts, widths, near):
    """The most common area label on each side of a traced path."""

    t = np.gradient(ndi.gaussian_filter1d(pts, 2.0, axis=0, mode="nearest"), axis=0)
    t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-6)
    normal = np.stack([-t[:, 1], t[:, 0]], 1)
    off = (widths / 2 + 4)[:, None] * normal
    h, w = near.shape
    out = []
    for sign in (1, -1):
        q = np.rint(pts + sign * off).astype(int)
        q[:, 0] = np.clip(q[:, 0], 0, h - 1)
        q[:, 1] = np.clip(q[:, 1], 0, w - 1)
        out.append(np.bincount(near[q[:, 0], q[:, 1]]).argmax())
    return out


def redraw_lines(ink, lab, skin):
    """
    Traces the ink and redraws every line of at least DETAIL_WIDTH as a clean
    stroke. Lines drawn inside skin (eyebrows, noses, knuckles) are left alone
    so faces don't change. Returns (inner, outer, detail): coverage (0-1) of
    the redrawn inner lines and outline, and the mask of drawn ink that is kept
    as it is.
    """

    # Small separate drawings are kept whole.
    parts, n = ndi.label(ink, structure=np.ones((3, 3)))
    small = np.zeros(n + 1, bool)
    for i, sl in enumerate(ndi.find_objects(parts), 1):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        small[i] = np.hypot(h, w) < DETAIL_SIZE
    kept = small[parts]
    ink = ink & ~kept

    dist = ndi.distance_transform_edt(ink)
    skel = skeletonize(ink)
    paths, junction = trace_paths(skel)

    # The outline is anything running along the transparent outside.
    outside = lab == 1
    out_dist = ndi.distance_transform_edt(~outside)
    _, (ly, lx) = ndi.distance_transform_edt(lab == 0, return_indices=True)
    near = lab[ly, lx]

    inner, outer = [], []
    redrawn = np.zeros(ink.shape, bool)
    for pts, js, je, closed in paths:
        iy, ix = pts[:, 0].astype(int), pts[:, 1].astype(int)
        widths = dist[iy, ix] * 2.0
        length = len(pts)
        mw = float(np.median(widths))

        if mw < DETAIL_WIDTH:
            continue

        a, b = side_labels(pts, widths, near)
        if a == b and skin[a]:
            continue

        redrawn[iy, ix] = True

        # Skeleton spurs: short branches sticking off a junction into the
        # thickness of a line.
        if (js != je) and length < mw * 1.2:
            continue

        sp, sw = smooth_path(pts, widths, closed)
        is_outer = (out_dist[iy, ix] < widths / 2 + 5).mean() > 0.5
        sw = np.maximum(sw * (OUTLINE_SCALE if is_outer else WIDTH_SCALE), MIN_WIDTH)
        if not closed:
            sw = taper(sw, not js, not je)
        (outer if is_outer else inner).append((sp, sw))

    # Junction pixels go with the redrawn lines that end in them.
    jl, nj = ndi.label(junction, structure=np.ones((3, 3)))
    touched = np.zeros(nj + 1, bool)
    touched[np.unique(jl[ndi.binary_dilation(redrawn & ~junction, structure=np.ones((3, 3)))])] = True
    touched[0] = False
    redrawn |= touched[jl]

    # Every ink pixel belongs to the line whose middle is nearest to it.
    _, (ny, nx) = ndi.distance_transform_edt(~skel, return_indices=True)
    detail = (ink & ~redrawn[ny, nx]) | kept

    return render_lines(ink.shape, inner), render_lines(ink.shape, outer), detail


## Step 3: fills under the new lines ##########################################

def grow_labels(lab, walls, iterations):
    """
    Spreads labels into the unlabelled (0) pixels without crossing walls,
    then fills whatever is left from the nearest label.
    """

    lab = lab.copy()
    free = ~walls
    for _ in range(iterations):
        empty = (lab == 0) & free
        if not empty.any():
            break
        grown = ndi.grey_dilation(lab, size=(3, 3))
        lab[empty] = grown[empty]

    empty = lab == 0
    if empty.any():
        _, (iy, ix) = ndi.distance_transform_edt(empty, return_indices=True)
        lab = lab[iy, ix]
    return lab


def area_colours(rgba, lab, n, clean):
    """
    The flat colour of each area, from the pixels well away from any line.
    """

    rgb = rgba[..., :3].astype(np.float64)
    cols = np.zeros((n, 3))
    idx = np.arange(n)
    count = ndi.sum(clean, lab, idx)
    count_all = np.bincount(lab.ravel(), minlength=n)
    for c in range(3):
        m_clean = ndi.sum(rgb[..., c] * clean, lab, idx) / np.maximum(count, 1)
        m_all = ndi.sum(rgb[..., c], lab, idx) / np.maximum(count_all, 1)
        cols[:, c] = np.where(count > 0, m_clean, m_all)
    return cols


## Step 4: shading ############################################################

def label_adjacency(lab):
    """Counts how many pixel edges each pair of labels shares."""

    n = int(lab.max()) + 1
    pairs = []
    for a, b in ((lab[:-1], lab[1:]), (lab[:, :-1], lab[:, 1:])):
        d = a != b
        pairs.append(np.stack([a[d], b[d]], 1))
    pairs = np.concatenate(pairs)
    pairs = np.concatenate([pairs, pairs[:, ::-1]])
    key = pairs[:, 0].astype(np.int64) * n + pairs[:, 1]
    key, count = np.unique(key, return_counts=True)
    return key // n, key % n, count


def surface_labels(lab, area, outside_label=1):
    """
    Small patches sitting on a bigger area (pockets, buttons, logos, eyes) are
    part of that area's surface: they shouldn't make dents in it. Returns the
    parent of every label: itself, or the area it has been merged into.
    """

    n = len(area)
    a, b, count = label_adjacency(lab)
    parent = np.arange(n)
    best = np.zeros(n, np.int64)
    best_count = np.zeros(n, np.int64)
    out_count = np.zeros(n, np.int64)
    total = np.zeros(n, np.int64)
    np.add.at(total, a, count)
    for i, j, c in zip(a.tolist(), b.tolist(), count.tolist()):
        if j == outside_label:
            out_count[i] += c
        elif c > best_count[i]:
            best[i], best_count[i] = j, c

    for i in range(2, n):
        j = best[i]
        if best_count[i] == 0 or out_count[i] > 0.2 * total[i]:
            continue
        if area[i] < 0.08 * area[j]:
            parent[i] = j

    # Follow chains (a button on a pocket on a jacket).
    for _ in range(8):
        parent = parent[parent]
    return parent


def inflate(lab, shaded_labels, scale=4):
    """
    Puffs every painted area up into a smooth rounded surface, as if it were
    a cushion the shape of the area, and returns its height. Solved at
    1/scale resolution: inside each area the height satisfies
    laplacian(h) = -1 with h = 0 on its edge, and 2*sqrt(h) of that is an exact
    hemisphere for a circle.
    """

    from scipy.sparse import csr_matrix
    from scipy.sparse.linalg import spsolve

    small = lab[scale // 2::scale, scale // 2::scale]
    same = np.ones(small.shape, bool)
    same[1:] &= small[1:] == small[:-1]
    same[:-1] &= small[:-1] == small[1:]
    same[:, 1:] &= small[:, 1:] == small[:, :-1]
    same[:, :-1] &= small[:, :-1] == small[:, 1:]
    same[0] = same[-1] = False
    same[:, 0] = same[:, -1] = False
    inner = same & shaded_labels[small]

    idx = -np.ones(small.shape, np.int64)
    ys, xs = np.nonzero(inner)
    k = len(ys)
    idx[ys, xs] = np.arange(k)
    rows = [np.arange(k)]
    cols = [np.arange(k)]
    vals = [np.full(k, 4.0)]
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nb = idx[ys + dy, xs + dx]
        ok = nb >= 0
        rows.append(np.arange(k)[ok])
        cols.append(nb[ok])
        vals.append(np.full(ok.sum(), -1.0))

    A = csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                   shape=(k, k))
    sol = spsolve(A, np.ones(k))

    height = np.zeros(small.shape, np.float32)
    height[ys, xs] = 2.0 * np.sqrt(np.maximum(sol, 0)) * scale
    height = cv2.resize(height, (lab.shape[1], lab.shape[0]), interpolation=cv2.INTER_LINEAR)
    return cv2.GaussianBlur(height, (0, 0), scale)


def is_skin(cols):
    """Which area colours look like skin: pale, warm, not very saturated."""

    rgb = cols / 255.0
    mx, mn = rgb.max(1), rgb.min(1)
    sat = (mx - mn) / np.maximum(mx, 1e-6)
    r, g, b = rgb[:, 0], rgb[:, 1], rgb[:, 2]
    return (r >= g) & (r >= b) & (g >= b * 0.92) & (mx > 0.75) & (sat > 0.04) & (sat < 0.42)


def shade(lab, cols, outside_label=1):
    """
    Lights the inflated surface. Returns n.l per pixel, and how strongly each
    pixel takes the cel shadow and the soft shading (0 for areas too small to
    bother with; faces get no hard shadow so they stay clean).
    """

    n = int(lab.max()) + 1
    area = np.bincount(lab.ravel(), minlength=n)
    parent = surface_labels(lab, area, outside_label)
    surf = parent[lab]
    sarea = np.bincount(surf.ravel(), minlength=n)
    # A face is skin with features (eyes, mouth) on it.
    features = np.bincount(parent[parent != np.arange(n)], minlength=n)

    shaded = sarea > 2500
    shaded[outside_label] = False
    shaded[0] = False

    skin = is_skin(cols)
    face = skin & (features >= 2)
    strength = np.where(face, 0.0, np.where(skin, 0.6, 1.0))[surf] * shaded[surf]
    soft_strength = np.where(skin, 0.6, 1.0)[surf] * shaded[surf]

    # Big areas level off into a plateau so their shadow stays a band along
    # the edge instead of spreading across the middle.
    height = inflate(surf, shaded) * 0.55
    height = PLATEAU * np.tanh(height / PLATEAU)
    gy, gx = np.gradient(height)
    norm = np.sqrt(gx * gx + gy * gy + 1.0)
    nl = (-gx * LIGHT[0] - gy * LIGHT[1] + LIGHT[2]) / norm
    return nl, strength, soft_strength


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


## Putting it together ########################################################

def refine(rgba):
    """rgba: uint8 array at working resolution. Returns refined rgba float."""

    ink, opaque = split_ink(rgba)
    lab = label_fills(rgba, ink, opaque)
    n = int(lab.max()) + 1

    old = rgba[..., :3].astype(np.float64)
    clean = opaque & ~ndi.binary_dilation(ink, iterations=3)
    clean &= ~ndi.binary_dilation(~opaque, iterations=3)
    cols = area_colours(rgba, lab, n, clean)
    skin = is_skin(cols)
    skin[:2] = False   # undecided and outside

    inner, outer, detail = redraw_lines(ink, lab, skin)
    lines = np.maximum(inner, outer)
    thick = ink & ~detail

    lab = grow_labels(lab, lines > 0.5, iterations=40)
    cols[1] = 0
    base = cols[lab]
    # Keep the drawing's own colour wherever the lines haven't moved: that
    # keeps painted details (lips, eye colour, textures) and the detail lines
    # with their soft edges. Only what was under the redrawn lines gets the
    # flat colour of its area.
    keep = opaque & ~ndi.binary_dilation(thick, iterations=3)
    keep &= ~ndi.binary_dilation(~opaque, iterations=3)
    base[keep] = old[keep]
    zone = opaque & ~thick & ndi.binary_dilation(detail, iterations=2)
    base[zone] = old[zone]

    # How much of each kept detail pixel is ink, so it can be recoloured.
    detail_cov = np.clip((140.0 - luma(old)) / 110.0, 0, 1)
    # Pinholes in textured strokes count as ink.
    detail_cov = np.maximum(detail_cov, cv2.GaussianBlur(detail.astype(np.float32), (0, 0), 0.8))
    detail_cov = detail_cov * zone

    nl, strength, soft_strength = shade(lab, cols)
    # Two-tone cel shadow with a soft edge, plus a gentle overall gradient and
    # a rim light on the side facing the light.
    shadow = (1.0 - smoothstep(0.30, 0.36, nl)) * strength
    soft = 0.08 * (1.0 - np.clip(nl, 0, 1)) * soft_strength
    rim = smoothstep(0.90, 0.96, nl) * RIM_LIGHT * soft_strength

    tint = 1.0 - shadow[..., None] * (1.0 - SHADOW_TINT)
    col = base * tint * (1.0 - soft[..., None])
    col = col + (255.0 - col) * rim[..., None]

    # Lines: a dark shade of the colour beside them; the outline darker still.
    inside = lab != 1
    near_lab = lab.copy()
    near_lab[~inside] = 0
    _, (iy, ix) = ndi.distance_transform_edt(near_lab == 0, return_indices=True)
    beside = cols[near_lab[iy, ix]]
    dark = beside * 0.30 + np.array([14.0, 8.0, 18.0])
    line_col = dark * (1 - outer[..., None] * 0.45)

    cov = np.maximum(lines, detail_cov.astype(np.float32))[..., None]
    alpha = inside.astype(np.float32)
    # Soften the silhouette edge, which is pixel-hard after labelling.
    alpha = np.maximum(cv2.GaussianBlur(alpha, (0, 0), 1.0) * inside, lines)

    out_rgb = col * (1 - cov) + line_col * cov
    return np.dstack([np.clip(out_rgb, 0, 255), np.clip(alpha, 0, 1) * 255])


def load_work(name):
    im = Image.open(os.path.join(IMAGES, name)).convert("RGBA")
    return np.array(im.resize((WORK, WORK), Image.LANCZOS))


def to_image(out):
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def save_sprite(work_img, size, path):
    # Premultiply before shrinking so transparent edges don't go dark.
    a = np.array(work_img).astype(np.float32)
    a[..., :3] *= a[..., 3:] / 255.0
    pm = Image.fromarray(a.astype(np.uint8), "RGBA").resize((size, size), Image.LANCZOS)
    b = np.array(pm).astype(np.float32)
    al = b[..., 3:]
    b[..., :3] = np.where(al > 0, b[..., :3] * 255.0 / np.maximum(al, 1), 0)
    Image.fromarray(np.clip(b, 0, 255).astype(np.uint8), "RGBA").save(path, optimize=True)


def main(names):
    for name in names:
        src, size = SPRITES[name]
        print("refining", name)
        rgba = load_work(src)
        out = to_image(refine(rgba))
        save_sprite(out, size, os.path.join(IMAGES, name + ".png"))

        for close, (of, box, close_size) in CLOSEUPS.items():
            if of == name:
                k = WORK / 8192.0
                crop = out.crop(tuple(int(round(v * k)) for v in box))
                save_sprite(crop, close_size, os.path.join(IMAGES, close + ".png"))


if __name__ == "__main__":
    main(sys.argv[1:] or list(SPRITES))
