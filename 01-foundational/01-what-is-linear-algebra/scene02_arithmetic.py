from manim import *
from common.mobjects.coordinate_systems import MachNumberLine
from common.palette import GOLD_LIGHT, STONE_AXIS, IVORY_WHITE
from common.latex import mach_math_template


def play_scene02(scene):
    # 1. عنوان المشهد بخط Cairo
    title = Text("علم الحساب", font="Cairo", weight=BOLD, font_size=38, color=IVORY_WHITE).shift(UP * 2.5)

    # 2. خط الأعداد الرسمي المتماثل
    number_line = MachNumberLine(length=7.4).shift(DOWN * 1.8)

    # إشارات اللانهاية في موضعها المنضبط خارج رؤوس الأسهم
    inf_right = MathTex(r"\infty", font_size=22, color=STONE_AXIS).next_to(number_line.axis.get_right(), RIGHT, buff=0.15)
    inf_left = MathTex(r"-\infty", font_size=22, color=STONE_AXIS).next_to(number_line.axis.get_left(), LEFT, buff=0.15)
    line_group = VGroup(number_line, inf_right, inf_left).shift(DOWN * 0.8)

    # 3. رموز العمليات الأربعة
    plus = MathTex("+", tex_template=mach_math_template, font_size=65, color=GOLD_LIGHT).shift(UP * 0.9)
    minus = MathTex("-", tex_template=mach_math_template, font_size=65, color=GOLD_LIGHT).shift(RIGHT * 1.6 + UP * 0.1)
    times = MathTex(r"\times", tex_template=mach_math_template, font_size=65, color=GOLD_LIGHT).shift(DOWN * 0.7)
    div = MathTex(r"\div", tex_template=mach_math_template, font_size=65, color=GOLD_LIGHT).shift(LEFT * 1.6 + UP * 0.1)
    ops_group = VGroup(plus, minus, times, div)

    # الأنيميشن
    scene.play(FadeIn(title, shift=DOWN * 0.2), Create(line_group), run_time=1.0)
    scene.play(
        LaggedStart(
            FadeIn(plus, scale=0.5),
            FadeIn(minus, scale=0.5),
            FadeIn(times, scale=0.5),
            FadeIn(div, scale=0.5),
            lag_ratio=0.15
        ),
        run_time=1.0
    )
    scene.wait(1.5)

    # تفريغ المشهد
    scene.play(FadeOut(VGroup(title, line_group, ops_group)), run_time=0.6)