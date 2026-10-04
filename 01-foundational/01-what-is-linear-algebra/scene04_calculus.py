from manim import *
from common.mobjects.coordinate_systems import MachAxes
from common.palette import (
    COPPER_TERRA,
    BRONZE,
    GOLD_LIGHT,
    IVORY_WHITE,
)
from common.latex import mach_math_template


def play_scene04(scene):

    # ==============================================================
    # 1. رسم محاور الإحداثيات والمنحنى
    # ==============================================================

    axes = MachAxes(
        x_range=[-4, 4, 1],
        y_range=[-4, 4, 1],
        x_length=4.6,
        y_length=4.6,
        font_size=16,
    ).shift(LEFT * 3.2 + UP * 0.2)

    curve = axes.plot(
        lambda x: 0.06 * x**3 - 0.25 * x + 0.8,
        x_range=[-4, 4],
        color=COPPER_TERRA,
        stroke_width=3.2,
    )

    label_x = -1.5
    label_y = 0.06 * label_x**3 - 0.25 * label_x + 0.8

    curve_label = MathTex(
        r"f(x)",
        color=COPPER_TERRA,
        font_size=30,
    )

    curve_label.move_to(axes.c2p(label_x, label_y))
    curve_label.shift(UP * 0.22 + RIGHT * 0.10)

    graph_group = VGroup(
        axes,
        curve,
        curve_label,
    )

    # ==============================================================
    # 2. الجانب الأيمن (معادلتا التفاضل والتكامل)
    # ==============================================================

    # سطر التفاضل
    diff_lbl = MarkupText(
        '<span font_family="Cairo" weight="bold">التفاضل</span>',
        font_size=24,
        color=BRONZE,
    )
    diff_math = MathTex(
        r"\frac{df(x)}{dx}",
        tex_template=mach_math_template,
        color=BRONZE,
        font_size=32,
    )
    diff_equals = MathTex(
        r"=",
        tex_template=mach_math_template,
        color=BRONZE,
        font_size=32,
    )
    diff_line = VGroup(
        diff_math,
        diff_equals,
        diff_lbl,
    ).arrange(
        RIGHT,
        buff=0.25,
    )
    diff_line.shift(RIGHT * 2.0 + UP * 0.8)

    # سطر التكامل
    integ_lbl = MarkupText(
        '<span font_family="Cairo" weight="bold">التكامل</span>',
        font_size=24,
        color=GOLD_LIGHT,
    )
    integ_math = MathTex(
        r"\int f(x)\,dx",
        tex_template=mach_math_template,
        color=GOLD_LIGHT,
        font_size=32,
    )
    integ_equals = MathTex(
        r"=",
        tex_template=mach_math_template,
        color=GOLD_LIGHT,
        font_size=32,
    )
    integ_line = VGroup(
        integ_math,
        integ_equals,
        integ_lbl,
    ).arrange(
        RIGHT,
        buff=0.25,
    )
    integ_line.shift(RIGHT * 2.0 + DOWN * 0.6)

    diff_line.align_to(
        integ_line,
        RIGHT,
    )

    text_group = VGroup(
        diff_line,
        integ_line,
    )

    # ==============================================================
    # 3. الأنيميشن والتزامن (يبدأ عند 01:19 وينتهي عند 01:29)
    # ==============================================================

    # أ) بناء المحاور (حوالي 2.0s)
    axes.animate_creation(scene)

    # ب) رسم المنحنى f(x) (1.2s)
    scene.play(
        Create(curve),
        Write(curve_label),
        run_time=1.2,
    )

    # ج) ظهور عمليتي التفاضل والتكامل (1.0s)
    scene.play(
        FadeIn(
            text_group,
            shift=LEFT * 0.2,
        ),
        run_time=1.0,
    )

    # د) وقفة استيعاب العلاقة بين المنحنى والعمليات (4.6s)
    scene.wait(4.6)

    # ==============================================================
    # 4. تفريغ المشهد (1.2s)
    # ==============================================================

    scene.play(
        FadeOut(
            VGroup(
                graph_group,
                text_group,
            )
        ),
        run_time=0.6,
    )

    # استقرار الغرفة قبل دخول شخصية التفكير
    scene.wait(0.6)

    # إجمالي زمن المشهد الرابع: 10.0 ثوانٍ بالتمام والكمال!