"""
Redraws the characters' shoes for refine_sprites.py.

The hand-drawn shoes are cleared away and rebuilt:

  * the shoe's outline comes from the drawing, smoothed,
  * the parts (upper, toe cap, sole...) are the drawing's own painted areas,
    picked out by a point inside each, tidied up, and filling the shoe between
    them,
  * the lines are redrawn along the edges between the parts at the same fixed
    weights as the rest of the character, plus a few fine details (stitching,
    sole stripes), and
  * the laces are drawn from scratch: neat criss-cross laces between two rows
    of eyelets, and a bow of two loops and two ends.

Everything is given in the 4096 pixel working space of refine_sprites.py
(the originals are 8192, so halve those coordinates).
"""

import cv2
import numpy as np
from scipy import ndimage as ndi


## The shoes ##################################################################
##
## inset    (optional) how far in from the drawing's edge the new outline
##          runs, in working pixels; by default half the drawing's heavy line.
## zone     where the old shoe is cleared. Its top edge runs along the middle
##          of the trouser hem (or across the leg); elsewhere it can be loose,
##          as only the drawing inside it counts.
## parts    (colour, points inside the part in the drawing, extra polygon or
##          None). Every bit of the shoe goes to the nearest part. A colour
##          of None keeps the drawing's colour (for skin showing at the ankle).
##          Points "rest" make the part take whatever no other part covers.
## details  fine lines: (points, closed).
## laces    two rows of eyelets, each (first, last) from the ankle down, how
##          many eyelets per row, and optionally the lace colour, width and
##          style ("bars" for dress shoes laced straight across).
## bow      the knot, the loops (closed curves through these points) and the
##          loose ends (curves from the knot).

GREY_CANVAS = (112, 112, 116)
BLACK_CANVAS = (40, 38, 44)
WHITE_RUBBER = (246, 244, 240)
WHITE_LEATHER = (252, 252, 252)
PALE_SOLE = (226, 226, 232)
BROWN_LEATHER = (132, 90, 62)
DARK_SOLE = (88, 60, 44)

WHITE_LACE = (250, 250, 248)
BROWN_LACE = (72, 46, 32)

