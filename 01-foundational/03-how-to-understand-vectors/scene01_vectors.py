from manim import *
import numpy as np

from common.palette import (
    GOLD_LIGHT,
    GOLD_DARK,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.latex import mach_math_template
from common.mobjects.card import MachCard
from common.mobjects.vector_space import MachVectorSpace

# ==============================================================
# المشهد الأول (المدة المضبوطة: 29.5 ثانية من 00:00 إلى 00:29.5)
# ==============================================================

def play_scene01(scene):

    X_RIGHT = 3.55
    X_CENTER_LEFT = -3.55

    # ==========================================================
    # 1. الخط الفاصل الرأسي في منتصف الشاشة
    # ==========================================================

    center_split_line = Line(
        [0.0, -3.9, 0],
        [0.0, 3.9, 0],
        color=GOLD_LIGHT,
        stroke_width=1.8,
        stroke_opacity=0.65,
    ).set_z_index(25)

    # ==========================================================
    # 2. أبعاد البطاقة
    # ==========================================================

    card_w = 5.9
    card_h = 4.5
    card_center = np.array([X_RIGHT, 0.0, 0.0])

    # ==========================================================
    # 3. العمود الأيمن: قواعد الجمع (Right-to-Left)
    # ==========================================================

    title_add = MarkupText(
        "1. الجمع",
        font="Cairo",
        font_size=15,
        color=COPPER_TERRA,
    )

    add_axioms = VGroup(
        # الانغلاق تحت الجمع
        MathTex(
            r"\mathbf{u}+\mathbf{v}\in V",
            tex_template=mach_math_template,
            font_size=19,
            color=IVORY_WHITE,
        ),
        # خاصية الإبدال
        MathTex(
            r"\mathbf{u}+\mathbf{v}=\mathbf{v}+\mathbf{u}",
            tex_template=mach_math_template,
            font_size=19,
            color=IVORY_WHITE,
        ),
        # خاصية التجميع
        MathTex(
            r"(\mathbf{u}+\mathbf{v})+\mathbf{w}=\mathbf{u}+(\mathbf{v}+\mathbf{w})",
            tex_template=mach_math_template,
            font_size=16,
            color=IVORY_WHITE,
        ),
        # العنصر المحايد الجمعي
        MathTex(
            r"\mathbf{u}+\mathbf{0}=\mathbf{u}",
            tex_template=mach_math_template,
            font_size=19,
            color=IVORY_WHITE,
        ),
        # المعكوس الجمعي
        MathTex(
            r"\mathbf{u}+(-\mathbf{u})=\mathbf{0}",
            tex_template=mach_math_template,
            font_size=19,
            color=IVORY_WHITE,
        ),
    ).arrange(DOWN, buff=0.20, aligned_edge=LEFT)

    col_add = VGroup(title_add, add_axioms).arrange(DOWN, buff=0.18)

    # ==========================================================
    # 4. العمود الأيسر: قواعد الضرب القياسي
    # ==========================================================

    title_scale = MarkupText(
        "2. الضرب القياسي",
        font="Cairo",
        font_size=15,
        color=COPPER_TERRA,
    )

    scale_axioms = VGroup(
        # الانغلاق تحت الضرب القياسي
        MathTex(
            r"c\mathbf{u}\in V",
            tex_template=mach_math_template,
            font_size=19,
            color=IVORY_WHITE,
        ),
        # التوزيع على جمع المتجهات
        MathTex(
            r"c(\mathbf{u}+\mathbf{v})=c\mathbf{u}+c\mathbf{v}",
            tex_template=mach_math_template,
            font_size=17,
            color=IVORY_WHITE,
        ),
        # التوزيع على جمع الأعداد القياسية
        MathTex(
            r"(c+d)\mathbf{u}=c\mathbf{u}+d\mathbf{u}",
            tex_template=mach_math_template,
            font_size=17,
            color=IVORY_WHITE,
        ),
        # التوافق مع ضرب الأعداد القياسية
        MathTex(
            r"c(d\mathbf{u})=(cd)\mathbf{u}",
            tex_template=mach_math_template,
            font_size=18,
            color=IVORY_WHITE,
        ),
        # عنصر الوحدة في الضرب القياسي
        MathTex(
            r"1\mathbf{u}=\mathbf{u}",
            tex_template=mach_math_template,
            font_size=19,
            color=IVORY_WHITE,
        ),
    ).arrange(DOWN, buff=0.20, aligned_edge=LEFT)

    col_scale = VGroup(title_scale, scale_axioms).arrange(DOWN, buff=0.18)

    # ==========================================================
    # 5. الفاصل المنقط وتجميع محتوى البطاقة بنظام مرن
    # ==========================================================

    col_sep = DashedLine(
        UP * 1.3,
        DOWN * 1.3,
        dash_length=0.08,
        dashed_ratio=0.5,
        stroke_width=1.0,
        color=GOLD_DARK,
        stroke_opacity=0.45,
    )

    board_content = VGroup(col_scale, col_sep, col_add).arrange(RIGHT, buff=0.35)

    # ==========================================================
    # 6. بناء البطاقة عبر MachCard النظيفة
    # ==========================================================

    right_board = MachCard(
        width=card_w,
        height=card_h,
        center=card_center,
        title="قواعد فضاء المتجهات",
        title_font_size=19,
        title_buff=0.18,
        corner_radius=0.26,
        content=board_content,
        auto_fit_content=True,
    )

    # ==========================================================
    # 7. فضاء المتجهات في النصف الأيسر
    # ==========================================================

    # العرض 7.1 (مش 7.2) علشان الحافة اليمنى للفضاء تقع بالظبط على الخط الفاصل x=0:
    # الحافة اليمنى = X_CENTER_LEFT + width/2 = -3.55 + 3.55 = 0
    left_vs_group = MachVectorSpace(
        center=(X_CENTER_LEFT, 0, 0),
        width=2 * abs(X_CENTER_LEFT),
        height=7.8,
        grid_step=0.55,
        vectors=None,
        title="فضاء المتجهات (Vector Space)",
    )

    # ==========================================================
    # 8. التحريك والتزامن (29.5 ثانية بالضبط)
    # ==========================================================

    # [00:00.0 - 00:02.0] (2.0s): "السلام عليكم" + ظهور الخط الفاصل في المنتصف
    scene.play(
        Create(center_split_line),
        run_time=1.5,
    )
    scene.wait(0.5)

    # [00:02.0 - 00:06.5] (4.5s): "...المتجه هو جزء من عالم ... فضاء المتجهات"
    # ظهور فضاء المتجهات يساراً
    scene.play(
        FadeIn(left_vs_group.glow),
        FadeIn(left_vs_group.grid),
        FadeIn(left_vs_group.rotated_grid),
        FadeIn(left_vs_group.sheared_grid),
        FadeIn(left_vs_group.frame_marks),
        Create(left_vs_group.axes),
        FadeIn(left_vs_group.origin),
        FadeIn(
            left_vs_group.title_group,
            shift=DOWN * 0.15,
        ),
        run_time=3.5,
    )
    scene.wait(1.0)

    # إظهار أي متجهات إضافية إن وُجدت
    vector_animations = []
    if left_vs_group.vectors:
        vector_animations.append(
            LaggedStart(
                *[
                    GrowFromPoint(
                        group[0],
                        left_vs_group.center,
                    )
                    for group in left_vs_group.vectors
                    if len(group) > 0
                ],
                lag_ratio=0.15,
            )
        )

        pivot_animations = [
            FadeIn(group[1])
            for group in left_vs_group.vectors
            if len(group) > 1
        ]
        if pivot_animations:
            vector_animations.append(
                LaggedStart(
                    *pivot_animations,
                    lag_ratio=0.15,
                )
            )

    if vector_animations:
        scene.play(
            *vector_animations,
            run_time=1.3,
            rate_func=smooth,
        )

    # [00:06.5 - 00:12.0] (5.5s): "...عالم ليه قواعد وقوانين بتحكمه"
    # بناء بطاقة القواعد الزجاجية يميناً بدقة
    scene.play(
        right_board.construct(
            run_time=4.0,
            show_reflection=True,
            illuminate_glass=True,
            show_content=True,
        )
    )
    scene.wait(1.5)

    # [00:12.0 - 00:22.5] (10.5s): "احنا المفروض في الحلقة دي ابدأ اوريك امثلة توضحلك الصورة الذهنية... قبل ما اشرحلك القواعد"
    # إتاحة الوقت الكافي للمشاهد لقراءة القواعد واستيعاب التقسيم بين الفضاء والقوانين
    scene.wait(10.5)

    # [00:22.5 - 00:27.5] (5.0s): "عشان لو دخلت في الموضوع علي طول مش هتقدر تستوعب المتجه بشكل بديهي كفاية"
    # استقرار المشهد حتى نهاية الجملة
    scene.wait(5.0)

    # [00:27.5 - 00:29.5] (2.0s): تفريغ المشهد بهدوء أثناء السكتة قبل بداية المشهد الثاني
    all_scene = VGroup(
        center_split_line,
        right_board,
        left_vs_group,
    )

    scene.play(
        FadeOut(all_scene),
        run_time=1.5,
    )
    scene.wait(0.5)

    # المجموع: 2.0 + 4.5 + 5.5 + 10.5 + 5.0 + 2.0 = 29.5 ثانية بالمللي!