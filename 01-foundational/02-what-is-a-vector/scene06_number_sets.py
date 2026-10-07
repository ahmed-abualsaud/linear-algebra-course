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
from common.mobjects.coordinate_systems import MachAxes, MachNumberLine
from common.latex import mach_math_template


def play_scene06(scene):

    # ==============================================================
    # 1. المركز الهندسي العام للدوائر في اليمين
    # ==============================================================
    CENTER_RIGHT = np.array([3.35, 0.45, 0])
    CENTER_LEFT_X = -3.15  # خط المنتصف لجميع العناصر الهندسية في اليسار

    # ----------------- أ) مجموعة الأعداد المركبة C (الكبرى في الخلفية) -----------------
    r_complex = 2.40
    circle_c = Circle(
        radius=r_complex,
        stroke_width=1.6,
        color=STONE_AXIS,
        stroke_opacity=0.85,
        fill_color="#100D08",
        fill_opacity=0.45,
    ).move_to(CENTER_RIGHT).set_z_index(1)

    badge_c = VGroup(
        MathTex(r"\mathbb{C}", tex_template=mach_math_template, font_size=28, color=IVORY_WHITE),
        MarkupText("الأعداد المركبة", font="Cairo", font_size=17, color=IVORY_WHITE),
    ).arrange(RIGHT, buff=0.15).move_to(CENTER_RIGHT + UP * 2.05).set_z_index(5)

    sample_c = VGroup(
        MathTex(r"i", tex_template=mach_math_template, font_size=25, color=STONE_AXIS)\
            .move_to(CENTER_RIGHT + np.array([-1.75, 0.95, 0])),
        MathTex(r"2 + 3i", tex_template=mach_math_template, font_size=24, color=STONE_AXIS)\
            .move_to(CENTER_RIGHT + np.array([1.78, 0.95, 0])),
    ).set_z_index(5)

    group_c = VGroup(circle_c, badge_c, sample_c)

    # ----------------- ب) مجموعة الأعداد الحقيقية R (الوسطى) -----------------
    r_real = 1.65
    circle_r = Circle(
        radius=r_real,
        stroke_width=2.0,
        color=GOLD_LIGHT,
        stroke_opacity=0.95,
        fill_color="#16110A",
        fill_opacity=0.70,
    ).move_to(CENTER_RIGHT + DOWN * 0.18).set_z_index(2)

    badge_r = VGroup(
        MathTex(r"\mathbb{R}", tex_template=mach_math_template, font_size=26, color=GOLD_LIGHT),
        MarkupText("الأعداد الحقيقية", font="Cairo", font_size=16, color=GOLD_LIGHT),
    ).arrange(RIGHT, buff=0.14).move_to(circle_r.get_center() + UP * 1.05).set_z_index(5)

    sample_r = VGroup(
        MathTex(r"3.5", tex_template=mach_math_template, font_size=23, color=GOLD_LIGHT)\
            .move_to(circle_r.get_center() + np.array([-1.18, 0.15, 0])),
        MathTex(r"\pi", tex_template=mach_math_template, font_size=25, color=GOLD_LIGHT)\
            .move_to(circle_r.get_center() + np.array([1.18, 0.15, 0])),
        MathTex(r"\sqrt{2}", tex_template=mach_math_template, font_size=23, color=GOLD_LIGHT)\
            .move_to(circle_r.get_center() + np.array([1.08, -0.75, 0])),
    ).set_z_index(5)

    group_r = VGroup(circle_r, badge_r, sample_r)

    # ----------------- ج) مجموعة الأعداد الصحيحة Z (الصغرى) -----------------
    r_int = 0.95
    circle_z = Circle(
        radius=r_int,
        stroke_width=2.2,
        color=COPPER_TERRA,
        stroke_opacity=1.0,
        fill_color="#24180C",
        fill_opacity=0.92,
    ).move_to(CENTER_RIGHT + DOWN * 0.50).set_z_index(3)

    badge_z = VGroup(
        MathTex(r"\mathbb{Z}", tex_template=mach_math_template, font_size=24, color=COPPER_TERRA),
        MarkupText("الأعداد الصحيحة", font="Cairo", font_size=13, color=COPPER_TERRA),
    ).arrange(RIGHT, buff=0.12).move_to(circle_z.get_center() + UP * 0.45).set_z_index(5)

    sample_z = VGroup(
        MathTex(r"0", tex_template=mach_math_template, font_size=21, color=IVORY_WHITE)\
            .move_to(circle_z.get_center() + np.array([-0.35, -0.02, 0])),
        MathTex(r"1", tex_template=mach_math_template, font_size=21, color=IVORY_WHITE)\
            .move_to(circle_z.get_center() + np.array([0.35, -0.02, 0])),
        MathTex(r"3", tex_template=mach_math_template, font_size=21, color=IVORY_WHITE)\
            .move_to(circle_z.get_center() + np.array([-0.35, -0.42, 0])),
        MathTex(r"-10", tex_template=mach_math_template, font_size=20, color=IVORY_WHITE)\
            .move_to(circle_z.get_center() + np.array([0.35, -0.42, 0])),
    ).set_z_index(5)

    group_z = VGroup(circle_z, badge_z, sample_z)

    # ==============================================================
    # 2. الكائنات الهندسية في النصف الأيسر من الشاشة
    # ==============================================================

    # ----------------- 1. الأعداد الصحيحة Z (في الجزء العلوي Y = 2.30) -----------------
    y_integers = 2.30
    discrete_line = DashedLine(
        start=[CENTER_LEFT_X - 2.5, y_integers, 0],
        end=[CENTER_LEFT_X + 2.5, y_integers, 0],
        dash_length=0.08,
        dashed_ratio=0.5,
        color=COPPER_TERRA,
        stroke_width=1.2,
        stroke_opacity=0.45,
    )

    arrow_int_r = Arrow(
        [CENTER_LEFT_X + 2.35, y_integers, 0], [CENTER_LEFT_X + 2.8, y_integers, 0],
        buff=0, color=COPPER_TERRA, stroke_width=2.0, max_tip_length_to_length_ratio=0.45
    )
    arrow_int_l = Arrow(
        [CENTER_LEFT_X - 2.35, y_integers, 0], [CENTER_LEFT_X - 2.8, y_integers, 0],
        buff=0, color=COPPER_TERRA, stroke_width=2.0, max_tip_length_to_length_ratio=0.45
    )

    int_dots_group = VGroup()
    int_labels_group = VGroup()
    int_values = [-3, -2, -1, 0, 1, 2, 3]

    for val in int_values:
        x_pos = CENTER_LEFT_X + val * 0.70
        dot = Dot([x_pos, y_integers, 0], radius=0.052, color=COPPER_TERRA)
        lbl = MathTex(str(val), tex_template=mach_math_template, font_size=17, color=IVORY_WHITE)\
            .next_to(dot, DOWN, buff=0.12)
        int_dots_group.add(dot)
        int_labels_group.add(lbl)

    group_integers_geom = VGroup(discrete_line, arrow_int_l, arrow_int_r, int_dots_group, int_labels_group)

    # ----------------- 2. خط الأعداد الحقيقية R (في المنتصف Y = 0.40) -----------------
    y_real = 0.40
    real_line = MachNumberLine(
        length=5.6,
        color=GOLD_LIGHT,
        stroke_width=1.8,
        font_size=18,
    ).move_to([CENTER_LEFT_X, y_real, 0])

    # ----------------- 3. شبكة الأعداد المركبة C (في الأسفل Y = -1.95) بستايل MachAxes الرسمي -----------------
    y_complex = -1.95
    complex_axes = MachAxes(
        x_range=[-2, 2, 1],
        y_range=[-2, 2, 1],
        x_length=2.5,
        y_length=2.5,
        font_size=12,
        color=STONE_AXIS,
        stroke_width=1.4,
    ).move_to([CENTER_LEFT_X, y_complex, 0])

    label_re = MathTex(r"\text{Re}", tex_template=mach_math_template, font_size=18, color=STONE_AXIS)\
        .next_to(complex_axes.x_axis.get_right(), UR, buff=0.06)
    label_im = MathTex(r"\text{Im}", tex_template=mach_math_template, font_size=18, color=STONE_AXIS)\
        .next_to(complex_axes.y_axis.get_top(), UR, buff=0.06)

    group_complex_geom = VGroup(complex_axes, label_re, label_im)

    # ==============================================================
    # 3. شريط القواعد والقوانين الصارمة (ترتيب عربي: النص يميناً والعمليات يساراً)
    # ==============================================================
    rules_card = RoundedRectangle(
        corner_radius=0.18,
        width=5.6,
        height=0.95,
        stroke_width=1.4,
        color=GOLD_LIGHT,
        fill_color="#18140E",
        fill_opacity=0.92,
    ).move_to([CENTER_RIGHT[0], -2.65, 0])

    rules_label = MarkupText("قوانين وقواعد صارمة:", font="Cairo", font_size=18, color=GOLD_LIGHT)
    rules_ops = MathTex(
        r"+ \quad - \quad \times \quad \div",
        tex_template=mach_math_template,
        font_size=32,
        color=GOLD_BRIGHT,
    )
    
    # الترتيب بـ LEFT يجعل النص العربي على اليمين والعمليات الحسابية على يساره
    rules_content = VGroup(rules_label, rules_ops).arrange(LEFT, buff=0.35).move_to(rules_card.get_center())
    rules_group = VGroup(rules_card, rules_content)

    # ==============================================================
    # 4. التزامن الصوتي المحسوب للمشهد السادس
    # ==============================================================

    # أ) ظهور مجموعة الأعداد الحقيقية R يميناً + خط الأعداد الحقيقية يساراً
    scene.play(
        Create(circle_r),
        FadeIn(badge_r),
        FadeIn(sample_r),
        Create(real_line),
        run_time=1.4,
    )
    scene.wait(1.5)

    # ب) ظهور مجموعة الأعداد الصحيحة Z يميناً + نقاط الأعداد الصحيحة والسهمين يساراً
    scene.play(
        Create(circle_z),
        FadeIn(badge_z),
        FadeIn(sample_z),
        FadeIn(group_integers_geom, shift=DOWN * 0.15),
        run_time=1.2,
    )
    scene.wait(1.6)

    # ج) ظهور مجموعة الأعداد المركبة C يميناً + شبكة الأعداد المركبة الرسمية يساراً
    scene.play(
        Create(circle_c),
        FadeIn(badge_c),
        FadeIn(sample_c),
        FadeIn(group_complex_geom, scale=0.92),
        run_time=1.4,
    )
    scene.wait(1.8)

    # د) ظهور القوانين والقواعد الصارمة مع وميض ذهبي
    scene.play(
        FadeIn(rules_group, shift=UP * 0.25),
        run_time=0.9,
    )
    scene.play(
        rules_ops.animate.scale(1.15).set_color(GOLD_BRIGHT),
        rate_func=there_and_back,
        run_time=0.8,
    )
    scene.wait(3.2)

    # ==============================================================
    # 5. تفريغ المشهد للانتقال للمشهد السابع
    # ==============================================================
    all_scene = Group(
        group_c, group_r, group_z,
        real_line, group_integers_geom, group_complex_geom,
        rules_group
    )

    scene.play(
        FadeOut(all_scene),
        run_time=0.9,
    )
    scene.wait(0.5)