SHOES = {
    "gus": [
        dict(
            zone=[(1398, 3728), (1500, 3732), (1612, 3740), (1700, 3740), (1700, 4097),
                  (1090, 4097), (1090, 3880), (1330, 3700), (1398, 3700)],
            parts=[
                (GREY_CANVAS, [(1500, 3850), (1450, 3785), (1290, 3870), (1580, 3900)],
                 [(1310, 3900), (1340, 3820), (1420, 3770), (1490, 3760), (1480, 3820),
                  (1430, 3900), (1380, 3940), (1320, 3935)]),
                (WHITE_RUBBER, [(1251, 3960)], None),
                (WHITE_RUBBER, [(1400, 4030), (1250, 4030)], None),
            ],
            details=[([(1185, 4040), (1300, 4044), (1450, 4036), (1610, 4020)], False)],
            laces=dict(rows=[((1405, 3772), (1322, 3910)), ((1486, 3782), (1400, 3938))], eyelets=5),
            bow=dict(
                knot=(1440, 3768),
                loops=[[(1440, 3768), (1395, 3738), (1340, 3726), (1318, 3752), (1362, 3776)],
                       [(1440, 3768), (1500, 3744), (1568, 3756), (1582, 3790), (1520, 3802)]],
                ends=[[(1436, 3772), (1395, 3830), (1342, 3902)],
                      [(1446, 3772), (1470, 3840), (1492, 3906)]],
            ),
        ),
        dict(
            zone=[(2132, 3724), (2366, 3724), (2380, 3700), (2700, 3700), (2700, 4097),
                  (2050, 4097), (2050, 3724)],
            parts=[
                (GREY_CANVAS, [(2200, 3900), (2150, 3800), (2300, 3975)],
                 [(2240, 3830), (2330, 3820), (2440, 3880), (2450, 3930), (2400, 3960),
                  (2300, 3950), (2240, 3880)]),
                (WHITE_RUBBER, [(2500, 3960)], None),
                (WHITE_RUBBER, [(2300, 4040)], None),
            ],
            details=[([(2112, 4040), (2300, 4052), (2480, 4050), (2620, 4030)], False)],
            laces=dict(rows=[((2265, 3824), (2425, 3882)), ((2245, 3890), (2395, 3945))], eyelets=5),
            bow=dict(
                knot=(2295, 3815),
                loops=[[(2295, 3815), (2250, 3780), (2192, 3770), (2186, 3802), (2240, 3834)],
                       [(2295, 3815), (2330, 3770), (2382, 3748), (2425, 3762), (2408, 3792),
                        (2342, 3820)]],
                ends=[[(2290, 3820), (2258, 3880), (2215, 3975)],
                      [(2300, 3820), (2370, 3862), (2435, 3912)]],
            ),
        ),
    ],

    "zane": [
        dict(
            inset=4,
            zone=[(1503, 3822), (1560, 3822), (1612, 3818), (1660, 3802), (1700, 3790),
                  (1720, 3790), (1720, 4099), (1286, 4099), (1286, 3950), (1420, 3790),
                  (1500, 3790)],
            parts=[
                (BLACK_CANVAS, "rest", None),
                (WHITE_RUBBER, [(1390, 4020)], None),
                (WHITE_RUBBER, [], [(1270, 4020), (1320, 4048), (1400, 4052), (1460, 4040),
                                    (1580, 3970), (1700, 3898), (1760, 3898), (1760, 4110),
                                    (1270, 4110)]),
                (WHITE_LEATHER, [(1560, 3840)], None),
            ],
            details=[([(1470, 4062), (1580, 3998), (1700, 3928)], False)],
            laces=dict(rows=[((1478, 3880), (1350, 3992)), ((1545, 3884), (1424, 4004))], eyelets=5),
            bow=dict(
                knot=(1525, 3872),
                loops=[[(1525, 3872), (1490, 3842), (1456, 3824), (1448, 3846), (1488, 3866)],
                       [(1525, 3872), (1570, 3862), (1606, 3876), (1600, 3904), (1560, 3896)]],
                ends=[[(1520, 3876), (1440, 3884), (1385, 3906), (1366, 3926)],
                      [(1528, 3878), (1545, 3925), (1555, 3978)]],
            ),
        ),
        dict(
            inset=4,
            zone=[(2188, 3903), (2272, 3903), (2276, 3866), (2392, 3862), (2420, 3840),
                  (2600, 3840), (2600, 4099), (2150, 4099), (2150, 3903)],
            parts=[
                (BLACK_CANVAS, "rest", None),
                (WHITE_RUBBER, [(2490, 4010)], None),
                (WHITE_RUBBER, [], [(2130, 3990), (2300, 4008), (2440, 4028), (2500, 4036),
                                    (2540, 4036), (2560, 4020), (2610, 4020), (2610, 4110),
                                    (2130, 4110)]),
                (WHITE_LEATHER, [(2330, 3885)], None),
            ],
            details=[([(2180, 4030), (2300, 4044), (2430, 4062)], False)],
            laces=dict(rows=[((2352, 3904), (2462, 3950)), ((2330, 3944), (2422, 4006))], eyelets=4),
            bow=dict(
                knot=(2364, 3915),
                loops=[[(2364, 3915), (2378, 3884), (2398, 3862), (2408, 3880), (2384, 3906)],
                       [(2364, 3915), (2335, 3904), (2310, 3916), (2318, 3942), (2350, 3936)]],
                ends=[[(2362, 3920), (2345, 3962), (2348, 4012)],
                      [(2368, 3918), (2418, 3922), (2455, 3940)]],
            ),
        ),
    ],

    "elena": [
        dict(
            zone=[(1405, 3745), (1560, 3745), (1600, 3790), (1610, 4081), (1206, 4081),
                  (1206, 3900), (1380, 3790)],
            parts=[
                (None, [(1500, 3746)], None),
                (WHITE_LEATHER, "rest", None),
                (PALE_SOLE, [], [(1190, 3992), (1250, 3988), (1300, 3996), (1350, 4016),
                                 (1440, 4026), (1500, 4004), (1545, 3975), (1590, 3935),
                                 (1640, 3930), (1640, 4100), (1190, 4100)]),
            ],
            details=[([(1240, 4052), (1330, 4062), (1450, 4058), (1520, 4036)], False),
                     ([(1300, 3970), (1360, 3988), (1440, 3994), (1500, 3970), (1560, 3920)], False)],
            laces=dict(rows=[((1420, 3830), (1326, 3964)), ((1505, 3838), (1440, 3984))], eyelets=5),
            bow=dict(
                knot=(1441, 3840),
                loops=[[(1441, 3840), (1420, 3822), (1404, 3830), (1414, 3848)],
                       [(1441, 3840), (1472, 3825), (1514, 3830), (1510, 3852), (1466, 3854)]],
                ends=[[(1437, 3845), (1392, 3880), (1332, 3910)],
                      [(1446, 3845), (1488, 3882), (1492, 3938)]],
            ),
        ),
        dict(
            zone=[(2440, 3762), (2590, 3762), (2620, 3790), (2800, 3790), (2800, 4081),
                  (2430, 4081)],
            parts=[
                (None, [(2470, 3770)], None),
                (WHITE_LEATHER, "rest", None),
                (PALE_SOLE, [], [(2410, 3978), (2500, 3986), (2560, 3996), (2640, 4002),
                                 (2700, 4006), (2760, 4012), (2820, 4012), (2820, 4100),
                                 (2410, 4100)]),
            ],
            details=[([(2470, 4034), (2580, 4054), (2690, 4060), (2770, 4048)], False),
                     ([(2470, 3965), (2560, 3975), (2650, 3982), (2740, 3990)], False)],
            laces=dict(rows=[((2532, 3838), (2612, 3984)), ((2610, 3822), (2690, 3962))], eyelets=5),
            bow=dict(
                knot=(2567, 3835),
                loops=[[(2567, 3835), (2530, 3810), (2482, 3815), (2476, 3850), (2520, 3866)],
                       [(2567, 3835), (2602, 3810), (2650, 3800), (2680, 3816), (2640, 3845)]],
                ends=[[(2563, 3840), (2532, 3900), (2518, 3948)],
                      [(2572, 3840), (2650, 3880), (2700, 3922)]],
            ),
        ),
    ],

    "emma": [
        dict(
            zone=[(1880, 3880), (1945, 3862), (1990, 3845), (2050, 3848), (2100, 3872),
                  (2127, 3886), (2127, 4102), (1830, 4102), (1830, 3880)],
            parts=[
                (BROWN_LEATHER, [(2000, 3900), (1950, 3990), (2050, 3960)], None),
                (DARK_SOLE, [(1960, 4065), (2010, 4055)], None),
            ],
            details=[([(1904, 3990), (1950, 3984), (2030, 3974), (2072, 3922), (2112, 3884)], False),
                     ([(1915, 4040), (1990, 4040), (2060, 4012), (2100, 3972)], False)],
            laces=dict(rows=[((1984, 3906), (1966, 3972)), ((2026, 3914), (2008, 3978))], eyelets=4,
                       colour=BROWN_LACE, width=1.5, style="bars"),
        ),
        dict(
            zone=[(2129, 3886), (2150, 3868), (2200, 3843), (2250, 3836), (2300, 3845),
                  (2340, 3850), (2390, 3850), (2390, 4102), (2129, 4102)],
            parts=[
                (BROWN_LEATHER, [(2250, 3900), (2200, 3950), (2300, 3960)], None),
                (DARK_SOLE, [(2280, 4045), (2240, 4040)], None),
            ],
            details=[([(2160, 3888), (2195, 3920), (2238, 3930), (2280, 3916), (2340, 3908)], False),
                     ([(2215, 4020), (2280, 4030), (2340, 4026)], False)],
            laces=dict(rows=[((2208, 3882), (2226, 3948)), ((2252, 3874), (2272, 3938))], eyelets=4,
                       colour=BROWN_LACE, width=1.5, style="bars"),
        ),
    ],
}

