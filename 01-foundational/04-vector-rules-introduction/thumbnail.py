from manim import *
import numpy as np

from common.palette import (
    GOLD_BRIGHT, GOLD_LIGHT, GOLD, TEAL,
    STONE_AXIS, COPPER_TERRA, IVORY_WHITE,
)
from common.latex import mach_math_template
from common.thumbnails import *

# ==============================================================
# Thumbnail — الحلقة 04
# تمهيد لقواعد المتجهات: الصيغة الرياضية للمتجه، المركّبات، متجهات الأساس،
# تغيير الأساس، ونظام الإحداثيات
# ==============================================================

# ---------------- إعدادات سريعة ----------------
TITLE_LINE1 = "تمهيد لقواعد"
TITLE_LINE2 = "المتجهات"
BADGE_TEXT = "الجبر الخطي • الحلقة 04"

# رفع خفيف للرسمة لتكون متوازنة بصرياً
PLOT_SHIFT = UP * 0.45 + RIGHT * 0.0

DRAW_SHIFT_X = -0.90
O = np.array([-1.55 + DRAW_SHIFT_X, -2.65, 0.0]) + PLOT_SHIFT
U = 0.60                                                        # طول وحدة الأساس

# حدود الشبكة لتمتد في الخلفية وتغطي السواد دون لمس الشخصية (تبدأ من -3.3 يميناً حتى 6.8)
GRID_BOX = (-3.3, 6.8, -3.85, 3.85)
FADE_W = 1.3                             # عرض منطقة تلاشي الشبكة عند الحد الأيسر (قدام الشخصية)
AXIS_FADE_LEN = 6.0                      # طول تلاشي المحاور القطرية التركواز

F2_COL = "#A8EDE3"                       # تركواز فاتح لـ f2 (يتفرق عن ذهبي v وعن تركواز f1)

E1, E2 = np.array([1.0, 0.0]), np.array([0.0, 1.0])
F1, F2 = np.array([1.0, 1.0]), np.array([-1.0, 1.0])
V_STD = (3, 5)                           # v = 3 e1 + 5 e2
V_NEW = (4, 1)                           # v = 4 f1 + 1 f2  →  4(1,1) + (-1,1) = (3,5)

# مقدار إزاحة كتلة النصوص بالكامل (العناوين + المعادلات) لليمين
TEXT_SHIFT_X = 0.30
BASIS_TAG_SIZE = 64                      # حجم رمز الأساس e / f جنب المصفوفتين


def P(vec):
    """نقطة على الشاشة من إحداثيات (x, y) بوحدة U."""
    return np.array([O[0] + U * vec[0], O[1] + U * vec[1], 0.0])


