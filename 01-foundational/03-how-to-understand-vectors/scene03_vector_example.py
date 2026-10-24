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
from common.latex import mach_math_template
from common.mobjects.card import MachCard
from common.mobjects.vectors import MachVector


# ==============================================================
# الرسوم التوضيحية للمحتوى (أيقونات متجهة ناعمة)
# ==============================================================

def make_scale_with_weight(color=GOLD_LIGHT, scale=1.0):
    """ميزان مختبرات رقمي دقيق مع شاشة واسعة وثقل معايرة فيزيائي."""
    foot_l = RoundedRectangle(corner_radius=0.02, width=0.10, height=0.04, stroke_width=0, fill_color=color, fill_opacity=0.7).shift(LEFT * 0.38 + DOWN * 0.28)
    foot_r = RoundedRectangle(corner_radius=0.02, width=0.10, height=0.04, stroke_width=0, fill_color=color, fill_opacity=0.7).shift(RIGHT * 0.38 + DOWN * 0.28)

    scale_chassis = RoundedRectangle(
        corner_radius=0.06, width=0.96, height=0.34, stroke_width=1.5,
        color=color, fill_color="#14100B", fill_opacity=0.95
    ).shift(DOWN * 0.12)

    screen_border = RoundedRectangle(
        corner_radius=0.03, width=0.70, height=0.17, stroke_width=1.2,
        color=color, fill_color="#0A0805", fill_opacity=1.0
    ).move_to(scale_chassis.get_center() + DOWN * 0.02)

    screen_val = Text("3.500", font="Cairo", font_size=12, color=GOLD_BRIGHT).move_to(screen_border.get_center() + LEFT * 0.08)
    screen_unit = Text("kg", font="Cairo", font_size=9, color=color).next_to(screen_val, RIGHT, buff=0.08)
    screen_display = VGroup(screen_val, screen_unit)

    stem = Rectangle(width=0.12, height=0.08, stroke_width=1.2, color=color, fill_color=color, fill_opacity=0.6).next_to(scale_chassis.get_top(), UP, buff=-0.01)
    pan_top = Line(LEFT * 0.46, RIGHT * 0.46, stroke_width=2.5, color=color).next_to(stem, UP, buff=0)
    pan_lip = ArcBetweenPoints(LEFT * 0.46, RIGHT * 0.46, angle=0.18 * PI, stroke_width=1.2, color=color).next_to(pan_top, DOWN, buff=0.01)
    scale_pan = VGroup(stem, pan_top, pan_lip)

    scale_full = VGroup(foot_l, foot_r, scale_chassis, screen_border, screen_display, scale_pan)

    pan_y = pan_top.get_center()[1]
    w_base = RoundedRectangle(
        corner_radius=0.03, width=0.44, height=0.28, stroke_width=1.4,
        color=color, fill_color=color, fill_opacity=0.35
    ).move_to([0, pan_y + 0.14, 0])

    w_rim = Line(w_base.get_left() + UP * 0.05, w_base.get_right() + UP * 0.05, stroke_width=1.1, color=color, stroke_opacity=0.6)
    w_neck = Rectangle(width=0.14, height=0.08, stroke_width=1.3, color=color, fill_color=color, fill_opacity=0.8).next_to(w_base, UP, buff=-0.02)
    w_knob = Circle(radius=0.095, stroke_width=1.5, color=color, fill_color=color, fill_opacity=0.85).next_to(w_neck, UP, buff=-0.02)

    weight_full = VGroup(w_base, w_rim, w_neck, w_knob)
    return VGroup(scale_full, weight_full).scale(scale)


