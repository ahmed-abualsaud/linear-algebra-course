from manim import *
import numpy as np

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_DARK,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.latex import mach_math_template


# ==============================================================
# أدوات مساعدة صغيرة
# ==============================================================

def _V(x, y):
    return np.array([float(x), float(y), 0.0])


def _mix(c, other="#000000", a=0.4):
    """مزج لونين (لعمل ظل أو إضاءة)."""
    return interpolate_color(ManimColor(c), ManimColor(other), a)


def _poly(pts, fill, stroke=None, sw=0.8, fo=1.0, so=1.0, r=0.0):
    m = Polygon(
        *[_V(p[0], p[1]) for p in pts],
        stroke_width=sw,
        stroke_color=stroke if stroke is not None else fill,
        stroke_opacity=so,
        fill_color=fill,
        fill_opacity=fo,
    )
    if r > 0:
        m.round_corners(r)
    return m


def _ell(cx, cy, w, h, fill, stroke=None, sw=0.8, fo=1.0, so=1.0):
    return Ellipse(
        width=w,
        height=h,
        stroke_width=sw,
        stroke_color=stroke if stroke is not None else fill,
        stroke_opacity=so,
        fill_color=fill,
        fill_opacity=fo,
    ).move_to(_V(cx, cy))


def _seg(a, b, color, sw=1.5, op=1.0):
    return Line(_V(*a), _V(*b), stroke_width=sw, stroke_color=color, stroke_opacity=op)


def _path(pts, color, sw=1.0, op=1.0):
    """خط منكسر من عدة نقاط (للطيّات والتفاصيل الدقيقة)."""
    g = VGroup()
    for a, b in zip(pts[:-1], pts[1:]):
        g.add(_seg(a, b, color, sw, op))
    return g


def _limb(p0, p1, w0, w1, color, edge=None, sw=0.6):
    """طرف مخروطي (ذراع/ساق) بعرضين مختلفين عند الطرفين + مفصلين مدورين."""
    p0, p1 = np.array(p0, dtype=float), np.array(p1, dtype=float)
    d = p1 - p0
    n = np.array([-d[1], d[0]])
    n = n / (np.linalg.norm(n) + 1e-9)
    quad = [p0 + n * w0 / 2, p1 + n * w1 / 2, p1 - n * w1 / 2, p0 - n * w0 / 2]
    g = VGroup()
    g.add(_poly(quad, color, edge if edge is not None else color, sw))
    g.add(Dot(_V(*p0), radius=w0 / 2, color=color))
    g.add(Dot(_V(*p1), radius=w1 / 2, color=color))
    return g


def _vgrad(x0, x1, y0, y1, c_top, c_bot, n=12, op=1.0):
    """مستطيل بتدرّج لوني رأسي (شرائح متراصة)."""
    g = VGroup()
    h = (y1 - y0) / n
    for i in range(n):
        col = _mix(c_top, c_bot, (i + 0.5) / n)
        ya, yb = y1 - i * h, y1 - (i + 1) * h
        g.add(_poly([(x0, ya), (x1, ya), (x1, yb - 0.012), (x0, yb - 0.012)], col, col, 0.4, op, op))
    return g


# ==============================================================
# هندسة الغرفة (منظور ثلاثي الأبعاد)
# ==============================================================

WX = 3.7          # نصف عرض الجدار الخلفي
WY0 = 0.85        # خط التقاء الجدار بالأرض
WY1 = 3.62        # أعلى الجدار
VY = 14.0         # ارتفاع نقطة التلاشي
FLOOR_FRONT = -2.70
WAIN = 1.20       # ارتفاع الدادو الخشبي أسفل الجدار


def _kf(y):
    """معامل التكبير للأرض عند الإحداثي y على الشاشة."""
    return (VY - y) / (VY - WY0)


def _fl(x0, y):
    """نقطة على الأرض: x0 هو الموضع الجانبي عند الجدار الخلفي."""
    return (x0 * _kf(y), y)


def _lw(k, y0):
    return (-WX * k, VY + (y0 - VY) * k)


def _rw(k, y0):
    return (WX * k, VY + (y0 - VY) * k)


KMAX = _kf(FLOOR_FRONT)


def _wall_quad(side, k0, k1, ya, yb):
    f = _lw if side < 0 else _rw
    return [f(k0, ya), f(k1, ya), f(k1, yb), f(k0, yb)]


# ==============================================================
# 1. الكتاب المفتوح على الطاولة
# ==============================================================

def _make_book(cx, cy, s, cover=COPPER_TERRA):
    hf, hb, hh = 0.38 * s, 0.33 * s, 0.18 * s
    yf, yb = cy - hh, cy + hh
    m = 0.03 * s

    g = VGroup()
    # ظل الكتاب على سطح الطاولة
    g.add(_poly(
        [(cx - hf - m + 0.03, yf - m - 0.02), (cx + hf + m + 0.03, yf - m - 0.02),
         (cx + hb + m + 0.03, yb + m - 0.02), (cx - hb - m + 0.03, yb + m - 0.02)],
        "#000000", "#000000", 0.0, 0.28, 0.0,
    ))
    g.add(_poly(
        [(cx - hf - m, yf - m), (cx + hf + m, yf - m), (cx + hb + m, yb + m), (cx - hb - m, yb + m)],
        cover, _mix(cover, "#000000", 0.45), 0.7,
    ))
    g.add(_poly(
        [(cx - hf, yf), (cx, yf + 0.012 * s), (cx, yb + 0.012 * s), (cx - hb, yb)],
        "#D8CDB0", "#8F8468", 0.5,
    ))
    g.add(_poly(
        [(cx, yf + 0.012 * s), (cx + hf, yf), (cx + hb, yb), (cx, yb + 0.012 * s)],
        "#C4B898", "#8F8468", 0.5,
    ))
    g.add(_seg((cx, yf + 0.012 * s), (cx, yb + 0.012 * s), "#6E654F", 0.9, 0.9))

    for t in (0.2, 0.4, 0.6, 0.8):
        y = yf + (yb - yf) * t
        half = hf + (hb - hf) * t
        g.add(_seg((cx - half * 0.88, y), (cx - half * 0.14, y), "#6E654F", 0.6, 0.55))
        g.add(_seg((cx + half * 0.14, y), (cx + half * 0.88, y), "#6E654F", 0.6, 0.55))
    return g


# ==============================================================
# 2. الطاولة (سطح بمنظور + سمك أمامي + أرجل + ظل على الأرض)
# ==============================================================

