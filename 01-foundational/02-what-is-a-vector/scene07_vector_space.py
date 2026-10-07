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
from common.mobjects import mach_stick_figure, speech_bubble
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


def make_board_floor_reflection(
    width=12.2,
    height=5.8,
    corner_radius=0.28,
    reflection_offset=0.22,
    reflection_opacity=0.32,
):
    """بناء الانعكاس الأرضي ثلاثي الأبعاد والتوهج الفوتوني بالخوارزمية الأصلية لـ MachTable."""
    floor_group = VGroup()
    y_base = -height / 2 - reflection_offset

    n_glow_layers = 10
    for i in range(n_glow_layers):
        t = i / (n_glow_layers - 1)
        w_layer = width * interpolate(0.85, 1.25, t)
        h_layer = 0.40 * interpolate(0.35, 1.50, t)
        op_layer = reflection_opacity * interpolate(0.65, 0.005, t**0.6)

        glow_ellipse = Ellipse(
            width=w_layer, height=h_layer, stroke_width=0,
            fill_color=GOLD_MUTED if t > 0.4 else GOLD_DARK,
            fill_opacity=op_layer,
        ).move_to([0, y_base - h_layer * 0.25, 0])
        floor_group.add(glow_ellipse)

    reflection_h = 0.55
    p_top_l = np.array([-width / 2 + corner_radius, -height / 2, 0])
    p_top_r = np.array([width / 2 - corner_radius, -height / 2, 0])
    p_bot_r = np.array([(width / 2 - corner_radius) * 1.06, -height / 2 - reflection_h, 0])
    p_bot_l = np.array([(-width / 2 + corner_radius) * 1.06, -height / 2 - reflection_h, 0])

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
            fill_color=GOLD_LIGHT if alpha_a < 0.3 else GOLD_DARK,
            fill_opacity=slice_op,
        )
        floor_group.add(refl_slice)

    contact_line = Line(
        p_top_l, p_top_r, color=GOLD_LIGHT,
        stroke_width=1.0, stroke_opacity=reflection_opacity * 0.75,
    )
    floor_group.add(contact_line)
    floor_group.set_z_index(-1)
    return floor_group


