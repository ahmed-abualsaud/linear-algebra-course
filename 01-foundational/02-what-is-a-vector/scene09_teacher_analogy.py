from manim import *
import numpy as np
from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_DARK,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.mobjects.card import MachCard
from common.latex import mach_math_template
from common.mobjects.vectors import MachVector
from common.mobjects.characters import mach_mathematician


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

    X_RIGHT = 2.4

    # بطاقة التشبيه باستخدام MachCard
    card_analogy = MachCard(
        width=7.4,
        height=5.2,
        center=[X_RIGHT, 0, 0],
        show_divider=False,
        corner_radius=0.28,
        border_opacity=0.45,
    )

    # ---------------- محتوى التشبيه ----------------
    title_t1 = MarkupText(
        "1. تعليم الاشتقاق والتكامل بدون دوال!",
        font="Cairo",
        font_size=18,
        color=COPPER_TERRA,
    ).move_to([X_RIGHT, 1.75, 0])

    calc_ops = MathTex(
        r"\frac{d}{dx} \quad \int",
        tex_template=mach_math_template,
        font_size=32,
        color=GOLD_LIGHT,
    )
    cross_calc = MathTex(r"\ne", font_size=36, color=GOLD_BRIGHT)
    func_q = MathTex(
        r"f(x)\; \text{?}",
        tex_template=mach_math_template,
        font_size=30,
        color=IVORY_WHITE,
    )
    row_calc = (
        VGroup(calc_ops, cross_calc, func_q)
        .arrange(RIGHT, buff=0.28)
        .move_to([X_RIGHT, 1.15, 0])
    )

    div_line = DashedLine(
        [X_RIGHT - 3.1, 0.45, 0],
        [X_RIGHT + 3.1, 0.45, 0],
        dash_length=0.08,
        dashed_ratio=0.5,
        stroke_width=1.0,
        color=GOLD_DARK,
        stroke_opacity=0.4,
    )

    title_t2 = MarkupText(
        "2. تعليم قواعد الحساب بدون الأرقام!",
        font="Cairo",
        font_size=18,
        color=COPPER_TERRA,
    ).move_to([X_RIGHT, -0.25, 0])

    arith_ops = MathTex(
        r"+ \quad - \quad \times \quad \div",
        tex_template=mach_math_template,
        font_size=32,
        color=GOLD_LIGHT,
    )
    cross_arith = MathTex(r"\ne", font_size=36, color=GOLD_BRIGHT)
    num_q = MathTex(
        r"1, 2, 3\; \text{?}",
        tex_template=mach_math_template,
        font_size=28,
        color=IVORY_WHITE,
    )
    row_arith = (
        VGroup(arith_ops, cross_arith, num_q)
        .arrange(RIGHT, buff=0.28)
        .move_to([X_RIGHT, -0.85, 0])
    )

    note_text = MarkupText(
        "لا بد من بناء الصورة الذهنية أولاً!",
        font="Cairo",
        font_size=16,
        color=GOLD_BRIGHT,
    ).move_to([X_RIGHT, -1.85, 0])

    analogy_content = VGroup(
        title_t1,
        row_calc,
        div_line,
        title_t2,
        row_arith,
        note_text,
    )

    # ==============================================================
    # التزامن الصوتي المحسوب (إجمالي المشهد: 38.0 ثانية)
    # [04:30.0 -> 05:08.0 في التراك الصوتي]
    # ==============================================================

    # أ) ظهور عالم الرياضيات وبناء هيكل التشبيه (10.0 ث)
    # "لكن لو دخلت في شرح القواعد دي مرة واحدة من غير ما أشرحلك أمثلة..." [04:30.0 - 04:31.0]
    scene.play(
        FadeIn(mathematician, shift=RIGHT * 0.3),
        run_time=1.0,
    )
    # استماع أثناء "...تقربلك الصورة الذهنية اللي المفروض تتخيلها عن المتجه..." [04:31.0 - 04:35.0]
    scene.wait(4.0)

    # بناء هيكل البطاقة والفاصل [04:35.0 - 04:36.2]
    scene.play(
        card_analogy.animate_shell(run_time=1.2),
        Create(div_line, run_time=0.8),
    )
    scene.wait(3.8)

    # ب) التشبيه الأول: مدرس التفاضل والتكامل بدون دوال (9.0 ث)
    # "هكون عملت زي المدرس اللي بدأ يعلمك إزاي تشتق دالة أو تكاملها..." [04:40.0 - 04:41.0]
    scene.play(
        FadeIn(title_t1),
        FadeIn(row_calc, shift=LEFT * 0.15),
        run_time=1.0,
    )
    # نبض علامة الاستفهام مع "...من غير ما يضربلك أمثلة توضحلك إيه هي الدالة أصلاً" [04:41.0 - 04:42.0]
    scene.play(
        func_q.animate.scale(1.2).set_color(GOLD_BRIGHT),
        rate_func=there_and_back,
        run_time=1.0,
    )
    scene.wait(7.0)

    # ج) التشبيه الثاني: مدرس الحساب بدون أرقام (8.0 ث)
    # "أو زي المدرس اللي بيعلم الأطفال في المدرسة قواعد الجمع والطرح والضرب والقسمة..." [04:49.0 - 04:50.0]
    scene.play(
        FadeIn(title_t2),
        FadeIn(row_arith, shift=LEFT * 0.15),
        FadeIn(note_text),
        run_time=1.0,
    )
    # نبض علامة استفهام الأرقام مع "...من غير ما يعلمهم الأرقام" [04:50.0 - 04:51.0]
    scene.play(
        num_q.animate.scale(1.2).set_color(GOLD_BRIGHT),
        rate_func=there_and_back,
        run_time=1.0,
    )
    scene.wait(4.2)

    # تفريغ لوحة التشبيهات قبل الانتقال لوعد الحلقة القادمة [04:55.2 - 04:56.2]
    scene.play(
        FadeOut(VGroup(card_analogy, analogy_content)),
        run_time=1.0,
    )
    scene.wait(0.8)

    # ==============================================================
    # 2. المرحلة الثانية: الوعد بالحلقة القادمة والختام (11.0 ث)
    # [04:57.0 -> 05:08.0 في التراك الصوتي]
    # ==============================================================

    next_badge = MarkupText(
        "الحلقة القادمة",
        font="Cairo",
        font_size=15,
        color=COPPER_TERRA,
    )
    next_title = MarkupText(
        "بناء الصورة الذهنية للمتجه",
        font="Cairo",
        font_size=23,
        color=GOLD_LIGHT,
    )
    next_header = VGroup(next_badge, next_title).arrange(DOWN, buff=0.14)

    # بطاقة الحلقة القادمة
    next_card = MachCard(
        width=7.6,
        height=3.6,
        center=[X_RIGHT, 0, 0],
        title=next_header,
        show_divider=False,
        corner_radius=0.26,
        content_padding=0.28,
        border_opacity=0.55,
    )

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
    vec_label = MathTex(
        r"\mathbf{v}",
        tex_template=mach_math_template,
        font_size=28,
        color=GOLD_BRIGHT,
    ).next_to(promise_vector.tip, UR, buff=0.10)

    promise_desc = MarkupText(
        "أمثلة بصرية وفيزيائية وتطبيقية",
        font="Cairo",
        font_size=16,
        color=IVORY_WHITE,
    ).next_to(next_card.body.get_bottom(), UP, buff=0.30)

    # بناء هيكل بطاقة الحلقة القادمة مع جملة:
    # "وإن شاء الله الحلقة الجاية هنبتدي ناخد أمثلة..." [04:57.0 - 04:58.2]
    scene.play(
        next_card.animate_shell(run_time=1.2),
    )

    # انبثاق سهم المتجه والوصف مع: "...نتعرف أكتر من خلالها على المتجه قبل ما ندخل في شرح القواعد"
    # [04:58.2 - 04:59.4]
    scene.play(
        GrowFromPoint(promise_vector, promise_vector.start),
        FadeIn(vec_label),
        FadeIn(promise_desc, shift=UP * 0.1),
        run_time=1.2,
    )

    # استقرار البطاقة وسماع: "وأشوفكوا الحلقة الجاية بإذن الله..." [04:59.4 - 05:06.0]
    scene.wait(6.6)

    # ==============================================================
    # 3. تفريغ المشهد بالكامل لتسليم الشاشة للأوترو (2.0 ث)
    # يتزامن مع جملة "سلام عليكم" [05:06.0 -> 05:08.0]
    # ==============================================================
    promise_group = VGroup(
        next_card,
        promise_vector,
        vec_label,
        promise_desc,
    )
    all_scene = Group(mathematician, promise_group)

    scene.play(
        FadeOut(all_scene),
        run_time=1.2,
    )
    scene.wait(0.8)  # سكون تام عند 05:08.0 لتسليم الشاشة لكليب الأوترو