def _make_desk(cx, y_back, y_front, w_back, w_front, thick, floor_y):
    g = VGroup()
    top_col = "#6B4B2D"

    # ظل الطاولة على الأرض
    g.add(_ell(cx + 0.10, floor_y + 0.02, w_front * 0.98, 0.30, "#000000", sw=0, fo=0.30))
    g.add(_ell(cx + 0.10, floor_y + 0.02, w_front * 0.80, 0.18, "#000000", sw=0, fo=0.22))

    # الأرجل الخلفية
    for xf in (cx - w_back / 2 + 0.12, cx + w_back / 2 - 0.12):
        g.add(_seg((xf, y_back), (xf, floor_y + 0.20), "#2A1C0E", 2.0))

    g.add(_poly(
        [(cx - w_back / 2, y_back), (cx + w_back / 2, y_back), (cx + w_front / 2, y_front), (cx - w_front / 2, y_front)],
        top_col, GOLD_DARK, 0.9,
    ))
    # عروق الخشب
    for t in (0.2, 0.42, 0.66, 0.86):
        y = y_front + (y_back - y_front) * t
        w = w_front + (w_back - w_front) * t
        g.add(_seg((cx - w / 2 + 0.05, y), (cx + w / 2 - 0.05, y), _mix(top_col, "#000000", 0.35), 0.7, 0.55))
    g.add(_poly(
        [(cx - w_back / 2 + 0.05, y_back - 0.02), (cx - w_back * 0.05, y_back - 0.02),
         (cx - w_front * 0.15, y_front + 0.10), (cx - w_front / 2 + 0.10, y_front + 0.10)],
        "#FFFFFF", sw=0, fo=0.05,
    ))
    # السمك الأمامي
    g.add(_poly(
        [(cx - w_front / 2, y_front), (cx + w_front / 2, y_front),
         (cx + w_front / 2, y_front - thick), (cx - w_front / 2, y_front - thick)],
        "#3A2711", GOLD_DARK, 0.8,
    ))
    g.add(_seg((cx - w_front / 2, y_front), (cx + w_front / 2, y_front), GOLD_LIGHT, 1.0, 0.55))
    # الأرجل الأمامية
    for xf in (cx - w_front / 2 + 0.10, cx + w_front / 2 - 0.10):
        g.add(_seg((xf, y_front - thick), (xf, floor_y), "#2E200F", 2.4))
        g.add(_seg((xf + 0.012, y_front - thick), (xf + 0.012, floor_y), GOLD_DARK, 0.8, 0.8))
    return g


# ==============================================================
# 3. طالب/طالبة من الخلف
# ==============================================================

