"""
أدوات مشتركة لكل thumbnails قناة MACH-MATH.
الاستخدام:  from common.thumbnails import *
"""
from manim import *
import numpy as np

from common.palette import (
    GOLD_BRIGHT, GOLD_LIGHT, GOLD, GOLD_DARK, GOLD_MUTED,
    STONE_AXIS, STONE_DASH, COPPER_TERRA, BRONZE, IVORY_WHITE, LABEL_MUTED, TEAL,
)
from common.latex import mach_math_template
from common.mobjects.characters import mach_mathematician

THUMB_BG = "#070503"
THUMB_FONT = "Cairo"
TEAL_LIGHT = interpolate_color(ManimColor(TEAL), ManimColor(IVORY_WHITE), 0.35)  # teal أفتح للتسميات

# ثوابت التخطيط الموحّد لكل الـ Thumbnails
TITLE_CX = 3.70
FRAME_FX = 6.85
FRAME_TOP = 3.78
MARGIN = 0.45  # مسافة موحدة بين الإطار وبين العنوان / اسم القناة

# ثوابت الشبكة المستقيمة الموحّدة (Unified Coordinate Grid)
GRID_BOX = (-6.65, 6.65, -3.58, 3.58)
GRID_ORIGIN = np.array([-3.45, -1.25, 0.0])  # مساحة ممتازة للرسم على الشمال وبعيد عن MACH-MATH والعنوان
GRID_ORIGIN_LTR = np.array([2.65, -1.25, 0.0])  # للنسخ LTR: الرسمة في المساحة الفاضية يمين العنوان (بعيدة عنه شوية)
GRID_STEP = 0.85

CHAR_SCALE = 1.75
CHAR_POS = np.array([-4.9, -0.85, 0.0])

# متجها الأساس بعد التحويل (اتجاهات محاور الشبكة المائلة) ووحدة الأساس بعدد خطوات الشبكة
BASIS_E1 = np.array([1.08, 0.32]) * GRID_STEP
BASIS_E2 = np.array([-0.40, 0.94]) * GRID_STEP
BASIS_UNIT = 2

# أصل رسمة المتجه (الحلقة 02): RTL = الرسمة على الشمال، LTR = على اليمين
VECTOR_ORIGIN = np.array([-5.30, -2.20, 0.0])
VECTOR_ORIGIN_LTR = np.array([0.30, -2.20, 0.0])
VECTOR_STEPS = (6, 4)  # مركّبات المتجه البطل بعدد خطوات الشبكة


# ---------------------------------------------------------------- أساسيات
def soft_glow(center, radius, color, layers=22, peak=0.05, power=2.0):
    """هالة ناعمة بلا حواف: طبقات دوائر متراكبة."""
    g = VGroup()
    for i in range(layers):
        t = i / (layers - 1)
        r = radius * (1 - t * 0.92)
        op = peak * (0.25 + 0.75 * t ** power) / layers * 6
        g.add(Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=op).move_to(center))
    return g


def fit_width(mob, width):
    mob.set(width=width)
    return mob


def _round_joints(mob):
    for sm in mob.family_members_with_points():
        sm.joint_type = LineJointType.ROUND
    return mob


def solid_text(text, width, color_a=IVORY_WHITE, color_b=GOLD_BRIGHT, glow=GOLD_LIGHT,
               stroke_w=0.7, outline_w=2.4, halo_w=(9, 4), font=THUMB_FONT):
    """نص عريض (عربي أو لاتيني) بتدرج لوني وتركيب حواف دائري نظيف وتوهج ناعم."""
    main = MarkupText(f"<b>{text}</b>", font=font, font_size=96)
    if len(main.family_members_with_points()) == 0:
        main = Text(text, font=font, font_size=96, weight=BOLD)
    main.set(width=width)
    main.set_color_by_gradient(color_a, color_b)
    for sm in main.family_members_with_points():
        sm.set_stroke(sm.get_fill_color(), width=stroke_w, opacity=1)
    _round_joints(main)
    outline = _round_joints(
        main.copy().set_fill(opacity=0).set_stroke(THUMB_BG, width=outline_w, opacity=0.92)
    )
    halo = VGroup(
        main.copy().set_fill(opacity=0).set_stroke(glow, width=halo_w[0], opacity=0.07),
        main.copy().set_fill(opacity=0).set_stroke(glow, width=halo_w[1], opacity=0.11),
    )
    _round_joints(halo)
    return VGroup(halo, outline, main)


