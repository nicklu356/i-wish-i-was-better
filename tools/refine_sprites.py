"""
Turns the hand-drawn character sprites into clean "digital" line art so they
sit better on the painted backgrounds, without changing anyone's proportions,
pose, face or hair.

For each character it reads the full-size drawing (game/images/*_original.png,
which stays untouched) and:

  1. separates the ink lines from the colour fills, and cleans the fills up
     into flat areas of colour with smooth edges,
  2. traces every line, fits a smooth curve through it that stays on the
     drawn path, and redraws it at a fixed weight with tapered ends. Every
     character uses the same three weights: the outline, lines between two
     areas, and fine lines inside one (hair strands, folds, seams). Lines on
     the face keep their drawn shape with the shaky edges smoothed,
  3. colours the lines with a dark shade of the colour next to them instead of
     pure black,
  4. redraws the shoes (see shoes.py next to this file),
  5. adds two-tone cel shading and a soft rim light to each painted area, lit
     from the upper left (faces only get the soft shading), and
  6. saves the in-game sprite (game/images/<name>.png), and the waist-up
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

sys.path.insert(0, os.path.dirname(__file__))
import shoes  # noqa: E402

IMAGES = os.path.join(os.path.dirname(__file__), "..", "game", "images")

## Working resolution. The originals are 8192 square; half of that is plenty.
WORK = 4096

## Which drawing makes which sprite, the sprite's canvas size, and how tall that
## canvas is on screen (see sprites.rpy), which sets how thick lines come out.
SPRITES = {
    "elena": ("Elena_original.png", 900, 940),
    "emma": ("Emma_original.png", 1000, 940),
    "gus": ("Gus_original.png", 1000, 1000),
    "zane": ("Zane_original.png", 1000, 1000),
}

## The waist-up close-ups are crops of the full drawings: which sprite, the
## crop box in the original's 8192 pixel space, and the close-up's canvas size.
CLOSEUPS = {
    "elenaclassroom": ("elena", (2460, 0, 6128, 3668), 900),
    "emmabus": ("emma", (2064, 0, 6272, 4208), 1000),
}

## Line weights, in pixels on a 1920x1080 screen: the outline, lines between
## two areas, and fine lines inside an area (hair strands, folds, seams). Every
## character gets the same ones. Lines on the face keep their drawn thickness.
OUTLINE_WEIGHT = 3.2
INNER_WEIGHT = 2.1
FINE_WEIGHT = 1.1

## A drawn line thinner than this fraction of the drawing's usual heavy line
## is fine detail (face, hair strands, folds, seams).
FINE_FRACTION = 0.55

## Separate little drawings smaller than this across (working pixels) are
## details such as eyes, mouths and buttons, and keep their drawn shape. So do
## the lines on skin. FACE_SMOOTH is how much their edges get evened out.
DETAIL_SIZE = 260
FACE_SMOOTH = 1.2

## The face is the top FACE_PART of the figure's height.
FACE_PART = 0.2

## Separate bits of ink and paint smaller than that, closer than STRAY_DIST
## (working pixels) to the outline, are rubbed-out left-overs and go.
STRAY_DIST = 45
STRAY_AREA = 800

## Branches of a line shorter than this many line widths are stubs.
SPUR_LENGTH = 2.5

## Painted strokes this different in colour from their area are details to
## keep (eyeliner, eye shadow, blush).
DETAIL_DIFF = 45

## Fine lines (folds, hair strands) may drift this far from the drawing.
FINE_DRIFT = 4.0

## Ink is anything this dark (0-255 luminance).
INK_LUMA = 32

## Ink more than this many times as thick as the drawing's usual lines is a
## filled black shape (hair, shoes), not a line.
SOLID_FACTOR = 1.6 / 2
SOLID_AREA = 3000

## How far (as a fraction of the drawn line's width) a smoothed line may drift
## from the drawn one, with limits in working pixels. Long strokes may always
## drift at least LONG_DRIFT. Bigger is straighter.
DRIFT = 0.20
DRIFT_MIN = 1.2
DRIFT_MAX = 5.0
LONG_STROKE = 250
LONG_DRIFT = 3.0

## Per character touches (working pixel coordinates; the drawings are 4096
## square here, so halve coordinates read off the 8192 originals):
##
## SKIN_TONES   the main skin colour to use instead of the drawn one,
## GLOSS        how shiny the skin below the face is,
## EXTRA_LINES  soft lines added on the body (knees, tummy),
## FEATURES     the part of the face holding the eyebrows, eyes, nose and
##              mouth: these are kept exactly as drawn,
## SHAPES       changes to the figure's outline: "mirror" makes the outline in
##              region the mirror image of the other side about x = axis;
##              "shape" replaces it in region with these closed curves,
## ORIGINAL     parts kept exactly as drawn, with only the line weights evened
##              out to the same ones as everywhere else,
## REDRAWS      parts drawn again from scratch: the drawing in "erase" goes
##              (painted with the colour at "fill", if given, or else with the
##              colours round it) and these lines (curves through the points)
##              are drawn instead; "closed" lines are loops.
SKIN_TONES = {
    "emma": (247, 222, 204),
    "elena": (244, 219, 196),
}
GLOSS_DEFAULT = 0.18
GLOSS = {
    "elena": 0.55,
}
EXTRA_LINES = {
    "elena": [
        [(1652, 2958), (1690, 2974), (1732, 2964)],
        [(2420, 2898), (2455, 2912), (2492, 2900)],
        [(2094, 1548), (2098, 1600), (2102, 1645)],
    ],
}
FEATURES = {
    "zane": [(1912, 300), (2185, 300), (2185, 420), (2135, 572), (1960, 572), (1912, 420)],
    "emma": [(1912, 355), (2228, 355), (2228, 460), (2160, 655), (1985, 655), (1912, 460)],
    "elena": [(2047, 280), (2352, 300), (2345, 395), (2290, 420), (2230, 600), (2060, 600),
              (2030, 420), (2045, 330)],
}
SHAPES = {
    # Emma's right shoulder, as wide as her left one.
    "emma": [dict(mirror=2070, region=[(2330, 860), (2800, 860), (2800, 1290), (2330, 1290)])],
}
REDRAWS = {}
ORIGINAL = {
    # Gus's whole face with the ears and hairline.
    "gus": [[(1735, 185), (2265, 185), (2265, 450), (2180, 560), (2100, 612), (1900, 612),
             (1830, 560), (1735, 450)]],
    # Elena's hands: the one on her tummy and the hanging one.
    "elena": [[(2190, 1590), (2390, 1585), (2450, 1615), (2478, 1680), (2450, 1765),
               (2415, 1800), (2190, 1805)],
              [(1385, 2080), (1640, 2080), (1640, 2350), (1385, 2350)]],
}

## The figure's outline: notches narrower than twice NOTCH go, and the edge
## is evened out by SHAPE_SMOOTH (working pixels).
NOTCH = 5
SHAPE_SMOOTH = 2.5

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


def is_skin(cols):
    """Which colours look like skin: pale, warm, not very saturated."""

    rgb = cols / 255.0
    mx, mn = rgb.max(1), rgb.min(1)
    sat = (mx - mn) / np.maximum(mx, 1e-6)
    r, g, b = rgb[:, 0], rgb[:, 1], rgb[:, 2]
    return (r >= g) & (r >= b) & (g >= b * 0.92) & (mx > 0.75) & (sat > 0.04) & (sat < 0.42)


## Step 1: lines and fills ####################################################

def split_ink(rgba):
    """
    Returns (ink, opaque, heavy). Ink is the line art; solid black shapes
    (black hair or shoes) are left out of it and treated as fills. Heavy is
    the width of the drawing's usual heavy line.
    """

    alpha = rgba[..., 3]
    opaque = alpha > 127
    ink = opaque & (luma(rgba[..., :3]) < INK_LUMA)
    # Some strokes were drawn with a textured brush and are full of pinholes;
    # fill the holes, but not real gaps such as between teeth.
    holes, n = ndi.label(~ink)
    ink |= (np.bincount(holes.ravel()) < 20)[holes] & opaque
    # Specks of a few pixels are dirt, not lines.
    lab, n = ndi.label(ink, structure=np.ones((3, 3)))
    ink &= (np.bincount(lab.ravel()) >= 12)[lab]

    dist = ndi.distance_transform_edt(ink)
    widths = dist[skeletonize(ink)] * 2.0
    heavy = float(np.percentile(widths, 90))

    # Anything that survives opening with a disk wider than the thickest line
    # is a filled shape, not a line.
    radius = int(np.ceil(heavy * SOLID_FACTOR))
    solid = ndi.binary_opening(ink, structure=disk(radius))
    lab, n = ndi.label(solid)
    if n:
        idx = np.arange(1, n + 1)
        sizes = ndi.sum(solid, lab, idx)
        keep = np.zeros(n + 1, bool)
        keep[1:] = sizes > SOLID_AREA
        # Heavy black lines bunched up on skin (fingers drawn over each
        # other) are still lines.
        ring = ndi.grey_dilation(lab, footprint=disk(radius)) * (opaque & ~ink)
        ring_size = np.maximum(ndi.sum(ring > 0, ring, idx), 1)
        around = np.stack([ndi.sum(rgba[..., c].astype(float), ring, idx) / ring_size
                           for c in range(3)], 1)
        keep[1:] &= ~(is_skin(around) & (sizes < 15000))
        solid = keep[lab]
    # The thin black wedges between solid patches (say between shoelaces)
    # belong to the patch too.
    solid = ndi.binary_dilation(solid, structure=disk(radius * 3 // 2)) & ink

    return ink & ~solid, opaque, heavy


def palette_labels(rgba, ink, opaque, colours=36):
    """
    Splits everything that isn't ink into flat areas of one colour each.
    Label 1 is the transparent outside, 2.. are the areas and 0 is not decided
    yet (ink, and specks too small to keep).
    """

    rgb = rgba[..., :3]
    paint = opaque & ~ink
    # Drop the anti-aliased fringe next to lines, which is the fill colour
    # muddied with black, but keep thin coloured details that run along a
    # line (eyeliner, lip edges): their colour isn't just a darker fill.
    fringe = paint & ndi.binary_dilation(ink, iterations=2)
    body = paint & ~fringe
    _, (iy, ix) = ndi.distance_transform_edt(~body, return_indices=True)
    fill = rgb[iy, ix].astype(np.float32)
    px = rgb.astype(np.float32)
    cos = (px * fill).sum(-1) / np.maximum(np.linalg.norm(px, axis=-1) * np.linalg.norm(fill, axis=-1), 1)
    paint &= ~fringe | (cos < 0.985) & (luma(px) > 45)

    # A small palette for the whole drawing, then every pixel to its nearest
    # colour through a lookup table. Rare colours are sampled more often so
    # small details still get a colour of their own.
    rng = np.random.default_rng(0)
    pix = rgb[paint]
    qbin = ((pix // 16).astype(np.int32) * [256, 16, 1]).sum(1)
    count = np.bincount(qbin, minlength=4096)[qbin]
    prob = 1.0 / np.sqrt(count)
    prob /= prob.sum()
    pick = rng.choice(len(pix), min(len(pix), 200000), replace=False, p=prob)
    sample = pix[pick].astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5)
    _, _, centres = cv2.kmeans(sample, colours, None, crit, 2, cv2.KMEANS_PP_CENTERS)
    q = np.arange(0, 256, 8, dtype=np.float32) + 4
    grid = np.stack(np.meshgrid(q, q, q, indexing="ij"), -1).reshape(-1, 3)
    lut = ((grid[:, None, :] - centres[None]) ** 2).sum(-1).argmin(1).astype(np.int32)
    qi = (rgb // 8).astype(np.int32)
    index = lut[(qi[..., 0] * 32 + qi[..., 1]) * 32 + qi[..., 2]]

    lab = np.zeros(ink.shape, np.int32)
    nxt = 2
    for c in range(colours):
        part, n = ndi.label(paint & (index == c))
        lab[part > 0] = part[part > 0] + nxt - 1
        nxt += n
    # The outside is the transparent area round the figure and the gaps
    # through it (between an arm and the body). Tiny transparent holes inside
    # a drawing (such as in the navel) get painted over by their surroundings.
    clear = ~opaque & ~ndi.binary_dilation(ink, iterations=2)
    parts, _ = ndi.label(clear)
    big = np.bincount(parts.ravel()) >= 1500
    big[0] = False
    lab[big[parts]] = 1

    lab = smooth_labels(lab, 2.0)
    sizes = np.bincount(lab.ravel())
    lab[(sizes[lab] < 30) & (lab > 1)] = 0
    return relabel(lab)


def smooth_labels(lab, sigma):
    """
    Rounds off the jagged edges between areas: every pixel goes to whichever
    area covers most of its neighbourhood. Undecided pixels stay undecided.
    """

    out = lab.copy()
    best = np.zeros(lab.shape, np.float32)
    pad = int(3 * sigma) + 1
    h, w = lab.shape
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        if sl is None:
            continue
        y0, y1 = max(sl[0].start - pad, 0), min(sl[0].stop + pad, h)
        x0, x1 = max(sl[1].start - pad, 0), min(sl[1].stop + pad, w)
        m = (lab[y0:y1, x0:x1] == i).astype(np.float32)
        # Small areas only get a light touch, or they'd melt away.
        sg = float(np.clip(np.sqrt(m.sum()) / 12.0, 0.6, sigma))
        b = cv2.GaussianBlur(m, (0, 0), sg)
        sb = best[y0:y1, x0:x1]
        win = b > sb
        sb[win] = b[win]
        out[y0:y1, x0:x1][win] = i
    out[lab == 0] = 0
    return out


def relabel(lab):
    """Renumbers labels 2.. so there are no gaps, keeping 0 and 1."""

    used = np.unique(lab)
    table = np.zeros(int(used.max()) + 1, np.int32)
    table[1] = 1
    rest = used[used > 1]
    table[rest] = np.arange(2, 2 + len(rest))
    return table[lab]


## Step 2: tracing and redrawing lines ########################################

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


def smooth_path(pts, widths, closed, min_tol=DRIFT_MIN):
    """
    Fits a smoothing spline through a traced path, letting it drift a little
    (at least min_tol) from the drawn line so the shake disappears. Returns
    resampled points.
    """

    n = len(pts)
    w = float(np.median(widths))
    tol = float(np.clip(DRIFT * w, min_tol, DRIFT_MAX))
    if n > LONG_STROKE:
        tol = max(tol, LONG_DRIFT)

    if n < 6:
        return pts

    # Subsample long paths; a point every couple of pixels is enough.
    step = max(1, int(round(w / 6)))
    idx = np.arange(0, n, step)
    if idx[-1] != n - 1:
        idx = np.append(idx, n - 1)
    p = pts[idx]
    m = len(p)
    if m < 4:
        return pts

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
        return pts

    seg = np.sqrt((np.diff(pts, axis=0) ** 2).sum(1)).sum()
    k = max(8, int(seg / 1.5))
    x, y = splev(np.linspace(0, 1, k), tck)
    return np.stack([y, x], 1)


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


def redraw_lines(ink, lab, skin, heavy, weights, face_y):
    """
    Traces the ink and redraws every line as a clean stroke; weights are the
    line weights in working pixels. The outline round the figure isn't drawn
    here (see outline()). Returns coverage masks (0-1) for three kinds of
    line:

      inner  lines between two different areas, at INNER_WEIGHT,
      fine   lines drawn inside one area (hair strands, folds, seams), at
             FINE_WEIGHT,
      face   lines on the face (above face_y: eyes, brows, nose, mouth) and
             other small separate drawings (buttons, navel): these keep
             their drawn shape, with the edges smoothed, so faces keep their
             character.

    Little separate bits of ink close to the outline, below the face, are
    left-overs from rubbing out and are dropped.
    """

    outside = lab == 1
    out_dist = ndi.distance_transform_edt(~outside)

    # Small separate drawings go to the face kind whole.
    parts, n = ndi.label(ink, structure=np.ones((3, 3)))
    small = np.zeros(n + 1, bool)
    stray = np.zeros(n + 1, bool)
    for i, sl in enumerate(ndi.find_objects(parts), 1):
        small[i] = np.hypot(sl[0].stop - sl[0].start, sl[1].stop - sl[1].start) < DETAIL_SIZE
        if small[i] and sl[0].start > face_y:
            stray[i] = out_dist[sl][parts[sl] == i].min() < STRAY_DIST
    kept = small[parts] & ~stray[parts]
    ink = ink & ~small[parts]

    dist = ndi.distance_transform_edt(ink)
    skel = skeletonize(ink)
    paths, junction = trace_paths(skel)
    _, (ly, lx) = ndi.distance_transform_edt(lab == 0, return_indices=True)
    near = lab[ly, lx]

    strokes = {"inner": [], "fine": []}
    face_skel = np.zeros(ink.shape, bool)

    for pts, js, je, closed in paths:
        iy, ix = pts[:, 0].astype(int), pts[:, 1].astype(int)
        widths = dist[iy, ix] * 2.0
        length = len(pts)
        mw = float(np.median(widths))

        # Skeleton spurs and rubbed-out stubs: short branches sticking off
        # a line, tiny loops round pinholes, and specks.
        if (js != je) and length < mw * SPUR_LENGTH:
            continue
        if closed and length < mw * 4:
            continue
        if not (js or je or closed) and length < 4:
            continue

        a, b = side_labels(pts, widths, near)
        thin = mw < heavy * FINE_FRACTION
        in_face = pts[:, 0].mean() < face_y
        if 1 in (a, b):
            # The outline is drawn from the figure's shape instead.
            continue
        elif in_face and (skin[a] or skin[b]) and (thin or a == b):
            face_skel[iy, ix] = True
            continue
        elif thin:
            kind = "fine"
        else:
            kind = "inner"

        if kind == "fine":
            # Folds, creases and hair strands: smoother still, and thinning
            # out at both ends like a brush stroke. Tiny ones are scribble.
            if length < weights["fine"] * 3:
                continue
            sp = smooth_path(pts, widths, closed, FINE_DRIFT)
            sw = np.full(len(sp), weights[kind])
            if not closed:
                # Short ticks (frayed hems, lashes) only taper at a free end.
                both = length > weights["fine"] * 10
                sw = taper(sw, both or not js, both or not je)
        else:
            sp = smooth_path(pts, widths, closed)
            sw = np.full(len(sp), weights[kind])
            if not closed:
                sw = taper(sw, not js, not je)
        # Ends that join another line reach a little further, so they meet
        # the outline (drawn along the edge now) without a gap.
        sp, sw = extend_ends(sp, sw, js, je, heavy * 0.35)
        strokes[kind].append((sp, sw))

    lines = {k: render_lines(ink.shape, v) for k, v in strokes.items()}

    # Face lines: the drawn ink that belongs to them (each ink pixel goes with
    # the nearest line middle), edges smoothed.
    face_skel |= junction & ndi.binary_dilation(face_skel, iterations=2)
    _, (ny, nx) = ndi.distance_transform_edt(~skel, return_indices=True)
    face_ink = (ink & face_skel[ny, nx]) | kept
    lines["face"] = smooth_shape(face_ink, FACE_SMOOTH)
    return lines


def extend_ends(pts, wid, start, end, by):
    """Lengthens a stroke along its direction at the ends that are flagged."""

    if len(pts) < 2 or by <= 0:
        return pts, wid
    if start:
        d = pts[0] - pts[1]
        d /= max(np.linalg.norm(d), 1e-6)
        pts = np.vstack([pts[:1] + d * by, pts])
        wid = np.concatenate([wid[:1], wid])
    if end:
        d = pts[-1] - pts[-2]
        d /= max(np.linalg.norm(d), 1e-6)
        pts = np.vstack([pts, pts[-1:] + d * by])
        wid = np.concatenate([wid, wid[-1:]])
    return pts, wid


def smooth_shape(mask, sigma):
    """An anti-aliased version of a mask with its jagged, shaky edges evened."""

    b = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), sigma)
    # A threshold a little under a half keeps thin lines from thinning out.
    return np.clip((b - 0.45) * 4.0 + 0.5, 0, 1)


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


def area_colours(rgba, lab, clean):
    """The flat colour of each area, from its pixels away from any line."""

    n = int(lab.max()) + 1
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


def shade(lab, cols, outside_label=1):
    """
    Lights the inflated surface. Returns n.l per pixel, how strongly each
    pixel takes the cel shadow and the soft shading (0 for areas too small to
    bother with; faces get no hard shadow so they stay clean), and where the
    skin below the face is, which gets a glossy highlight.
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
    skin[:2] = False
    face = skin & (features >= 2)
    strength = np.where(face, 0.0, np.where(skin, 0.75, 1.0))[surf] * shaded[surf]
    soft_strength = np.where(skin, 0.6, 1.0)[surf] * shaded[surf]
    body = (skin & ~face)[surf] * shaded[surf]

    # Big areas level off into a plateau so their shadow stays a band along
    # the edge instead of spreading across the middle.
    height = inflate(surf, shaded) * 0.55
    height = PLATEAU * np.tanh(height / PLATEAU)
    gy, gx = np.gradient(height)
    norm = np.sqrt(gx * gx + gy * gy + 1.0)
    nl = (-gx * LIGHT[0] - gy * LIGHT[1] + LIGHT[2]) / norm
    return nl, strength, soft_strength, body


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


