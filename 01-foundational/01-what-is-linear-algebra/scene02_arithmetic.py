from manim import *
from common.identity import turn_off_neon
from common.latex import mach_math_template
from common.mobjects.coordinate_systems import MachNumberLine
from common.palette import GOLD_LIGHT, STONE_AXIS, IVORY_WHITE


def play_scene02(scene):
    # 1. عنوان المشهد بخط Cairo
    title = Text(
        "علم الحساب", font="Cairo", weight=BOLD, font_size=38, color=IVORY_WHITE
    ).shift(UP * 2.5)

    # 2. خط الأعداد الرسمي المتماثل
    number_line = MachNumberLine(length=7.4).shift(DOWN * 1.8)

    # إشارات اللانهاية في موضعها المنضبط خارج رؤوس الأسهم
    inf_right = MathTex(
        r"\infty", font_size=22, color=STONE_AXIS
    ).next_to(number_line.axis.get_right(), RIGHT, buff=0.15)
    inf_left = MathTex(
        r"-\infty", font_size=22, color=STONE_AXIS
    ).next_to(number_line.axis.get_left(), LEFT, buff=0.15)
    line_group = VGroup(number_line, inf_right, inf_left).shift(DOWN * 0.8)

    # 3. رموز العمليات الأربعة
    plus = MathTex(
        "+", tex_template=mach_math_template, font_size=65, color=GOLD_LIGHT
    ).shift(UP * 0.9)
    minus = MathTex(
        "-", tex_template=mach_math_template, font_size=65, color=GOLD_LIGHT
    ).shift(RIGHT * 1.6 + UP * 0.1)
    times = MathTex(
        r"\times",
        tex_template=mach_math_template,
        font_size=65,
        color=GOLD_LIGHT,
    ).shift(DOWN * 0.7)
    div = MathTex(
        r"\div", tex_template=mach_math_template, font_size=65, color=GOLD_LIGHT
    ).shift(LEFT * 1.6 + UP * 0.1)
    ops_group = VGroup(plus, minus, times, div)

    # ==============================================================
    # 1. رسم العنوان وخط الأعداد (7.0 ثوانٍ)
    # الكلام:
    # "ممكن لو سألتك: إيه هو علم الحساب؟
    # فغالباً هترد عليا بجملة قريبة من الجملة دي:
    # الحساب هو علم بنتعامل فيه مع الأرقام..."
    # ==============================================================
    scene.play(
        FadeIn(title, shift=DOWN * 0.2), Create(line_group), run_time=1.4
    )
    scene.wait(5.6)

    # ==============================================================
    # 2. ظهور العمليات الأربعة بالتزامن مع النطق (5.0 ثوانٍ)
    # الكلام: "... من خلال تطبيق عمليات حسابية زي: الجمع، والطرح، والضرب، والقسمة."
    # ==============================================================
    scene.play(
        LaggedStart(
            FadeIn(plus, scale=0.5),  # الجمع
            FadeIn(minus, scale=0.5),  # الطرح
            FadeIn(times, scale=0.5),  # الضرب
            FadeIn(div, scale=0.5),  # القسمة
            lag_ratio=0.35,
        ),
        run_time=2.2,
    )
    scene.wait(2.8)

    # ==============================================================
    # 3. استقرار المشهد أثناء التعقيب الصوتي (10.0 ثوانٍ)
    # الكلام:
    # "طبعاً إجابتك مش هتكون متماثلة بالحرف،
    # لكن أنت هتعبر عن نفس الفكرة بس بطريقتك أنت."
    # ==============================================================
    scene.wait(10.0)

    # ==============================================================
    # 4. تفريغ المشهد وإطفاء النيون بسلاسة (2.0 ثانية)
    # التزامن: نهاية المشهد والانتقال لمشهد الحوار
    # ==============================================================
    scene.play(FadeOut(VGroup(title, line_group, ops_group)), run_time=0.8)
    turn_off_neon(scene, run_time=0.8)
    scene.wait(0.4)

    # الحسبة الإجمالية للمشهد الثاني:
    # 1.4 (رسم الخط والعنوان) + 5.6 (شرح الأرقام) + 2.2 (ظهور العمليات) + 2.8 (استيعابها)
    # + 10.0 (التعقيب والشرح) + 0.8 (تفريغ العناصر) + 0.8 (إطفاء النيون) + 0.4 (استقرار)
    # = 24.0 ثانية بالضبط!