def glowing_text(text, width, color_a=GOLD_BRIGHT, color_b=GOLD, outline=THUMB_BG,
                 weight=BOLD, glow=GOLD, font=THUMB_FONT):
    return solid_text(text, width, color_a=color_a, color_b=color_b, glow=glow, font=font)


def glow_dot(point, scale=1.0, color=GOLD_BRIGHT):
    """نقطة أصل متوهجة."""
    return VGroup(
        Dot(point, radius=0.32 * scale, color=GOLD).set_opacity(0.16),
        Dot(point, radius=0.18 * scale, color=GOLD_LIGHT).set_opacity(0.38),
        Dot(point, radius=0.095 * scale, color=color),
    )


def glow_arrow(start, end, color=GOLD_BRIGHT, width=11, glow_color=None, tip_ratio=0.22):
    """سهم بطل قوي وواضح."""
    glow_color = glow_color or color
    g = VGroup()
    for k, op in ((3.2, 0.07), (2.0, 0.14)):
        g.add(Arrow(start, end, buff=0, stroke_width=width * k, color=glow_color,
                    stroke_opacity=op, max_tip_length_to_length_ratio=tip_ratio + 0.03))
    g.add(Arrow(start, end, buff=0, stroke_width=width, color=color,
                max_tip_length_to_length_ratio=tip_ratio))
    return g


def stroked(mob, width=10, color=THUMB_BG):
    return mob.set_stroke(color, width=width, background=True)


# ---------------------------------------------------------------- الشبكة المستقيمة الموحدة (متصلة بلا تقطيع)
def grid_point(i, j, origin=GRID_ORIGIN, step=GRID_STEP, e1=None, e2=None):
    """تحويل إحداثيات الشبكة (i, j) إلى نقطة ثلاثية الأبعاد على الشاشة."""
    v1 = np.array([step, 0.0]) if e1 is None else np.asarray(e1, float)[:2]
    v2 = np.array([0.0, step]) if e2 is None else np.asarray(e2, float)[:2]
    pt = np.asarray(origin, float)[:2] + i * v1 + j * v2
    return np.array([pt[0], pt[1], 0.0])


def unified_grid(
    origin=GRID_ORIGIN,
    step=GRID_STEP,
    box=GRID_BOX,
    e1=None,
    e2=None,
    show_axes=True,
    color=STONE_AXIS,
    axis_color=GOLD_LIGHT,
    line_opacity=0.18,
    axis_opacity=0.52,
    span=16,
):
    """شبكة إحداثيات مستقيمة وموحّدة لكل الـ Thumbnails بخطوط متصلة ونظيفة."""
    v1 = np.array([step, 0.0]) if e1 is None else np.asarray(e1, float)[:2]
    v2 = np.array([0.0, step]) if e2 is None else np.asarray(e2, float)[:2]
    O2 = np.asarray(origin, float)[:2]
    P = lambda i, j: O2 + i * v1 + j * v2

    grid_group = VGroup()
    ext = span + 6

    for k in range(-span, span + 1):
        is_axis = (k == 0) and show_axes
        line_color = axis_color if is_axis else color
        sw = 2.2 if is_axis else 1.2
        op = axis_opacity if is_axis else line_opacity

        for a, b in ((P(k, -ext), P(k, ext)), (P(-ext, k), P(ext, k))):
            clipped = clip_line(a, b, box)
            if clipped:
                p0, p1 = clipped
                grid_group.add(
                    Line([p0[0], p0[1], 0], [p1[0], p1[1], 0],
                         color=line_color, stroke_width=sw, stroke_opacity=op)
                )

    return grid_group