## Putting it together ########################################################

def line_colour(cols, lab, lines):
    """
    A dark shade of the colour beside each line; the outline darker still.
    """

    near = lab.copy()
    near[lab == 1] = 0
    _, (iy, ix) = ndi.distance_transform_edt(near == 0, return_indices=True)
    beside = cols[near[iy, ix]]
    dark = beside * 0.28 + np.array([12.0, 7.0, 16.0])
    # Lines beside white would come out grey; keep every line properly dark.
    lum = luma(dark)[..., None]
    dark = dark * np.minimum(1.0, 62.0 / np.maximum(lum, 1))
    return dark * (1 - lines["outer"][..., None] * 0.45)


def clean_specks(lab, rgba):
    """
    Drops painted bits that are left-overs: small specks next to the outline
    and thin pale streaks across a fill (rubbing out), and small near-black
    patches (bits of the old lines). Their pixels
    become undecided, so the colour around them grows over them.
    """

    n = int(lab.max()) + 1
    area = np.bincount(lab.ravel(), minlength=n)
    near_out = ndi.binary_dilation(lab == 1, iterations=STRAY_DIST)
    touches = np.bincount(lab[near_out].ravel(), minlength=n) > 0
    drop = (area < STRAY_AREA) & touches

    # Thin and paler than the area round it.
    radius = ndi.maximum(ndi.distance_transform_edt(lab > 1), lab, np.arange(n))
    rgb = rgba[..., :3].astype(np.float64)
    mean = np.stack([ndi.sum(rgb[..., c], lab, np.arange(n)) / np.maximum(area, 1)
                     for c in range(3)], 1)
    a, b, count = label_adjacency(lab)
    best = np.zeros(n, np.int64)
    best_count = np.zeros(n, np.int64)
    for i, j, c in zip(a.tolist(), b.tolist(), count.tolist()):
        if j > 1 and c > best_count[i]:
            best[i], best_count[i] = j, c
    paler = luma(mean) > luma(mean[best]) + 25
    sat = mean.max(1) - mean.min(1)
    drop |= (radius < 2.5) & paler & (sat < 30) & (best_count > 0)
    # Small near-black patches are bits of old line, not paint.
    drop |= (luma(mean) < 60) & (area < 4000)
    drop[:2] = False
    lab = lab.copy()
    lab[drop[lab]] = 0
    return lab