LACE_EDGE = (52, 46, 58)
AGLET = (150, 150, 158)
EYELET = (196, 196, 204)


## Curves #####################################################################

def spline(pts, closed=False, per=16):
    """A smooth (centripetal Catmull-Rom) curve through the points."""

    p = np.asarray(pts, float)
    if len(p) < 3:
        if len(p) == 1:
            return p
        t = np.linspace(0, 1, per + 1)[:, None]
        return p[0] * (1 - t) + p[1] * t
    if closed:
        p = np.vstack([p[-1:], p, p[:2]])
    else:
        p = np.vstack([2 * p[0] - p[1], p, 2 * p[-1] - p[-2]])
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        t0 = 0.0
        t1 = t0 + max(np.linalg.norm(p1 - p0), 1e-6) ** 0.5
        t2 = t1 + max(np.linalg.norm(p2 - p1), 1e-6) ** 0.5
        t3 = t2 + max(np.linalg.norm(p3 - p2), 1e-6) ** 0.5
        for t in np.linspace(t1, t2, per, endpoint=False):
            a1 = (t1 - t) / (t1 - t0) * p0 + (t - t0) / (t1 - t0) * p1
            a2 = (t2 - t) / (t2 - t1) * p1 + (t - t1) / (t2 - t1) * p2
            a3 = (t3 - t) / (t3 - t2) * p2 + (t - t2) / (t3 - t2) * p3
            b1 = (t2 - t) / (t2 - t0) * a1 + (t - t0) / (t2 - t0) * a2
            b2 = (t3 - t) / (t3 - t1) * a2 + (t - t1) / (t3 - t1) * a3
            out.append((t2 - t) / (t2 - t1) * b1 + (t - t1) / (t2 - t1) * b2)
    out.append(p[1] if closed else p[-2])
    return np.array(out)