# ---------------------------------------------------------------- مكونات الـ thumbnail
def vignette_bg(center=(-2.5, -0.5, 0), radius=7.5, color=GOLD_DARK, peak=0.06):
    return soft_glow(np.array(center, dtype=float), radius, color, layers=24, peak=peak)


def backdrop(origin=GRID_ORIGIN, ltr=False):
    """الخلفية الدافئة + الهالة الساخنة حول نقطة الأصل (طبقات سفلية)."""
    warm = vignette_bg(center=(2.5 if ltr else -2.5, -0.5, 0))
    hot = soft_glow(np.asarray(origin, float) + np.array([0.8, 1.2, 0]), 3.4, GOLD, layers=20, peak=0.055)
    return VGroup(warm, hot)


def channel_frame(fx=FRAME_FX, fy=FRAME_TOP, arm=0.50):
    """إطار القناة الهادئ في الأركان."""
    frame = VGroup()
    for sx, sy in ((-1, 1), (1, 1), (1, -1), (-1, -1)):
        c = np.array([sx * fx, sy * fy, 0])
        frame.add(
            Line(c, c + np.array([-sx * arm, 0, 0]), color=GOLD_LIGHT, stroke_width=2.6, stroke_opacity=0.65),
            Line(c, c + np.array([0, -sy * arm, 0]), color=GOLD_LIGHT, stroke_width=2.6, stroke_opacity=0.65),
        )
    rect = Rectangle(width=2 * fx, height=2 * fy, stroke_width=0.9,
                     stroke_color=GOLD_MUTED, stroke_opacity=0.40)
    return VGroup(rect, frame)


def brand_mark(pos=(-5.65, 3.28, 0), width=1.80):
    p = np.array(pos, dtype=float)
    backing = soft_glow(p, 1.5, THUMB_BG, layers=10, peak=0.22)
    brand = Text("MACH-MATH", font="Serif", weight=BOLD)
    fit_width(brand, width)
    brand.set_color_by_gradient(GOLD_BRIGHT, GOLD_LIGHT, GOLD_DARK)
    brand.move_to(p)
    return VGroup(backing, brand)


def brand_mark_at(corner=UL, margin=MARGIN, width=1.80):
    """اسم القناة في ركن محدد (UL / UR / DL / DR) على بعد margin من الإطار."""
    brand = brand_mark(width=width)
    target = np.array([np.sign(corner[0]) * (FRAME_FX - margin),
                       np.sign(corner[1]) * (FRAME_TOP - margin), 0.0])
    brand.shift(target - brand[1].get_corner(corner))
    brand.set_z_index(30)
    return brand


def series_badge(text, width=3.5, align_right_to=None, y=3.2, cx=TITLE_CX):
    txt = Text(text, font=THUMB_FONT, weight=BOLD, color=COPPER_TERRA)
    fit_width(txt, width)
    bg = RoundedRectangle(corner_radius=0.18, width=txt.width + 0.55, height=txt.height + 0.36,
                          stroke_width=2.2, stroke_color=COPPER_TERRA,
                          fill_color="#17100A", fill_opacity=0.96)
    txt.move_to(bg)
    badge = VGroup(bg, txt).move_to([cx, y, 0])
    if align_right_to is not None:
        badge.align_to(align_right_to, RIGHT)
    return badge


def title_backing(cx=TITLE_CX, ltr=False):
    """خلفية داكنة ناعمة منفصلة على طبقة سفلية (z=2) عشان متغطيش أي معادلات أو رسوم."""
    if ltr:
        cx = -TITLE_CX - 0.8  # صورة مرآة لمكان الخلفية في النسخ RTL
    g = VGroup(*[
        Ellipse(width=9.2 - 2.2 * (i / 9), height=7.4 - 1.8 * (i / 9), stroke_width=0,
                fill_color=THUMB_BG, fill_opacity=0.20).move_to([cx + 0.4, 0.2, 0])
        for i in range(10)
    ])
    g.set_z_index(2)
    return g