def refine(rgba, scale, name):
    """
    rgba: uint8 array at working resolution; scale: working pixels per screen
    pixel. Returns the refined rgba as floats.
    """

    ink, opaque, heavy = split_ink(rgba)
    drawn_ink = ink.copy()
    lab = palette_labels(rgba, ink, opaque)
    lab = clean_specks(lab, rgba)
    clean = opaque & ~ndi.binary_dilation(ink, iterations=3)
    clean &= ~ndi.binary_dilation(~opaque, iterations=3)
    skin = is_skin(area_colours(rgba, lab, clean))
    skin[:2] = False   # undecided and outside

    rows = np.nonzero(opaque.any(1))[0]
    face_y = rows.min() + FACE_PART * (rows.max() - rows.min())

    # The shoes are redrawn from scratch.
    weights = {"outer": OUTLINE_WEIGHT * scale, "inner": INNER_WEIGHT * scale,
               "fine": FINE_WEIGHT * scale}
    shoe = shoes.ShoeArt(name, rgba, lab, weights, heavy)
    lab = shoe.lab
    skin = np.concatenate([skin, np.zeros(int(lab.max()) + 1 - len(skin), bool)])

    # The figure's shape, from which the outline is drawn. Parts redrawn from
    # scratch are cleared, and their areas grow back from round them.
    inside, alpha = figure_shape(opaque, shoe, name)
    canvas = shoes.Canvas(0, 0, lab.shape[1], lab.shape[0])
    erase = np.zeros(lab.shape, bool)
    fills = []
    for r in REDRAWS.get(name, []):
        m = canvas.polygon(shoes.spline(r["erase"], closed=True, per=6))
        erase |= m
        if "fill" in r:
            x, y = r["fill"]
            fills.append((m, lab[y, x]))
    ink &= inside & ~shoe.zone & ~erase
    lab[~inside] = 1
    lab[inside & ((lab == 1) | erase)] = 0
    for m, l in fills:
        lab[m & inside] = l

    lines = redraw_lines(ink, lab, skin, heavy, weights, face_y)
    for k in ("inner", "fine"):
        lines[k] = np.maximum(lines[k] * ~shoe.zone, shoe.lines[k])
    lines["outer"] = outline(inside, weights["outer"])
    redrawn = []
    for r in REDRAWS.get(name, []):
        for pts in r.get("lines", []):
            p = shoes.spline(pts)[:, ::-1]
            redrawn.append((p, taper(np.full(len(p), weights["inner"]), True, True)))
        for pts in r.get("closed", []):
            p = shoes.spline(pts, closed=True)[:, ::-1]
            redrawn.append((p, np.full(len(p), weights["inner"])))
    if redrawn:
        lines["inner"] = np.maximum(lines["inner"], render_lines(lab.shape, redrawn))
    walls = np.maximum.reduce(list(lines.values())) > 0.5
    lab = grow_labels(lab, walls, iterations=60)

    cols = area_colours(rgba, lab, clean)
    cols = shoe.colours(cols)
    cols[1] = 0
    if name in SKIN_TONES:
        cols = retone_skin(cols, lab, SKIN_TONES[name])
    col = keep_painted_details(rgba, cols[lab], lab, drawn_ink | shoe.zone, face_y)

    nl, strength, soft_strength, body = shade(lab, cols)
    # Two-tone cel shadow with a soft edge, plus a gentle overall gradient and
    # a rim light on the side facing the light. Skin below the face also gets
    # a glossy highlight.
    shadow = (1.0 - smoothstep(0.30, 0.36, nl)) * strength
    soft = 0.08 * (1.0 - np.clip(nl, 0, 1)) * soft_strength
    rim = smoothstep(0.90, 0.96, nl) * RIM_LIGHT * soft_strength
    gloss = smoothstep(0.76, 0.82, nl) * GLOSS.get(name, GLOSS_DEFAULT) * body

    tint = 1.0 - shadow[..., None] * (1.0 - SHADOW_TINT)
    col = col * tint * (1.0 - soft[..., None])
    # No rim light on near-black areas, which it would turn grey.
    lit = smoothstep(40.0, 110.0, luma(cols[lab]))
    col = col + (255.0 - col) * (np.maximum(rim, gloss) * lit)[..., None]

    # Extra lines on the body (knees, tummy): soft, in a deeper skin tone.
    extra = [shoes.spline(pts)[:, ::-1] for pts in EXTRA_LINES.get(name, [])]
    if extra:
        strokes = [(p, taper(np.full(len(p), weights["fine"] * 0.9), True, True)) for p in extra]
        ecov = render_lines(lab.shape, strokes)[..., None]
        col = col * (1 - ecov) + cols[lab] * 0.62 * ecov

    lcol = line_colour(cols, lab, lines)
    cov = np.maximum.reduce(list(lines.values()))
    for polygon in ORIGINAL.get(name, []):
        keep_original(rgba, drawn_ink, inside, polygon, col, cov, heavy, weights)

    out_rgb = col * (1 - cov[..., None]) + lcol * cov[..., None]
    out_rgb, alpha = shoe.overlay(out_rgb, alpha)
    if name in FEATURES:
        out_rgb = restore_features(rgba, out_rgb, FEATURES[name])
    return np.dstack([np.clip(out_rgb, 0, 255), np.clip(alpha, 0, 1) * 255])


