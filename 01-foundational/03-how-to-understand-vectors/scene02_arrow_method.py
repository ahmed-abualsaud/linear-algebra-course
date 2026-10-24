from manim import *
import numpy as np

from common.mobjects.vectors import MachVector
from common.mobjects.card import MachCard
from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_DARK,
    GOLD_MUTED,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.mobjects.coordinate_systems import MachAxes2D
from common.latex import mach_math_template


# ==============================================================
# MACH-MATH | Premium Vector Scene
# ==============================================================

BG_DARK = "#100D07"


# ==============================================================
# 1. Origin glow
# ==============================================================

def make_origin_glow(point):
    """توهج ذهبي هادئ حول نقطة الأصل."""

    glow = VGroup()

    for radius, opacity, width in [
        (0.20, 0.08, 8),
        (0.13, 0.13, 5),
        (0.075, 0.22, 3),
    ]:
        ring = Circle(
            radius=radius,
            stroke_color=GOLD_BRIGHT,
            stroke_width=width,
            stroke_opacity=opacity,
            fill_opacity=0,
        ).move_to(point)

        glow.add(ring)

    glow.add(
        Dot(
            point,
            radius=0.045,
            color=GOLD_BRIGHT,
        )
    )

    return glow


# ==============================================================
# 2. Scene 02 (المدة المضبوطة: 20.0 ثانية من 00:30 إلى 00:50)
# ==============================================================