def title_block(line1, line2, badge_text, cx=TITLE_CX, line1_width=2.6, line2_width=5.3,
                line2_y=0.30, badge_gap=0.34, badge_margin=0.40,
                ltr=False, margin=None, badge_width=3.5, ltr_offsets=(1.25, -0.75)):
    """
    كتلة العنوان الفخمة بالتدرج والتوهج (solid_text).
    ترجع VGroup بالترتيب: line1, line2, underline, badge

    RTL (الافتراضي): على اليمين، محاذاة لليمين.
      margin=None  -> السلوك القديم (badge_margin فقط).
      margin=قيمة  -> الـ badge على بعد margin من أعلى الإطار، والحافة اليمنى على بعد margin من الإطار.
    ltr=True: على الشمال، محاذاة لليسار، بمواضع رأسية ثابتة نسبة إلى line2_y:
      السطر الأول عند line2_y + ltr_offsets[0]، والخط التحتي عند line2_y + ltr_offsets[1]،
      والـ badge أعلى حافته على بعد margin من الإطار. (الحروف اللاتينية أطول من العربية بنفس العرض،
      فالمسافات النسبية بتخلي العنوان ينزل؛ المواضع الثابتة بتمنع ده.)
    """
    if ltr:
        m = MARGIN if margin is None else margin
        left = np.array([-FRAME_FX + m, 0.0, 0.0])

        l2 = solid_text(line2, line2_width, GOLD_BRIGHT, GOLD, glow=GOLD,
                        stroke_w=1.5, outline_w=7, halo_w=(18, 9))
        l2.move_to([0, line2_y, 0]).align_to(left, LEFT)
        l2.shift(UP * (line2_y - l2.get_center()[1]))

        l1 = solid_text(line1, line1_width, IVORY_WHITE, GOLD_BRIGHT, glow=GOLD_LIGHT,
                        stroke_w=0.7, outline_w=2.4, halo_w=(9, 4))
        l1.align_to(left, LEFT)
        l1.shift(UP * (line2_y + ltr_offsets[0] - l1.get_center()[1]))

        half = max(line1_width, line2_width) / 2  # الخط التحتي بعرض أعرض سطر
        underline = VGroup(
            Line(LEFT * half, RIGHT * half, color=GOLD, stroke_width=16, stroke_opacity=0.10),
            Line(LEFT * half, RIGHT * half, color=COPPER_TERRA, stroke_width=6),
        )
        for u in underline:
            u.set_cap_style(CapStyleType.ROUND)
        underline.align_to(left, LEFT)
        underline.shift(UP * (line2_y + ltr_offsets[1] - underline.get_center()[1]))

        badge = series_badge(badge_text, width=badge_width, y=0, cx=0)
        badge.align_to(left, LEFT)
        badge.shift(UP * ((FRAME_TOP - m) - badge.get_top()[1]))

        block = VGroup(l1, l2, underline, badge)
        block.set_z_index(30)
        return block

    if margin is not None:
        badge_margin = margin

    l2 = solid_text(line2, line2_width, GOLD_BRIGHT, GOLD, glow=GOLD,
                    stroke_w=1.5, outline_w=7, halo_w=(18, 9))
    l2.move_to([cx, line2_y, 0])

    l1 = solid_text(line1, line1_width, IVORY_WHITE, GOLD_BRIGHT, glow=GOLD_LIGHT,
                    stroke_w=0.7, outline_w=2.4, halo_w=(9, 4))
    l1.next_to(l2, UP, buff=0.32).align_to(l2, RIGHT)

    half = max(line1_width, line2_width) / 2  # الخط التحتي بعرض أعرض سطر
    underline = VGroup(
        Line(LEFT * half, RIGHT * half, color=GOLD, stroke_width=16, stroke_opacity=0.10),
        Line(LEFT * half, RIGHT * half, color=COPPER_TERRA, stroke_width=6),
    ).next_to(l2, DOWN, buff=0.26).align_to(l2, RIGHT)
    for u in underline:
        u.set_cap_style(CapStyleType.ROUND)

    badge = series_badge(badge_text, width=badge_width, cx=cx, align_right_to=l2)
    badge.next_to(l1, UP, buff=badge_gap).align_to(l2, RIGHT)

    block = VGroup(l1, l2, underline, badge)
    overflow = badge.get_top()[1] - (FRAME_TOP - badge_margin)
    if overflow > 0:
        block.shift(DOWN * overflow)
    if margin is not None:
        block.shift(RIGHT * ((FRAME_FX - margin) - badge.get_right()[0]))
    block.set_z_index(30)
    return block