def make_realistic_clock(color=GOLD_LIGHT, scale=1.0):
    """ساعة توقيت دقيقة مع تدريج الساعات وعقارب دقيقة."""
    r_outer = 0.38
    outer_ring = Circle(radius=r_outer, stroke_width=1.8, color=color)
    inner_ring = Circle(radius=r_outer - 0.04, stroke_width=0.8, color=color, stroke_opacity=0.45)
    dial_face  = Circle(radius=r_outer, stroke_width=0, fill_color="#120E09", fill_opacity=0.8)

    ticks = VGroup()
    for i in range(12):
        angle = i * (TAU / 12)
        is_cardinal = (i % 3 == 0)
        tick_len = 0.07 if is_cardinal else 0.04
        t_width  = 1.6 if is_cardinal else 0.9

        p_start = np.array([(r_outer - 0.05) * np.sin(angle), (r_outer - 0.05) * np.cos(angle), 0])
        p_end = np.array([(r_outer - 0.05 - tick_len) * np.sin(angle), (r_outer - 0.05 - tick_len) * np.cos(angle), 0])
        ticks.add(Line(p_start, p_end, stroke_width=t_width, color=color))

    hand_hour = Line(ORIGIN, UP * 0.16 + RIGHT * 0.06, stroke_width=2.4, color=color)
    hand_min = Line(ORIGIN, UP * 0.24 + LEFT * 0.11, stroke_width=1.6, color=color)
    center_pin = Circle(radius=0.035, stroke_width=1.2, color=color, fill_color=GOLD_BRIGHT, fill_opacity=1.0)

    clock = VGroup(dial_face, outer_ring, inner_ring, ticks, hand_hour, hand_min, center_pin)
    return clock.scale(scale)


def make_apple(color=COPPER_TERRA, scale=1.0):
    """تفاحة ناعمة وانسيابية بمتجهات نقية."""
    apple_body = VMobject()
    p_notch_top = np.array([0.0, 0.12, 0])
    p_tr1       = np.array([0.13, 0.19, 0])
    p_tr2       = np.array([0.22, 0.10, 0])
    p_br1       = np.array([0.20, -0.10, 0])
    p_br2       = np.array([0.11, -0.20, 0])
    p_notch_bot = np.array([0.0, -0.17, 0])
    p_bl2       = np.array([-0.11, -0.20, 0])
    p_bl1       = np.array([-0.20, -0.10, 0])
    p_tl2       = np.array([-0.22, 0.10, 0])
    p_tl1       = np.array([-0.13, 0.19, 0])

    apple_body.set_points_smoothly([
        p_notch_top, p_tr1, p_tr2, p_br1, p_br2,
        p_notch_bot,
        p_bl2, p_bl1, p_tl2, p_tl1, p_notch_top
    ])
    apple_body.set_stroke(color=color, width=1.4)
    apple_body.set_fill(color=color, opacity=0.30)

    stem = ArcBetweenPoints(
        p_notch_top,
        p_notch_top + UP * 0.14 + RIGHT * 0.04,
        angle=-PI / 3,
        stroke_width=1.8,
        color=color,
    )

    leaf_r = Ellipse(width=0.12, height=0.045, stroke_width=1.1, color=color, fill_color=color, fill_opacity=0.85)\
        .rotate(28 * DEGREES).next_to(p_notch_top + UP * 0.08, RIGHT, buff=-0.02).shift(UP * 0.02)

    leaf_l = Ellipse(width=0.12, height=0.045, stroke_width=1.1, color=color, fill_color=color, fill_opacity=0.85)\
        .rotate(-28 * DEGREES).next_to(p_notch_top + UP * 0.08, LEFT, buff=-0.02).shift(UP * 0.02)

    return VGroup(apple_body, stem, leaf_l, leaf_r).scale(scale)


def make_building(color=COPPER_TERRA, scale=1.0):
    """مبنى معماري بواجهة واضحة ونوافذ مقوسة."""
    base_box = Rectangle(width=0.96, height=0.76, stroke_width=1.6, color=color, fill_color=color, fill_opacity=0.16)
    cornice = Rectangle(width=1.06, height=0.08, stroke_width=1.6, color=color, fill_color=color, fill_opacity=0.85)\
        .next_to(base_box, UP, buff=0)

    attic_box = Rectangle(width=0.90, height=0.46, stroke_width=1.6, color=color, fill_color=color, fill_opacity=0.16)\
        .next_to(cornice, UP, buff=0)

    roof = Rectangle(width=1.02, height=0.07, stroke_width=1.6, color=color, fill_color=color, fill_opacity=0.85)\
        .next_to(attic_box, UP, buff=0)

    def arched_win():
        arch = Arc(radius=0.07, start_angle=0, angle=PI, stroke_width=1.4, color=color)
        leg_l = Line(LEFT * 0.07, LEFT * 0.07 + DOWN * 0.08, stroke_width=1.4, color=color)
        leg_r = Line(RIGHT * 0.07, RIGHT * 0.07 + DOWN * 0.08, stroke_width=1.4, color=color)
        sill = Line(LEFT * 0.095 + DOWN * 0.08, RIGHT * 0.095 + DOWN * 0.08, stroke_width=1.6, color=color)
        return VGroup(arch, leg_l, leg_r, sill)

    win_top_l = arched_win().move_to(attic_box.get_center() + LEFT * 0.22)
    win_top_r = arched_win().move_to(attic_box.get_center() + RIGHT * 0.22)

    win_grid = VGroup()
    for dx in (-0.28, 0.0, 0.28):
        for dy in (0.16, -0.06):
            w = Rectangle(width=0.13, height=0.12, stroke_width=1.3, color=color, fill_color=color, fill_opacity=0.35)\
                .move_to(base_box.get_center() + RIGHT * dx + UP * dy)
            win_grid.add(w)

    door = Rectangle(width=0.18, height=0.18, stroke_width=1.5, color=color, fill_color=color, fill_opacity=0.85)\
        .next_to(base_box.get_bottom(), UP, buff=0)

    return VGroup(
        base_box, cornice, attic_box, roof,
        win_top_l, win_top_r, win_grid, door
    ).scale(scale)


