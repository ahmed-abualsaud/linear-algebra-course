from manim import *
from common.mobjects.tables import MachTable
from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_DARK,
    COPPER_TERRA,
    BRONZE,
    IVORY_WHITE,
    STONE_DASH,
)
from common.latex import mach_math_template


def play_scene07(scene):

    # ==============================================================
    # 1. TABLE (بالفواصل الذهبية المتقطعة المتناسقة مع الهوية)
    # ==============================================================

    table = MachTable(
        rows=4,
        cols=3,
        width=10.4,
        height=4.8,
        # LEFT = rules, CENTER = subject, RIGHT = science
        col_widths=[4.1, 3.2, 3.1],
        cell_padding=0.12,
        border_color=GOLD_LIGHT,
        border_width=1.4,
        border_opacity=0.45,
        fill_color="#100D07",
        fill_opacity=0.82,
        glass_color=GOLD_LIGHT,
        glass_opacity=0.035,
        glass_border_opacity=0.12,
        separator_color=GOLD_DARK,  # خطوط متقطعة ذهبية فخمة
        separator_width=0.9,
        separator_opacity=0.38,
        shimmer=True,
        shimmer_speed=12.0,
        shimmer_radius=0.010,
    )

    # ==============================================================
    # 2. FONTS (مطابق للأصل 100%)
    # ==============================================================

    font_title = {
        "font": "Cairo",
        "font_size": 24,
    }

    font_cell = {
        "font": "Cairo",
        "font_size": 22,
    }

    # ==============================================================
    # 3. HEADERS
    # ==============================================================

    c1_h = MarkupText(
        "العلم",
        **font_title,
        color=IVORY_WHITE,
    )
    c2_h = MarkupText(
        "إيه اللي بيدرسه؟",
        **font_title,
        color=BRONZE,
    )
    c3_h = MarkupText(
        "إيه القواعد اللي بتطبّق عليه؟",
        **font_title,
        color=BRONZE,
    )

    # ==============================================================
    # 4. ARITHMETIC
    # ==============================================================

    r1_c1 = MarkupText(
        "الحساب",
        **font_cell,
        color=COPPER_TERRA,
    )
    r1_c2 = MarkupText(
        "الأرقام",
        **font_cell,
        color=GOLD_LIGHT,
    )
    r1_c3 = MarkupText(
        "جمع  -  طرح  -  ضرب  -  قسمة",
        **font_cell,
        color=IVORY_WHITE,
    )

    # ==============================================================
    # 5. CALCULUS
    # ==============================================================

    r2_c1 = MarkupText(
        "التفاضل والتكامل",
        **font_cell,
        color=COPPER_TERRA,
    )
    r2_c2 = MarkupText(
        "الدوال",
        **font_cell,
        color=GOLD_LIGHT,
    )
    r2_c3 = MarkupText(
        "التفاضل  ،  التكامل",
        **font_cell,
        color=IVORY_WHITE,
    )

    # ==============================================================
    # 6. LINEAR ALGEBRA
    # ==============================================================

    r3_c1 = MarkupText(
        "الجبر الخطي",
        **font_cell,
        color=COPPER_TERRA,
    )
    r3_c2 = MarkupText(
        "المتجه",
        **font_cell,
        color=GOLD_LIGHT,
    )
    r3_c3 = MathTex(
        "?",
        tex_template=mach_math_template,
        font_size=56,
        color=IVORY_WHITE,
    )

    # ==============================================================
    # 7. PLACE CONTENT (مطابق للأصل 100%)
    # ==============================================================

    # Header
    table.place(
        c1_h,
        row=0,
        col=2,
    )
    table.place(
        c2_h,
        row=0,
        col=1,
    )
    table.fit(
        c3_h,
        row=0,
        col=0,
        padding=0.12,
    )

    # Arithmetic
    table.place(
        r1_c1,
        row=1,
        col=2,
    )
    table.place(
        r1_c2,
        row=1,
        col=1,
    )
    table.fit(
        r1_c3,
        row=1,
        col=0,
        padding=0.12,
    )

    # Calculus
    table.place(
        r2_c1,
        row=2,
        col=2,
    )
    table.place(
        r2_c2,
        row=2,
        col=1,
    )
    table.place(
        r2_c3,
        row=2,
        col=0,
    )

    # Linear Algebra
    table.place(
        r3_c1,
        row=3,
        col=2,
    )
    table.place(
        r3_c2,
        row=3,
        col=1,
    )
    table.place(
        r3_c3,
        row=3,
        col=0,
    )

    # ==============================================================
    # 8. ROW GROUPS
    # ==============================================================

    header_row = VGroup(
        c1_h,
        c2_h,
        c3_h,
    )
    row_arith = VGroup(
        r1_c1,
        r1_c2,
        r1_c3,
    )
    row_calc = VGroup(
        r2_c1,
        r2_c2,
        r2_c3,
    )
    row_linear = VGroup(
        r3_c1,
        r3_c2,
    )

    # ==============================================================
    # 9. التزامن الصوتي المحسوب (المجموع: 28.0 ثانية)
    # ==============================================================

    # أ) بناء الجدول الكبير وظهور صف العناوين (4.5s)
    # الكلام: "خليني أجاوبك وأقولك: أيوة..."
    scene.play(
        table.construct(
            run_time=2.2,
            show_shimmer=True,
            center_point=True,
        )
    )
    scene.play(
        FadeIn(
            header_row,
            run_time=0.8,
        )
    )
    scene.wait(1.5)

    # ب) ظهور صف الحساب (2.0s)
    scene.play(
        FadeIn(
            row_arith,
            shift=LEFT * 0.2,
            run_time=0.8,
        )
    )
    scene.wait(1.2)

    # ج) ظهور صف التفاضل والتكامل (3.0s)
    scene.play(
        FadeIn(
            row_calc,
            shift=LEFT * 0.2,
            run_time=0.8,
        )
    )
    scene.wait(2.2)

    # د) إعلان الجبر الخطي والمفاجأة (5.5s)
    # الكلام: "... الجبر الخطي فيه حاجة معينة إحنا بندرسها، والحاجة دي تخضع لمجموعة من القواعد...
    # الحاجة دي اسمها: المتجه..."
    scene.play(
        FadeIn(
            row_linear,
            shift=LEFT * 0.2,
            run_time=1.0,
        )
    )
    scene.wait(4.5)

    # هـ) ظهور علامة الاستفهام الكبرى مع ذروة الموسيقى الملحمية (11.2s)
    # التزامن: تظهر '?' وتنبض بالذهب الساطع مع جملة:
    # "... وطبعاً ليه قواعد خاصة للتعامل معاه."
    # ثم تظل الشاشة ثابتة ومبهرة أثناء خاتمتك:
    # "في الحلقة الجاية إن شاء الله هنبدأ أول خطوة في رحلة تعلم الجبر الخطي...
    # ونحاول نفهم: إيه هو المتجه؟
    # أشوفكوا الحلقة الجاية بإذن الله."
    scene.play(
        FadeIn(
            r3_c3,
            scale=0.4,
        ),
        r3_c3.animate.set_color(GOLD_BRIGHT),
        run_time=1.2,
        rate_func=rate_functions.ease_out_back,
    )
    scene.wait(10.0)

    # ==============================================================
    # 10. تفريغ المشهد والانتقال للأوترو (1.8s)
    # ==============================================================
    table.stop_shimmer()

    scene.play(
        FadeOut(
            table,
            header_row,
            row_arith,
            row_calc,
            row_linear,
            r3_c3,
            scale=0.95,
        ),
        run_time=1.0,
    )

    # استقرار الغرفة قبل بدء انكماش الأوترو ("سلام عليكم")
    scene.wait(0.8)

    # الحسبة الإجمالية للمشهد السابع:
    # 2.2 (بناء الجدول) + 0.8 (العناوين) + 1.5 (وقفة)
    # + 0.8 (صف الحساب) + 1.2 (وقفة)
    # + 0.8 (صف التفاضل) + 2.2 (وقفة)
    # + 1.0 (ظهور الجبر والمتجه) + 4.5 (شرح المتجه)
    # + 1.2 (انبثاق علامة الاستفهام) + 10.0 (الخاتمة والتشويق للحلقة 2)
    # + 1.0 (تفريغ الجدول) + 0.8 (استقرار أخير)
    # = 28.0 ثانية بالتمام والكمال!