def mathematician_with_glow(pos=CHAR_POS, scale=CHAR_SCALE, pose="explaining", **kwargs):
    opts = dict(
        color=COPPER_TERRA,
        accent_color=GOLD_LIGHT,
        pose=pose,
        scale=scale,
        blink=False,
        breathing=False,
        glasses=True,
        tie_type="necktie")
    opts.update(kwargs)
    char = mach_mathematician(**opts).move_to(pos)
    glow = soft_glow(np.array(pos) + np.array([0.2, 0.2, 0]), 3.4, COPPER_TERRA, layers=14, peak=0.045)
    glow.set_z_index(15)
    char.set_z_index(20)
    return glow, char


def clip_line(p, q, box):
    """قص خط p→q داخل مستطيل box=(x0,x1,y0,y1) (Liang–Barsky)."""
    x0, x1, y0, y1 = box
    p, q = np.asarray(p, float), np.asarray(q, float)
    d = q - p
    t0, t1 = 0.0, 1.0
    for pk, qk in ((-d[0], p[0] - x0), (d[0], x1 - p[0]), (-d[1], p[1] - y0), (d[1], y1 - p[1])):
        if abs(pk) < 1e-9:
            if qk < 0:
                return None
            continue
        r = qk / pk
        if pk < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return None
    return p + t0 * d, p + t1 * d


def layer(mobs, z):
    g = VGroup(*mobs) if not isinstance(mobs, VGroup) else mobs
    g.set_z_index(z)
    return g


# ---------------------------------------------------------------- مكونات التحويل الخطي (الجبر الخطي)
def matrix_A(font_size=62):
    """A = [[a, b], [c, d]] بتلوين الأعمدة: العمود الأول BRONZE والثاني COPPER_TERRA."""
    mat = MathTex(
        r"A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}",
        tex_template=mach_math_template, font_size=font_size, color=IVORY_WHITE,
    )
    mat[0][0].set_color(GOLD_LIGHT)
    if len(mat[0]) == 8:
        mat[0][3].set_color(BRONZE)
        mat[0][5].set_color(BRONZE)
        mat[0][4].set_color(COPPER_TERRA)
        mat[0][6].set_color(COPPER_TERRA)
    else:
        entries = [g for g in mat[0][2:] if g.height < 0.45 * mat.height]
        mid_x = np.mean([g.get_center()[0] for g in entries])
        for g in entries:
            g.set_color(BRONZE if g.get_center()[0] < mid_x else COPPER_TERRA)
    stroked(mat, width=10)
    mat.set_z_index(12)
    return mat


def place_matrix_under(mat, title, ltr=False, gap=0.80):
    """يحط المصفوفة تحت الخط التحتي للعنوان: متمركزة (RTL) أو محاذية لليسار (LTR)."""
    mat.next_to(title[2], DOWN, buff=gap)
    if ltr:
        mat.set_x(title[1].get_left()[0] + mat.width / 2 + 0.3)
    else:
        mat.set_x(title[2].get_center()[0] - 0.1)
    return mat