SHIFT = 4


def _pts(xy, origin):
    xy = np.asarray(xy, float) - origin
    return np.round(xy * (1 << SHIFT)).astype(np.int32).reshape(-1, 1, 2)


class Canvas:
    """Draws shapes into a window (x0, y0, width, height) of the sprite."""

    def __init__(self, x0, y0, w, h):
        self.origin = np.array([x0, y0], float)
        self.shape = (h, w)

    def polygon(self, pts):
        m = np.zeros(self.shape, np.uint8)
        cv2.fillPoly(m, [_pts(pts, self.origin)], 1, cv2.LINE_8, SHIFT)
        return m.astype(bool)

    def stroke(self, xy, width, closed=False):
        """Anti-aliased coverage (0-1) of a round-capped stroke along a curve."""

        m = np.zeros(self.shape, np.uint8)
        cv2.polylines(m, [_pts(xy, self.origin)], closed, 255, max(1, int(round(width))),
                      cv2.LINE_AA, SHIFT)
        return m.astype(np.float32) / 255.0

    def disc(self, centre, radius):
        m = np.zeros(self.shape, np.uint8)
        c = tuple(int(round(v)) for v in (np.asarray(centre) - self.origin) * (1 << SHIFT))
        cv2.circle(m, c, int(round(radius * (1 << SHIFT))), 255, -1, cv2.LINE_AA, SHIFT)
        return m.astype(np.float32) / 255.0