def play_scene02(scene):

    # ==========================================================
    # A. Layout
    # ==========================================================

    LEFT_X = -5.5
    RIGHT_X = 3.75

    # ----------------------------------------------------------
    # شبكة الإحداثيات (الجانب الأيسر)
    # ----------------------------------------------------------

    axes = MachAxes2D(
        center=np.array([-3.35, -0.05, 0]),
        x_range=(-6, 6),
        y_range=(-6, 6),
        grid_step=0.55,
        show_ticks=True,
        show_numbers=True,
        number_font_size=12,
        number_buff=0.12,
        tick_length=0.09,
        tick_width=1.5,
        show_zero_label=True,
        show_origin=True,
    )

    origin = axes.get_origin()
    origin_glow = make_origin_glow(origin)

    # ----------------------------------------------------------
    # B. ترويسة الرسم البياني
    # ----------------------------------------------------------

    graph_title = MarkupText(
        "متجه في فضاء الإحداثيات",
        font="Cairo",
        font_size=18,
        color=GOLD_LIGHT,
    ).move_to([LEFT_X, 3.20, 0])

    graph_title_bg = RoundedRectangle(
        corner_radius=0.12,
        width=graph_title.width + 0.36,
        height=graph_title.height + 0.20,
        stroke_color=GOLD_LIGHT,
        stroke_width=0.9,
        stroke_opacity=0.32,
        fill_color=BG_DARK,
        fill_opacity=0.90,
    ).move_to(graph_title.get_center())

    graph_heading = VGroup(
        graph_title_bg,
        graph_title,
    ).set_z_index(10)

    # ----------------------------------------------------------
    # C. دالة بناء المتجه والإسقاطات ديناميكياً
    # ----------------------------------------------------------

    def build_vector(coords):
        x, y = coords
        end = axes.c2p(x, y)

        vector = MachVector(
            start=origin,
            end=end,
            color=COPPER_TERRA,
            stroke_width=3.8,
            tip_length=0.23,
            show_pivot=False,
        )

        label_direction = UP + RIGHT if x >= 0 else UP + LEFT

        label = MathTex(
            rf"\mathbf{{v}} = ({x},\,{y})",
            tex_template=mach_math_template,
            font_size=22,
            color=GOLD_LIGHT,
        ).next_to(
            end,
            label_direction,
            buff=0.24,
        )

        # خطوط الإسقاط المنقطة
        proj_x = DashedLine(
            end,
            axes.c2p(x, 0),
            dash_length=0.065,
            dashed_ratio=0.55,
            color=IVORY_WHITE,
            stroke_width=1.15,
            stroke_opacity=0.52,
        )

        proj_y = DashedLine(
            end,
            axes.c2p(0, y),
            dash_length=0.065,
            dashed_ratio=0.55,
            color=IVORY_WHITE,
            stroke_width=1.15,
            stroke_opacity=0.52,
        )

        projections = VGroup(proj_x, proj_y)

        endpoint = Dot(
            end,
            radius=0.045,
            color=GOLD_BRIGHT,
        )

        # حساب المقدار
        magnitude = np.hypot(x, y)

        magnitude_text = MathTex(
            rf"\|\mathbf{{v}}\| = {magnitude:g}",
            tex_template=mach_math_template,
            font_size=17,
            color=GOLD_BRIGHT,
        ).next_to(
            label,
            DOWN,
            buff=0.10,
        )

        magnitude_bg = SurroundingRectangle(
            magnitude_text,
            color=BG_DARK,
            fill_color=BG_DARK,
            fill_opacity=0.88,
            stroke_width=0,
            buff=0.055,
            corner_radius=0.04,
        )

        magnitude_bg.set_z_index(4)
        magnitude_text.set_z_index(5)

        magnitude_label = VGroup(
            magnitude_bg,
            magnitude_text,
        )

        return (
            vector,
            label,
            projections,
            endpoint,
            magnitude_label,
        )

    # بناء المتجه الأولي
    (
        vector_v,
        vector_label,
        projections,
        endpoint,
        magnitude_label,
    ) = build_vector((2, 2))

    # ----------------------------------------------------------
    # D. بطاقة التعريف باستخدام MachCard النظيفة
    # ----------------------------------------------------------

    card_center = np.array([RIGHT_X, 0.10, 0.0])

    main_definition = MarkupText(
        "سهم له مقدار واتجاه",
        font="Cairo",
        font_size=21,
        color=IVORY_WHITE,
    )

    english_definition = Text(
        "(Magnitude & Direction)",
        font="Cairo",
        font_size=14,
        color=GOLD_MUTED,
    )

    accent_line = Line(
        LEFT * 0.30,
        RIGHT * 0.30,
        color=COPPER_TERRA,
        stroke_width=1.8,
    )

    card_content = VGroup(
        main_definition,
        english_definition,
        accent_line,
    ).arrange(DOWN, buff=0.14)

    card = MachCard(
        width=4.35,
        height=2.55,
        center=card_center,
        title="التعريف التقليدي:",
        title_font_size=18,
        title_buff=0.16,
        content=card_content,
        reflection_offset=0.18,
        reflection_opacity=0.20,
    )

    # ==========================================================
    # E. التحريك والتزامن (مضبوط على 20.0 ثانية بالضبط)
    # ==========================================================

    # 1. رسم شبكة المحاور (3.0s إجمالي)
    scene.wait(1.0)
    axes.animate_creation(
        scene,
        run_time=2.0,
    )

    # 2. إظهار ترويسة الرسم وتوهج الأصل (2.0s إجمالي)
    scene.play(
        FadeIn(graph_heading, shift=DOWN * 0.10),
        FadeIn(origin_glow),
        run_time=0.8,
    )
    scene.wait(1.2)

    # 3. إظهار المتجه وإسقاطاته (2.0s إجمالي)
    scene.play(
        Create(projections),
        GrowFromPoint(vector_v, origin),
        FadeIn(endpoint, scale=0.6),
        FadeIn(vector_label, shift=UP * 0.08),
        FadeIn(magnitude_label, shift=UP * 0.08),
        run_time=1.5,
        rate_func=smooth,
    )
    scene.wait(0.5)

    # 4. بناء البطاقة الزجاجية ومحتواها (2.5s إجمالي)
    scene.play(
        card.construct(
            run_time=2.0,
            rate_func=smooth,
            show_reflection=True,
            illuminate_glass=True,
            show_content=True,
        ),
        run_time=2.0,
    )
    scene.wait(0.5)

    # ----------------------------------------------------------
    # F. استكشاف اتجاهات مختلفة للمتجه (7.0s إجمالي للنقاط الأربعة)
    # ----------------------------------------------------------

    target_points = [
        (2, -4.5),
        (-2.7, 1),
        (-3, 0),
        (3, 2),
    ]

    for coords in target_points:
        (
            new_vector,
            new_label,
            new_proj,
            new_endpoint,
            new_magnitude_label,
        ) = build_vector(coords)

        scene.play(
            Transform(vector_v, new_vector),
            Transform(vector_label, new_label),
            Transform(projections, new_proj),
            Transform(endpoint, new_endpoint),
            Transform(magnitude_label, new_magnitude_label),
            run_time=1.0,
            rate_func=smooth,
        )

        scene.wait(0.75)

    # إبقاء الوضع الأخير للتأمل مع نهاية الجملة
    scene.wait(1.5)

    # ----------------------------------------------------------
    # G. تفريغ المشهد (2.0s إجمالي)
    # ----------------------------------------------------------

    all_elements = VGroup(
        axes,
        graph_heading,
        origin_glow,
        vector_v,
        vector_label,
        projections,
        endpoint,
        magnitude_label,
        card,
    )

    scene.play(
        FadeOut(all_elements),
        run_time=1.2,
    )

    scene.wait(0.8)

    # الحسبة الدقيقة: 3.0 + 2.0 + 2.0 + 2.5 + 7.0 + 1.5 + 2.0 = 20.0 ثانية بالمللي!