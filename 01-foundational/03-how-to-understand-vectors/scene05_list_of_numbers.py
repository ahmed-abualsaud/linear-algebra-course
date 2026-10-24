from manim import *
import numpy as np

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_MUTED,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.latex import mach_math_template
from common.mobjects.card import MachCard
from common.classroom import make_kindergarten_classroom


# ==============================================================
# كود المشهد الخامس الكامل (Scene 05) - المدة: 29.5 ثانية (01:49.0 إلى 02:18.5)
# ==============================================================

def play_scene05(scene):

    # ==========================================================
    # A. القائمة الثلاثية الابتدائية (حرة وبدون أي مربع)
    # ==========================================================

    initial_pos = np.array([0.0, 0.35, 0.0])

    hero_3d_math = MathTex(
        r"\mathbf{v} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}",
        tex_template=mach_math_template,
        font_size=46,
        color=IVORY_WHITE,
    )
    hero_3d_math[0][0].set_color(GOLD_BRIGHT)

    hero_3d_tag = MarkupText(
        "قائمة من 3 أرقام",
        font="Cairo",
        font_size=15,
        color=GOLD_MUTED,
    ).next_to(hero_3d_math, UP, buff=0.25)

    hero_3d_group = VGroup(hero_3d_math, hero_3d_tag).move_to(initial_pos)

    # 1. انبثاق القائمة الحرة في قلب الشاشة (10.0s إجمالي)
    # [01:49.0 - 01:59.0]: "دلوقتي تعال اوريك مثال تاني... ممكن اقولك ان المتجه عبارة عن ليست او قائمة من الارقام"
    scene.wait(1.0)
    scene.play(
        GrowFromCenter(hero_3d_group),
        run_time=1.5,
        rate_func=smooth,
    )
    scene.wait(7.5)

    # 2. تحرك القائمة إلى أعلى يمين الشاشة لتفسح المجال لمشهد الفصل (2.0s إجمالي)
    # [01:59.0 - 02:01.0]: "على الرغم ان في المثالين..."
    top_right_pos = np.array([4.6, 2.45, 0.0])
    scene.play(
        hero_3d_group.animate.scale(0.72).move_to(top_right_pos),
        run_time=1.2,
        rate_func=smooth,
    )
    scene.wait(0.8)

    # ==========================================================
    # B. ظهور مشهد الفصل (المعلم والعصا في يده والطلاب) (7.2s إجمالي)
    # ==========================================================

    # [02:01.0 - 02:08.2]: "...بشرحلك بنفس اسلوب مدرس ابتدائي او كي جي اللي بيشرح الارقام والحساب للاطفال"
    classroom_scene = make_kindergarten_classroom().move_to([-0.7, -0.15, 0.0])

    scene.play(
        FadeIn(classroom_scene, shift=UP * 0.25),
        run_time=1.2,
    )
    scene.wait(6.0)

    # ==========================================================
    # C. اختفاء مشهد الفصل وعودة التركيز (1.0s إجمالي)
    # ==========================================================

    # [02:08.2 - 02:09.2]: سكتة قصيرة بعد جملة الأطفال
    scene.play(
        FadeOut(classroom_scene, shift=DOWN * 0.20),
        FadeOut(hero_3d_tag),
        run_time=1.0,
    )

    # ==========================================================
    # D. الانفجار البعدي: الأبعاد الأربعة حرة تماماً ومتراصة بانتظام (7.8s إجمالي)
    # ==========================================================

    title_dim = MarkupText(
        "التمثيل الجبري: كسر حاجز الأبعاد",
        font="Cairo",
        font_size=23,
        color=GOLD_LIGHT,
    ).move_to([0, 3.10, 0])

    y_matrix_center = 0.85
    y_tag_center    = -0.90

    # 1. قائمة بُعد واحد (1D) في أقصى اليمين
    x_1d = 4.30
    vec_1d = MathTex(
        r"\mathbf{v} = [x_1]",
        tex_template=mach_math_template,
        font_size=40,
        color=IVORY_WHITE,
    ).move_to([x_1d, y_matrix_center, 0])
    vec_1d[0][0].set_color(GOLD_BRIGHT)

    tag_1d_t = MarkupText("1D", font="Cairo", font_size=17, color=COPPER_TERRA)
    tag_1d_s = MarkupText("(بُعد واحد)", font="Cairo", font_size=12, color=IVORY_WHITE)
    tag_1d   = VGroup(tag_1d_t, tag_1d_s).arrange(DOWN, buff=0.06).move_to([x_1d, y_tag_center, 0])
    group_1d = VGroup(vec_1d, tag_1d)

    # 2. قائمة بُعدين (2D) في يمين الوسط
    x_2d = 1.60
    vec_2d = MathTex(
        r"\mathbf{v} = \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}",
        tex_template=mach_math_template,
        font_size=40,
        color=IVORY_WHITE,
    ).move_to([x_2d, y_matrix_center, 0])
    vec_2d[0][0].set_color(GOLD_BRIGHT)

    tag_2d_t = MarkupText("2D", font="Cairo", font_size=17, color=GOLD_LIGHT)
    tag_2d_s = MarkupText("(بُعدان)", font="Cairo", font_size=12, color=IVORY_WHITE)
    tag_2d   = VGroup(tag_2d_t, tag_2d_s).arrange(DOWN, buff=0.06).move_to([x_2d, y_tag_center, 0])
    group_2d = VGroup(vec_2d, tag_2d)

    # 3. القائمة الثلاثية (3D) في الوسط
    x_3d = -1.10
    vec_3d = MathTex(
        r"\mathbf{v} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}",
        tex_template=mach_math_template,
        font_size=40,
        color=IVORY_WHITE,
    ).move_to([x_3d, y_matrix_center, 0])
    vec_3d[0][0].set_color(GOLD_BRIGHT)

    tag_3d_t = MarkupText("3D", font="Cairo", font_size=17, color=GOLD_LIGHT)
    tag_3d_s = MarkupText("(3 أبعاد)", font="Cairo", font_size=12, color=IVORY_WHITE)
    tag_3d   = VGroup(tag_3d_t, tag_3d_s).arrange(DOWN, buff=0.06).move_to([x_3d, y_tag_center, 0])
    group_3d = VGroup(vec_3d, tag_3d)

    # 4. القائمة اللانهائية البطلة (nD) في أقصى اليسار
    x_nd = -4.00
    vec_nd = MathTex(
        r"\mathbf{v} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \\ \vdots \\ x_n \end{bmatrix}",
        tex_template=mach_math_template,
        font_size=38,
        color=IVORY_WHITE,
    ).move_to([x_nd, y_matrix_center, 0])
    vec_nd[0][0].set_color(GOLD_BRIGHT)

    tag_nd_t = Text("n-Dimensions", font="DejaVu Sans", font_size=15, color=GOLD_BRIGHT)
    tag_nd_s = MarkupText("(أي عدد من الأبعاد!)", font="Cairo", font_size=12.5, color=GOLD_LIGHT)
    tag_nd   = VGroup(tag_nd_t, tag_nd_s).arrange(DOWN, buff=0.06).move_to([x_nd, y_tag_center, 0])
    group_nd = VGroup(vec_nd, tag_nd)

    # 5. بطاقة التحرر البعدي السفلية (MachCard)
    banner_text = MarkupText(
        "ميزة قائمة الأرقام: حرية مطلقة من قيود الأبعاد المكانية!",
        font="Cairo",
        font_size=17,
        color=IVORY_WHITE,
    )
    banner_sub = MarkupText(
        "يمكنك وصف 4 أبعاد أو 1000 بُعد بنفس السهولة والوضوح",
        font="Cairo",
        font_size=13,
        color=GOLD_MUTED,
    )
    banner_content = VGroup(banner_text, banner_sub).arrange(DOWN, buff=0.10)

    banner_card = MachCard(
        width=8.8,
        height=1.45,
        center=[0.0, -2.45, 0.0],
        show_divider=False,
        corner_radius=0.18,
        content=banner_content,
        background_opacity=0.90,
        border_opacity=0.55,
    )

    # [02:09.2 - 02:17.0]: "لكن ميزة المثال ده عن المثال الاول بتاع السهم هي انه مش بيربطك بعدد ابعاد معينة"
    # أ) ظهور العنوان العلوي وتحول القائمة 3D
    scene.play(
        FadeIn(title_dim, shift=DOWN * 0.15),
        ReplacementTransform(hero_3d_math, vec_3d),
        FadeIn(tag_3d, shift=UP * 0.10),
        run_time=1.0,
    )

    # ب) انبثاق القائمة 2D ثم 1D
    scene.play(
        FadeIn(group_2d, shift=LEFT * 0.20),
        run_time=0.6,
    )
    scene.play(
        FadeIn(group_1d, shift=LEFT * 0.20),
        run_time=0.6,
    )

    # ج) انبثاق القائمة اللانهائية n-Dimensions في اليسار
    scene.play(
        GrowFromCenter(group_nd),
        run_time=1.2,
        rate_func=smooth,
    )

    # د) بناء بطاقة الملخص السفلية
    scene.play(
        banner_card.construct(
            run_time=1.4,
            show_reflection=True,
            illuminate_glass=True,
            show_content=True,
        ),
        run_time=1.4,
    )

    # مهلة استيعاب الأبعاد المتعددة حتى نهاية الجملة
    scene.wait(3.0)

    # ==========================================================
    # E. تفريغ المشهد (1.5s إجمالي)
    # ==========================================================

    # [02:17.0 - 02:18.5]: سكتة قبل بداية المشهد السادس عند 02:19.0
    all_scene = VGroup(
        title_dim,
        group_1d,
        group_2d,
        group_3d,
        group_nd,
        banner_card,
    )

    scene.play(
        FadeOut(all_scene),
        run_time=1.0,
    )
    scene.wait(0.5)

    # المجموع: 10.0 + 2.0 + 7.2 + 1.0 + 7.8 + 1.5 = 29.5 ثانية بالتمام والكمال!