def play_scene07(scene):

    # ==============================================================
    # 1. المرحلة الأولى: السؤال والحوار (تلاشي الشخصيتين معاً)
    # ==============================================================
    asker = mach_stick_figure(
        color=STONE_AXIS,
        pose="neutral",
        scale=0.90,
        blink=True,
        breathing=True,
    ).shift(RIGHT * 2.2 + DOWN * 0.4)

    mathematician = mach_mathematician(
        color=COPPER_TERRA,
        accent_color=GOLD_LIGHT,
        pose="thinking",
        scale=0.90,
        blink=True,
        breathing=True,
        glasses=True,
        tie_type="bowtie",
    ).shift(LEFT * 2.2 + DOWN * 0.4)

    box_ask, dots_ask, text_ask = speech_bubble(
        lines_text=["إيه هو المتجه؟"],
        anchor_head=asker[0],
        color=GOLD_LIGHT,
        font_size=24,
        shift=RIGHT * 0.6 + UP * 0.1,
    )

    scene.play(
        FadeIn(asker, shift=UP * 0.2),
        FadeIn(mathematician, shift=UP * 0.2),
        run_time=0.8,
    )

    scene.play(
        FadeIn(dots_ask, scale=0.5),
        FadeIn(box_ask, scale=0.9),
        FadeIn(text_ask, shift=LEFT * 0.2),
        run_time=0.8,
    )
    scene.wait(2.2)

    scene.play(
        FadeOut(box_ask),
        FadeOut(dots_ask),
        FadeOut(text_ask),
        FadeOut(asker, shift=RIGHT * 0.3),
        FadeOut(mathematician, shift=LEFT * 0.3),
        run_time=0.9,
    )
    scene.wait(0.3)

    # ==============================================================
    # 2. المرحلة الثانية: ظهور "فضاء المتجهات" بمتجهات القناة المخصصة
    # ==============================================================
    grid_lines = VGroup()
    step = 0.80

    # 1. المحوران الذهبيان الرئيسيان المتقاطعان في المركز [0,0,0]
    axis_x = DashedLine(
        [-7.2, 0, 0], [7.2, 0, 0],
        dash_length=0.08, dashed_ratio=0.55,
        color=GOLD_LIGHT, stroke_width=2.2, stroke_opacity=0.90,
    )
    axis_y = DashedLine(
        [0, -4.0, 0], [0, 4.0, 0],
        dash_length=0.08, dashed_ratio=0.55,
        color=GOLD_LIGHT, stroke_width=2.2, stroke_opacity=0.90,
    )
    grid_lines.add(axis_x, axis_y)

    # 2. الخطوط الرأسية الموازية
    for i in range(1, 10):
        for sgn in [-1, 1]:
            x_val = sgn * i * step
            if abs(x_val) <= 7.2:
                grid_lines.add(
                    DashedLine(
                        [x_val, -4.0, 0], [x_val, 4.0, 0],
                        dash_length=0.08, dashed_ratio=0.55,
                        color=STONE_AXIS, stroke_width=0.9, stroke_opacity=0.45,
                    )
                )

    # 3. الخطوط الأفقية الموازية
    for j in range(1, 6):
        for sgn in [-1, 1]:
            y_val = sgn * j * step
            if abs(y_val) <= 4.0:
                grid_lines.add(
                    DashedLine(
                        [-7.2, y_val, 0], [7.2, y_val, 0],
                        dash_length=0.08, dashed_ratio=0.55,
                        color=STONE_AXIS, stroke_width=0.9, stroke_opacity=0.45,
                    )
                )

    # نقطة التقاطع المركزية المتوهجة فوق المحورين بالضبط
    origin_dot = Dot(ORIGIN, radius=0.075, color=GOLD_BRIGHT).set_z_index(15)

    # باقة المتجهات بأطوال متباينة تنطلق من نقطة الأصل الدقيقة
    vec_data = [
        ([ 3.2,  2.1, 0], GOLD_BRIGHT,  r"\mathbf{v}_1"),  # طويل
        ([-1.7,  1.9, 0], COPPER_TERRA, r"\mathbf{v}_2"),  # متوسط
        ([-1.2, -0.6, 0], STONE_AXIS,   r"\mathbf{v}_3"),  # قصير
        ([ 1.4, -1.9, 0], GOLD_LIGHT,   r"\mathbf{v}_4"),  # متوسط
        ([ 3.8, -0.5, 0], IVORY_WHITE,  r"\mathbf{v}_5"),  # طويل جداً
        ([-0.8, -2.4, 0], GOLD_MUTED,   r"\mathbf{v}_6"),  # متوسط / قصير
    ]

    vector_mobs = VGroup()
    for end_pt, color, label_tex in vec_data:
        vec = MachVector(
            start=ORIGIN,
            end=end_pt,
            color=color,
            stroke_width=3.2,
            tip_length=0.24,
            show_pivot=False,
        )
        lbl = MathTex(label_tex, tex_template=mach_math_template, font_size=20, color=color)\
            .next_to(end_pt, normalize(end_pt), buff=0.14)
        vector_mobs.add(VGroup(vec, lbl))

    vs_title = MarkupText(
        "فضاء المتجهات (Vector Space)",
        font="Cairo", font_size=26, color=GOLD_LIGHT,
    ).to_edge(UP, buff=0.45)
    vs_title_bg = RoundedRectangle(
        corner_radius=0.14, width=vs_title.width + 0.6, height=vs_title.height + 0.35,
        stroke_width=1.0, color=GOLD_LIGHT, stroke_opacity=0.4,
        fill_color="#100D07", fill_opacity=0.85,
    ).move_to(vs_title.get_center())

    title_group = VGroup(vs_title_bg, vs_title).set_z_index(20)

    # ظهور فضاء المتجهات المتناسق هندسياً
    scene.play(
        FadeIn(grid_lines),
        FadeIn(origin_dot),
        FadeIn(title_group, shift=DOWN * 0.15),
        run_time=1.2,
    )
    # انبثاق متجهات القناة من نقطة الأصل (ORIGIN) بسلاسة
    scene.play(
        LaggedStart(*[GrowFromPoint(v[0], ORIGIN) for v in vector_mobs], lag_ratio=0.15),
        LaggedStart(*[FadeIn(v[1]) for v in vector_mobs], lag_ratio=0.15),
        run_time=1.4,
    )

    scene.wait(2.2)

    # ==============================================================
    # تقليص المتجهات تدريجياً لتعود لنقطة الأصل ثم تلاشي الفضاء
    # ==============================================================
    scene.play(
        LaggedStart(
            *[v[0].animate.scale(0.0001, about_point=ORIGIN) for v in vector_mobs],
            lag_ratio=0.10,
        ),
        LaggedStart(
            *[FadeOut(v[1], scale=0.4) for v in vector_mobs],
            lag_ratio=0.10,
        ),
        run_time=1.2,
        rate_func=rush_into,
    )

    # إزالة كائنات المتجهات بعد انكماشها تماماً
    scene.remove(vector_mobs)

    # تلاشي الشبكة، نقطة الأصل، والعنوان
    scene.play(
        FadeOut(grid_lines),
        FadeOut(origin_dot, scale=0.3),
        FadeOut(title_group, shift=UP * 0.2),
        run_time=0.8,
    )
    scene.wait(0.3)

    # ==============================================================
    # 3. المرحلة الثالثة: اللوحة الزجاجية المتوهجة وقواعد المتجهات
    # ==============================================================
    card_w, card_h = 12.2, 5.8
    corner_r = 0.28

    board_rect = RoundedRectangle(
        corner_radius=corner_r, width=card_w, height=card_h,
        stroke_width=1.4, color=GOLD_LIGHT, stroke_opacity=0.45,
        fill_color="#100D07", fill_opacity=0.82,
    )

    board_glass = RoundedRectangle(
        corner_radius=max(0, corner_r - 0.04),
        width=card_w - 0.12, height=card_h - 0.12,
        stroke_color=GOLD_LIGHT, stroke_width=0.5, stroke_opacity=0.18,
        fill_color=GOLD_LIGHT, fill_opacity=0.038,
    )

    floor_reflection = make_board_floor_reflection(
        width=card_w, height=card_h, corner_radius=corner_r,
        reflection_offset=0.22, reflection_opacity=0.32,
    )

    board_title = MarkupText(
        "فضاء المتجهات: القواعد  والبديهيات (Vector Space Axioms)",
        font="Cairo", font_size=23, color=GOLD_LIGHT,
    ).next_to(board_rect.get_top(), DOWN, buff=0.38)

    header_line = Line(
        board_rect.get_left() + RIGHT * 0.6,
        board_rect.get_right() + LEFT * 0.6,
        stroke_width=1.0, color=GOLD_DARK, stroke_opacity=0.45,
    ).next_to(board_title, DOWN, buff=0.28)

    col_sep = DashedLine(
        header_line.get_center() + DOWN * 0.15,
        board_rect.get_bottom() + UP * 0.35,
        dash_length=0.08, dashed_ratio=0.5,
        stroke_width=1.0, color=GOLD_DARK, stroke_opacity=0.45,
    )

    y_col_title = header_line.get_center()[1] - 0.50

    title_add = MarkupText("1. قواعد الجمع (Vector Addition)", font="Cairo", font_size=18, color=COPPER_TERRA)\
        .move_to([3.0, y_col_title, 0])

    add_axioms = VGroup(
        MathTex(r"\mathbf{u} + \mathbf{v} \in V", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"\mathbf{u} + \mathbf{v} = \mathbf{v} + \mathbf{u}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"(\mathbf{u} + \mathbf{v}) + \mathbf{w} = \mathbf{u} + (\mathbf{v} + \mathbf{w})", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"\mathbf{u} + \mathbf{0} = \mathbf{u}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"\mathbf{u} + (-\mathbf{u}) = \mathbf{0}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
    ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([3.0, y_col_title - 1.45, 0])

    col_add = VGroup(title_add, add_axioms)

    title_scale = MarkupText("2. قواعد الضرب القياسي (Scalar Mult.)", font="Cairo", font_size=18, color=COPPER_TERRA)\
        .move_to([-3.0, y_col_title, 0])

    scale_axioms = VGroup(
        MathTex(r"c\mathbf{u} \in V", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"c(\mathbf{u} + \mathbf{v}) = c\mathbf{u} + c\mathbf{v}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"(c + d)\mathbf{u} = c\mathbf{u} + d\mathbf{u}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"c(d\mathbf{u}) = (cd)\mathbf{u}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"1\mathbf{u} = \mathbf{u}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
    ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([-3.0, y_col_title - 1.45, 0])

    col_scale = VGroup(title_scale, scale_axioms)

    board_core = VGroup(board_rect, board_glass, board_title, header_line, col_sep)
    rules_board = VGroup(floor_reflection, board_core, col_add, col_scale)

    scene.play(
        Create(board_rect),
        FadeIn(board_title),
        Create(header_line),
        Create(col_sep),
        run_time=1.0,
    )

    scene.play(
        FadeIn(floor_reflection),
        FadeIn(board_glass),
        run_time=0.55,
        rate_func=smooth,
    )

    scene.play(
        FadeIn(col_add, shift=LEFT * 0.15),
        FadeIn(col_scale, shift=RIGHT * 0.15),
        run_time=1.1,
    )

    scene.wait(4.0)

    # ==============================================================
    # 4. تفريغ المشهد للانتقال للمشهد الثامن
    # ==============================================================
    scene.play(
        FadeOut(rules_board),
        run_time=0.9,
    )
    scene.wait(0.5)