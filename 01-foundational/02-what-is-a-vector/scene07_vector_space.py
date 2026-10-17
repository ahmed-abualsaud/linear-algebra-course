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

from common.mobjects.card import MachCard
from common.latex import mach_math_template
from common.mobjects.vector_space import MachVectorSpace


def play_scene07(scene):

    # ==============================================================
    # 1. المرحلة الأولى: السؤال والحوار (13.0 ث)
    # [03:12.0 -> 03:25.0 في التراك الصوتي]
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

    # ظهور الشخصيتين مع بداية جملة:
    # "طيب جرب تسأل عالم الرياضيات..." [03:12.0 - 03:12.8]
    scene.play(
        FadeIn(asker, shift=UP * 0.2),
        FadeIn(mathematician, shift=UP * 0.2),
        run_time=0.8,
    )

    # ظهور بالونة السؤال مع نطق "...إيه هو المتجه؟" [03:12.8 - 03:13.6]
    scene.play(
        FadeIn(dots_ask, scale=0.5),
        FadeIn(box_ask, scale=0.9),
        FadeIn(text_ask, shift=LEFT * 0.2),
        run_time=0.8,
    )

    # بقاء الشخصيات وعالم الرياضيات يتأمل أثناء استكمال الجملة:
    # "...وإنت ما عندكش أي تصور ولو حتى بسيط عن إيه هو المتجه لحد دلوقتي؟ طبعاً ده على عكس الأرقام..."
    # [03:13.6 - 03:23.2]
    scene.wait(9.6)

    # تفريغ الشخصيتين قبل الدخول في فضاء المتجهات [03:23.2 - 03:24.2]
    scene.play(
        FadeOut(box_ask),
        FadeOut(dots_ask),
        FadeOut(text_ask),
        FadeOut(asker, shift=RIGHT * 0.3),
        FadeOut(mathematician, shift=LEFT * 0.3),
        run_time=1.0,
    )
    scene.wait(0.8)

    # ==============================================================
    # 2. المرحلة الثانية: فضاء المتجهات على الشاشة بالكامل (17.0 ث)
    # [03:25.0 -> 03:42.0 في التراك الصوتي]
    # ==============================================================

    full_vector_space = MachVectorSpace(
        center=ORIGIN,
        width=14.4,
        height=8.0,
        grid_step=0.80,
        vectors=[
            ([3.2, 2.1, 0],   GOLD_BRIGHT,  r"\mathbf{v}_1"),
            ([-1.7, 1.9, 0],  COPPER_TERRA, r"\mathbf{v}_2"),
            ([-1.2, -0.6, 0], STONE_AXIS,   r"\mathbf{v}_3"),
            ([1.4, -1.9, 0],  GOLD_LIGHT,   r"\mathbf{v}_4"),
            ([3.8, -0.5, 0],  IVORY_WHITE,  r"\mathbf{v}_5"),
            ([-0.8, -2.4, 0], GOLD_MUTED,   r"\mathbf{v}_6"),
        ],
        title="فضاء المتجهات (Vector Space)",
        show_title=True,
        show_origin=True,
        grid_color=STONE_AXIS,
        axis_color=GOLD_LIGHT,
        grid_width=0.9,
        grid_opacity=0.45,
        axis_width=2.2,
        axis_opacity=0.90,
        dash_length=0.08,
        dashed_ratio=0.55,
        vector_width=3.2,
        tip_length=0.24,
        label_font_size=20,
        title_font_size=26,
        title_color=GOLD_LIGHT,
        title_background=True,
        title_top_buff=0.45,
        show_vector_labels=True,
    )

    grid_lines = VGroup(full_vector_space.grid, full_vector_space.axes)
    origin_dot = full_vector_space.origin
    vector_mobs = full_vector_space.vectors
    title_group = full_vector_space.title_group

    # ظهور الشبكة ونقطة الأصل مع جملة:
    # "رد عالم الرياضيات هنا هيكون مشابه لإجابته الأولى عن الأرقام..." [03:25.0 - 03:26.5]
    scene.play(
        FadeIn(grid_lines),
        FadeIn(origin_dot),
        run_time=1.5,
    )

    # ظهور العنوان مع جملة: "...وإن العالم الخاص بالمتجهات ده اسمه فضاء المتجهات..." [03:26.5 - 03:27.5]
    scene.play(
        FadeIn(title_group, shift=DOWN * 0.15),
        run_time=1.0,
    )

    # انبثاق المتجهات الملونة من نقطة الأصل [03:27.5 - 03:29.5]
    vector_animations = [
        GrowFromPoint(vector_group[0], ORIGIN)
        for vector_group in vector_mobs
    ]
    label_animations = [
        FadeIn(vector_group[1])
        for vector_group in vector_mobs
        if len(vector_group) > 1
    ]

    scene.play(
        LaggedStart(*vector_animations, lag_ratio=0.15),
        LaggedStart(*label_animations, lag_ratio=0.15),
        run_time=2.0,
    )

    # تأمل واستقرار شبكة فضاء المتجهات مع جملة:
    # "...وبرضه له قواعد وقوانين تحكمه" [03:29.5 - 03:37.7]
    scene.wait(8.2)

    # انكماش المتجهات تدريجياً إلى نقطة الأصل [03:37.7 - 03:39.1]
    vector_shrink_animations = [
        vector_group[0].animate.scale(0.0001, about_point=ORIGIN)
        for vector_group in vector_mobs
    ]
    label_fade_animations = [
        FadeOut(vector_group[1], scale=0.4)
        for vector_group in vector_mobs
        if len(vector_group) > 1
    ]

    scene.play(
        LaggedStart(*vector_shrink_animations, lag_ratio=0.10),
        LaggedStart(*label_fade_animations, lag_ratio=0.10),
        run_time=1.4,
        rate_func=rush_into,
    )

    scene.remove(vector_mobs)

    # إزالة الشبكة ونقطة الأصل والعنوان [03:39.1 - 03:40.5]
    scene.play(
        FadeOut(grid_lines),
        FadeOut(origin_dot, scale=0.3),
        FadeOut(title_group, shift=UP * 0.2),
        run_time=1.4,
    )
    scene.wait(1.5)

    # ==============================================================
    # 3. المرحلة الثالثة: اللوحة الزجاجية وقواعد فضاء المتجهات (10.0 ث)
    # [03:42.0 -> 03:52.0 في التراك الصوتي]
    # ==============================================================

    board_card = MachCard(
        width=12.2,
        height=5.8,
        center=ORIGIN,
        title="فضاء المتجهات: القواعد والبديهيات (Vector Space Axioms)",
        title_font="Cairo",
        title_font_size=23,
        title_color=GOLD_LIGHT,
        title_buff=0.28,
        content_padding=0.38,
        show_divider=True,
        divider_style="horizontal",
        corner_radius=0.28,
        background_color="#100D07",
        accent_color=GOLD_LIGHT,
        border_opacity=0.45,
    )

    col_sep = DashedLine(
        board_card.divider.get_center() + DOWN * 0.15,
        board_card.body.get_bottom() + UP * 0.35,
        dash_length=0.08,
        dashed_ratio=0.5,
        stroke_width=1.0,
        color=GOLD_DARK,
        stroke_opacity=0.45,
    )
    col_sep.set_z_index(2)

    y_col_title = board_card.divider.get_center()[1] - 0.50

    # قواعد الجمع
    title_add = MarkupText(
        "1. قواعد الجمع (Vector Addition)",
        font="Cairo",
        font_size=18,
        color=COPPER_TERRA,
    ).move_to([3.0, y_col_title, 0])

    add_axioms = VGroup(
        MathTex(r"\mathbf{u} + \mathbf{v} \in V", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"\mathbf{u} + \mathbf{v} = \mathbf{v} + \mathbf{u}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"(\mathbf{u} + \mathbf{v}) + \mathbf{w} = \mathbf{u} + (\mathbf{v} + \mathbf{w})", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"\mathbf{u} + \mathbf{0} = \mathbf{u}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"\mathbf{u} + (-\mathbf{u}) = \mathbf{0}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
    ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([3.0, y_col_title - 1.45, 0])

    col_add = VGroup(title_add, add_axioms)

    # قواعد الضرب القياسي
    title_scale = MarkupText(
        "2. قواعد الضرب القياسي (Scalar Mult.)",
        font="Cairo",
        font_size=18,
        color=COPPER_TERRA,
    ).move_to([-3.0, y_col_title, 0])

    scale_axioms = VGroup(
        MathTex(r"c\mathbf{u} \in V", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"c(\mathbf{u} + \mathbf{v}) = c\mathbf{u} + c\mathbf{v}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"(c + d)\mathbf{u} = c\mathbf{u} + d\mathbf{u}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"c(d\mathbf{u}) = (cd)\mathbf{u}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
        MathTex(r"1\mathbf{u} = \mathbf{u}", tex_template=mach_math_template, font_size=24, color=IVORY_WHITE),
    ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([-3.0, y_col_title - 1.45, 0])

    col_scale = VGroup(title_scale, scale_axioms)

    rules_board = VGroup(board_card, col_sep, col_add, col_scale)

    # بناء هيكل اللوحة مع جملة:
    # "طيب إيه هي القواعد اللي بتحكم المتجهات دي بالظبط؟" [03:42.0 - 03:43.2]
    scene.play(
        board_card.animate_shell(run_time=1.2),
        Create(col_sep, run_time=0.8),
    )

    # ظهور محتوى القواعد مع جملة:
    # "...القواعد دي هي اللي معروضة قدامك دلوقتي في الفيديو" [03:43.2 - 03:44.4]
    scene.play(
        FadeIn(col_add, shift=LEFT * 0.15),
        FadeIn(col_scale, shift=RIGHT * 0.15),
        run_time=1.2,
    )

    # استقرار اللوحة للقراءة السريعة [03:44.4 - 03:50.0]
    scene.wait(5.6)

    # ==============================================================
    # 4. تفريغ المشهد للانتقال للمشهد الثامن (2.0 ث)
    # [03:50.0 -> 03:52.0 في التراك الصوتي]
    # ==============================================================
    scene.play(
        FadeOut(rules_board),
        run_time=1.2,
    )
    scene.wait(0.8)  # سكون الانتقال النظيف للمشهد الثامن عند 03:52.0