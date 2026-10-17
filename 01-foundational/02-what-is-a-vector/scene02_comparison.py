from manim import *
from common.latex import mach_math_template
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


def play_scene02(scene):

    # ==========================================================
    # 1. TABLE (3 أعمدة بكامل أبعاد الغرفة)
    # ==========================================================
    table = MachTable(
        rows=4,
        cols=3,
        width=12.2,
        height=6.2,
        cell_padding=0.12,
        shimmer=True,
        shimmer_speed=65.0,
        shimmer_radius=0.011,
    )

    # ==========================================================
    # 2. TITLES (الصف 0)
    # ==========================================================
    title_linear = Text(
        "الجبر الخطي",
        font="Cairo",
        font_size=28,
        color=GOLD_LIGHT,
    )

    title_calc = Text(
        "التفاضل والتكامل",
        font="Cairo",
        font_size=28,
        color=COPPER_TERRA,
    )

    title_arith = MarkupText(
        "الحساب",
        font="Cairo",
        font_size=28,
        color=COPPER_TERRA,
    )

    table.place(title_linear, row=0, col=0)
    table.place(title_calc,   row=0, col=1)
    table.place(title_arith,  row=0, col=2)

    # ==========================================================
    # 3. SUBTITLES (الصف 1)
    # ==========================================================
    sub_vectors = MarkupText(
        "متجهات",
        font="Cairo",
        font_size=24,
        color=GOLD_LIGHT,
    )

    sub_funcs = MarkupText(
        "دوال",
        font="Cairo",
        font_size=24,
        color=IVORY_WHITE,
    )

    sub_numbers = MarkupText(
        "أرقام",
        font="Cairo",
        font_size=24,
        color=IVORY_WHITE,
    )

    table.place(sub_vectors, row=1, col=0)
    table.place(sub_funcs,   row=1, col=1)
    table.place(sub_numbers, row=1, col=2)

    # ==========================================================
    # 4. GRAPHS & NUMBER LINE (الصف 2)
    # ==========================================================
    # العمود 0: شبكة محاور + متجه
    vec_axes = MachAxes(
        x_range=[-2, 2, 1],
        y_range=[-2, 2, 1],
        x_length=1.9,
        y_length=1.9,
        font_size=8,
    )
    vec_arrow = Arrow(
        start=vec_axes.c2p(0, 0),
        end=vec_axes.c2p(1.3, 1.3),
        color=GOLD_LIGHT,
        buff=0,
        stroke_width=3.6,
        max_tip_length_to_length_ratio=0.28,
    )
    mini_vector_graph = VGroup(vec_axes, vec_arrow)
    table.fit(mini_vector_graph, row=2, col=0, padding=0.08)

    # العمود 1: رسمة التفاضل
    mini_axes = MachAxes(
        x_range=[-3, 3, 1],
        y_range=[-3, 3, 1],
        x_length=1.9,
        y_length=1.9,
        font_size=8,
    )
    mini_curve = mini_axes.plot(
        lambda x: 0.35 * x**2 - 1,
        x_range=[-2.4, 2.4],
        color=COPPER_TERRA,
        stroke_width=2.2,
    )
    mini_graph = VGroup(mini_axes, mini_curve)
    table.fit(mini_graph, row=2, col=1, padding=0.08)

    # العمود 2: خط الأعداد
    num_line = MachNumberLine(
        length=2.8,
        font_size=13,
    )
    table.fit(num_line, row=2, col=2, padding=0.18)

    # ==========================================================
    # 5. OPERATIONS & QUESTION BADGE (الصف 3)
    # ==========================================================
    circle_glow = Circle(
        radius=0.48,
        color=GOLD_LIGHT,
        stroke_width=6,
        stroke_opacity=0.35,
    )
    circle_inner = Circle(
        radius=0.40,
        color=GOLD_LIGHT,
        stroke_width=2.5,
    )
    q_mark = MathTex(
        r"?",
        tex_template=mach_math_template,
        font_size=42,
        color=GOLD_LIGHT,
    )
    q_mark.move_to(circle_inner.get_center())
    question_badge = VGroup(circle_glow, circle_inner, q_mark)

    table.fit(question_badge, row=3, col=0, padding=0.15)

    calculus_ops = MathTex(
        r"\frac{df(x)}{dx}" r"\qquad" r"\int f(x)\,dx",
        tex_template=mach_math_template,
        font_size=25,
        color=COPPER_TERRA,
    )
    table.fit(calculus_ops, row=3, col=1, padding=0.15)

    arithmetic_ops = MathTex(
        r"+ \quad - \quad \times \quad \div",
        tex_template=mach_math_template,
        font_size=25,
        color=COPPER_TERRA,
    )
    table.fit(arithmetic_ops, row=3, col=2, padding=0.15)

    all_content = Group(
        title_linear, title_calc, title_arith,
        sub_vectors, sub_funcs, sub_numbers,
        mini_vector_graph, mini_graph, num_line,
        question_badge, calculus_ops, arithmetic_ops,
    )

    # ==========================================================
    # 6. التزامن الصوتي المحسوب (إجمالي المشهد: 45.0 ثانية)
    # [00:13.0 -> 00:58.0 في التراك الصوتي]
    # ==========================================================

    # أ) بناء الجدول وظهور محتوياته (3.2 ث)
    # "لو فاكر من الحلقة اللي فاتت إني عرضتلك في الجدول ده..." [00:13.0 - 00:16.2]
    scene.play(
        table.construct(
            run_time=2.0,
            show_shimmer=True,
            center_point=True,
        )
    )
    scene.play(
        FadeIn(all_content),
        run_time=1.2,
    )

    # استكمال الجملة: "...مقارنة بين علم الحساب والتفاضل والتكامل والجبر الخطي" [00:16.2 - 00:21.5]
    scene.wait(5.3)

    # "وقلنا إن كل واحد فيهم بيتعامل مع حاجة معينة..." [00:21.5 - 00:25.5]
    scene.wait(4.0)

    # ب) نبض "الأعداد في علم الحساب" (2.5 ث)
    # "...زي الأعداد في علم الحساب..." [00:25.5 - 00:28.0]
    scene.play(
        sub_numbers.animate.scale(1.2).set_color(GOLD_LIGHT),
        num_line.animate.set_color(GOLD_LIGHT),
        run_time=0.8,
    )
    scene.play(
        sub_numbers.animate.scale(1 / 1.2).set_color(IVORY_WHITE),
        num_line.animate.set_color(WHITE),
        run_time=0.5,
    )
    scene.wait(1.2)

    # ج) نبض "الدوال في علم التفاضل والتكامل" (2.5 ث)
    # "...والدوال في علم التفاضل والتكامل..." [00:28.0 - 00:30.5]
    scene.play(
        sub_funcs.animate.scale(1.2).set_color(GOLD_LIGHT),
        mini_curve.animate.set_color(GOLD_LIGHT),
        run_time=0.8,
    )
    scene.play(
        sub_funcs.animate.scale(1 / 1.2).set_color(IVORY_WHITE),
        mini_curve.animate.set_color(COPPER_TERRA),
        run_time=0.5,
    )
    scene.wait(1.2)

    # د) نبض "المتجهات في الجبر الخطي" (3.0 ث)
    # "...والمتجهات في الجبر الخطي." [00:30.5 - 00:33.5]
    scene.play(
        sub_vectors.animate.scale(1.25),
        vec_arrow.animate.scale(1.15),
        run_time=0.8,
    )
    scene.play(
        sub_vectors.animate.scale(1 / 1.25),
        vec_arrow.animate.scale(1 / 1.15),
        run_time=0.6,
    )
    scene.wait(1.6)

    # هـ) التركيز على علامة الاستفهام وسؤال المتجه (8.0 ث)
    # "فأقدر أستنتج من الجدول إنه لو سألنا إيه هو الشيء ده اللي اسمه المتجه واللي بيتعامل معاه علم الجبر الخطي..."
    # [00:33.5 - 00:41.5]
    scene.play(
        question_badge.animate.scale(1.3),
        title_linear.animate.scale(1.1),
        run_time=1.0,
    )
    scene.play(
        question_badge.animate.scale(1 / 1.3),
        title_linear.animate.scale(1 / 1.1),
        run_time=0.8,
    )
    scene.wait(6.2)

    # و) وميض عمود الحساب (5.0 ث)
    # "...كأني بسأل بالظبط إيه هو مفهوم العدد في علم الحساب؟..." [00:41.5 - 00:46.5]
    scene.play(
        title_arith.animate.set_color(GOLD_LIGHT).scale(1.12),
        sub_numbers.animate.set_color(GOLD_LIGHT),
        run_time=0.8,
    )
    scene.play(
        title_arith.animate.set_color(COPPER_TERRA).scale(1 / 1.12),
        sub_numbers.animate.set_color(IVORY_WHITE),
        run_time=0.6,
    )
    scene.wait(3.6)

    # ز) وميض عمود التفاضل والتكامل (6.0 ث)
    # "...أو كأني بسأل إيه هو الشيء ده اللي اسمه دالة واللي إحنا بنتعامل معاها في التفاضل والتكامل؟!!"
    # [00:46.5 - 00:52.5]
    scene.play(
        title_calc.animate.set_color(GOLD_LIGHT).scale(1.12),
        sub_funcs.animate.set_color(GOLD_LIGHT),
        run_time=0.8,
    )
    scene.play(
        title_calc.animate.set_color(COPPER_TERRA).scale(1 / 1.12),
        sub_funcs.animate.set_color(IVORY_WHITE),
        run_time=0.6,
    )
    scene.wait(4.6)

    # ح) هزة الأسئلة الثلاثة والتفريغ (5.5 ث)
    # "وبصراحة الـ 3 أسئلة أصعب من بعض وإجابتهم مش سهلة إطلاقاً." [00:52.5 - 00:58.0]
    scene.play(
        Wiggle(question_badge, scale_value=1.15),
        Wiggle(title_calc, scale_value=1.1),
        Wiggle(title_arith, scale_value=1.1),
        run_time=2.0,
    )
    scene.wait(1.5)

    # تفريغ المشهد للانتقال للمشهد الثالث
    table.stop_shimmer()
    scene.play(
        FadeOut(table),
        FadeOut(all_content),
        run_time=1.2,
    )
    scene.wait(0.8)  # سكون للانتقال النظيف عند 00:58.0