# ==============================================================
# كود المشهد الثالث (Scene 03) - المدة: 39.5 ثانية (من 00:50 إلى 01:29.5)
# ==============================================================

def play_scene03(scene):

    card_w, card_h = 3.85, 5.4

    X_LEFT   = -4.1
    X_CENTER =  0.0
    X_RIGHT  =  4.1

    Y_ROW1 =  0.55
    Y_ROW2 = -1.35

    # ----------------------------------------------------------
    # 1. إعداد البطاقات الثلاث (استحضار مشهد الحلقة السابقة)
    # ----------------------------------------------------------
    card_phys = MachCard(
        width=card_w, height=card_h, center=[X_LEFT, 0, 0],
        title="كميات فيزيائية", title_font_size=20,
        title_color=GOLD_LIGHT, accent_color=GOLD_LIGHT,
        show_divider=False, corner_radius=0.22, content_padding=0.28,
        background_color="#18140E", background_opacity=0.85,
    )

    card_count = MachCard(
        width=card_w, height=card_h, center=[X_CENTER, 0, 0],
        title="أشياء معدودة", title_font_size=20,
        title_color=COPPER_TERRA, accent_color=COPPER_TERRA,
        show_divider=False, corner_radius=0.22, content_padding=0.28,
        background_color="#18140E", background_opacity=0.85,
    )

    card_geom = MachCard(
        width=card_w, height=card_h, center=[X_RIGHT, 0, 0],
        title="كميات هندسية", title_font_size=20,
        title_color=GOLD_LIGHT, accent_color=GOLD_LIGHT,
        show_divider=False, corner_radius=0.22, content_padding=0.28,
        background_color="#18140E", background_opacity=0.85,
    )

    # محتويات البطاقة اليسرى (الفيزياء)
    scale_icon = make_scale_with_weight(color=GOLD_LIGHT, scale=0.92)
    weight_text = MathTex(r"3.5\text{ kg}", tex_template=mach_math_template, font_size=27, color=IVORY_WHITE)
    row_weight = VGroup(scale_icon, weight_text).arrange(RIGHT, buff=0.25).move_to([X_LEFT, Y_ROW1, 0])

    clock_icon = make_realistic_clock(color=GOLD_LIGHT, scale=0.95)
    time_text = MathTex(r"7\text{ s}", tex_template=mach_math_template, font_size=27, color=IVORY_WHITE)
    row_time = VGroup(clock_icon, time_text).arrange(RIGHT, buff=0.28).move_to([X_LEFT, Y_ROW2, 0])

    # محتويات البطاقة الوسطى (المعدودات)
    apples_list = [make_apple(color=COPPER_TERRA, scale=0.88) for _ in range(4)]
    apples_group = VGroup(*apples_list).arrange(RIGHT, buff=0.15)
    apples_label = MarkupText("4 تفاحات", font="Cairo", font_size=19, color=IVORY_WHITE)
    row_apples = VGroup(apples_group, apples_label).arrange(DOWN, buff=0.18).move_to([X_CENTER, Y_ROW1, 0])

    building_icon = make_building(color=COPPER_TERRA, scale=0.82)
    floor_label = MarkupText("الدور العاشر", font="Cairo", font_size=19, color=IVORY_WHITE)
    row_floor = VGroup(building_icon, floor_label).arrange(DOWN, buff=0.15).move_to([X_CENTER, Y_ROW2, 0])

    # محتويات البطاقة اليمنى (الهندسة)
    ruler_len = 2.5
    measure_line = Line(LEFT * (ruler_len / 2), RIGHT * (ruler_len / 2), stroke_width=2.4, color=GOLD_LIGHT)
    cap_l = Line(UP * 0.14, DOWN * 0.14, stroke_width=2, color=GOLD_LIGHT).move_to(measure_line.get_left())
    cap_r = Line(UP * 0.14, DOWN * 0.14, stroke_width=2, color=GOLD_LIGHT).move_to(measure_line.get_right())
    ruler_ticks = VGroup()
    for i in range(1, 6):
        x_val = interpolate(-ruler_len / 2, ruler_len / 2, i / 6)
        tick = Line([x_val, -0.045, 0], [x_val, 0.045, 0], stroke_width=1.2, color=GOLD_LIGHT)
        ruler_ticks.add(tick)
    length_text = MathTex(r"3\text{ m}", tex_template=mach_math_template, font_size=26, color=IVORY_WHITE).next_to(measure_line, UP, buff=0.16)
    row_length = VGroup(measure_line, cap_l, cap_r, ruler_ticks, length_text).move_to([X_RIGHT, Y_ROW1, 0])

    r_prot = 0.76
    angle_base = Line(LEFT * 1.25, RIGHT * 1.25, stroke_width=1.8, color=STONE_AXIS)
    angle_arc = Arc(radius=r_prot, start_angle=0, angle=PI, color=GOLD_LIGHT, stroke_width=2.2)
    angle_center_dot = Dot(angle_base.get_center(), radius=0.035, color=GOLD_LIGHT)
    prot_ticks = VGroup()
    for deg in range(15, 180, 15):
        rad = deg * DEGREES
        p_out = np.array([r_prot * np.cos(rad), r_prot * np.sin(rad), 0])
        p_in  = np.array([(r_prot - 0.05) * np.cos(rad), (r_prot - 0.05) * np.sin(rad), 0])
        prot_ticks.add(Line(p_out, p_in, stroke_width=1.0, color=GOLD_LIGHT))
    angle_text = MathTex(r"180^\circ", tex_template=mach_math_template, font_size=26, color=IVORY_WHITE).next_to(angle_arc.get_top(), UP, buff=0.14)
    row_angle = VGroup(angle_base, angle_arc, angle_center_dot, prot_ticks, angle_text).move_to([X_RIGHT, Y_ROW2, 0])

    all_cards = VGroup(card_phys, card_count, card_geom)
    all_rows = VGroup(row_weight, row_time, row_apples, row_floor, row_length, row_angle)

    # ----------------------------------------------------------
    # أ) استحضار الأمثلة الثلاثة (12.5s إجمالي)
    # ----------------------------------------------------------
    scene.play(
        FadeIn(all_cards, shift=UP * 0.15),
        FadeIn(all_rows, shift=UP * 0.15),
        run_time=1.5,
    )
    scene.wait(4.0)

    # لفت الانتباه نحو (الـ 4 تفاحات، 7 ثوان، الدور العاشر) أثناء ذكرها
    scene.play(
        row_apples.animate.scale(1.08),
        row_time.animate.scale(1.08),
        row_floor.animate.scale(1.08),
        run_time=1.8,
        rate_func=there_and_back,
    )
    scene.wait(5.2)

    # ----------------------------------------------------------
    # ب) عزل تفاحة المتجهات ونقلها إلى قلب الشاشة (5.0s إجمالي)
    # ----------------------------------------------------------
    chosen_apple = apples_list[2]
    solo_apple = chosen_apple.copy()

    # خفتان باقي عناصر المشهد
    background_faded = VGroup(
        card_phys, card_geom, card_count,
        row_weight, row_time, row_floor, row_length, row_angle,
        apples_label, apples_list[0], apples_list[1], apples_list[3]
    )

    apple_title = MarkupText(
        "تفاحة المتجهات",
        font="Cairo",
        font_size=24,
        color=COPPER_TERRA,
    ).move_to([0, 1.95, 0])

    apple_sub = Text(
        "(تمثيل حسي ملموس)",
        font="Cairo",
        font_size=15,
        color=GOLD_MUTED,
    ).next_to(apple_title, DOWN, buff=0.10)

    apple_tag = VGroup(apple_title, apple_sub)

    scene.play(
        FadeOut(background_faded),
        FadeOut(chosen_apple),
        solo_apple.animate.scale(3.2).move_to([0, 0.15, 0]),
        FadeIn(apple_tag, shift=DOWN * 0.15),
        run_time=2.0,
        rate_func=smooth,
    )
    scene.wait(3.0)

    # ----------------------------------------------------------
    # ج) التحول السينمائي: من التفاحة إلى سهم المتجه (10.0s إجمالي)
    # ----------------------------------------------------------
    vector_arrow = MachVector(
        start=[-2.3, 0.5, 0],
        end=[2.3, 1.5, 0],
        color=GOLD_BRIGHT,
        stroke_width=4.8,
        tip_length=0.30,
        show_pivot=True,
        pivot_radius=0.065,
    )
    vec_label = MathTex(
        r"\mathbf{v}",
        tex_template=mach_math_template,
        font_size=32,
        color=GOLD_BRIGHT,
    ).next_to(vector_arrow.tip, UR, buff=0.12)

    vector_title = MarkupText(
        "سهم المتجه",
        font="Cairo",
        font_size=24,
        color=GOLD_LIGHT,
    ).move_to([0, 3, 0])

    vector_sub = Text(
        "(تمثيل هندسي وفيزيائي للمقدار والاتجاه)",
        font="Cairo",
        font_size=14,
        color=GOLD_MUTED,
    ).next_to(vector_title, DOWN, buff=0.10)

    vector_tag = VGroup(vector_title, vector_sub)

    scene.play(
        ReplacementTransform(solo_apple, vector_arrow),
        Transform(apple_tag, vector_tag),
        FadeIn(vec_label, shift=LEFT * 0.1),
        run_time=2.0,
        rate_func=smooth,
    )
    scene.wait(8.0)

    # ----------------------------------------------------------
    # د) الصدمة البصرية: علامة الغلط وكارت التحذير (10.0s إجمالي)
    # ----------------------------------------------------------
    cross_c = vector_arrow.get_center()
    cross_arm1 = Line(
        cross_c + [-0.85, -0.85, 0], cross_c + [0.85, 0.85, 0],
        stroke_width=5.5, color=COPPER_TERRA, stroke_opacity=0.95
    )
    cross_arm2 = Line(
        cross_c + [-0.85, 0.85, 0], cross_c + [0.85, -0.85, 0],
        stroke_width=5.5, color=COPPER_TERRA, stroke_opacity=0.95
    )
    red_cross = VGroup(cross_arm1, cross_arm2)

    banner_main = MarkupText(
        "السهم مش هو المتجه!",
        font="Cairo",
        font_size=25,
        color=IVORY_WHITE,
    )
    banner_note = Text(
        "السهم مجرد تمثيل حسي.. وليس المفهوم الرياضي نفسه",
        font="Cairo",
        font_size=14,
        color=GOLD_MUTED,
    )
    banner_text_group = VGroup(banner_main, banner_note).arrange(DOWN, buff=0.12)

    banner_card = MachCard(
        width=6.6,
        height=1.75,
        center=[0, -1.5, 0],
        show_divider=False,
        corner_radius=0.20,
        content=banner_text_group,
        accent_color=COPPER_TERRA,
        background_color="#100D07",
        border_opacity=0.65,
        background_opacity=0.92,
        reflection_opacity=0.22,
    )

    # ضرب علامة الخطأ وتخفيت السهم
    scene.play(
        Create(cross_arm1, run_time=0.35),
        Create(cross_arm2, run_time=0.35),
        vector_arrow.animate.set_opacity(0.20).set_color(GOLD_MUTED),
        vec_label.animate.set_opacity(0.20).set_color(GOLD_MUTED),
        run_time=0.7,
    )

    # بناء كارت التحذير
    scene.play(
        banner_card.construct(
            run_time=1.8,
            show_reflection=True,
            illuminate_glass=True,
            show_content=True,
        ),
        run_time=1.8,
    )
    # إبقاء الكارت مع نهاية كلامك عن مثال السهم
    scene.wait(7.5)

    # ----------------------------------------------------------
    # هـ) تفريغ المشهد (2.0s إجمالي)
    # ----------------------------------------------------------
    final_group = VGroup(
        vector_arrow,
        vec_label,
        apple_tag,
        red_cross,
        banner_card,
    )

    scene.play(
        FadeOut(final_group),
        run_time=1.2,
    )
    scene.wait(0.8)

    # المجموع الكلي الدقيق: 12.5 + 5.0 + 10.0 + 10.0 + 2.0 = 39.5 ثانية بالمللي!