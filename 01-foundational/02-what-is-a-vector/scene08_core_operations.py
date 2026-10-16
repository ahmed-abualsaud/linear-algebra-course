from manim import *
import numpy as np
from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_DARK,
    GOLD_MUTED,
    STONE_AXIS,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.mobjects.card import MachCard
from common.latex import mach_math_template
from common.mobjects.vectors import MachVector

# ==============================================================
# كود المشهد الثامن (Scene 08)
# ==============================================================

def play_scene08(scene):

    # ==============================================================
    # 1. المرحلة الأولى: شرط ومعيار الانتماء لفضاء المتجهات
    # ==============================================================
    crit_w, crit_h = 9.8, 3.4
    crit_center_y = 0.1

    # بناء بطاقة المعيار باستخدام MachCard
    crit_card = MachCard(
        width=crit_w,
        height=crit_h,
        center=[0, crit_center_y, 0],
        corner_radius=0.26,
        accent_color=GOLD_LIGHT,
        title="معيار الانتماء لفضاء المتجهات",
        title_font_size=23,
        show_divider=True,
        divider_style="vertical",  # فاصل رأسي يقسم البطاقة لعمودين
        auto_fit_content=False,
    )

    # ---------------- الجانب الأيمن: تنطبق القواعد ----------------
    icon_check = MathTex(r"\checkmark", font_size=36, color=GOLD_LIGHT)
    txt_check_1 = MarkupText("تنطبق القواعد", font="Cairo", font_size=19, color=IVORY_WHITE)
    math_check = MathTex(r"\implies \mathbf{v} \in V", tex_template=mach_math_template, font_size=25, color=GOLD_BRIGHT)
    lbl_check = MarkupText("(متجه)", font="Cairo", font_size=17, color=GOLD_BRIGHT)
    row_check = VGroup(math_check, lbl_check).arrange(LEFT, buff=0.14)
    box_right = VGroup(icon_check, txt_check_1, row_check).arrange(DOWN, buff=0.18).move_to([2.4, crit_center_y - 0.22, 0])

    # ---------------- الجانب الأيسر: لا تنطبق القواعد ----------------
    icon_cross = MathTex(r"\times", font_size=40, color=COPPER_TERRA)
    txt_cross_1 = MarkupText("لا تنطبق القواعد", font="Cairo", font_size=19, color=IVORY_WHITE)
    math_cross = MathTex(r"\implies \mathbf{v} \notin V", tex_template=mach_math_template, font_size=25, color=COPPER_TERRA)
    lbl_cross = MarkupText("(ليس متجهاً)", font="Cairo", font_size=17, color=COPPER_TERRA)
    row_cross = VGroup(math_cross, lbl_cross).arrange(LEFT, buff=0.14)
    box_left = VGroup(icon_cross, txt_cross_1, row_cross).arrange(DOWN, buff=0.16).move_to([-2.4, crit_center_y - 0.22, 0])

    # أ) بناء الإطار والعنوان والفاصل الرأسي
    scene.play(
        Create(crit_card.body),
        FadeIn(crit_card.title_group),
        Create(crit_card.divider),
        run_time=0.9,
    )
    # ب) اشتعال الإضاءة والانعكاس مع ظهور الجانب الأيمن
    scene.play(
        FadeIn(crit_card.reflection),
        FadeIn(crit_card.glass),
        FadeIn(box_right, shift=LEFT * 0.2),
        run_time=0.8,
    )
    scene.wait(1.5)

    # ج) ظهور الجانب الأيسر
    scene.play(
        FadeIn(box_left, shift=RIGHT * 0.2),
        run_time=0.8,
    )
    scene.wait(2.5)

    # د) تفريغ لوحة المعيار بالكامل
    scene.play(
        FadeOut(VGroup(crit_card, box_right, box_left)),
        run_time=0.8,
    )
    scene.wait(0.3)

    # ==============================================================
    # 2. المرحلة الثانية: اختزال القواعد (الجمع والضرب في ثابت) بصرياً
    # ==============================================================
    card_op_w, card_op_h = 5.8, 5.5
    X_OP_RIGHT = 3.1
    X_OP_LEFT  = -3.1

    # ---------------- 1. بطاقة جمع المتجهات (يمين) ----------------
    card_add = MachCard(
        width=card_op_w,
        height=card_op_h,
        center=[X_OP_RIGHT, 0, 0],
        corner_radius=0.28,
        accent_color=GOLD_LIGHT,
        title="1. جمع المتجهات",
        title_font_size=23,
        subtitle="Vector Addition",
        subtitle_font_size=14,
        subtitle_color=STONE_AXIS,
        show_divider=False,
        auto_fit_content=False,
    )

    math_op_add = MathTex(
        r"\mathbf{u} + \mathbf{v}",
        tex_template=mach_math_template,
        font_size=34,
        color=GOLD_BRIGHT,
    ).next_to(card_add.title_group, DOWN, buff=0.20)

    desc_add = MathTex(
        r"\mathbf{u}, \mathbf{v} \in V \implies (\mathbf{u} + \mathbf{v}) \in V",
        tex_template=mach_math_template,
        font_size=21,
        color=IVORY_WHITE,
    ).next_to(card_add.body.get_bottom(), UP, buff=0.35)

    O_add = np.array([X_OP_RIGHT - 1.05, -0.75, 0])
    P_u   = O_add + np.array([1.25, 0.35, 0])
    P_v   = P_u + np.array([0.55, 1.15, 0])

    vec_u = MachVector(start=O_add, end=P_u, color=GOLD_LIGHT, stroke_width=3.2, tip_length=0.18, show_pivot=True, pivot_radius=0.04)
    lbl_u = MathTex(r"\mathbf{u}", tex_template=mach_math_template, font_size=20, color=GOLD_LIGHT)\
        .next_to(vec_u.line.get_center(), DOWN, buff=0.10)

    vec_v = MachVector(start=P_u, end=P_v, color=COPPER_TERRA, stroke_width=3.0, tip_length=0.18, show_pivot=True, pivot_radius=0.04)
    lbl_v = MathTex(r"\mathbf{v}", tex_template=mach_math_template, font_size=20, color=COPPER_TERRA)\
        .next_to(vec_v.line.get_center(), RIGHT, buff=0.12)

    vec_sum = MachVector(start=O_add, end=P_v, color=GOLD_BRIGHT, stroke_width=3.6, tip_length=0.22, show_pivot=True, pivot_radius=0.048)
    lbl_sum = MathTex(r"\mathbf{u} + \mathbf{v}", tex_template=mach_math_template, font_size=21, color=GOLD_BRIGHT)\
        .next_to(vec_sum.line.get_center(), UL, buff=0.08)

    add_geo_group = VGroup(vec_u, lbl_u, vec_v, lbl_v, vec_sum, lbl_sum)

    # ---------------- 2. بطاقة الضرب القياسي (يسار) ----------------
    card_scalar = MachCard(
        width=card_op_w,
        height=card_op_h,
        center=[X_OP_LEFT, 0, 0],
        corner_radius=0.28,
        accent_color=COPPER_TERRA,
        title="2. الضرب في رقم (قياسي)",
        title_color=COPPER_TERRA,
        title_font_size=23,
        subtitle="Scalar Multiplication",
        subtitle_font_size=14,
        subtitle_color=STONE_AXIS,
        show_divider=False,
        auto_fit_content=False,
    )

    math_op_scalar = MathTex(
        r"c \cdot \mathbf{v}",
        tex_template=mach_math_template,
        font_size=34,
        color=COPPER_TERRA,
    ).next_to(card_scalar.title_group, DOWN, buff=0.20)

    desc_scalar = MathTex(
        r"c \in \mathbb{R}, \; \mathbf{v} \in V \implies c\mathbf{v} \in V",
        tex_template=mach_math_template,
        font_size=21,
        color=IVORY_WHITE,
    ).next_to(card_scalar.body.get_bottom(), UP, buff=0.35)

    O_scale  = np.array([X_OP_LEFT - 1.05, -0.65, 0])
    P_orig   = O_scale + np.array([0.85, 0.50, 0])
    P_scaled = O_scale + np.array([1.95, 1.15, 0])

    vec_scaled = MachVector(start=O_scale, end=P_scaled, color=COPPER_TERRA, stroke_width=3.6, tip_length=0.22, show_pivot=False)
    vec_scaled.set_z_index(5)
    lbl_scaled = MathTex(r"c\mathbf{v}\; (c > 1)", tex_template=mach_math_template, font_size=21, color=COPPER_TERRA)\
        .next_to(vec_scaled.tip, UR, buff=0.10).set_z_index(6)

    vec_orig = MachVector(start=O_scale, end=P_orig, color=STONE_AXIS, stroke_width=3.6, tip_length=0.18, show_pivot=True, pivot_radius=0.045)
    vec_orig.set_z_index(15)
    lbl_orig = MathTex(r"\mathbf{v}", tex_template=mach_math_template, font_size=20, color=STONE_AXIS)\
        .next_to(vec_orig.line.get_center(), UL, buff=0.10).set_z_index(16)

    scale_geo_group = VGroup(vec_scaled, lbl_scaled, vec_orig, lbl_orig)

    # بناء إطارات البطاقتين والعناوين أولاً
    scene.play(
        Create(card_add.body),
        Create(card_scalar.body),
        FadeIn(card_add.title_group),
        FadeIn(card_scalar.title_group),
        run_time=1.0,
    )

    # اشتعال التوهج والزجاج بالتوازي مع ظهور العبارات الرياضية
    scene.play(
        FadeIn(card_add.reflection),
        FadeIn(card_add.glass),
        FadeIn(card_scalar.reflection),
        FadeIn(card_scalar.glass),
        FadeIn(math_op_add),
        FadeIn(math_op_scalar),
        run_time=0.55,
        rate_func=smooth,
    )

    # رسم المتجهات خطوة بخطوة بالترتيب الهندسي الدقيق
    scene.play(
        GrowFromPoint(vec_u, O_add),
        FadeIn(lbl_u),
        GrowFromPoint(vec_orig, O_scale),
        FadeIn(lbl_orig),
        run_time=0.9,
    )

    scene.play(
        GrowFromPoint(vec_v, P_u),
        FadeIn(lbl_v),
        GrowFromPoint(vec_scaled, O_scale),
        FadeIn(lbl_scaled),
        run_time=1.0,
    )

    scene.play(
        GrowFromPoint(vec_sum, O_add),
        FadeIn(lbl_sum),
        FadeIn(desc_add, shift=UP * 0.1),
        FadeIn(desc_scalar, shift=UP * 0.1),
        run_time=1.1,
    )

    scene.wait(4.5)

    # ==============================================================
    # 3. تفريغ المشهد للانتقال للمشهد التاسع
    # ==============================================================
    all_scene = Group(
        card_add, math_op_add, desc_add, add_geo_group,
        card_scalar, math_op_scalar, desc_scalar, scale_geo_group
    )

    scene.play(
        FadeOut(all_scene),
        run_time=0.9,
    )
    scene.wait(0.5)