def make_student_from_behind(pos, s=0.8, skin="#C99A78", hair="#17100A",
                             shirt="#3F5A6B", style="short", hijab="#6B4E71", look=0.0):
    ox, oy = float(pos[0]), float(pos[1])

    def Q(x, y):
        return (ox + x * s, oy + y * s)

    wood, wood_dark = "#4A3622", "#2A1D10"
    floor_y = oy - 0.74 * s
    g = VGroup()

    # ---- ظل على الأرض + أرجل الكرسي ----
    g.add(_ell(ox + 0.05 * s, floor_y, 0.80 * s, 0.13 * s, "#000000", sw=0, fo=0.5))
    for sx in (-1, 1):
        g.add(_seg(Q(sx * 0.19, 0.06), (ox + sx * 0.19 * s, floor_y + 0.13 * s), GOLD_DARK, 1.6, 0.8))
    for sx in (-1, 1):
        g.add(_seg(Q(sx * 0.20, 0.0), (ox + sx * 0.22 * s, floor_y), GOLD_DARK, 2.0))

    # ---- الجذع (كتفان مائلان) ----
    torso_pts = [(-0.12, 0.66), (0.12, 0.66), (0.27, 0.60), (0.285, 0.48),
                 (0.23, 0.0), (-0.23, 0.0), (-0.285, 0.48), (-0.27, 0.60)]
    g.add(_poly([Q(*p) for p in torso_pts], shirt, _mix(shirt, "#FFFFFF", 0.25), 0.8, r=0.03 * s))
    g.add(_poly([Q(*p) for p in [(0.0, 0.66), (0.12, 0.66), (0.27, 0.60), (0.285, 0.48), (0.23, 0.0), (0.0, 0.0)]],
                "#000000", sw=0, fo=0.22))
    g.add(_seg(Q(0, 0.60), Q(0, 0.06), _mix(shirt, "#000000", 0.4), 1.0, 0.7))
    g.add(_poly([Q(-0.12, 0.66), Q(0.12, 0.66), Q(0.09, 0.60), Q(-0.09, 0.60)],
                _mix(shirt, "#FFFFFF", 0.15), sw=0.6))

    # ---- الرقبة ----
    g.add(_poly([Q(-0.055, 0.74), Q(0.055, 0.74), Q(0.06, 0.66), Q(-0.06, 0.66)],
                _mix(skin, "#000000", 0.18), sw=0))

    # ---- الذراعان: الكوع للخارج والساعد للأمام على الطاولة ----
    sleeve = _mix(shirt, "#000000", 0.1)
    for sx in (-1, 1):
        sh, el, hd = Q(sx * 0.26, 0.56), Q(sx * 0.40, 0.40), Q(sx * 0.29, 0.78)
        g.add(_seg(sh, el, sleeve, 11 * s))
        g.add(Dot(_V(*sh), radius=0.055 * s, color=sleeve))
        g.add(Dot(_V(*el), radius=0.045 * s, color=sleeve))
        g.add(_seg(el, hd, skin, 7.5 * s))
        g.add(Dot(_V(*hd), radius=0.042 * s, color=skin))

    # ---- الكرسي ----
    g.add(_poly([Q(-0.25, -0.01), Q(0.25, -0.01), Q(0.23, -0.08), Q(-0.23, -0.08)], wood_dark, GOLD_DARK, 0.8))
    for sx in (-1, 1):
        g.add(_seg(Q(sx * 0.18, 0.0), Q(sx * 0.18, 0.25), wood, 2.0))
    back = RoundedRectangle(
        corner_radius=0.04 * s, width=0.46 * s, height=0.15 * s,
        stroke_width=1.0, stroke_color=GOLD_DARK, fill_color=wood, fill_opacity=1.0,
    ).move_to(_V(*Q(0, 0.27)))
    g.add(back)

    # ---- الشعر الخلفي / غطاء الرأس ----
    if style == "long":
        g.add(_poly([Q(-0.20, 0.96), Q(0.20, 0.96), Q(0.19, 0.50), Q(0.14, 0.40), Q(-0.14, 0.40), Q(-0.19, 0.50)],
                    hair, _mix(hair, "#FFFFFF", 0.2), 0.7, r=0.05 * s))
        g.add(_poly([Q(0.0, 0.96), Q(0.20, 0.96), Q(0.19, 0.50), Q(0.14, 0.40), Q(0.0, 0.40)],
                    "#000000", sw=0, fo=0.25))
        g.add(_seg(Q(-0.06, 0.88), Q(-0.07, 0.48), _mix(hair, "#FFFFFF", 0.3), 1.0, 0.45))
    elif style == "ponytail":
        g.add(_ell(*Q(0.0, 0.70), 0.10 * s, 0.34 * s, hair, _mix(hair, "#FFFFFF", 0.2), 0.7))
        g.add(Dot(_V(*Q(0.0, 0.87)), radius=0.03 * s, color=COPPER_TERRA))
    elif style == "hijab":
        hj_edge = _mix(hijab, "#FFFFFF", 0.22)
        hj_dark = _mix(hijab, "#000000", 0.40)
        hj_lite = _mix(hijab, "#FFFFFF", 0.30)
        # القماش ينزل من خلف الرأس فوق الكتفين وينتهي أسفل لوح الكتف بحافة منحنية
        drape = [(-0.14, 0.85), (-0.215, 0.76), (-0.285, 0.66), (-0.305, 0.58), (-0.292, 0.50), (-0.262, 0.445),
                 (-0.14, 0.41), (0.0, 0.40), (0.14, 0.41), (0.262, 0.445), (0.292, 0.50), (0.305, 0.58),
                 (0.285, 0.66), (0.215, 0.76), (0.14, 0.85)]
        g.add(_poly([Q(*p) for p in drape], hijab, hj_edge, 0.8, r=0.04 * s))
        # ظل الجهة اليمنى (الإضاءة من اليسار)
        g.add(_poly([Q(*p) for p in [(0.02, 0.85), (0.14, 0.85), (0.215, 0.76), (0.285, 0.66), (0.305, 0.58),
                                     (0.292, 0.50), (0.262, 0.445), (0.14, 0.41), (0.02, 0.40)]],
                    "#000000", sw=0, fo=0.22))
        # لمعة القماش فوق الكتف الأيسر
        g.add(_path([Q(-0.17, 0.79), Q(-0.25, 0.69), Q(-0.285, 0.60)], hj_lite, 1.6, 0.45))
        # طيّات ناعمة متوازية تنساب من الرأس إلى الحافة السفلية
        g.add(_path([Q(-0.08, 0.80), Q(-0.12, 0.68), Q(-0.13, 0.56), Q(-0.10, 0.44)], hj_dark, 1.1, 0.70))
        g.add(_path([Q(0.03, 0.82), Q(0.04, 0.68), Q(0.035, 0.55), Q(0.04, 0.41)], hj_dark, 1.0, 0.55))
        g.add(_path([Q(0.13, 0.80), Q(0.19, 0.68), Q(0.215, 0.56), Q(0.19, 0.445)], hj_dark, 1.1, 0.70))
        # لمعة الحافة السفلية + ظل أسفل الرأس
        g.add(_path([Q(-0.25, 0.455), Q(-0.14, 0.418), Q(0.0, 0.408), Q(0.14, 0.418), Q(0.25, 0.455)], hj_lite, 1.0, 0.45))
        g.add(_ell(*Q(0, 0.80), 0.28 * s, 0.09 * s, "#000000", sw=0, fo=0.20))

    # ---- الرأس ----
    head = VGroup()
    hc = Q(0, 0.97)
    if style == "hijab":
        hj_edge = _mix(hijab, "#FFFFFF", 0.22)
        hj_dark = _mix(hijab, "#000000", 0.40)
        # قبة الرأس الملفوفة (ناعمة بدون أي تفاصيل غريبة)
        head.add(_ell(*Q(0, 0.965), 0.39 * s, 0.44 * s, hijab, hj_edge, 0.8))
        head.add(_ell(*Q(0.075, 0.95), 0.25 * s, 0.35 * s, "#000000", sw=0, fo=0.20))
        head.add(_path([Q(0.0, 1.17), Q(-0.01, 1.05), Q(0.0, 0.92), Q(0.005, 0.80)], hj_dark, 0.9, 0.35))
        hl_col = _mix(hijab, "#FFFFFF", 0.45)
    elif style == "bob":
        # شعر قصير (بوب) من الخلف: قبة ناعمة تنزل لمستوى الذقن بحافة منحنية
        bob = [(-0.205, 0.745), (-0.225, 0.80), (-0.232, 0.88), (-0.222, 0.98), (-0.19, 1.08), (-0.13, 1.155),
               (-0.06, 1.19), (0.0, 1.198), (0.06, 1.19), (0.13, 1.155), (0.19, 1.08), (0.222, 0.98),
               (0.232, 0.88), (0.225, 0.80), (0.205, 0.745), (0.10, 0.728), (0.0, 0.722), (-0.10, 0.728)]
        head.add(_poly([Q(*p) for p in bob], hair, _mix(hair, "#FFFFFF", 0.2), 0.7, r=0.05 * s))
        head.add(_poly([Q(*p) for p in [(0.0, 1.198), (0.06, 1.19), (0.13, 1.155), (0.19, 1.08), (0.222, 0.98),
                                        (0.232, 0.88), (0.225, 0.80), (0.205, 0.745), (0.10, 0.728), (0.0, 0.722)]],
                    "#000000", sw=0, fo=0.25))
        head.add(_poly([Q(*p) for p in [(-0.20, 0.775), (0.20, 0.775), (0.205, 0.745), (0.10, 0.728), (0.0, 0.722),
                                        (-0.10, 0.728), (-0.205, 0.745)]], "#000000", sw=0, fo=0.22))
        head.add(_path([Q(-0.10, 1.15), Q(-0.15, 1.0), Q(-0.17, 0.85), Q(-0.16, 0.76)],
                       _mix(hair, "#FFFFFF", 0.4), 1.0, 0.30))
        head.add(_path([Q(0.06, 1.17), Q(0.10, 1.0), Q(0.115, 0.86), Q(0.11, 0.75)],
                       _mix(hair, "#000000", 0.5), 1.0, 0.45))
        hl_col = _mix(hair, "#FFFFFF", 0.5)
    else:
        head.add(_ell(*Q(0, 0.94), 0.36 * s, 0.40 * s, skin, _mix(skin, "#000000", 0.3), 0.6))
        if style in ("short", "ponytail", "bun"):
            for sx in (-1, 1):
                head.add(_ell(*Q(sx * 0.185, 0.92), 0.05 * s, 0.09 * s, _mix(skin, "#000000", 0.12), sw=0))
            head.add(_ell(*Q(0, 0.995), 0.40 * s, 0.36 * s, hair, _mix(hair, "#FFFFFF", 0.2), 0.7))
            if style == "bun":
                # كعكة شعر فوق الرأس + رباط شعر (لا شيء يغطي الرقبة)
                head.add(_ell(*Q(0, 1.215), 0.17 * s, 0.15 * s, hair, _mix(hair, "#FFFFFF", 0.2), 0.7))
                head.add(_ell(*Q(-0.03, 1.245), 0.06 * s, 0.035 * s, _mix(hair, "#FFFFFF", 0.45), sw=0, fo=0.55))
                head.add(_ell(*Q(0, 1.165), 0.15 * s, 0.045 * s, COPPER_TERRA, _mix(COPPER_TERRA, "#000000", 0.35), 0.6))
        else:
            head.add(_ell(*Q(0, 0.985), 0.42 * s, 0.42 * s, hair, _mix(hair, "#FFFFFF", 0.2), 0.7))
        head.add(_ell(*Q(0.08, 0.97), 0.24 * s, 0.30 * s, "#000000", sw=0, fo=0.18))
        hl_col = _mix(hair, "#FFFFFF", 0.5)
    head.add(Arc(radius=0.15 * s, start_angle=105 * DEGREES, angle=55 * DEGREES,
                 arc_center=_V(*hc), stroke_color=hl_col, stroke_width=1.4, stroke_opacity=0.6))
    head.rotate(look * DEGREES, about_point=_V(*Q(0, 0.70)))
    g.add(head)
    return g


# ==============================================================
# 4. المعلم (كف يد متناسب وأصابع مضمومة عند الحافة الداخلية للنوتة)
# ==============================================================