def figure_shape(opaque, shoe, name):
    """
    The figure's silhouette: everything but the transparent area round it
    (and gaps through it, such as between an arm and the body), with the
    redrawn shoes in place of the old ones, small notches filled, the edits
    in SHAPES applied and the edge evened out. Returns the mask and its
    anti-aliased coverage.
    """

    parts, _ = ndi.label(~opaque)
    big = np.bincount(parts.ravel()) >= 1500
    big[0] = False
    inside = ~big[parts]
    inside = (inside & ~shoe.zone) | shoe.silhouette
    # Where a shoe meets the leg, keep what was drawn between them, so no gap
    # opens up.
    leg = ndi.binary_dilation(inside & ~shoe.zone, structure=disk(28))
    inside |= shoe.zone & opaque & leg & ndi.binary_dilation(shoe.silhouette, structure=disk(28))
    inside |= ndi.binary_closing(inside, structure=disk(NOTCH))

    h, w = inside.shape
    canvas = shoes.Canvas(0, 0, w, h)
    for edit in SHAPES.get(name, []):
        region = canvas.polygon(edit["region"])
        if "mirror" in edit:
            xs = np.clip(2 * edit["mirror"] - np.arange(w), 0, w - 1)
            new = inside[:, xs]
        else:
            new = np.zeros_like(inside)
            for pts in edit["shape"]:
                new |= canvas.polygon(shoes.spline(pts, closed=True, per=8))
        inside = np.where(region, new, inside)

    f = cv2.GaussianBlur(inside.astype(np.float32), (0, 0), SHAPE_SMOOTH)
    inside = f > 0.5
    alpha = np.clip((f - 0.5) * SHAPE_SMOOTH * 2.0 + 0.5, 0, 1)
    return inside, alpha


