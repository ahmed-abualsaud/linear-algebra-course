"""طائرة ركاب واقعية (منظر علوي) لقناة MACH-MATH.

الاستخدام:
    from common.mobjects.airplane import make_airplane, fly_along

    plane = make_airplane(scale=0.55)                 # المقدمة باتجاه +X، المركز عند الأصل
    plane.set_pose(path.point_from_proportion(0), path_heading(path, 0))
    scene.play(fly_along(plane, path, run_time=1.8))  # تدور تلقائياً مع مماس المسار

المكوّنات: جسم انسيابي بمقدمة مستديرة وذيل مدبب، أجنحة مائلة للخلف بمفصلات وأجنحة
تحكم (flaps/ailerons)، محركان نفاثان بمدخل هواء، أذيال أفقية وعمودية، زجاج قمرة القيادة،
تظليل ثنائي اللون وخطوط تقسيم الألواح.
"""

from manim import *
import numpy as np

from common.palette import COPPER_TERRA, IVORY_WHITE


def _mix(c1, c2, t):
    return interpolate_color(ManimColor(c1), ManimColor(c2), t)


def _half_width(x):
    """نصف عرض الجسم عند الموضع x (من -1 ذيل إلى +1 مقدمة)."""
    W = 0.105
    if x >= 0.55:
        t = (x - 0.55) / 0.45
        return W * max(0.0, 1.0 - t ** 2.3) ** 0.5
    if x >= -0.45:
        return W
    u = (x + 1.0) / 0.55
    return W * (0.17 + 0.83 * u ** 0.85)


def _poly(pts, fill, opacity=1.0, stroke=None, sw=0.0, so=1.0):
    p = Polygon(*[np.array([x, y, 0.0]) for x, y in pts])
    p.set_fill(fill, opacity=opacity)
    if stroke is None or sw == 0:
        p.set_stroke(width=0)
    else:
        p.set_stroke(stroke, width=sw, opacity=so)
    return p


def _build(body, accent, wing, dark):
    shade = _mix(body, "#000000", 0.28)       # جانب الظل
    light = _mix(body, "#FFFFFF", 0.35)       # لمعة
    wing_dark = _mix(wing, "#000000", 0.35)
    outline = _mix(body, "#000000", 0.55)
    engine = _mix(wing, "#000000", 0.18)

    parts = VGroup()

    # ---------------- الأجنحة الأفقية (الذيل) ----------------
    for s in (1, -1):
        parts.add(_poly(
            [(-0.78, s * 0.07), (-0.97, s * 0.42), (-1.07, s * 0.42), (-0.93, s * 0.07)],
            wing, 1.0, outline, 0.6))
        parts.add(_poly(
            [(-0.86, s * 0.07), (-1.02, s * 0.42), (-1.07, s * 0.42), (-0.93, s * 0.07)],
            wing_dark, 0.30))

    # ---------------- الأجنحة الرئيسية ----------------
    def LE(y):  # حافة الهجوم
        return 0.24 + (-0.44 - 0.24) * (y - 0.10) / 0.88

    def TE(y):  # حافة الخروج: خطان مائلان (كسر عند منتصف الجناح)
        if y <= 0.42:
            return -0.30 + (-0.46 + 0.30) * (y - 0.10) / 0.32
        return -0.46 + (-0.64 + 0.46) * (y - 0.42) / 0.56

    for s in (1, -1):
        ys = np.linspace(0.10, 0.98, 12)
        outline_pts = [(LE(y), s * y) for y in ys] + [(TE(y), s * y) for y in ys[::-1]]
        parts.add(_poly(outline_pts, wing, 1.0, outline, 0.8))
        # لمعة الحافة الأمامية (35% من الوتر)
        front = [(LE(y), s * y) for y in ys] + [
            (LE(y) + 0.35 * (TE(y) - LE(y)), s * y) for y in ys[::-1]]
        parts.add(_poly(front, light, 0.30))
        # ظل الجزء الخلفي
        back = [(LE(y) + 0.70 * (TE(y) - LE(y)), s * y) for y in ys] + [(TE(y), s * y) for y in ys[::-1]]
        parts.add(_poly(back, wing_dark, 0.22))
        # أجنحة التحكم: flaps داخلية و ailerons خارجية
        for (y0, y1, f0) in ((0.15, 0.56, 0.62), (0.66, 0.94, 0.70)):
            yy = np.linspace(y0, y1, 6)
            pts = [(LE(y) + f0 * (TE(y) - LE(y)), s * y) for y in yy] + [(TE(y), s * y) for y in yy[::-1]]
            parts.add(_poly(pts, wing_dark, 0.45, outline, 0.5, 0.7))
        # خطوط ألواح خفيفة
        for y in (0.30, 0.52, 0.74):
            a = LE(y) + 0.10 * (TE(y) - LE(y))
            b = LE(y) + 0.62 * (TE(y) - LE(y))
            parts.add(Line([a, s * y, 0], [b, s * y, 0], stroke_width=0.5, color=outline, stroke_opacity=0.35))
        # زعنفة طرف الجناح (winglet)
        parts.add(_poly(
            [(LE(0.98) - 0.02, s * 0.98), (TE(0.98), s * 0.98), (TE(0.98) - 0.05, s * 1.03), (LE(0.98) - 0.05, s * 1.03)],
            accent, 0.95, outline, 0.5))

    # ---------------- المحركات النفاثة ----------------
    for s in (1, -1):
        y = s * 0.42
        cx = LE(0.42) - 0.02
        nac = RoundedRectangle(corner_radius=0.065, width=0.44, height=0.13)
        nac.set_fill(engine, 1.0).set_stroke(outline, width=0.8)
        nac.move_to([cx, y, 0])
        hi = RoundedRectangle(corner_radius=0.03, width=0.36, height=0.035)
        hi.set_fill("#FFFFFF", 0.28).set_stroke(width=0)
        hi.move_to([cx - 0.01, y + s * 0.035, 0])
        inlet = Ellipse(width=0.05, height=0.105)
        inlet.set_fill(dark, 1.0).set_stroke(_mix(wing, "#FFFFFF", 0.4), width=1.0)
        inlet.move_to([cx + 0.22, y, 0])
        fan = Ellipse(width=0.022, height=0.06)
        fan.set_fill(_mix(dark, "#FFFFFF", 0.25), 1.0).set_stroke(width=0)
        fan.move_to([cx + 0.214, y, 0])
        exhaust = Ellipse(width=0.04, height=0.085)
        exhaust.set_fill("#121212", 1.0).set_stroke(outline, width=0.6)
        exhaust.move_to([cx - 0.215, y, 0])
        parts.add(nac, hi, inlet, fan, exhaust)

    # ---------------- الجسم ----------------
    xs = np.linspace(1.0, -1.0, 140)
    upper = [(x, _half_width(x)) for x in xs]
    lower = [(x, -_half_width(x)) for x in xs[::-1]]
    fus = _poly(upper + lower, body, 1.0, outline, 1.0)
    parts.add(fus)
    # تظليل: النصف السفلي أغمق، والنصف العلوي له لمعة
    parts.add(_poly([(x, 0.0) for x in xs] + lower, shade, 0.38))
    xs2 = np.linspace(0.92, -0.88, 80)
    parts.add(_poly([(x, _half_width(x) * 0.62) for x in xs2] +
                    [(x, _half_width(x) * 0.18) for x in xs2[::-1]], light, 0.35))
    # خطوط تقسيم الألواح
    for x in np.arange(0.50, -0.80, -0.14):
        w = _half_width(x)
        parts.add(Line([x, -w, 0], [x, w, 0], stroke_width=0.45, color=outline, stroke_opacity=0.28))
    # شريط الهوية (cheatline)
    parts.add(_poly([(x, -0.012) for x in np.linspace(0.62, -0.78, 30)] +
                    [(x, 0.012) for x in np.linspace(-0.78, 0.62, 30)], accent, 0.9))

    # ---------------- الذيل العمودي (منظر علوي: شريطاً رفيعاً) ----------------
    parts.add(_poly([(-0.58, 0.028), (-0.98, 0.016), (-0.98, -0.016), (-0.58, -0.028)],
                    accent, 1.0, outline, 0.5))
    parts.add(_poly([(-0.58, 0.028), (-0.98, 0.016), (-0.98, 0.0), (-0.58, 0.0)], "#FFFFFF", 0.22))

    # ---------------- قمرة القيادة ----------------
    parts.add(_poly([(0.87, 0.0), (0.79, 0.070), (0.745, 0.062), (0.745, -0.062), (0.79, -0.070)],
                    dark, 1.0, outline, 0.6))
    parts.add(_poly([(0.84, 0.0), (0.795, 0.045), (0.775, 0.040), (0.80, 0.0)], "#FFFFFF", 0.30))
    return parts


