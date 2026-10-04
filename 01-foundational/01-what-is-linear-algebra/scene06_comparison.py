from manim import *
from common.mobjects.coordinate_systems import (
    MachAxes,
    MachNumberLine,
)
from common.mobjects.tables import MachTable
from common.palette import (
    COPPER_TERRA,
    GOLD_LIGHT,
    IVORY_WHITE,
)
from common.latex import mach_math_template


def play_scene06(scene):

    # ==========================================================
    # 1. TABLE (بسرعة 65 ثانية الهادئة جداً وانعكاس الأرضية ثلاثي الأبعاد)
    # ==========================================================

    table = MachTable(
        rows=4,
        cols=2,
        width=8.2,
        height=5.8,
        cell_padding=0.12,
        shimmer=True,
        shimmer_speed=65.0,  # سرعة ملكية شديدة الهدوء
        shimmer_radius=0.011,
    )

    # ==========================================================
    # 2. TITLES & SUBTITLES
    # ==========================================================

    title_calc = Text(
        "التفاضل والتكامل",
        font="Cairo",
        font_size=30,
        color=COPPER_TERRA,
    )

    title_arith = MarkupText(
        "الحساب",
        font="Cairo",
        font_size=30,
        color=COPPER_TERRA,
    )

    sub_funcs = MarkupText(
        "دوال",
        font="Cairo",
        font_size=25,
        color=IVORY_WHITE,
    )

    sub_numbers = MarkupText(
        "أرقام",
        font="Cairo",
        font_size=25,
        color=IVORY_WHITE,
    )

    table.place(
        title_calc,
        row=0,
        col=0,
    )
    table.place(
        title_arith,
        row=0,
        col=1,
    )
    table.place(
        sub_funcs,
        row=1,
        col=0,
    )
    table.place(
        sub_numbers,
        row=1,
        col=1,
    )

    # ==========================================================
    # 3. NUMBER LINE & GRAPH
    # ==========================================================

    num_line = MachNumberLine(
        length=3.0,
        font_size=14,
    )
    table.fit(
        num_line,
        row=2,
        col=1,
        padding=0.18,
    )

    mini_axes = MachAxes(
        x_range=[-3, 3, 1],
        y_range=[-3, 3, 1],
        x_length=2.05,
        y_length=2.05,
        font_size=9,
    )
    mini_curve = mini_axes.plot(
        lambda x: 0.35 * x**2 - 1,
        x_range=[-2.4, 2.4],
        color=GOLD_LIGHT,
        stroke_width=2.2,
    )
    mini_graph = VGroup(
        mini_axes,
        mini_curve,
    )
    table.fit(
        mini_graph,
        row=2,
        col=0,
        padding=0.08,
    )

    # ==========================================================
    # 4. OPERATIONS
    # ==========================================================

    arithmetic_ops = MathTex(
        r"+ \qquad - \qquad \times \qquad \div",
        tex_template=mach_math_template,
        font_size=28,
        color=GOLD_LIGHT,
    )

    calculus_ops = MathTex(
        r"\frac{df(x)}{dx}" r"\qquad" r"\int f(x)\,dx",
        tex_template=mach_math_template,
        font_size=27,
        color=GOLD_LIGHT,
    )

    table.fit(
        calculus_ops,
        row=3,
        col=0,
        padding=0.16,
    )
    table.fit(
        arithmetic_ops,
        row=3,
        col=1,
        padding=0.16,
    )

    # ==========================================================
    # 5. التزامن الصوتي المحسوب (يبدأ عند 02:09 وينتهي عند 02:39)
    # ==========================================================

    # أ) بناء الجدول الخارجي ثم اشتعال الزجاج وانعكاس الأرضية (2.5s)
    # يتزامن مع فجوة الصمت التأملية في صوتك
    scene.play(
        table.construct(
            run_time=2.5,
            show_shimmer=True,
            center_point=True,
        )
    )

    # ب) ظهور عناوين العمودين (2.0s)
    # الكلام: "يبقى ملخص اللي أنا قلته هو إن في علم الحساب وعلم التفاضل..."
    scene.play(
        FadeIn(
            title_calc,
            title_arith,
        ),
        run_time=0.8,
    )
    scene.wait(1.2)

    # ج) ظهور موضوع كل علم (3.0s)
    # الكلام: "... عندي حاجة بدرسها اسمها الأرقام، وفي التفاضل حاجة اسمها الدوال..."
    scene.play(
        FadeIn(
            sub_funcs,
            sub_numbers,
        ),
        run_time=0.8,
    )
    scene.wait(2.2)

    # د) ظهور التمثيل البصري (3.5s)
    # الكلام: "... وبنمثلهم بصرياً..."
    scene.play(
        FadeIn(
            mini_graph,
            num_line,
        ),
        run_time=1.0,
    )
    scene.wait(2.5)

    # هـ) ظهور العمليات والقواعد (6.0s)
    # الكلام: "... وبنفذ على الأرقام قواعد زي: جمع وطرح وضرب وقسمة،
    # وعلى الدوال قواعد وعمليات زي: التفاضل والتكامل."
    scene.play(
        FadeIn(
            calculus_ops,
            arithmetic_ops,
        ),
        run_time=1.0,
    )
    scene.wait(5.0)

    # و) اللحظة التأملية الكبرى وطرح فرضية الجبر الخطي (11.0s)
    # الكلام: "هنا ممكن نسأل: بما إن الجبر الخطي هو فرع من فروع الرياضيات...
    # فهل ممكن يكون ليه حاجة بنردسها... وتخضع لمجموعة من القواعد برضو؟"
    scene.wait(11.0)

    # ==========================================================
    # 6. تفريغ المشهد (2.0s)
    # ==========================================================
    table.stop_shimmer()

    scene.play(
        FadeOut(
            Group(
                table,
                title_calc,
                title_arith,
                sub_funcs,
                sub_numbers,
                mini_graph,
                num_line,
                calculus_ops,
                arithmetic_ops,
            )
        ),
        run_time=1.0,
    )

    # استقرار الغرفة قبل المشهد السابع الكبير
    scene.wait(1.0)

    # إجمالي زمن المشهد السادس: 30.0 ثانية بالتمام والكمال!