def make_teacher(feet_pos, H=1.95, target=(0.0, 1.8), stick_length=0.86):
    """
    feet_pos     : موضع القدمين على الأرض
    H            : الطول الكلي للمعلم
    target       : النقطة التي تشير إليها العصا على السبورة
    stick_length : طول عصا الإشارة ليكون متناسباً وطبيعياً
    """
    fx, fy = float(feet_pos[0]), float(feet_pos[1])

    def P(x, y):
        return (fx + x * H, fy + y * H)

    skin = "#C8946F"
    skin_sh = _mix(skin, "#000000", 0.22)
    hair = "#1A110A"
    jacket = "#7B3F26"
    jacket_sh = _mix(jacket, "#000000", 0.32)
    jacket_hi = _mix(jacket, "#FFFFFF", 0.22)
    pants, pants_far = "#2F303A", "#20212A"
    shirt, tie = "#E7DDC6", "#C9972A"
    shoe = "#140E09"

    g = VGroup()

    # ---- 1. ظل على الأرض ----
    g.add(_ell(fx + 0.08 * H, fy - 0.004 * H, 0.62 * H, 0.060 * H, "#000000", sw=0, fo=0.50))
    g.add(_ell(fx + 0.05 * H, fy - 0.002 * H, 0.34 * H, 0.038 * H, "#000000", sw=0, fo=0.35))

    # ---- 2. الساق البعيدة والحذاء ----
    g.add(_poly([P(-0.048, 0.520), P(0.012, 0.520), P(0.004, 0.300), P(0.000, 0.045), P(-0.046, 0.045), P(-0.052, 0.300)],
                pants_far, _mix(pants_far, "#FFFFFF", 0.12), 0.6))
    g.add(_poly([P(-0.052, 0.048), P(0.004, 0.048), P(0.030, 0.026), P(0.060, 0.017), P(0.060, 0.000), P(-0.056, 0.000)],
                shoe, _mix(shoe, "#FFFFFF", 0.2), 0.6, r=0.004 * H))

    # ---- 3. الذراع البعيدة (تشير بالعصا نحو السبورة - تخرج من خلف الجذع) ----
    S_far = P(0.020, 0.790)
    E_far = P(0.090, 0.725)
    W_far = P(0.165, 0.785)
    g.add(_limb(S_far, E_far, 0.046 * H, 0.036 * H, jacket_sh))
    g.add(_limb(E_far, W_far, 0.036 * H, 0.028 * H, jacket_sh))

    cuff_far_dir = np.array(W_far) - np.array(E_far)
    cuff_far_dir = cuff_far_dir / np.linalg.norm(cuff_far_dir)
    cuff_far_a = np.array(W_far) - cuff_far_dir * 0.008 * H
    cuff_far_b = np.array(W_far) + cuff_far_dir * 0.004 * H
    g.add(_limb(cuff_far_a, cuff_far_b, 0.030 * H, 0.030 * H, shirt, _mix(shirt, "#000000", 0.35), 0.5))

    hand_far = np.array(W_far) + cuff_far_dir * 0.018 * H

    # عصا الإشارة (ممتدة من اليد البعيدة نحو السبورة)
    tgt = np.array(target, dtype=float)
    d = tgt - hand_far
    d = d / np.linalg.norm(d)
    stick_tip = hand_far + d * stick_length

    g.add(_seg(hand_far - d * 0.035 * H, stick_tip, "#E9C46A", 2.2))
    g.add(_seg(hand_far - d * 0.035 * H, stick_tip, _mix("#E9C46A", "#000000", 0.5), 0.8, 0.7))
    g.add(Dot(_V(*stick_tip), radius=0.012, color="#8E6B1E"))

    # كف اليد البعيدة يقبض على العصا
    g.add(_ell(hand_far[0], hand_far[1], 0.034 * H, 0.025 * H, skin_sh, _mix(skin_sh, "#000000", 0.2), 0.5).rotate(30 * DEGREES))
    g.add(_ell(hand_far[0] + 0.010 * H, hand_far[1] - 0.005 * H, 0.018 * H, 0.012 * H, skin_sh, sw=0).rotate(20 * DEGREES))

    # ---- 4. الساق القريبة والحذاء ----
    g.add(_poly([P(-0.038, 0.520), P(0.054, 0.520), P(0.050, 0.300), P(0.044, 0.045), P(-0.008, 0.045), P(-0.020, 0.300)],
                pants, _mix(pants, "#FFFFFF", 0.14), 0.7))
    g.add(_poly([P(-0.038, 0.520), P(-0.020, 0.300), P(-0.008, 0.045), P(0.014, 0.045), P(0.004, 0.300), P(0.012, 0.520)],
                "#000000", sw=0, fo=0.20))
    g.add(_seg(P(0.018, 0.505), P(0.020, 0.060), _mix(pants, "#FFFFFF", 0.22), 0.8, 0.7))
    g.add(_poly([P(-0.010, 0.048), P(0.048, 0.048), P(0.074, 0.026), P(0.104, 0.017), P(0.104, 0.000), P(-0.016, 0.000)],
                shoe, _mix(shoe, "#FFFFFF", 0.25), 0.7, r=0.004 * H))
    g.add(_seg(P(-0.014, 0.006), P(0.100, 0.006), "#3A2A1A", 1.0, 0.9))
    g.add(_seg(P(0.050, 0.044), P(0.092, 0.024), _mix(shoe, "#FFFFFF", 0.45), 0.8, 0.6))

    # ---- 5. الجاكيت والجذع (ظهر مستقيم طبيعي وأنيق بدون أي بروز) ----
    torso = [
        (-0.034, 0.835), (0.050, 0.835), (0.070, 0.785), (0.072, 0.690),
        (0.068, 0.590), (0.062, 0.490), (-0.040, 0.490), (-0.042, 0.590),
        (-0.044, 0.710), (-0.038, 0.790)
    ]
    g.add(_poly([P(*p) for p in torso], jacket, jacket_hi, 0.9, r=0.010 * H))
    
    # تظليل الظهر المعتدل
    g.add(_poly([P(*p) for p in [(-0.034, 0.835), (-0.005, 0.835), (-0.008, 0.490), (-0.040, 0.490), (-0.042, 0.590), (-0.044, 0.710)]],
                "#000000", sw=0, fo=0.18))
    g.add(_seg(P(-0.020, 0.500), P(-0.022, 0.600), jacket_sh, 0.8, 0.8))
    g.add(_seg(P(-0.036, 0.495), P(0.056, 0.495), jacket_sh, 1.0, 0.9))

    # الياقة والقميص والكرافتة أعلى الصدر
    g.add(_poly([P(0.022, 0.838), P(0.050, 0.832), P(0.054, 0.710), P(0.032, 0.710)],
                shirt, _mix(shirt, "#000000", 0.35), 0.5))
    g.add(_poly([P(0.032, 0.834), P(0.046, 0.830), P(0.050, 0.720), P(0.043, 0.690), P(0.036, 0.720)],
                tie, _mix(tie, "#000000", 0.4), 0.5))
    g.add(_poly([P(0.038, 0.838), P(0.064, 0.735), P(0.054, 0.690), P(0.042, 0.760)], jacket_sh, jacket_hi, 0.6))

    # أزرار البدلة في المنتصف
    g.add(Dot(_V(*P(0.054, 0.670)), radius=0.0042 * H, color="#2A160C"))
    g.add(Dot(_V(*P(0.052, 0.590)), radius=0.0042 * H, color="#2A160C"))

    # جيب البدلة الجانبي
    g.add(_poly([P(-0.026, 0.535), P(0.012, 0.535), P(0.012, 0.520), P(-0.026, 0.520)], jacket_sh, jacket_hi, 0.5))

    # ---- 6. الرقبة والياقة ----
    g.add(_poly([P(-0.026, 0.800), P(0.034, 0.800), P(0.030, 0.878), P(-0.024, 0.878)], skin_sh, sw=0.4))
    g.add(_poly([P(-0.034, 0.842), P(0.036, 0.844), P(0.050, 0.822), P(0.022, 0.810), P(-0.032, 0.818)],
                shirt, _mix(shirt, "#000000", 0.35), 0.5))

    # ---- 7. الرأس والوجه ----
    face = [(0.018, 0.992), (0.038, 0.970), (0.043, 0.950), (0.041, 0.938), (0.043, 0.930), (0.058, 0.914),
            (0.050, 0.907), (0.047, 0.901), (0.049, 0.895), (0.046, 0.889), (0.044, 0.880), (0.046, 0.871),
            (0.036, 0.862), (0.012, 0.859), (-0.012, 0.872), (-0.030, 0.900), (-0.040, 0.930), (-0.040, 0.962)]
    g.add(_ell(*P(-0.004, 0.945), 0.098 * H, 0.116 * H, skin, skin_sh, 0.5))
    g.add(_poly([P(*p) for p in face], skin, skin_sh, 0.6))
    g.add(_poly([P(*p) for p in [(0.000, 0.870), (0.040, 0.864), (0.030, 0.856), (0.004, 0.858)]], "#000000", sw=0, fo=0.18))
    # الشعر
    hair_pts = [(0.040, 0.972), (0.030, 0.992), (0.005, 1.004), (-0.025, 0.996), (-0.048, 0.966), (-0.053, 0.930),
                (-0.046, 0.900), (-0.034, 0.886), (-0.030, 0.906), (-0.014, 0.934), (0.010, 0.952), (0.030, 0.962)]
    g.add(_poly([P(*p) for p in hair_pts], hair, _mix(hair, "#FFFFFF", 0.25), 0.7, r=0.006 * H))
    g.add(Arc(radius=0.045 * H, start_angle=60 * DEGREES, angle=60 * DEGREES, arc_center=_V(*P(-0.004, 0.945)),
              stroke_color=_mix(hair, "#FFFFFF", 0.55), stroke_width=1.2, stroke_opacity=0.6))
    # الأذن
    g.add(_ell(*P(-0.010, 0.924), 0.020 * H, 0.034 * H, skin_sh, _mix(skin, "#000000", 0.45), 0.5))
    g.add(_seg(P(-0.012, 0.930), P(-0.009, 0.918), _mix(skin, "#000000", 0.5), 0.6, 0.8))
    # العين والحاجب والفم والشارب
    g.add(Dot(_V(*P(0.034, 0.934)), radius=0.0042 * H, color="#120C08"))
    g.add(_seg(P(0.024, 0.946), P(0.043, 0.949), "#2A1A10", 1.6, 0.95))
    g.add(_seg(P(0.048, 0.893), P(0.039, 0.892), "#5A3322", 1.1))
    g.add(_poly([P(0.047, 0.903), P(0.050, 0.899), P(0.045, 0.896), P(0.034, 0.899)], hair, sw=0.4))
    # نظارة رفيعة
    g.add(_ell(*P(0.033, 0.934), 0.034 * H, 0.028 * H, "#000000", GOLD_LIGHT, 1.0, fo=0.0, so=0.9))
    g.add(_seg(P(0.016, 0.936), P(-0.008, 0.936), GOLD_LIGHT, 0.9, 0.8))

    # ---- 8. الذراع القريبة ودفتر التحضير ----
    # الساعد يمتد للأمام واليد تقبض على كعب النوتة: ظهر الكف والأصابع الأربعة
    # ملتفة فوق الغلاف ظاهرة، أما الإبهام فخلف الدفتر (مخفي).
    S_near = P(-0.005, 0.795)
    E_near = P(0.005, 0.645)
    W_near = P(0.074, 0.612)
    g.add(_limb(S_near, E_near, 0.046 * H, 0.038 * H, jacket, jacket_hi, 0.6))
    g.add(_limb(E_near, W_near, 0.038 * H, 0.030 * H, jacket, jacket_hi, 0.6))

    fore_dir = np.array(W_near) - np.array(E_near)
    fore_dir = fore_dir / np.linalg.norm(fore_dir)
    cuff_near_a = np.array(W_near) - fore_dir * 0.007 * H
    cuff_near_b = np.array(W_near) + fore_dir * 0.004 * H
    g.add(_limb(cuff_near_a, cuff_near_b, 0.030 * H, 0.030 * H, shirt, _mix(shirt, "#000000", 0.35), 0.5))

    # ==========================================================
    # النوتة (الغلاف يواجه المشاهد)
    # ==========================================================
    nb_cover = "#C28532"   # لون الغلاف الجلدي
    nb_spine = "#7A4E18"   # كعب الدفتر (الحافة الداخلية)
    nb_edge  = "#5C370C"

    BL, BR, TR, TL = (0.092, 0.552), (0.164, 0.560), (0.162, 0.676), (0.090, 0.668)

    # شريط إشارة مرجعية يتدلى من أسفل الأوراق (يُرسم قبل الغلاف فيخرج من تحته)
    g.add(_path([P(0.136, 0.560), P(0.139, 0.532), P(0.146, 0.514)], COPPER_TERRA, 2.0, 0.95))
    g.add(_path([P(0.146, 0.514), P(0.1415, 0.5095)], COPPER_TERRA, 1.6, 0.95))
    g.add(_path([P(0.146, 0.514), P(0.1505, 0.5105)], COPPER_TERRA, 1.6, 0.95))

    # ظل خفيف للنوتة (الإضاءة من اليسار فيسقط الظل لليمين وأسفل)
    g.add(_poly([P(BL[0] + 0.007, BL[1] - 0.008), P(BR[0] + 0.007, BR[1] - 0.008),
                 P(TR[0] + 0.007, TR[1] - 0.008), P(TL[0] + 0.007, TL[1] - 0.008)],
                "#000000", sw=0, fo=0.24, r=0.004 * H))

    # حواف الأوراق (فوق ويمين الغلاف)
    g.add(_poly([P(0.092, 0.6685), P(0.1615, 0.6765), P(0.1635, 0.6825), P(0.0945, 0.6745)],
                "#FAF6EC", "#D4C8B0", 0.4))
    g.add(_poly([P(0.164, 0.560), P(0.1685, 0.5625), P(0.1668, 0.6825), P(0.1625, 0.676)],
                "#EDE3CB", "#D4C8B0", 0.4))

    # الغلاف الرئيسي
    g.add(_poly([P(*BL), P(*BR), P(*TR), P(*TL)], nb_cover, nb_edge, 0.8, r=0.004 * H))
    g.add(_poly([P(0.106, 0.556), P(0.124, 0.558), P(0.112, 0.670), P(0.104, 0.669)],
                "#FFFFFF", sw=0, fo=0.07))
    # كعب الدفتر (الحافة الداخلية) + خط الخياطة
    g.add(_poly([P(0.092, 0.552), P(0.104, 0.553), P(0.102, 0.669), P(0.090, 0.668)], nb_spine, nb_edge, 0.5))
    g.add(_seg(P(0.1045, 0.556), P(0.1025, 0.665), GOLD_LIGHT, 0.6, 0.85))
    # شريط مطاطي للإغلاق + بطاقة اسم صغيرة في أعلى الغلاف
    g.add(_seg(P(0.150, 0.559), P(0.148, 0.675), "#3A2410", 1.4, 0.9))
    g.add(_poly([P(0.117, 0.640), P(0.145, 0.643), P(0.145, 0.664), P(0.117, 0.661)],
                "#EBDDB8", "#8E6B1E", 0.5))
    g.add(_seg(P(0.122, 0.656), P(0.139, 0.658), "#6E5A30", 0.6, 0.7))
    g.add(_seg(P(0.122, 0.648), P(0.134, 0.650), "#6E5A30", 0.6, 0.7))

    # ==========================================================
    # اليد: ظهر الكف + أربعة أصابع ملتفة فوق الغلاف (الإبهام خلف الدفتر)
    # ==========================================================
    O = np.array(cuff_near_b)
    u = fore_dir
    v = np.array([-u[1], u[0]])            # عمودي على الساعد (لأعلى)

    def Lh(s, t):
        """نقطة في إطار اليد: s على امتداد الساعد، t عمودياً عليه (بوحدات H)."""
        return O + (u * s + v * t) * H

    # ظل اليد على الغلاف
    kc = Lh(0.034, 0.0)
    g.add(_ell(kc[0] + 0.004 * H, kc[1] - 0.006 * H, 0.044 * H, 0.052 * H, "#000000", sw=0, fo=0.20).rotate(-10 * DEGREES))

    # ظهر الكف (صغير ومتناسب مع جسم المعلم النحيف)
    g.add(_poly([Lh(-0.004, -0.0105), Lh(-0.004, 0.0105), Lh(0.025, 0.0185), Lh(0.027, -0.0175)],
                skin, skin_sh, 0.6, r=0.004 * H))
    g.add(_poly([Lh(-0.004, -0.0105), Lh(0.027, -0.0175), Lh(0.026, -0.003), Lh(-0.004, 0.0)],
                "#000000", sw=0, fo=0.10))
    # أوتار ظهر اليد
    for t0, t1 in ((0.005, 0.0065), (-0.0015, -0.0025)):
        g.add(_seg(Lh(0.004, t0), Lh(0.021, t1), skin_sh, 0.5, 0.5))

    # الأصابع الأربعة (من الخنصر إلى السبابة) تلتف على الغلاف: مفصلان لكل إصبع
    f1 = np.array([np.cos(-10 * DEGREES), np.sin(-10 * DEGREES)])
    f2 = np.array([np.cos(-40 * DEGREES), np.sin(-40 * DEGREES)])
    for t, ln in ((-0.0132, 0.017), (-0.0044, 0.021), (0.0044, 0.023), (0.0132, 0.021)):
        K = Lh(0.026, t)
        Jn = K + f1 * 0.62 * ln * H
        Tp = Jn + f2 * 0.38 * ln * H
        g.add(_limb(K, Jn, 0.0092 * H, 0.0085 * H, skin, skin_sh, 0.4))
        g.add(_limb(Jn, Tp, 0.0085 * H, 0.0078 * H, skin, skin_sh, 0.4))
        pr = np.array([-f1[1], f1[0]])
        g.add(_seg(Jn - pr * 0.0033 * H, Jn + pr * 0.0033 * H, skin_sh, 0.5, 0.65))
        g.add(Dot(_V(*K), radius=0.0024 * H, color=_mix(skin, "#FFFFFF", 0.14)))

    return g