class MachAirplane(VGroup):
    """طائرة ركاب (منظر علوي). المقدمة باتجاه +X والمركز عند الأصل حتى تُحرَّك."""

    def __init__(self, body_color=IVORY_WHITE, accent_color=COPPER_TERRA,
                 wing_color="#CFC5AE", dark_color="#23201B", scale=1.0, **kwargs):
        super().__init__(**kwargs)
        self.add(*_build(body_color, accent_color, wing_color, dark_color))
        self.move_to(ORIGIN)
        self.scale(scale, about_point=ORIGIN)
        self._home = self.copy()  # الوضعية الأصلية: المقدمة +X، المركز ORIGIN
        self.heading = 0.0

    def set_pose(self, point, heading=0.0):
        """ضع الطائرة عند point بحيث تتجه مقدمتها بزاوية heading (راديان من +X)."""
        self.become(self._home)
        self.rotate(heading, about_point=ORIGIN)
        self.shift(np.array(point, dtype=float))
        self.heading = float(heading)
        return self


def make_airplane(color=IVORY_WHITE, accent=COPPER_TERRA, scale=1.0, **kwargs):
    """مصنع مختصر. الطول الكلي ≈ 2.1 وحدة × scale، وعرض الجناحين ≈ 2.1 × scale."""
    return MachAirplane(body_color=color, accent_color=accent, scale=scale, **kwargs)


def path_heading(path, alpha, eps=0.01):
    """زاوية مماس المسار عند النسبة alpha (0..1)."""
    a0, a1 = max(0.0, alpha - eps), min(1.0, alpha + eps)
    d = path.point_from_proportion(a1) - path.point_from_proportion(a0)
    return float(np.arctan2(d[1], d[0]))


def fly_along(plane, path, run_time=2.0, rate_func=smooth, **kwargs):
    """أنيميشن تحليق: تتحرك الطائرة على المسار وتدور مقدمتها مع المماس (تنعطف بسلاسة)."""
    state = {"h": plane.heading}

    def update(m, alpha):
        target = path_heading(path, alpha)
        # تنعيم الدوران (تجنب القفزات عند ±π)
        dh = (target - state["h"] + np.pi) % (2 * np.pi) - np.pi
        state["h"] += dh * 0.35 if alpha > 0 else dh
        m.set_pose(path.point_from_proportion(alpha), state["h"])

    return UpdateFromAlphaFunc(plane, update, run_time=run_time, rate_func=rate_func, **kwargs)