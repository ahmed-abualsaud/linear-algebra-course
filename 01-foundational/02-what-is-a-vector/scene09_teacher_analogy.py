from manim import *
import numpy as np
from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_DARK,
    GOLD_MUTED,
    STONE_AXIS,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.mobjects.characters import mach_mathematician
from common.latex import mach_math_template


# ==============================================================
# كلاس المتجه المعتمد الخاص بقناة MACH-MATH
# ==============================================================
class MachVector(VGroup):
    """المتجه الرسمي المخصص لقناة MACH-MATH."""
    def __init__(
        self,
        start=ORIGIN,
        end=RIGHT,
        color=COPPER_TERRA,
        stroke_width=3.0,
        tip_length=0.22,
        tip_angle=PI / 5.5,
        show_pivot=True,
        pivot_radius=0.045,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.start = np.array(start)
        self.end = np.array(end)
        self.color = color

        direction = self.end - self.start
        length = np.linalg.norm(direction)
        unit_dir = RIGHT if length == 0 else direction / length

        actual_end = self.end - unit_dir * (tip_length * 0.8)
        self.line = Line(self.start, actual_end, color=color, stroke_width=stroke_width, buff=0)

        left_angle = np.arctan2(unit_dir[1], unit_dir[0]) + PI - tip_angle
        right_angle = np.arctan2(unit_dir[1], unit_dir[0]) + PI + tip_angle

        wing_left = self.end + tip_length * np.array([np.cos(left_angle), np.sin(left_angle), 0])
        wing_right = self.end + tip_length * np.array([np.cos(right_angle), np.sin(right_angle), 0])

        self.tip = Polygon(
            self.end,
            wing_left,
            self.end - unit_dir * (tip_length * 0.35),
            wing_right,
            color=color,
            fill_color=color,
            fill_opacity=1.0,
            stroke_width=0,
        )
        self.add(self.line, self.tip)

        if show_pivot:
            self.pivot = Dot(self.start, radius=pivot_radius, color=color)
            self.add(self.pivot)


def make_card_floor_glow(
    card,
    accent_color=GOLD_LIGHT,
    reflection_offset=0.22,
    reflection_opacity=0.30,
):
    """بناء الانعكاس الأرضي والتوهج ثلاثي الأبعاد أسفل البطاقة بمطابقة خوارزمية MachTable."""
    glow_group = VGroup()
    w = card.width
    corner_radius = 0.22
    y_base = card.get_bottom()[1] - reflection_offset
    center_x = card.get_center()[0]

    # 1. طبقات التوهج البيضاوي
    n_glow_layers = 10
    for i in range(n_glow_layers):
        t = i / (n_glow_layers - 1)
        w_layer = w * interpolate(0.85, 1.25, t)
        h_layer = 0.38 * interpolate(0.35, 1.45, t)
        op_layer = reflection_opacity * interpolate(0.65, 0.005, t**0.6)

        glow_ellipse = Ellipse(
            width=w_layer, height=h_layer, stroke_width=0,
            fill_color=GOLD_MUTED if t > 0.4 else accent_color,
            fill_opacity=op_layer,
        ).move_to([center_x, y_base - h_layer * 0.25, 0])
        glow_group.add(glow_ellipse)

    # 2. شرائح الانعكاس المنظوري الزجاجي
    reflection_h = 0.45
    p_top_l = np.array([center_x - w / 2 + corner_radius, card.get_bottom()[1], 0])
    p_top_r = np.array([center_x + w / 2 - corner_radius, card.get_bottom()[1], 0])
    p_bot_r = np.array([center_x + (w / 2 - corner_radius) * 1.05, card.get_bottom()[1] - reflection_h, 0])
    p_bot_l = np.array([center_x - (w / 2 - corner_radius) * 1.05, card.get_bottom()[1] - reflection_h, 0])

    n_refl_slices = 8
    for j in range(n_refl_slices):
        alpha_a = j / n_refl_slices
        alpha_b = (j + 1) / n_refl_slices

        pt_tl = interpolate(p_top_l, p_bot_l, alpha_a)
        pt_tr = interpolate(p_top_r, p_bot_r, alpha_a)
        pt_br = interpolate(p_top_r, p_bot_r, alpha_b)
        pt_bl = interpolate(p_top_l, p_bot_l, alpha_b)

        slice_op = reflection_opacity * 0.45 * ((1.0 - alpha_a) ** 1.8)

        refl_slice = Polygon(
            pt_tl, pt_tr, pt_br, pt_bl, stroke_width=0,
            fill_color=accent_color if alpha_a < 0.3 else GOLD_DARK,
            fill_opacity=slice_op,
        )
        glow_group.add(refl_slice)

    contact_line = Line(
        p_top_l, p_top_r, color=accent_color,
        stroke_width=1.0, stroke_opacity=reflection_opacity * 0.8,
    )
    glow_group.add(contact_line)
    glow_group.set_z_index(-1)
    return glow_group


def play_scene09(scene):

    # ==============================================================
    # 1. المرحلة الأولى: ظهور عالم الرياضيات والحديث عن تشبيه المدرس
    # ==============================================================

    mathematician = mach_mathematician(
        color=COPPER_TERRA,
        accent_color=GOLD_LIGHT,
        pose="explaining",
        scale=0.92,
        blink=True,
        breathing=True,
        glasses=True,
        tie_type="bowtie",
    ).shift(LEFT * 4.2 + DOWN * 0.3)

    card_w, card_h = 7.4, 5.2
    X_RIGHT = 2.4

    # هيكل البطاقة الخارجي
    board_analogy = RoundedRectangle(
        corner_radius=0.28, width=card_w, height=card_h,
        stroke_width=1.4, color=GOLD_LIGHT, stroke_opacity=0.45,
        fill_color="#100D07", fill_opacity=0.85,
    ).move_to([X_RIGHT, 0, 0])

    # الطبقة الزجاجية الداخلية التي تجعل الخلفية "تنور"
    glass_analogy = RoundedRectangle(
        corner_radius=0.24, width=card_w - 0.12, height=card_h - 0.12,
        stroke_width=0.5, color=GOLD_LIGHT, stroke_opacity=0.18,
        fill_color=GOLD_LIGHT, fill_opacity=0.038,
    ).move_to(board_analogy.get_center())

    glow_analogy = make_card_floor_glow(board_analogy, accent_color=GOLD_LIGHT)

    # ---------------- محتوى التشبيه ----------------
    title_t1 = MarkupText("1. تعليم الاشتقاق والتكامل بدون دوال!", font="Cairo", font_size=18, color=COPPER_TERRA)\
        .move_to([X_RIGHT, 1.75, 0])

    calc_ops = MathTex(
        r"\frac{d}{dx} \quad \int",
        tex_template=mach_math_template,
        font_size=32,
        color=GOLD_LIGHT,
    )
    cross_calc = MathTex(r"\ne", font_size=36, color=GOLD_BRIGHT)
    func_q = MathTex(r"f(x)\; \text{?}", tex_template=mach_math_template, font_size=30, color=IVORY_WHITE)
    row_calc = VGroup(calc_ops, cross_calc, func_q).arrange(RIGHT, buff=0.28).move_to([X_RIGHT, 1.15, 0])

    div_line = DashedLine(
        [X_RIGHT - 3.1, 0.45, 0], [X_RIGHT + 3.1, 0.45, 0],
        dash_length=0.08, dashed_ratio=0.5, stroke_width=1.0, color=GOLD_DARK, stroke_opacity=0.4,
    )

    title_t2 = MarkupText("2. تعليم قواعد الحساب بدون الأرقام!", font="Cairo", font_size=18, color=COPPER_TERRA)\
        .move_to([X_RIGHT, -0.25, 0])

    arith_ops = MathTex(
        r"+ \quad - \quad \times \quad \div",
        tex_template=mach_math_template,
        font_size=32,
        color=GOLD_LIGHT,
    )
    cross_arith = MathTex(r"\ne", font_size=36, color=GOLD_BRIGHT)
    num_q = MathTex(r"1, 2, 3\; \text{?}", tex_template=mach_math_template, font_size=28, color=IVORY_WHITE)
    row_arith = VGroup(arith_ops, cross_arith, num_q).arrange(RIGHT, buff=0.28).move_to([X_RIGHT, -0.85, 0])

    note_text = MarkupText(
        "لا بد من بناء الصورة الذهنية أولاً!",
        font="Cairo", font_size=16, color=GOLD_BRIGHT,
    ).move_to([X_RIGHT, -1.85, 0])

    analogy_content = VGroup(
        title_t1, row_calc, div_line,
        title_t2, row_arith, note_text
    )

    analogy_full_group = VGroup(glow_analogy, board_analogy, glass_analogy, analogy_content)

    # أ) ظهور عالم الرياضيات
    scene.play(
        FadeIn(mathematician, shift=RIGHT * 0.3),
        run_time=0.9,
    )
    scene.wait(1.5)

    # ب) بناء إطار البطاقة أولاً (0.8s)
    scene.play(
        Create(board_analogy),
        Create(div_line),
        run_time=0.8,
    )

    # ج) اشتعال الزجاج الداخلي مع الانعكاس الأرضي في نفس اللحظة (فتضيء البطاقة تماماً كـ MachTable!) (0.5s)
    scene.play(
        FadeIn(glow_analogy),
        FadeIn(glass_analogy),
        run_time=0.5,
        rate_func=smooth,
    )

    # د) ظهور محتوى التشبيهات
    scene.play(
        FadeIn(title_t1),
        FadeIn(row_calc, shift=LEFT * 0.15),
        run_time=0.9,
    )
    scene.wait(2.2)

    scene.play(
        FadeIn(title_t2),
        FadeIn(row_arith, shift=LEFT * 0.15),
        FadeIn(note_text),
        run_time=1.0,
    )
    scene.wait(3.0)

    # هـ) تفريغ لوحة التشبيهات
    scene.play(
        FadeOut(analogy_full_group),
        run_time=0.8,
    )

    # ==============================================================
    # 2. المرحلة الثانية: الوعد بالحلقة القادمة (أبعاد ملمومة واشتعال مماثل)
    # ==============================================================

    next_card_w, next_card_h = 7.6, 3.6
    next_center_y = 0.0

    next_card_bg = RoundedRectangle(
        corner_radius=0.26, width=next_card_w, height=next_card_h,
        stroke_width=1.4, color=GOLD_LIGHT, stroke_opacity=0.55,
        fill_color="#100D07", fill_opacity=0.88,
    ).move_to([X_RIGHT, next_center_y, 0])

    next_glass = RoundedRectangle(
        corner_radius=0.22, width=next_card_w - 0.12, height=next_card_h - 0.12,
        stroke_width=0.5, color=GOLD_LIGHT, stroke_opacity=0.18,
        fill_color=GOLD_LIGHT, fill_opacity=0.038,
    ).move_to(next_card_bg.get_center())

    next_glow = make_card_floor_glow(next_card_bg, accent_color=GOLD_LIGHT)

    # العناوين
    next_badge = MarkupText("الحلقة القادمة", font="Cairo", font_size=15, color=COPPER_TERRA)\
        .next_to(next_card_bg.get_top(), DOWN, buff=0.28)

    next_title = MarkupText(
        "بناء الصورة الذهنية للمتجه",
        font="Cairo", font_size=23, color=GOLD_LIGHT,
    ).next_to(next_badge, DOWN, buff=0.14)

    # المتجه في قلب البطاقة
    y_vector_center = -0.05

    promise_vector = MachVector(
        start=[X_RIGHT - 1.85, y_vector_center, 0],
        end=[X_RIGHT + 1.85, y_vector_center, 0],
        color=GOLD_BRIGHT,
        stroke_width=4.0,
        tip_length=0.26,
        show_pivot=True,
        pivot_radius=0.05,
    )
    vec_label = MathTex(r"\mathbf{v}", tex_template=mach_math_template, font_size=28, color=GOLD_BRIGHT)\
        .next_to(promise_vector.tip, UR, buff=0.10)

    promise_desc = MarkupText(
        "أمثلة بصرية وفيزيائية وتطبيقية",
        font="Cairo", font_size=16, color=IVORY_WHITE,
    ).next_to(next_card_bg.get_bottom(), UP, buff=0.30)

    # و) بناء إطار بطاقة الحلقة القادمة أولاً (0.8s)
    scene.play(
        Create(next_card_bg),
        FadeIn(next_badge),
        FadeIn(next_title),
        run_time=0.8,
    )

    # ز) اشتعال الزجاج الداخلي مع الانعكاس الأرضي في نفس اللحظة (فتضيء البطاقة بالكامل!) (0.5s)
    scene.play(
        FadeIn(next_glow),
        FadeIn(next_glass),
        run_time=0.5,
        rate_func=smooth,
    )

    # ح) انبثاق المتجه والوصف
    scene.play(
        GrowFromPoint(promise_vector, promise_vector.start),
        FadeIn(vec_label),
        FadeIn(promise_desc, shift=UP * 0.1),
        run_time=1.1,
    )

    scene.wait(3.5)

    # ==============================================================
    # 3. تفريغ المشهد بالكامل لتسليم الشاشة للأوترو
    # ==============================================================
    promise_group = VGroup(
        next_glow, next_card_bg, next_glass,
        next_badge, next_title, promise_vector, vec_label, promise_desc
    )
    all_scene = Group(mathematician, promise_group)

    scene.play(
        FadeOut(all_scene),
        run_time=0.9,
    )
    scene.wait(0.5)