def transform_demo(origin=GRID_ORIGIN, side="left", e1=BASIS_E1, e2=BASIS_E2, unit=BASIS_UNIT,
                   tilted_box=None):
    """
    رسمة تحويل الإحداثيات: الشبكة المعتدلة + î/ĵ على محاورها + المربع الأصلي (COPPER_TERRA)
    + الشبكة المائلة (TEAL) + متوازي الأضلاع المظلل عليه det(A).
    side: "left" أو "right" = الجهة اللي الرسمة فيها من الشاشة (تحدد حدود الشبكة المائلة).
    ترجع: (grid, tilted_grid, det_visual, hero) — بالـ z-index جاهز (1 / 3 / 6 / 12).
    """
    O = np.asarray(origin, float)
    e1 = np.asarray(e1, float)
    e2 = np.asarray(e2, float)
    P_orig = lambda i, j: grid_point(i, j, origin=O)
    P_tilt = lambda i, j: grid_point(i, j, origin=O, e1=e1 * unit, e2=e2 * unit)

    box = tilted_box or GRID_BOX  # الشبكة المائلة تتمدد على الشاشة كلها زي المعتدلة

    # المحوران بسهم في كل طرف ومتماثلان حوالين الأصل (مش خط كامل لآخر الشاشة)
    hx = 2.7
    grid = unified_grid(origin=O, show_axes=False)
    grid.add(
        _axis_arrow(O + np.array([-hx, 0, 0]), O + np.array([hx, 0, 0])),
        _axis_arrow(O + np.array([0, -1.85, 0]), O + np.array([0, 4.1, 0])),
    )
    grid.set_z_index(1)

    tilted_grid = unified_grid(
        origin=O, e1=e1 * unit, e2=e2 * unit, box=box, show_axes=False,
        color=TEAL, line_opacity=0.34,
    )
    # محورا الشبكة المائلة: مقطعان أوضح وقصيران (مش خطين كاملين) عشان ما يقطعوش العنوان والمصفوفة
    for v in (e1 * unit, e2 * unit):
        a = np.array([*(O[:2] - 0.45 * v), 0.0])
        b = np.array([*(O[:2] + 1.70 * v), 0.0])
        tilted_grid.add(Line(a, b, color=TEAL, stroke_width=2.2, stroke_opacity=0.85))
    tilted_grid.set_z_index(3)

    orig_box = Polygon(
        P_orig(0, 0), P_orig(unit, 0), P_orig(unit, unit), P_orig(0, unit),
        stroke_color=COPPER_TERRA, stroke_width=2.8, stroke_opacity=0.95,
        fill_color=COPPER_TERRA, fill_opacity=0.10,
    )
    cell = [P_tilt(0, 0), P_tilt(1, 0), P_tilt(1, 1), P_tilt(0, 1)]
    cell_bg = Polygon(*cell, stroke_width=0, fill_color=TEAL, fill_opacity=0.26)
    cell_border = Polygon(*cell, stroke_color=TEAL, stroke_width=3.2, stroke_opacity=1.0)

    det_tag = MathTex(r"\det(A)", tex_template=mach_math_template, font_size=40, color=GOLD_BRIGHT)
    det_tag.move_to((cell[0] + cell[2]) / 2 + np.array([0.30, -0.05, 0]))  # يمين محور ĵ مش لازق فيه
    stroked(det_tag, width=10)
    det_visual = VGroup(orig_box, cell_bg, cell_border, det_tag)
    det_visual.set_z_index(6)

    i_tip, j_tip = P_orig(unit, 0), P_orig(0, unit)
    i_hat = MathTex(r"\hat{\imath}", tex_template=mach_math_template, font_size=84, color=GOLD_BRIGHT)
    j_hat = MathTex(r"\hat{\jmath}", tex_template=mach_math_template, font_size=84, color=COPPER_TERRA)
    i_hat.next_to(i_tip, DOWN, buff=0.14)
    j_hat.next_to(j_tip, LEFT, buff=0.16)
    stroked(i_hat, width=12)
    stroked(j_hat, width=12)

    hero = layer([
        glow_arrow(O, i_tip, GOLD_BRIGHT, 11),
        glow_arrow(O, j_tip, COPPER_TERRA, 11),
        glow_dot(O, scale=1.20),
        i_hat, j_hat,
    ], 12)
    return grid, tilted_grid, det_visual, hero