def outline(inside, weight):
    """Coverage of a line of the given weight running just inside the edge."""

    d = ndi.distance_transform_edt(inside)
    return np.clip(weight + 0.5 - d, 0, 1).astype(np.float32) * (d > 0)


def keep_original(rgba, ink, inside, polygon, col, cov, heavy, weights):
    """
    Inside the polygon, puts the drawing back as it was, changing only the
    line weights: the outline becomes a band of the outline weight along the
    edge, and every other line is thinned down to the inner weight round its
    middle (lines already thinner stay as they are). Where the ink is taken
    away, the colour next to it carries on. col (fills) and cov (line
    coverage) are changed in place; the edge of the polygon is feathered.
    """

    pts = np.asarray(polygon, float)
    h, w = cov.shape
    x0, y0 = [max(int(v) - 40, 0) for v in pts.min(0)]
    x1 = min(int(pts[:, 0].max()) + 40, w)
    y1 = min(int(pts[:, 1].max()) + 40, h)
    win = (slice(y0, y1), slice(x0, x1))
    region = shoes.Canvas(x0, y0, x1 - x0, y1 - y0).polygon(pts)

    drawn = ink[win]
    d_out = ndi.distance_transform_edt(inside[win])
    edge = d_out <= heavy * 1.2

    # The middles of the lines, without the little spurs skeletons grow.
    skel = skeletonize(drawn)
    paths, junction = trace_paths(skel)
    dist = ndi.distance_transform_edt(drawn)
    mid = junction.copy()
    for p, js, je, closed in paths:
        iy, ix = p[:, 0].astype(int), p[:, 1].astype(int)
        mw = float(np.median(dist[iy, ix])) * 2.0
        if (js != je) and len(p) < mw * 1.2:
            continue
        mid[iy, ix] = True
    near_mid = ndi.distance_transform_edt(~mid) <= weights["inner"] / 2.0
    keep = drawn & np.where(edge, d_out <= weights["outer"], near_mid)
    keep_cov = np.clip((cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 0.9) - 0.3) * 2.5, 0, 1)

    # Colours: the drawing's own wherever it differs from the refined fill
    # (eyes, mouth, the drawn shape of the hair), with the ink filled from
    # the colour beside it.
    rgb = rgba[win][..., :3].astype(np.float32)
    # Clear of the lines' soft edges too, which are muddied with black.
    source = (rgba[win][..., 3] > 200) & ~ndi.binary_dilation(drawn, iterations=4)
    _, (iy, ix) = ndi.distance_transform_edt(~source, return_indices=True)
    plain = rgb[iy, ix]
    fill = col[win]
    # The refined fills may have been re-toned (skin); carry that over.
    m = region & (np.linalg.norm(plain - fill, axis=-1) < 40)
    if m.sum() > 100:
        plain = plain * (np.median(fill[m], axis=0) / np.maximum(np.median(plain[m], axis=0), 1))
    differs = np.linalg.norm(plain - fill, axis=-1) > 40
    new_fill = np.where(differs[..., None], plain, fill)

    f = cv2.GaussianBlur(region.astype(np.float32), (0, 0), 4.0) * region
    f = np.clip(f * 2.0, 0, 1)
    new_cov = np.maximum(keep_cov, cov[win] * edge)
    col[win] = fill * (1 - f[..., None]) + new_fill * f[..., None]
    cov[win] = cov[win] * (1 - f) + new_cov * f