# ==============================================================
# 5. صف مقاعد (طاولة + كتب + طلبة)
# ==============================================================

def _build_row(c, specs, xs, s, hip_y, w_back, w_front, covers):
    cx = float(np.mean(xs))
    y_front = hip_y + 0.55 * s
    y_back = hip_y + 1.55 * s
    floor_y = hip_y - 0.74 * s + 0.25 * s
    c.add(_make_desk(cx, y_back, y_front, w_back, w_front, 0.06 * s + 0.01, floor_y))
    for x, cv in zip(xs, covers):
        c.add(_make_book(x, hip_y + 1.18 * s, s, cv))
    for x, sp in zip(xs, specs):
        c.add(make_student_from_behind(_V(x, hip_y), s=s, **sp))


# ==============================================================
# 6. الغرفة الكاملة
# ==============================================================

def _make_room(BX, BY):
    r = VGroup()

    # ---------------- الجدار الخلفي ----------------
    r.add(_vgrad(-WX, WX, WAIN, WY1, "#171009", "#2C2218", n=16))
    for w, h, a in ((6.8, 2.6, 0.022), (5.4, 2.1, 0.028), (4.0, 1.6, 0.034)):
        r.add(_ell(0.0, 2.22, w, h, "#FFC878", sw=0, fo=a))

    for i in range(8):
        a = 0.34 * (1 - i / 8.0) ** 1.6
        w = 0.24
        r.add(_poly([(-WX + i * w, WY0), (-WX + (i + 1) * w + 0.01, WY0), (-WX + (i + 1) * w + 0.01, WY1), (-WX + i * w, WY1)],
                    "#000000", sw=0, fo=a))
        r.add(_poly([(WX - i * w, WY0), (WX - (i + 1) * w - 0.01, WY0), (WX - (i + 1) * w - 0.01, WY1), (WX - i * w, WY1)],
                    "#000000", sw=0, fo=a))

    r.add(_vgrad(-WX, WX, WY0, WAIN, "#3B2A1A", "#2D2013", n=6))
    pw = 0.62
    xs = np.arange(-WX, WX - 0.01, pw)
    for x in xs:
        r.add(_poly([(x + 0.07, WY0 + 0.20), (x + pw - 0.07, WY0 + 0.20), (x + pw - 0.07, WAIN - 0.08), (x + 0.07, WAIN - 0.08)],
                    _mix("#3B2A1A", "#000000", 0.18), _mix("#5A4128", "#FFFFFF", 0.1), 0.6, 1.0, 0.55))
        r.add(_seg((x + 0.07, WAIN - 0.08), (x + pw - 0.07, WAIN - 0.08), "#6B4B2D", 0.7, 0.5))

    r.add(_poly([(-WX, WAIN), (WX, WAIN), (WX, WAIN + 0.07), (-WX, WAIN + 0.07)], "#5A4128", "#7A5A36", 0.7))
    r.add(_seg((-WX, WAIN + 0.07), (WX, WAIN + 0.07), "#9B7A48", 0.8, 0.6))
    r.add(_poly([(-WX, WY0), (WX, WY0), (WX, WY0 + 0.13), (-WX, WY0 + 0.13)], "#4A3522", "#6B4B2D", 0.7))

    r.add(_poly([(-WX, WY1 - 0.14), (WX, WY1 - 0.14), (WX, WY1), (-WX, WY1)], "#4A3825", "#7A5A36", 0.8))
    r.add(_seg((-WX, WY1 - 0.14), (WX, WY1 - 0.14), "#9B7A48", 0.8, 0.6))
    r.add(_poly([(-WX, WY1 - 0.14), (WX, WY1 - 0.14), (WX, WY1 - 0.30), (-WX, WY1 - 0.30)], "#000000", sw=0, fo=0.22))

    # ---------------- ساعة الحائط المرتفعة ----------------
    cx_, cy_, cr = BX, 3.24, 0.155
    r.add(_ell(cx_ + 0.015, cy_ - 0.02, 2 * cr + 0.06, 2 * cr + 0.06, "#000000", sw=0, fo=0.4))
    r.add(Circle(radius=cr + 0.025, stroke_width=1.6, stroke_color=GOLD_DARK, fill_color="#3A2A18", fill_opacity=1.0).move_to(_V(cx_, cy_)))
    r.add(Circle(radius=cr, stroke_width=0.8, stroke_color="#6B5B3A", fill_color="#EDE3C8", fill_opacity=0.95).move_to(_V(cx_, cy_)))
    for i in range(12):
        a = i * 30 * DEGREES
        r1, r2 = cr * (0.80 if i % 3 else 0.72), cr * 0.93
        r.add(_seg((cx_ + r1 * np.cos(a), cy_ + r1 * np.sin(a)), (cx_ + r2 * np.cos(a), cy_ + r2 * np.sin(a)), "#3A2A18", 0.9, 0.9))
    r.add(_seg((cx_, cy_), (cx_ + cr * 0.50 * np.cos(150 * DEGREES), cy_ + cr * 0.50 * np.sin(150 * DEGREES)), "#2A1A10", 1.6))
    r.add(_seg((cx_, cy_), (cx_ + cr * 0.78 * np.cos(10 * DEGREES), cy_ + cr * 0.78 * np.sin(10 * DEGREES)), "#2A1A10", 1.1))
    r.add(Dot(_V(cx_, cy_), radius=0.012, color=COPPER_TERRA))

    # لوحة الإعلانات الفلين
    bx0, bx1, by0, by1 = 2.72, 3.50, 1.50, 2.72
    r.add(_poly([(bx0 + 0.04, by0 - 0.04), (bx1 + 0.04, by0 - 0.04), (bx1 + 0.04, by1 - 0.04), (bx0 + 0.04, by1 - 0.04)], "#000000", sw=0, fo=0.35))
    r.add(_poly([(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)], "#4E3820", GOLD_DARK, 1.0))
    r.add(_poly([(bx0 + 0.05, by0 + 0.05), (bx1 - 0.05, by0 + 0.05), (bx1 - 0.05, by1 - 0.05), (bx0 + 0.05, by1 - 0.05)], "#7A5C38", "#5A4128", 0.6))
    for (px, py, pw_, ph, col, rot) in [
        (2.92, 2.40, 0.30, 0.34, "#E8724A", 6), (3.28, 2.38, 0.30, 0.30, "#E9C46A", -5),
        (2.90, 1.98, 0.28, 0.30, "#8FB3C2", -4), (3.26, 1.96, 0.32, 0.38, "#F5EBD6", 5),
        (3.10, 1.66, 0.36, 0.20, "#A9C98B", 2),
    ]:
        paper = _poly([(px - pw_ / 2, py - ph / 2), (px + pw_ / 2, py - ph / 2), (px + pw_ / 2, py + ph / 2), (px - pw_ / 2, py + ph / 2)],
                      col, _mix(col, "#000000", 0.4), 0.6).rotate(rot * DEGREES)
        r.add(paper)
        for t in (-0.2, 0.0, 0.2):
            r.add(_seg((px - pw_ * 0.32, py + ph * t), (px + pw_ * 0.32, py + ph * t), _mix(col, "#000000", 0.5), 0.6, 0.6).rotate(rot * DEGREES, about_point=_V(px, py)))
        r.add(Dot(_V(px, py + ph / 2 - 0.035), radius=0.016, color="#C0392B"))

    # مفتاح كهرباء
    r.add(_poly([(-3.42, 1.62), (-3.30, 1.62), (-3.30, 1.80), (-3.42, 1.80)], "#CFC4A8", "#8F8468", 0.6, r=0.01))
    r.add(_poly([(-3.38, 1.69), (-3.34, 1.69), (-3.34, 1.75), (-3.38, 1.75)], "#8F8468", sw=0.4))

    # ---------------- الجداران الجانبيان ----------------
    for side, wall_c, wain_c in ((-1, "#19120B", "#2A1D12"), (1, "#15100A", "#241910")):
        r.add(_poly(_wall_quad(side, 1.0, KMAX, WY0, WY1), wall_c, "#2A2016", 0.8, 1.0, 0.6))
        r.add(_poly(_wall_quad(side, 1.0, KMAX, WY0 + 0.13, WAIN), wain_c, wain_c, 0.5))
        r.add(_poly(_wall_quad(side, 1.0, KMAX, WAIN, WAIN + 0.07), "#4F3A24", "#7A5A36", 0.6))
        r.add(_poly(_wall_quad(side, 1.0, KMAX, WY0, WY0 + 0.13), "#3C2B1B", "#5A4128", 0.6))
        r.add(_poly(_wall_quad(side, 1.0, KMAX, WY1 - 0.14, WY1), "#3A2B1C", "#6B4B2D", 0.6))
        r.add(_poly(_wall_quad(side, 1.0, 1.05, WY0, WY1), "#000000", sw=0, fo=0.28))

    # النوافذ
    for (k0, k1) in ((1.025, 1.115), (1.150, 1.245)):
        ya, yb = 1.62, 3.08
        r.add(_poly(_wall_quad(-1, k0 - 0.008, k1 + 0.008, ya - 0.10, yb + 0.08), "#4A3524", "#7A5A36", 0.8))
        r.add(_poly(_wall_quad(-1, k0, k1, ya, yb), "#E8D4A0", "#B89A5E", 0.6, 0.62, 1.0))
        r.add(_poly(_wall_quad(-1, k0, k1, ya + 0.55, yb), "#FFF1C8", sw=0, fo=0.22))
        km = (k0 + k1) / 2
        r.add(_seg(_lw(km, ya), _lw(km, yb), "#4A3524", 1.8, 1.0))
        r.add(_seg(_lw(k0, (ya + yb) / 2 + 0.1), _lw(k1, (ya + yb) / 2 + 0.1), "#4A3524", 1.6, 1.0))
        r.add(_poly(_wall_quad(-1, k0 - 0.014, k1 + 0.014, ya - 0.14, ya - 0.08), "#6B4B2D", "#9B7A48", 0.6))
        a0, a1 = _lw(k0, (ya + yb) / 2), _lw(k1, (ya + yb) / 2)
        r.add(_ell((a0[0] + a1[0]) / 2, (a0[1] + a1[1]) / 2, 0.9, 1.9, "#FFD98A", sw=0, fo=0.045))

    # ---------------- الأرضية الخشبية ----------------
    levels = [WY0, 0.40, -0.08, -0.60, -1.16, -1.76, -2.38, FLOOR_FRONT]
    rs = np.random.RandomState(11)
    lanes = np.linspace(-WX, WX, 13)
    base_cols = ["#3A2B1D", "#40301F", "#352719", "#46341F", "#3C2C1E"]
    for i in range(12):
        xa, xb = lanes[i], lanes[i + 1]
        joints = [0]
        j = int(rs.randint(1, 3))
        while j < len(levels) - 1:
            joints.append(j)
            j += int(rs.randint(2, 4))
        joints.append(len(levels) - 1)
        for a, b in zip(joints[:-1], joints[1:]):
            col = _mix(base_cols[int(rs.randint(len(base_cols)))], "#000000", float(rs.uniform(0.0, 0.20)))
            quad = [_fl(xa, levels[a]), _fl(xb, levels[a]), _fl(xb, levels[b]), _fl(xa, levels[b])]
            r.add(_poly(quad, col, _mix(col, "#000000", 0.6), 0.6, 1.0, 0.9))
            mid = 0.5 * (xa + xb)
            r.add(_seg(_fl(mid + 0.06, levels[a] - 0.04), _fl(mid + 0.06, levels[b] + 0.04), _mix(col, "#FFFFFF", 0.10), 0.5, 0.6))

    r.add(_poly([_fl(-WX, WY0), _fl(WX, WY0), _fl(WX, WY0 - 0.12), _fl(-WX, WY0 - 0.12)], "#000000", sw=0, fo=0.30))

    for (k0, k1) in ((1.025, 1.115), (1.150, 1.245)):
        def on_floor(x0, k):
            return (x0 * k, VY - (VY - WY0) * k)
        kk = min(KMAX - 0.012, k1 + 0.05)
        patch = [on_floor(-3.6, k0 + 0.012), on_floor(-3.6, kk), on_floor(-0.9, kk), on_floor(-0.9, k0 + 0.012)]
        r.add(_poly(patch, "#FFD98A", sw=0, fo=0.07))
        inner = [on_floor(-3.2, k0 + 0.03), on_floor(-3.2, kk - 0.02), on_floor(-1.5, kk - 0.02), on_floor(-1.5, k0 + 0.03)]
        r.add(_poly(inner, "#FFE7B0", sw=0, fo=0.06))

    for w, h, a in ((6.8, 2.8, 0.030), (5.4, 2.2, 0.035), (4.0, 1.6, 0.040)):
        r.add(_ell(0.4, -0.9, w, h, "#FFC878", sw=0, fo=a))

    for i in range(6):
        a = 0.30 * (1 - i / 6.0) ** 1.5
        wd = 0.30
        r.add(_poly([_fl(-WX + i * wd, WY0), _fl(-WX + (i + 1) * wd + 0.01, WY0),
                     _fl(-WX + (i + 1) * wd + 0.01, FLOOR_FRONT), _fl(-WX + i * wd, FLOOR_FRONT)], "#000000", sw=0, fo=a * 0.6))
        r.add(_poly([_fl(WX - i * wd, WY0), _fl(WX - (i + 1) * wd - 0.01, WY0),
                     _fl(WX - (i + 1) * wd - 0.01, FLOOR_FRONT), _fl(WX - i * wd, FLOOR_FRONT)], "#000000", sw=0, fo=a * 0.6))
    return r