def silhouette(mask, inset, zone):
    """
    The shape of a shoe as a smooth vector outline: the drawing's outer edge,
    pulled in by inset, with lace bits that stuck out removed and the wobble
    taken out, filled.
    """

    m = ndi.binary_fill_holes(mask)
    m = ndi.binary_opening(m, structure=disk(10))
    m = ndi.distance_transform_edt(m) > inset
    out = np.zeros(m.shape, np.uint8)
    contours, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        c = c[:, 0, :].astype(float)
        if len(c) < 40:
            continue
        # Even spacing, then a moving average round the loop.
        seg = np.sqrt((np.diff(np.vstack([c, c[:1]]), axis=0) ** 2).sum(1))
        u = np.concatenate([[0], np.cumsum(seg)])
        k = max(int(u[-1] / 2), 20)
        t = np.linspace(0, u[-1], k, endpoint=False)
        cc = np.vstack([c, c[:1]])
        res = np.stack([np.interp(t, u, cc[:, 0]), np.interp(t, u, cc[:, 1])], 1)
        res = ndi.gaussian_filter1d(res, 7.0, axis=0, mode="wrap")
        cv2.fillPoly(out, [np.round(res * (1 << SHIFT)).astype(np.int32).reshape(-1, 1, 2)],
                     1, cv2.LINE_8, SHIFT)
    return out.astype(bool) & zone


def smooth_mask(mask, sigma):
    return cv2.GaussianBlur(mask.astype(np.float32), (0, 0), sigma) > 0.5


def edge_cover(boundary, width):
    """Coverage of a line of the given width centred on boundary pixels."""

    if not boundary.any():
        return np.zeros(boundary.shape, np.float32)
    d = ndi.distance_transform_edt(~boundary)
    return np.clip(width / 2.0 + 0.5 - d, 0, 1).astype(np.float32)


def boundaries(lab):
    """Pixels next to a pixel of another label."""

    edge = np.zeros(lab.shape, bool)
    dy = lab[1:] != lab[:-1]
    dx = lab[:, 1:] != lab[:, :-1]
    edge[1:] |= dy
    edge[:-1] |= dy
    edge[:, 1:] |= dx
    edge[:, :-1] |= dx
    return edge


## The shoe layer #############################################################

PAD = 24