def restore_features(rgba, out, polygon):
    """
    Puts the drawing's own eyebrows, eyes, nose and mouth back. Inside the
    polygon, whatever isn't plain skin in the drawing is pasted over the
    refined face, after the refined face's own features there are painted
    out with the skin round them.
    """

    h, w = out.shape[:2]
    pts = np.asarray(polygon, float)
    x0, y0 = [max(int(v) - 20, 0) for v in pts.min(0)]
    x1, y1 = int(pts[:, 0].max()) + 20, int(pts[:, 1].max()) + 20
    win = (slice(y0, y1), slice(x0, x1))
    region = shoes.Canvas(x0, y0, x1 - x0, y1 - y0).polygon(pts)

    orig = rgba[win][..., :3].astype(np.float32)
    new = out[win].astype(np.float32)

    def skin_of(img):
        px = img[region]
        return np.median(px[luma(px) > np.percentile(luma(px), 40)], axis=0)

    diff_o = np.linalg.norm(orig - skin_of(orig), axis=-1)
    diff_n = np.linalg.norm(new - skin_of(new), axis=-1)
    a = smoothstep(18.0, 80.0, diff_o) * region
    a = np.maximum(a, cv2.GaussianBlur(a.astype(np.float32), (0, 0), 0.7) * region)

    # Paint the refined features out.
    gone = ((diff_n > 18) | (a > 0)) & region
    gone = ndi.binary_dilation(gone, iterations=4) & region
    base = cv2.inpaint(np.clip(new, 0, 255).astype(np.uint8), gone.astype(np.uint8), 7,
                       cv2.INPAINT_TELEA).astype(np.float32)
    base = np.where(gone[..., None], base, new)

    result = out.copy()
    result[win] = base * (1 - a[..., None]) + orig * a[..., None]
    return result


