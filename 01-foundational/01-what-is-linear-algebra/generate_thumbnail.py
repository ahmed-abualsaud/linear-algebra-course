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
from manim import *


class ThumbnailScene(Scene):

    def construct(self):

        # ==========================================================
        # 1. TABLE (بأبعاد 16:9 الكاملة و 3 أعمدة)
        # ==========================================================

        table = MachTable(
            rows=4,
            cols=3,
            width=12.6,
            height=6.7,
            cell_padding=0.12,
            shimmer=False,
        )

        # ==========================================================
        # 2. TITLES (الصف 0)
        # ==========================================================

        # جملتان تشتملان على مسافات تعملان بـ Text بنجاح
        title_linear = Text(
            "الجبر الخطي",
            font="Cairo",
            font_size=30,
            color=GOLD_LIGHT,
        )

        title_calc = Text(
            "التفاضل والتكامل",
            font="Cairo",
            font_size=30,
            color=COPPER_TERRA,
        )

        # كلمة مفردة: يجب أن تكون MarkupText كما في كودك الأصلي
        title_arith = MarkupText(
            "الحساب",
            font="Cairo",
            font_size=30,
            color=COPPER_TERRA,
        )

        table.place(
            title_linear,
            row=0,
            col=0,
        )
        table.place(
            title_calc,
            row=0,
            col=1,
        )
        table.place(
            title_arith,
            row=0,
            col=2,
        )

        # ==========================================================
        # 3. SUBTITLES (الصف 1) - كلها كلمات مفردة لذا تستخدم MarkupText
        # ==========================================================

        sub_vectors = MarkupText(
            "متجهات",
            font="Cairo",
            font_size=25,
            color=IVORY_WHITE,
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
            sub_vectors,
            row=1,
            col=0,
        )
        table.place(
            sub_funcs,
            row=1,
            col=1,
        )
        table.place(
            sub_numbers,
            row=1,
            col=2,
        )

        # ==========================================================
        # 4. GRAPHS & NUMBER LINE (الصف 2)
        # ==========================================================

        # العمود 0: شبكة محاور + متجه ذهبي
        vec_axes = MachAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=2.05,
            y_length=2.05,
            font_size=9,
        )
        vec_arrow = Arrow(
            start=vec_axes.c2p(0, 0),
            end=vec_axes.c2p(1.4, 1.4),
            color=GOLD_LIGHT,
            buff=0,
            stroke_width=4.0,
            max_tip_length_to_length_ratio=0.28,
        )
        mini_vector_graph = VGroup(
            vec_axes,
            vec_arrow,
        )
        table.fit(
            mini_vector_graph,
            row=2,
            col=0,
            padding=0.08,
        )

        # العمود 1: رسمة التفاضل
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
            col=1,
            padding=0.08,
        )

        # العمود 2: خط الأعداد
        num_line = MachNumberLine(
            length=3.0,
            font_size=14,
        )
        table.fit(
            num_line,
            row=2,
            col=2,
            padding=0.18,
        )

        # ==========================================================
        # 5. OPERATIONS & QUESTION MARK (الصف 3)
        # ==========================================================

        # العمود 0: علامة الاستفهام داخل الدائرة (عبر LaTeX لضمان الظهور 100%)
        circle_glow = Circle(
            radius=0.52,
            color=GOLD_LIGHT,
            stroke_width=6,
            stroke_opacity=0.35,
        )
        circle_inner = Circle(
            radius=0.45,
            color=GOLD_LIGHT,
            stroke_width=3.0,
        )
        q_mark = MathTex(
            r"?",
            tex_template=mach_math_template,
            font_size=46,
            color=GOLD_LIGHT,
        )
        q_mark.move_to(circle_inner.get_center())
        question_badge = VGroup(
            circle_glow,
            circle_inner,
            q_mark,
        )

        table.fit(
            question_badge,
            row=3,
            col=0,
            padding=0.16,
        )

        # العمود 1: عمليات التفاضل
        calculus_ops = MathTex(
            r"\frac{df(x)}{dx}" r"\qquad" r"\int f(x)\,dx",
            tex_template=mach_math_template,
            font_size=27,
            color=GOLD_LIGHT,
        )
        table.fit(
            calculus_ops,
            row=3,
            col=1,
            padding=0.16,
        )

        # العمود 2: عمليات الحساب
        arithmetic_ops = MathTex(
            r"+ \qquad - \qquad \times \qquad \div",
            tex_template=mach_math_template,
            font_size=28,
            color=GOLD_LIGHT,
        )
        table.fit(
            arithmetic_ops,
            row=3,
            col=2,
            padding=0.16,
        )

        # ==========================================================
        # 6. إضافة كل العناصر للفريم المباشر
        # ==========================================================
        self.add(
            table,
            title_linear,
            title_calc,
            title_arith,
            sub_vectors,
            sub_funcs,
            sub_numbers,
            mini_vector_graph,
            mini_graph,
            num_line,
            question_badge,
            calculus_ops,
            arithmetic_ops,
        )
        self.wait(0.1)