class ShoeArt:
    """
    name: the character; rgba: the drawing at working resolution; lab: its
    painted areas (refine_sprites.palette_labels); weights: line weights in
    working pixels for "outer", "inner" and "fine"; heavy: the width of the
    drawing's heavy lines.

    After construction: zone is where the old shoes were cleared, lab the
    painted areas with the new shoe parts in, and lines the shoes' outline,
    inner and fine line coverage. colours() fills in the parts' colours and
    overlay() draws the laces on the finished sprite.
    """

    def __init__(self, name, rgba, lab, weights, heavy):
        self.specs = SHOES.get(name, [])
        self.weights = weights
        shape = lab.shape
        self.zone = np.zeros(shape, bool)
        self.lab = lab.copy()
        self.part_colours = {}
        self.lines = {k: np.zeros(shape, np.float32) for k in ("outer", "inner", "fine")}
        self.windows = []
        nxt = int(lab.max()) + 1
        # How far the old heavy outline reaches in from the drawing's edge;
        # the new outline goes down its middle.
        inset = heavy * 0.5

        for spec in self.specs:
            pts = np.asarray(spec["zone"], float)
            x0 = max(int(pts[:, 0].min()) - PAD, 0)
            y0 = max(int(pts[:, 1].min()) - PAD, 0)
            x1 = min(int(pts[:, 0].max()) + PAD, shape[1])
            y1 = min(int(pts[:, 1].max()) + PAD, shape[0])
            win = (slice(y0, y1), slice(x0, x1))
            cv = Canvas(x0, y0, x1 - x0, y1 - y0)
            self.windows.append((win, cv))

            zone = cv.polygon(spline(pts, closed=True, per=6))
            old = lab[win]
            sub_rgba = rgba[win]
            drawn = sub_rgba[..., 3] > 60
            new = self.lab[win]
            self.zone[win] |= zone

            ins = spec.get("inset", inset)
            shoe = silhouette(zone & drawn, ins, zone)

            # Where the shoe meets the leg, keep the drawing's edge so nothing
            # opens up between them; the leg's colour grows into what's left.
            leg = ndi.binary_dilation(drawn & ~zone, structure=disk(int(ins) + 14)) & zone
            shoe |= leg & ndi.binary_erosion(drawn, iterations=int(ins)) & ndi.binary_dilation(shoe, iterations=4)
            new[zone] = 1
            # The rest of the leg's edge takes the colour of the leg above.
            gap = zone & drawn & ~shoe & leg
            if gap.any():
                above = (~zone) & (old > 1)
                _, (iy, ix) = ndi.distance_transform_edt(~above, return_indices=True)
                new[gap] = old[iy, ix][gap]

            masks, colours = [], []
            rest = None
            for colour, seeds, extra in spec["parts"]:
                m = np.zeros(zone.shape, bool)
                picked = []
                if seeds == "rest":
                    rest = len(masks)
                    seeds = []
                for x, y in seeds:
                    l = pick_label(old, sub_rgba, x - x0, y - y0, colour)
                    if l:
                        # Only the solid part round the point, without laces
                        # or lines of the same colour running off it.
                        c = ndi.binary_opening(old == l, structure=disk(6))
                        cl, _ = ndi.label(c)
                        y_, x_ = y - y0, x - x0
                        if cl[y_, x_]:
                            c = cl == cl[y_, x_]
                        else:
                            c = old == l
                        m |= c
                        picked.append(l)
                m &= zone
                if extra is not None:
                    m |= cv.polygon(spline(extra, closed=True, per=8))
                masks.append(ndi.binary_fill_holes(m))
                if colour is None:
                    sel = np.isin(old, picked)
                    colour = tuple(sub_rgba[..., :3][sel].mean(0)) if sel.any() else (200, 160, 140)
                colours.append(colour)

            # Every bit of the shoe goes to the nearest part, then the edges
            # between parts are evened out.
            dists = np.stack([ndi.distance_transform_edt(~m) if m.any()
                              else np.full(zone.shape, 1e9) for m in masks])
            nearest = dists.argmin(0)
            if rest is not None:
                # The "rest" part takes everything the others don't cover.
                claimed = np.zeros(zone.shape, bool)
                for i, m in enumerate(masks):
                    if i != rest:
                        claimed |= m
                nearest[~claimed] = rest
            soft = np.stack([cv2.GaussianBlur((nearest == i).astype(np.float32), (0, 0), 3.0)
                             for i in range(len(masks))])
            nearest = soft.argmax(0)
            ids = []
            for i, colour in enumerate(colours):
                new[shoe & (nearest == i)] = nxt
                self.part_colours[nxt] = colour
                ids.append(nxt)
                nxt += 1

            # Lines along the edges between the parts and round the shoe.
            edge = boundaries(new) & ndi.binary_dilation(zone, iterations=8)
            by_shoe = ndi.binary_dilation(np.isin(new, ids))
            outer = edge & by_shoe & ndi.binary_dilation(new == 1) & ndi.binary_dilation(new != 1)
            inner = edge & by_shoe & ~outer
            lines = self.lines
            lines["outer"][win] = np.maximum(lines["outer"][win], edge_cover(outer, weights["outer"]))
            lines["inner"][win] = np.maximum(lines["inner"][win], edge_cover(inner, weights["inner"]))

            for pts_, closed in spec.get("details", []):
                c = cv.stroke(spline(pts_, closed), weights["fine"], closed) * shoe
                lines["fine"][win] = np.maximum(lines["fine"][win], c)

    def colours(self, cols):
        cols = cols.copy()
        for i, c in self.part_colours.items():
            if i < len(cols):
                cols[i] = c
        return cols

    def overlay(self, rgb, alpha):
        """Draws the laces and bows over the finished sprite."""

        line = self.weights["fine"] * 1.1
        for spec, (win, cv) in zip(self.specs, self.windows):
            sub_rgb = rgb[win]
            sub_a = alpha[win]

            def paint(cov, colour):
                c = cov[..., None]
                sub_rgb[:] = sub_rgb * (1 - c) + np.asarray(colour, float) * c
                sub_a[:] = np.maximum(sub_a, cov)

            laces = spec["laces"]
            fill = laces.get("colour", WHITE_LACE)
            lace_w = self.weights["fine"] * laces.get("width", 2.6)

            def lace(xy, closed=False, end=False):
                paint(cv.stroke(xy, lace_w + 2 * line, closed), LACE_EDGE)
                paint(cv.stroke(xy, lace_w, closed), fill)
                if end:
                    # A plastic tip on the loose end.
                    paint(cv.disc(xy[-1], lace_w * 0.75 + line), LACE_EDGE)
                    paint(cv.disc(xy[-1], lace_w * 0.75), AGLET)

            (a0, a1), (b0, b1) = laces["rows"]
            n = laces["eyelets"]
            t = np.linspace(0, 1, n)[:, None]
            a = np.asarray(a0) * (1 - t) + np.asarray(a1) * t
            b = np.asarray(b0) * (1 - t) + np.asarray(b1) * t

            if laces.get("style") == "bars":
                # Dress shoes: thin laces straight across, with small eyelets.
                for p, q in zip(a, b):
                    paint(cv.stroke(np.array([p, q]), lace_w, False), fill)
                    for e in (p, q):
                        paint(cv.disc(e, lace_w * 0.9), LACE_EDGE)
                continue

            # Eyelets, then the laces criss-crossing from the toe up, so the
            # higher crossings lie on top.
            r = max(lace_w * 0.55, line * 1.2)
            for p in np.vstack([a, b]):
                paint(cv.disc(p, r + line), LACE_EDGE)
                paint(cv.disc(p, r), EYELET)
            for i in range(n - 2, -1, -1):
                lace(np.array([a[i + 1], b[i]]))
                lace(np.array([b[i + 1], a[i]]))
            if "bow" not in spec:
                # No bow: a straight bar across the top pair.
                lace(np.array([a[0], b[0]]))

            bow = spec.get("bow")
            if bow:
                for end in bow["ends"]:
                    lace(spline(end), end=True)
                for loop in bow["loops"]:
                    lace(spline(loop, closed=True), closed=True)
                paint(cv.disc(bow["knot"], lace_w * 0.9 + line), LACE_EDGE)
                paint(cv.disc(bow["knot"], lace_w * 0.9), fill)

        return rgb, alpha


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def pick_label(lab, rgba, x, y, colour, reach=12):
    """
    The painted area at (x, y), or the one nearby closest to the given colour
    (so a point a little off still finds the right part).
    """

    h, w = lab.shape
    if not (0 <= x < w and 0 <= y < h):
        return 0
    ys = slice(max(y - reach, 0), min(y + reach + 1, h))
    xs = slice(max(x - reach, 0), min(x + reach + 1, w))
    cand = lab[ys, xs]
    labels = [l for l in np.unique(cand) if l > 1]
    if not labels:
        return 0
    rgb = rgba[ys, xs, :3].astype(float)
    if colour is None:
        # Skin: the palest warm area nearby.
        def warmth(l):
            c = rgb[cand == l].mean(0)
            return (c.mean() > 150) * 1000 + c[0] - c[2]
        return max(labels, key=warmth)
    want = np.asarray(colour, float)
    return min(labels, key=lambda l: np.linalg.norm(rgb[cand == l].mean(0) - want))