def keep_painted_details(rgba, flat, lab, ink, face_y):
    """
    Puts back painted details the flat areas lost: strokes of a clearly
    different colour (eyeliner and eye shadow, lip highlights, blush, small
    marks on clothes), with their edges evened out. Below the face only
    darker or more colourful strokes away from the outline count, so pale
    rub-out marks don't come back.
    """

    rgb = rgba[..., :3].astype(np.float32)
    flat = flat.astype(np.float32)
    opaque = rgba[..., 3] > 127
    diff = np.linalg.norm(rgb - flat, axis=-1)
    cos = (rgb * flat).sum(-1) / np.maximum(np.linalg.norm(rgb, axis=-1) * np.linalg.norm(flat, axis=-1), 1)
    near_ink = ndi.binary_dilation(ink, iterations=3)
    cand = opaque & ~ink & (lab > 1) & (diff > DETAIL_DIFF)
    # Next to a line, only colours that aren't just the fill muddied by it.
    cand &= ~near_ink | (cos < 0.985)

    sat = lambda c: c.max(-1) - c.min(-1)
    rows = np.arange(lab.shape[0])[:, None]
    body = rows >= face_y
    strong = (luma(rgb) < luma(flat) - 20) | (sat(rgb) > sat(flat) + 40)
    away = ndi.distance_transform_edt(lab != 1) > STRAY_DIST
    cand &= ~body | (strong & away)

    # Specks on their own are noise; strokes are kept.
    part, n = ndi.label(ndi.binary_closing(cand, structure=disk(2)))
    big = np.bincount(part.ravel()) >= 40
    big[0] = False
    cand &= big[part]

    m = cand.astype(np.float32)
    cover = np.clip((cv2.GaussianBlur(m, (0, 0), 1.2) - 0.25) * 2.5, 0, 1)
    w = cv2.GaussianBlur(m, (0, 0), 1.5)
    colour = cv2.GaussianBlur(rgb * m[..., None], (0, 0), 1.5) / np.maximum(w, 1e-3)[..., None]
    return flat * (1 - cover[..., None]) + colour * cover[..., None]


def retone_skin(cols, lab, target):
    """Moves every skin colour so the main skin tone becomes target."""

    skin = is_skin(cols)
    skin[:2] = False
    if not skin.any():
        return cols
    area = np.bincount(lab.ravel(), minlength=len(cols))
    main = np.argmax(np.where(skin, area, -1))
    ratio = np.asarray(target, float) / np.maximum(cols[main], 1)
    cols = cols.copy()
    cols[skin] = np.clip(cols[skin] * ratio, 0, 255)
    return cols


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
        src, size, screen = SPRITES[name]
        print("refining", name)
        rgba = load_work(src)
        scale = WORK / float(screen)
        out = to_image(refine(rgba, scale, name))
        save_sprite(out, size, os.path.join(IMAGES, name + ".png"))

        for close, (of, box, close_size) in CLOSEUPS.items():
            if of == name:
                k = WORK / 8192.0
                crop = out.crop(tuple(int(round(v * k)) for v in box))
                save_sprite(crop, close_size, os.path.join(IMAGES, close + ".png"))


if __name__ == "__main__":
    main(sys.argv[1:] or list(SPRITES))