# ==============================================================
# 7. الفصل كاملاً
# ==============================================================

def make_kindergarten_classroom():
    c = VGroup()

    # خفض موضع السبورة قليلاً (BY = 2.05) لترك مسافة واسعة مع ساعة الحائط العلوية
    BX, BY, BW, BH = 0.55, 2.05, 3.7, 1.65

    c.add(_make_room(BX, BY))

    # ---------------- السبورة ----------------
    c.add(RoundedRectangle(corner_radius=0.08, width=BW + 0.20, height=BH + 0.20,
                           stroke_width=0, fill_color="#000000", fill_opacity=0.50).move_to(_V(BX + 0.07, BY - 0.08)))
    c.add(RoundedRectangle(corner_radius=0.08, width=BW + 0.18, height=BH + 0.18,
                           stroke_width=1.6, stroke_color=GOLD_LIGHT, stroke_opacity=0.85,
                           fill_color="#4A3520", fill_opacity=1.0).move_to(_V(BX, BY)))
    c.add(RoundedRectangle(corner_radius=0.05, width=BW, height=BH,
                           stroke_width=0.8, stroke_color=GOLD_DARK, stroke_opacity=0.7,
                           fill_color="#12100B", fill_opacity=1.0).move_to(_V(BX, BY)))
    c.add(_poly([(BX - 1.5, BY + 0.78), (BX + 1.5, BY + 0.78), (BX + 1.1, BY + 0.2), (BX - 1.1, BY + 0.2)],
                "#FFFFFF", sw=0, fo=0.03))

    # آثار طباشير
    for (sx, sy, sw_, sh_, a) in ((-1.1, -0.45, 0.9, 0.22, 0.05), (0.9, -0.55, 1.1, 0.18, 0.04), (-0.2, 0.62, 1.3, 0.14, 0.035)):
        c.add(_ell(BX + sx, BY + sy, sw_, sh_, "#FFFFFF", sw=0, fo=a))

    # حامل الطباشير
    ty = BY - BH / 2 - 0.09
    c.add(_poly([(BX - 1.72, ty + 0.09), (BX + 1.72, ty + 0.09), (BX + 1.86, ty), (BX - 1.86, ty)],
                GOLD_DARK, GOLD_LIGHT, 0.8, 0.95, 0.6))
    c.add(Rectangle(width=0.10, height=0.025, stroke_width=0, fill_color=IVORY_WHITE, fill_opacity=0.9).move_to(_V(BX - 0.9, ty + 0.115)))
    c.add(Rectangle(width=0.18, height=0.05, stroke_width=0, fill_color="#6B5B3A", fill_opacity=1.0).move_to(_V(BX + 1.1, ty + 0.12)))

    t_nums = MathTex(r"1 \quad 2 \quad 3 \quad 4", tex_template=mach_math_template, font_size=28, color=GOLD_LIGHT)
    t_dots = MathTex(r"\bullet \quad \bullet \quad \bullet \quad \bullet", font_size=18, color=GOLD_BRIGHT)
    t_calc = MathTex(r"1 + 1 = 2", tex_template=mach_math_template, font_size=22, color=COPPER_TERRA)
    notes = VGroup(t_nums, t_dots, t_calc).arrange(DOWN, buff=0.12).move_to(_V(BX, BY + 0.02))
    c.add(notes)

    # ---------------- المعلم ----------------
    c.add(make_teacher(_V(-2.15, 0.15), H=1.95, target=(BX - 0.75, BY + 0.15), stick_length=0.88))

    # ---------------- الصف البعيد ----------------
    far_specs = [
        dict(style="short", skin="#C99A78", hair="#17100A", shirt="#3F5A6B", look=4),
        dict(style="bob", skin="#D9AE8A", hair="#2E1B10", shirt="#8C3F24", look=3),
        dict(style="short", skin="#A8765A", hair="#120C08", shirt="#6B5B3A", look=1),
        dict(style="bun", skin="#E0B594", hair="#3A2414", shirt="#2F5D50", look=-2),
    ]
    far_xs = [BX + d for d in (-1.30, -0.43, 0.43, 1.30)]
    _build_row(c, far_specs, far_xs, s=0.60, hip_y=-0.45, w_back=3.8, w_front=4.1,
               covers=[COPPER_TERRA, "#3F5A6B", GOLD_DARK, "#2F5D50"])

    # ---------------- الصف القريب ----------------
    near_specs = [
        dict(style="long", skin="#D3A583", hair="#1B120C", shirt="#7A3A4A", look=5),
        dict(style="short", skin="#B9835F", hair="#0F0A06", shirt="#4A5568", look=3),
        dict(style="hijab", skin="#D9AE8A", hair="#2A1B14", shirt="#2F5D50", hijab="#9A6B7C", look=1),
        dict(style="short", skin="#C99A78", hair="#2B1A0F", shirt="#9A4B3C", look=-2),
    ]
    near_xs = [BX + d for d in (-1.65, -0.55, 0.55, 1.65)]
    _build_row(c, near_specs, near_xs, s=0.85, hip_y=-1.75, w_back=4.5, w_front=5.1,
               covers=["#3F5A6B", COPPER_TERRA, GOLD_DARK, "#7A3A4A"])

    return c