def edge_fade(x):
    """معامل تلاشي ناعم (0..1) عند الحد الأيسر للشبكة."""
    t = np.clip((x - GRID_BOX[0]) / FADE_W, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def add_faded(g, p, q, color, width, opacity):
    """خط من p لـ q بيتلاشى تدريجيًا عند الحد الأيسر (بيتقسّم لأجزاء بس لو داخل منطقة التلاشي)."""
    p, q = np.asarray(p, float)[:2], np.asarray(q, float)[:2]
    if min(p[0], q[0]) >= GRID_BOX[0] + FADE_W:
        g.add(Line([*p, 0], [*q, 0], color=color, stroke_width=width, stroke_opacity=opacity))
        return
    n = max(2, int(np.ceil(np.linalg.norm(q - p) / 0.4)))
    for i in range(n):
        a = p + (q - p) * i / n
        b = p + (q - p) * (i + 1) / n
        f = edge_fade((a[0] + b[0]) / 2)
        if f * opacity < 0.01:
            continue
        g.add(Line([*a, 0], [*b, 0], color=color, stroke_width=width, stroke_opacity=opacity * f))


def lattice(a, b, color, width, base, fade_rate=0.032, min_op=0.08, k0=-18, k1=22):
    """شبكة واضحة تملأ الخلفية وتخف تدريجياً (مع البعد، وعند الحد الأيسر) لتعطي عمقاً دون تشويش."""
    g = VGroup()
    for fam, step in ((a, b), (b, a)):
        for k in range(k0, k1 + 1):
            c0 = O[:2] + U * k * step
            c = clip_line(c0 - 45 * U * fam, c0 + 45 * U * fam, GRID_BOX)
            if c is None:
                continue
            mid = (c[0] + c[1]) / 2
            d = np.linalg.norm(mid - O[:2])
            opacity = max(min_op, base - fade_rate * d)
            add_faded(g, c[0], c[1], color, width, opacity)
    return g


def fade_ray(direction, color, width, op0, length, neg_scale=0.3):
    """محور قطري طالع من نقطة الأصل في الاتجاهين، بيخفت مع البعد. الاتجاه السالب (ناحية تحت) أقصر بنسبة neg_scale."""
    g = VGroup()
    for sign in (1.0, -1.0):
        c = clip_line(O[:2], O[:2] + sign * 45 * U * direction, GRID_BOX)
        if c is None:
            continue
        p, q = c
        L = length if sign > 0 else length * neg_scale
        n = max(4, int(np.ceil(np.linalg.norm(q - p) / 0.35)))
        for i in range(n):
            a = p + (q - p) * i / n
            b = p + (q - p) * (i + 1) / n
            d = np.linalg.norm((a + b) / 2 - O[:2])
            op = op0 * max(0.0, 1 - d / L) ** 1.4 * edge_fade((a[0] + b[0]) / 2)
            if op < 0.01:
                continue
            g.add(Line([*a, 0], [*b, 0], color=color, stroke_width=width, stroke_opacity=op))
    return g


def stack(start, d, n, color, width=5.5):
    """رصّة n متجه أساس ورا بعض بتحديد واضح."""
    g = VGroup()
    for i in range(n):
        g.add(Arrow(start + i * d, start + (i + 1) * d, buff=0, stroke_width=width, color=color,
                    max_tip_length_to_length_ratio=0.38, max_stroke_width_to_length_ratio=12))
    return g


def _round_joints(mob):
    """وصلات دايرية للستروك: بتمنع النتوءات الحادة (miter) عند أركان الحروف."""
    for sm in mob.family_members_with_points():
        sm.joint_type = LineJointType.ROUND
    return mob


def solid_text(text, width, color_a=IVORY_WHITE, color_b=GOLD_BRIGHT, glow=GOLD_LIGHT, outline_w=4,
               halo_w=(14, 7)):
    """
    نص بدون كتل سوداء في الخلفية، مع إغلاق شقوق الحروف، وهالة/إطار بوصلات دايرية (من غير نتوءات).
    """
    main = MarkupText(f"<b>{text}</b>", font=THUMB_FONT, font_size=96)
    main.set(width=width)
    main.set_color_by_gradient(color_a, color_b)
    for sm in main.family_members_with_points():
        sm.set_stroke(sm.get_fill_color(), width=1.6, opacity=1)
    _round_joints(main)

    outline = _round_joints(main.copy().set_fill(opacity=0).set_stroke(THUMB_BG, width=outline_w, opacity=0.9))
    halo = VGroup(
        main.copy().set_fill(opacity=0).set_stroke(glow, width=halo_w[0], opacity=0.07),
        main.copy().set_fill(opacity=0).set_stroke(glow, width=halo_w[1], opacity=0.11),
    )
    _round_joints(halo)
    return VGroup(halo, outline, main)


class Episode04Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = THUMB_BG

        # ---------------- 1. طبقة الخلفية والتوهج ----------------
        warm = vignette_bg()
        tip = P(V_STD)
        hot = soft_glow(tip * 0.55 + O * 0.45, 3.2, GOLD, layers=22, peak=0.060)

        # ---------------- 2. الشبكتين (واضحة وقوية تملأ السواد، وبتتلاشى قدام الشخصية) ----------------
        std_lat = lattice(E1, E2, STONE_AXIS, width=1.4, base=0.45, fade_rate=0.035, min_op=0.08)
        new_lat = lattice(F1, F2, TEAL, width=1.4, base=0.38, fade_rate=0.030, min_op=0.06)

        # المحاور القطرية للأساس الجديد: بتخفت مع البعد بدل ما تقطع الصورة لحد الركن
        new_axes = VGroup(*[fade_ray(f, TEAL, 2.4, 0.65, AXIS_FADE_LEN) for f in (F1, F2)])

        # ---------------- 3. المحاور الأصلية المضيئة ----------------
        axis_x_end = np.array([O[0] + 3.80, O[1], 0.0])
        axis_x = VGroup()
        add_faded(axis_x, [GRID_BOX[0], O[1]], axis_x_end[:2], GOLD_LIGHT, 3.2, 0.95)
        axis_y = Line([O[0], GRID_BOX[2], 0], [O[0], O[1] + 4.5, 0], color=GOLD_LIGHT, stroke_width=3.2,
                      stroke_opacity=0.95)
        tips = VGroup(
            Triangle(fill_color=GOLD_LIGHT, fill_opacity=0.95, stroke_width=0).scale(0.14).rotate(-PI / 2)
            .move_to(axis_x_end),
            Triangle(fill_color=GOLD_LIGHT, fill_opacity=0.95, stroke_width=0).scale(0.14)
            .move_to(axis_y.get_end()),
        )

        self.add(warm, hot, std_lat, new_lat, new_axes, axis_x, axis_y, tips, channel_frame())

        # ---------------- 4. رصّ متجهات الأساس ----------------
        # الطريقة 1: 3 × e1 ثم 5 × e2
        e_stack = VGroup(
            stack(O, U * np.array([E1[0], E1[1], 0.0]), V_STD[0], GOLD_BRIGHT, width=5.5),
            stack(P((V_STD[0], 0)), U * np.array([E2[0], E2[1], 0.0]), V_STD[1], COPPER_TERRA, width=5.5),
        )
        # الطريقة 2: 4 × f1 ثم 1 × f2
        f_stack = VGroup(
            stack(O, U * np.array([F1[0], F1[1], 0.0]), V_NEW[0], TEAL, width=5.5),
            stack(P(V_NEW[0] * F1), U * np.array([F2[0], F2[1], 0.0]), V_NEW[1], F2_COL, width=6.0),
        )

        # ---------------- 5. المتجه البطل v والتسميات ----------------
        v_glow = soft_glow(tip, 1.8, GOLD_BRIGHT, layers=16, peak=0.08)
        hero_arrow = glow_arrow(O, tip, GOLD_BRIGHT, 12, GOLD)
        v_label = MathTex(r"\vec{v}", tex_template=mach_math_template, font_size=100, color=GOLD_BRIGHT)
        v_label.next_to(tip, LEFT + UP * 0.15, buff=0.12)
        stroked(v_label)

        def tag(tex, color, pos, size=48):
            m = MathTex(tex, tex_template=mach_math_template, font_size=size, color=color)
            m.move_to(pos)
            return stroked(m, width=8)

        t_e1 = tag(r"3\,\mathbf{e}_1", GOLD_BRIGHT, O + np.array([0.90, -0.47, 0]))
        t_e2 = tag(r"5\,\mathbf{e}_2", COPPER_TERRA, O + np.array([2.45, 1.00, 0]))
        t_f1 = tag(r"4\,\mathbf{f}_1", TEAL, O + np.array([1.15, 0.60, 0]))
        t_f2 = tag(r"1\,\mathbf{f}_2", F2_COL, P(V_NEW[0] * F1) + np.array([0.25, 0.55, 0]), size=52)

        hero = layer([v_glow, e_stack, f_stack, hero_arrow, glow_dot(O), v_label, t_e1, t_e2, t_f1, t_f2], 35)
        self.add(hero)

        # ---------------- 6. الشخصية ----------------
        self.add(*mathematician_with_glow())

        # ---------------- 7. العنوان والبادج بالكامل وإزاحتهما يميناً ----------------
        title = title_block(TITLE_LINE1, TITLE_LINE2, BADGE_TEXT, line1_width=3.6, line2_width=5.4)

        for mob in title.get_family():
            if isinstance(mob, (Polygon, Ellipse, Rectangle, RoundedRectangle)):
                if mob.get_fill_color().to_hex().lower() in [THUMB_BG.lower(), "#000000", "#0e0905"]:
                    mob.set_fill(opacity=0)
                    mob.set_stroke(opacity=0)

        # السطر الصغير "تمهيد لقواعد": نص مقفول الشقوق + هالة بوصلات دايرية
        old_l1 = title[1][1]
        new_l1 = solid_text(TITLE_LINE1, old_l1.width)
        new_l1.move_to(old_l1.get_center())
        title.submobjects[1] = new_l1

        # السطر الكبير "المتجهات": نفس المعالجة (بدل الهالة المسننة)، مع إطار داكن أسمك عشان التباين فوق الشبكة
        old_l2 = title[2][1]
        new_l2 = solid_text(TITLE_LINE2, old_l2.width, GOLD_BRIGHT, GOLD, glow=GOLD, outline_w=9,
                            halo_w=(20, 10))
        new_l2.move_to(old_l2.get_center())
        title.submobjects[2] = new_l2

        # تحريك العنوان والبادج لليمين
        title.shift(RIGHT * TEXT_SHIFT_X)

        title.set_z_index(30)
        self.add(title, brand_mark().set_z_index(30))
        underline = title[3]

        # ---------------- 8. كتلة المعادلات الموزعة والمحاذاة يميناً ----------------
        # 1) الصيغة العامة للمتجه (3 حدود بدل 4: بتبان أكبر في نفس العرض)
        formula = MathTex(
            r"\mathbf{v}",
            r"=",
            r"v_1 \, \mathbf{e}_1",
            r"+",
            r"\cdots",
            r"+",
            r"v_n \, \mathbf{e}_n",
            tex_template=mach_math_template,
            font_size=70,
            color=IVORY_WHITE,
        )
        formula.set_width(5.4)
        formula[0].set_color(GOLD_BRIGHT)
        for term_idx in (2, 6):
            formula[term_idx][0:2].set_color(GOLD_LIGHT)
            formula[term_idx][2:].set_color(COPPER_TERRA)
        stroked(formula, width=4.0)

        # 2) التعبير عن المتجه في الأساسين e و f (القائمتين)
        r_v = MathTex(r"\mathbf{v}=", tex_template=mach_math_template, font_size=74, color=GOLD_BRIGHT)
        def basis_matrix(top, bottom, label, color):
            """مصفوفة عمودية + رمز الأساس (e أو f) كبير وبولد جنب أسفلها بدل أس سفلي صغير."""
            m = MathTex(rf"\begin{{bmatrix}}{top}\\[3pt]{bottom}\end{{bmatrix}}",
                        tex_template=mach_math_template, font_size=74, color=color)
            t = MathTex(rf"\mathbf{{{label}}}", tex_template=mach_math_template, font_size=BASIS_TAG_SIZE,
                        color=color)
            t.move_to(m.get_corner(DR) + np.array([t.width / 2 + 0.06, t.height / 2 - 0.04, 0]))
            return VGroup(m, t)

        r_a = basis_matrix(3, 5, "e", GOLD_LIGHT)
        r_eq = MathTex(r"=", tex_template=mach_math_template, font_size=74, color=IVORY_WHITE)
        r_b = basis_matrix(4, 1, "f", TEAL)

        row = VGroup(r_v, r_a, r_eq, r_b).arrange(RIGHT, buff=0.24)
        if row.width > 5.6:                       # عشان ما يطلعش برا إطار القناة يمين
            row.scale(5.6 / row.width)

        stroked(row, width=6)

        # إزاحة القائمتين (row) يميناً لتكون بمحاذاة تامة مع العناصر فوقها
        row.shift(RIGHT * 0.45)

        # تجميع المعادلتين رأسياً
        col = VGroup(formula, row).arrange(DOWN, buff=0.55)

        # ضبط المحاذاة الرأسية والأفقية المتوازنة تحت العنوان مع تطبيق الإزاحة الجديدة لليمين
        top_y = underline.get_bottom()[1] - 0.40
        bottom_limit = -3.25
        avail = top_y - bottom_limit
        if col.height > avail:
            col.scale(avail / col.height)

        target_x = underline.get_center()[0] + 0.45
        target_y = (top_y + bottom_limit) / 2
        col.move_to([target_x, target_y, 0])
        col.set_z_index(30)

        # تظهر المعادلتان مباشرة فوق الشبكة
        self.add(col)