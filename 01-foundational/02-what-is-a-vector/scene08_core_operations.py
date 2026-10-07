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


def play_scene08(scene):

    # ==============================================================
    # 1. المرحلة الأولى: شرط ومعيار الانتماء لفضاء المتجهات (أبعاد ملمومة)
    # ==============================================================
    # تقليص الارتفاع إلى 3.4 ليصبح متماسكاً وأنيقاً تماماً
    crit_w, crit_h = 9.8, 3.4
    crit_center_y = 0.1

    crit_bg = RoundedRectangle(
        corner_radius=0.26, width=crit_w, height=crit_h,
        stroke_width=1.4, color=GOLD_LIGHT, stroke_opacity=0.45,
        fill_color="#100D07", fill_opacity=0.88,
    ).move_to([0, crit_center_y, 0])

    crit_glass = RoundedRectangle(
        corner_radius=0.22, width=crit_w - 0.12, height=crit_h - 0.12,
        stroke_width=0.5, color=GOLD_LIGHT, stroke_opacity=0.18,
        fill_color=GOLD_LIGHT, fill_opacity=0.038,
    ).move_to(crit_bg.get_center())

    crit_glow = make_card_floor_glow(crit_bg, accent_color=GOLD_LIGHT)

    crit_title = MarkupText(
        "معيار الانتماء لفضاء المتجهات",
        font="Cairo", font_size=23, color=GOLD_LIGHT,
    ).next_to(crit_bg.get_top(), DOWN, buff=0.28)

    crit_divider = Line(
        crit_bg.get_top() + DOWN * 0.85, crit_bg.get_bottom() + UP * 0.28,
        stroke_width=1.0, color=GOLD_DARK, stroke_opacity=0.45,
    )

    # ---------------- الجانب الأيمن: تنطبق القواعد ----------------
    icon_check = MathTex(r"\checkmark", font_size=36, color=GOLD_LIGHT)
    txt_check_1 = MarkupText("تنطبق القواعد", font="Cairo", font_size=19, color=IVORY_WHITE)
    math_check = MathTex(r"\implies \mathbf{v} \in V", tex_template=mach_math_template, font_size=25, color=GOLD_BRIGHT)
    lbl_check = MarkupText("(متجه)", font="Cairo", font_size=17, color=GOLD_BRIGHT)
    row_check = VGroup(math_check, lbl_check).arrange(LEFT, buff=0.14)
    box_right = VGroup(icon_check, txt_check_1, row_check).arrange(DOWN, buff=0.18).move_to([2.4, crit_center_y - 0.22, 0])

    # ---------------- الجانب الأيسر: لا تنطبق القواعد ----------------
    icon_cross = MathTex(r"\times", font_size=40, color=COPPER_TERRA)
    txt_cross_1 = MarkupText("لا تنطبق القواعد", font="Cairo", font_size=19, color=IVORY_WHITE)
    math_cross = MathTex(r"\implies \mathbf{v} \notin V", tex_template=mach_math_template, font_size=25, color=COPPER_TERRA)
    lbl_cross = MarkupText("(ليس متجهاً)", font="Cairo", font_size=17, color=COPPER_TERRA)
    row_cross = VGroup(math_cross, lbl_cross).arrange(LEFT, buff=0.14)
    box_left = VGroup(icon_cross, txt_cross_1, row_cross).arrange(DOWN, buff=0.16).move_to([-2.4, crit_center_y - 0.22, 0])

    criterion_group = VGroup(
        crit_glow, crit_bg, crit_glass, crit_title, crit_divider,
        box_right, box_left
    )

    # أ) بناء الإطار والعنوان
    scene.play(
        Create(crit_bg),
        FadeIn(crit_title),
        Create(crit_divider),
        run_time=0.9,
    )
    # ب) اشتعال الإضاءة والانعكاس مع ظهور الجانب الأيمن
    scene.play(
        FadeIn(crit_glow),
        FadeIn(crit_glass),
        FadeIn(box_right, shift=LEFT * 0.2),
        run_time=0.8,
    )
    scene.wait(1.5)

    # ج) ظهور الجانب الأيسر
    scene.play(
        FadeIn(box_left, shift=RIGHT * 0.2),
        run_time=0.8,
    )
    scene.wait(2.5)

    # د) تفريغ لوحة المعيار
    scene.play(
        FadeOut(criterion_group),
        run_time=0.8,
    )
    scene.wait(0.3)

    # ==============================================================
    # 2. المرحلة الثانية: اختزال القواعد (الجمع والضرب في ثابت) بصرياً
    # ==============================================================
    card_op_w, card_op_h = 5.8, 5.5
    X_OP_RIGHT = 3.1
    X_OP_LEFT  = -3.1

    # ---------------- 1. بطاقة جمع المتجهات (يمين) ----------------
    card_add = RoundedRectangle(
        corner_radius=0.28, width=card_op_w, height=card_op_h,
        stroke_width=1.4, color=GOLD_LIGHT, stroke_opacity=0.45,
        fill_color="#100D07", fill_opacity=0.85,
    ).move_to([X_OP_RIGHT, 0, 0])

    glass_add = RoundedRectangle(
        corner_radius=0.24, width=card_op_w - 0.12, height=card_op_h - 0.12,
        stroke_width=0.5, color=GOLD_LIGHT, stroke_opacity=0.18,
        fill_color=GOLD_LIGHT, fill_opacity=0.038,
    ).move_to(card_add.get_center())

    glow_add = make_card_floor_glow(card_add, accent_color=GOLD_LIGHT)

    title_op_add = MarkupText("1. جمع المتجهات", font="Cairo", font_size=23, color=GOLD_LIGHT)\
        .next_to(card_add.get_top(), DOWN, buff=0.35)
    subtitle_op_add = Text("Vector Addition", font="Cairo", font_size=14, color=STONE_AXIS)\
        .next_to(title_op_add, DOWN, buff=0.10)

    math_op_add = MathTex(
        r"\mathbf{u} + \mathbf{v}",
        tex_template=mach_math_template,
        font_size=34,
        color=GOLD_BRIGHT,
    ).next_to(subtitle_op_add, DOWN, buff=0.20)

    desc_add = MathTex(
        r"\mathbf{u}, \mathbf{v} \in V \implies (\mathbf{u} + \mathbf{v}) \in V",
        tex_template=mach_math_template,
        font_size=21,
        color=IVORY_WHITE,
    ).next_to(card_add.get_bottom(), UP, buff=0.35)

    O_add = np.array([X_OP_RIGHT - 1.05, -0.75, 0])
    P_u   = O_add + np.array([1.25, 0.35, 0])
    P_v   = P_u + np.array([0.55, 1.15, 0])

    vec_u = MachVector(start=O_add, end=P_u, color=GOLD_LIGHT, stroke_width=3.2, tip_length=0.18, show_pivot=True, pivot_radius=0.04)
    lbl_u = MathTex(r"\mathbf{u}", tex_template=mach_math_template, font_size=20, color=GOLD_LIGHT)\
        .next_to(vec_u.line.get_center(), DOWN, buff=0.10)

    vec_v = MachVector(start=P_u, end=P_v, color=COPPER_TERRA, stroke_width=3.0, tip_length=0.18, show_pivot=True, pivot_radius=0.04)
    lbl_v = MathTex(r"\mathbf{v}", tex_template=mach_math_template, font_size=20, color=COPPER_TERRA)\
        .next_to(vec_v.line.get_center(), RIGHT, buff=0.12)

    vec_sum = MachVector(start=O_add, end=P_v, color=GOLD_BRIGHT, stroke_width=3.6, tip_length=0.22, show_pivot=True, pivot_radius=0.048)
    lbl_sum = MathTex(r"\mathbf{u} + \mathbf{v}", tex_template=mach_math_template, font_size=21, color=GOLD_BRIGHT)\
        .next_to(vec_sum.line.get_center(), UL, buff=0.08)

    add_geo_group = VGroup(vec_u, lbl_u, vec_v, lbl_v, vec_sum, lbl_sum)

    # ---------------- 2. بطاقة الضرب القياسي (يسار) ----------------
    card_scalar = RoundedRectangle(
        corner_radius=0.28, width=card_op_w, height=card_op_h,
        stroke_width=1.4, color=COPPER_TERRA, stroke_opacity=0.45,
        fill_color="#100D07", fill_opacity=0.85,
    ).move_to([X_OP_LEFT, 0, 0])

    glass_scalar = RoundedRectangle(
        corner_radius=0.24, width=card_op_w - 0.12, height=card_op_h - 0.12,
        stroke_width=0.5, color=COPPER_TERRA, stroke_opacity=0.18,
        fill_color=COPPER_TERRA, fill_opacity=0.038,
    ).move_to(card_scalar.get_center())

    glow_scalar = make_card_floor_glow(card_scalar, accent_color=COPPER_TERRA)

    title_op_scalar = MarkupText("2. الضرب في رقم (قياسي)", font="Cairo", font_size=23, color=COPPER_TERRA)\
        .next_to(card_scalar.get_top(), DOWN, buff=0.35)
    subtitle_op_scalar = Text("Scalar Multiplication", font="Cairo", font_size=14, color=STONE_AXIS)\
        .next_to(title_op_scalar, DOWN, buff=0.10)

    math_op_scalar = MathTex(
        r"c \cdot \mathbf{v}",
        tex_template=mach_math_template,
        font_size=34,
        color=COPPER_TERRA,
    ).next_to(subtitle_op_scalar, DOWN, buff=0.20)

    desc_scalar = MathTex(
        r"c \in \mathbb{R}, \; \mathbf{v} \in V \implies c\mathbf{v} \in V",
        tex_template=mach_math_template,
        font_size=21,
        color=IVORY_WHITE,
    ).next_to(card_scalar.get_bottom(), UP, buff=0.35)

    O_scale  = np.array([X_OP_LEFT - 1.05, -0.65, 0])
    P_orig   = O_scale + np.array([0.85, 0.50, 0])
    P_scaled = O_scale + np.array([1.95, 1.15, 0])

    vec_scaled = MachVector(start=O_scale, end=P_scaled, color=COPPER_TERRA, stroke_width=3.6, tip_length=0.22, show_pivot=False)
    vec_scaled.set_z_index(5)
    lbl_scaled = MathTex(r"c\mathbf{v}\; (c > 1)", tex_template=mach_math_template, font_size=21, color=COPPER_TERRA)\
        .next_to(vec_scaled.tip, UR, buff=0.10).set_z_index(6)

    vec_orig = MachVector(start=O_scale, end=P_orig, color=STONE_AXIS, stroke_width=3.6, tip_length=0.18, show_pivot=True, pivot_radius=0.045)
    vec_orig.set_z_index(15)
    lbl_orig = MathTex(r"\mathbf{v}", tex_template=mach_math_template, font_size=20, color=STONE_AXIS)\
        .next_to(vec_orig.line.get_center(), UL, buff=0.10).set_z_index(16)

    scale_geo_group = VGroup(vec_scaled, lbl_scaled, vec_orig, lbl_orig)

    # بناء إطارات البطاقتين أولاً ثم اشتعال التوهج
    scene.play(
        Create(card_add),
        Create(card_scalar),
        FadeIn(title_op_add),
        FadeIn(subtitle_op_add),
        FadeIn(title_op_scalar),
        FadeIn(subtitle_op_scalar),
        run_time=1.0,
    )

    scene.play(
        FadeIn(glow_add),
        FadeIn(glass_add),
        FadeIn(glow_scalar),
        FadeIn(glass_scalar),
        FadeIn(math_op_add),
        FadeIn(math_op_scalar),
        run_time=0.55,
        rate_func=smooth,
    )

    scene.play(
        GrowFromPoint(vec_u, O_add),
        FadeIn(lbl_u),
        GrowFromPoint(vec_orig, O_scale),
        FadeIn(lbl_orig),
        run_time=0.9,
    )

    scene.play(
        GrowFromPoint(vec_v, P_u),
        FadeIn(lbl_v),
        GrowFromPoint(vec_scaled, O_scale),
        FadeIn(lbl_scaled),
        run_time=1.0,
    )

    scene.play(
        GrowFromPoint(vec_sum, O_add),
        FadeIn(lbl_sum),
        FadeIn(desc_add, shift=UP * 0.1),
        FadeIn(desc_scalar, shift=UP * 0.1),
        run_time=1.1,
    )

    scene.wait(4.5)

    # ==============================================================
    # 3. تفريغ المشهد للانتقال للمشهد التاسع
    # ==============================================================
    all_scene = Group(
        card_add, glass_add, glow_add, title_op_add, subtitle_op_add, math_op_add, desc_add, add_geo_group,
        card_scalar, glass_scalar, glow_scalar, title_op_scalar, subtitle_op_scalar, math_op_scalar, desc_scalar, scale_geo_group
    )

    scene.play(
        FadeOut(all_scene),
        run_time=0.9,
    )
    scene.wait(0.5)