# ---------------------------------------------------------------- مكونات المتجه (الحلقة 02)
def column_vector(font_size=62):
    """v = [v_x; v_y]: صف v_x بلون BRONZE وصف v_y بلون COPPER_TERRA (نفس ألوان المركّبتين في الرسمة)."""
    mat = MathTex(
        r"\vec{v} = \begin{bmatrix} v_x \\ v_y \end{bmatrix}",
        tex_template=mach_math_template, font_size=font_size, color=IVORY_WHITE,
    )
    glyphs = list(mat[0])
    tall = sorted([g for g in glyphs if g.height > 0.7 * mat.height], key=lambda g: g.get_center()[0])
    if len(tall) >= 2:
        left, right = tall[0], tall[-1]
        entries = [g for g in glyphs if g not in tall
                   and left.get_right()[0] < g.get_center()[0] < right.get_left()[0]]
        mid_y = mat.get_center()[1]
        for g in entries:
            g.set_color(BRONZE if g.get_center()[1] > mid_y else COPPER_TERRA)
        before = [g for g in glyphs if g.get_center()[0] < left.get_left()[0]]
        if before:
            eq = max(before, key=lambda g: g.get_center()[0])
            for g in before:
                if g is not eq:
                    g.set_color(GOLD_LIGHT)
    stroked(mat, width=10)
    mat.set_z_index(12)
    return mat


def _axis_arrow(start, end, color=GOLD_LIGHT, width=3.0, both=True):
    """محور بسهم في كل طرف (both=False لسهم في الطرف الأخير فقط). طوله محدود عشان ما يلمسش اسم القناة أو العنوان."""
    start, end = np.asarray(start, float), np.asarray(end, float)
    line = Line(start, end, color=color, stroke_width=width, stroke_opacity=0.9)
    d = end - start
    ang = np.arctan2(d[1], d[0])

    def tip(point, a):
        t = Triangle(fill_color=color, fill_opacity=0.95, stroke_width=0).scale(0.13)
        return t.rotate(a - PI / 2).move_to(point)

    grp = VGroup(line, tip(end, ang))
    if both:
        grp.add(tip(start, ang + PI))
    return grp


def vector_demo(origin=VECTOR_ORIGIN, steps=VECTOR_STEPS):
    """
    رسمة المتجه: شبكة معتدلة + محوران منتهيان بسهم وتدريج + المتجه البطل v + مركّبتاه
    + مستطيل المركّبات ومثلثها بـ TEAL + خط قياس المقدار |v| + الزاوية θ.
    ترجع: (grid, under, hero) — بالـ z-index جاهز (1 / 5 / 12).
    """
    O = np.asarray(origin, float)
    sx, sy = steps
    st = GRID_STEP
    tip = grid_point(sx, sy, origin=O)
    foot = grid_point(sx, 0, origin=O)
    corner = grid_point(0, sy, origin=O)

    grid = unified_grid(origin=O, show_axes=False)
    grid.set_z_index(1)

    # ---- المحاوران (منتهيان) + التدريج + الحرفان
    x_end = O + np.array([(sx + 0.7) * st, 0, 0])
    y_end = O + np.array([0, (sy + 1.7) * st, 0])
    axes = VGroup(
        _axis_arrow(O + np.array([-0.7, 0, 0]), x_end),
        _axis_arrow(O + np.array([0, -0.6, 0]), y_end),
    )
    tk = dict(color=GOLD_LIGHT, stroke_width=1.8, stroke_opacity=0.8)
    ticks = VGroup()
    for k in range(1, sx + 1):
        p = grid_point(k, 0, origin=O)
        ticks.add(Line(p + UP * 0.07, p + DOWN * 0.07, **tk))
    for k in range(1, sy + 2):
        p = grid_point(0, k, origin=O)
        ticks.add(Line(p + LEFT * 0.07, p + RIGHT * 0.07, **tk))
    x_lbl = MathTex(r"x", tex_template=mach_math_template, font_size=46, color=GOLD_LIGHT)
    x_lbl.next_to(x_end + LEFT * 0.25, DOWN, buff=0.14)
    y_lbl = MathTex(r"y", tex_template=mach_math_template, font_size=46, color=GOLD_LIGHT)
    y_lbl.next_to(y_end, RIGHT, buff=0.16)
    stroked(x_lbl, width=8)
    stroked(y_lbl, width=8)

    # ---- teal: هالة + مستطيل المركّبات + المثلث + الخطوط المنقطة
    glow = soft_glow((O + foot + tip) / 3, 3.0, TEAL, layers=18, peak=0.05)
    rect_fill = Polygon(O, foot, tip, corner, stroke_width=0, fill_color=TEAL, fill_opacity=0.07)
    tri_fill = Polygon(O, foot, tip, stroke_width=0, fill_color=TEAL, fill_opacity=0.22)
    dashed = DashedLine(tip, corner, dash_length=0.10, color=TEAL, stroke_width=2.4, stroke_opacity=0.9)
    corner_dot = Dot(corner, radius=0.07, color=TEAL_LIGHT)

    under = layer([glow, rect_fill, tri_fill, dashed, axes, ticks, x_lbl, y_lbl, corner_dot], 5)

    # ---- المركّبتان وعلامة الزاوية القائمة
    comp_x = Arrow(O, foot, buff=0, stroke_width=6, color=BRONZE, stroke_opacity=0.95,
                   max_tip_length_to_length_ratio=0.10)
    comp_y = Arrow(foot, tip, buff=0, stroke_width=6, color=COPPER_TERRA, stroke_opacity=0.95,
                   max_tip_length_to_length_ratio=0.12)
    s = 0.24
    right_angle = VGroup(
        Line(foot + LEFT * s, foot + LEFT * s + UP * s, color=GOLD_LIGHT, stroke_width=2.2, stroke_opacity=0.85),
        Line(foot + LEFT * s + UP * s, foot + UP * s, color=GOLD_LIGHT, stroke_width=2.2, stroke_opacity=0.85),
    )

    # ---- الزاوية θ
    ang = np.arctan2(tip[1] - O[1], tip[0] - O[0])
    arc = Arc(radius=1.15, start_angle=0, angle=ang, arc_center=O, color=COPPER_TERRA, stroke_width=3.4)
    theta = MathTex(r"\theta", tex_template=mach_math_template, font_size=46, color=COPPER_TERRA)
    theta.move_to(O + 1.65 * np.array([np.cos(ang / 2), np.sin(ang / 2), 0]))
    stroked(theta, width=8)

    # ---- خط قياس المقدار |v| (teal) موازي للمتجه فوقه وعلى شماله
    u = (tip - O) / np.linalg.norm(tip - O)
    n = np.array([-u[1], u[0], 0.0])
    a, b = O + n * 0.55, tip + n * 0.55
    cap = 0.12
    dkw = dict(color=TEAL_LIGHT, stroke_width=3.0, stroke_opacity=0.95)
    dim = VGroup(Line(a, b, **dkw), Line(a - n * cap, a + n * cap, **dkw), Line(b - n * cap, b + n * cap, **dkw))
    mag = MathTex(r"|\vec{v}|", tex_template=mach_math_template, font_size=56, color=TEAL_LIGHT)
    mag.move_to((a + b) / 2 + n * 0.50)

    # ---- التسميات
    vx = MathTex(r"v_x", tex_template=mach_math_template, font_size=58, color=BRONZE)
    vx.next_to((O + foot) / 2, DOWN, buff=0.16)
    vy = MathTex(r"v_y", tex_template=mach_math_template, font_size=58, color=COPPER_TERRA)
    vy.next_to((foot + tip) / 2, LEFT, buff=0.16)
    vv = MathTex(r"\vec{v}", tex_template=mach_math_template, font_size=96, color=GOLD_BRIGHT)
    vv.next_to(tip, RIGHT + UP * 0.10, buff=0.12)
    for m in (vx, vy, vv, mag):
        stroked(m, width=10)

    hero = layer([
        comp_x, comp_y, right_angle, arc, theta, dim,
        glow_arrow(O, tip, GOLD_BRIGHT, 12, GOLD),
        glow_dot(O, scale=1.2),
        vx, vy, vv, mag,
    ], 12)
    return grid, under, hero