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


def make_card_floor_glow(
    card,
    accent_color=GOLD_LIGHT,
    reflection_offset=0.22,
    reflection_opacity=0.30,
):
    """
    إنشاء التوهج الأرضي ثلاثي الأبعاد وانعكاس الزجاج أسفل البطاقة
    (متطابق تماماً مع خوارزمية وهندسة MachTable).
    """
    glow_group = VGroup()
    w = card.width
    h = card.height
    corner_radius = 0.22
    y_base = card.get_bottom()[1] - reflection_offset
    center_x = card.get_center()[0]

    # 1. طبقات التوهج البيضاوي المتدرج الناعم (Glow Layers)
    n_glow_layers = 8
    for i in range(n_glow_layers):
        t = i / (n_glow_layers - 1)
        w_layer = w * interpolate(0.85, 1.25, t)
        h_layer = 0.35 * interpolate(0.35, 1.40, t)
        op_layer = reflection_opacity * interpolate(0.65, 0.005, t**0.6)

        glow_ellipse = Ellipse(
            width=w_layer,
            height=h_layer,
            stroke_width=0,
            fill_color=GOLD_MUTED if t > 0.4 else accent_color,
            fill_opacity=op_layer,
        ).move_to([center_x, y_base - h_layer * 0.25, 0])
        glow_group.add(glow_ellipse)

    # 2. شرائح الانعكاس المنظوري الزجاجي المتلاشي (Reflection Slices)
    reflection_h = 0.45
    p_top_l = np.array([center_x - w / 2 + corner_radius, card.get_bottom()[1], 0])
    p_top_r = np.array([center_x + w / 2 - corner_radius, card.get_bottom()[1], 0])
    p_bot_r = np.array([center_x + (w / 2 - corner_radius) * 1.05, card.get_bottom()[1] - reflection_h, 0])
    p_bot_l = np.array([center_x - (w / 2 - corner_radius) * 1.05, card.get_bottom()[1] - reflection_h, 0])

    n_refl_slices = 6
    for j in range(n_refl_slices):
        alpha_a = j / n_refl_slices
        alpha_b = (j + 1) / n_refl_slices

        pt_tl = interpolate(p_top_l, p_bot_l, alpha_a)
        pt_tr = interpolate(p_top_r, p_bot_r, alpha_a)
        pt_br = interpolate(p_top_r, p_bot_r, alpha_b)
        pt_bl = interpolate(p_top_l, p_bot_l, alpha_b)

        slice_op = reflection_opacity * 0.45 * ((1.0 - alpha_a) ** 1.8)

        refl_slice = Polygon(
            pt_tl, pt_tr, pt_br, pt_bl,
            stroke_width=0,
            fill_color=accent_color if alpha_a < 0.3 else GOLD_DARK,
            fill_opacity=slice_op,
        )
        glow_group.add(refl_slice)

    # 3. خط التماس المضيء
    contact_line = Line(
        p_top_l, p_top_r,
        color=accent_color,
        stroke_width=1.0,
        stroke_opacity=reflection_opacity * 0.8,
    )
    glow_group.add(contact_line)
    glow_group.set_z_index(-1)

    return glow_group


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


def play_scene04(scene):

    # ==============================================================
    # 1. إحداثيات الشبكة الموحدة (Grid Coordinates)
    # ==============================================================
    card_w, card_h = 3.85, 5.4

    X_LEFT   = -4.1
    X_CENTER =  0.0
    X_RIGHT  =  4.1

    Y_ROW1 =  0.55   # الصف العلوي (الميزان - التفاحات - الطول)
    Y_ROW2 = -1.35   # الصف السفلي (الساعة - المبنى - الزاوية)

    # 1. البطاقات الثلاث
    card_phys = RoundedRectangle(
        corner_radius=0.22, width=card_w, height=card_h,
        color=STONE_AXIS, stroke_width=1.4, fill_color="#18140E", fill_opacity=0.85
    ).move_to([X_LEFT, 0, 0])

    card_count = RoundedRectangle(
        corner_radius=0.22, width=card_w, height=card_h,
        color=STONE_AXIS, stroke_width=1.4, fill_color="#18140E", fill_opacity=0.85
    ).move_to([X_CENTER, 0, 0])

    card_geom = RoundedRectangle(
        corner_radius=0.22, width=card_w, height=card_h,
        color=STONE_AXIS, stroke_width=1.4, fill_color="#18140E", fill_opacity=0.85
    ).move_to([X_RIGHT, 0, 0])

    # 2. الإضاءة الأرضية والانعكاس ثلاثي الأبعاد أسفل كل بطاقة
    glow_phys  = make_card_floor_glow(card_phys, accent_color=GOLD_LIGHT)
    glow_count = make_card_floor_glow(card_count, accent_color=COPPER_TERRA)
    glow_geom  = make_card_floor_glow(card_geom, accent_color=GOLD_LIGHT)

    # 3. العناوين
    title_phys = Text("كميات فيزيائية", font="Cairo", font_size=20, color=GOLD_LIGHT)\
        .next_to(card_phys.get_top(), DOWN, buff=0.28)

    title_count = Text("أشياء معدودة", font="Cairo", font_size=20, color=COPPER_TERRA)\
        .next_to(card_count.get_top(), DOWN, buff=0.28)

    title_geom = Text("كميات هندسية", font="Cairo", font_size=20, color=GOLD_LIGHT)\
        .next_to(card_geom.get_top(), DOWN, buff=0.28)

    # ==============================================================
    # 2. الصف العلوي (Row 1): ميزان بوزن 3.5kg - 4 تفاحات - مسطرة 3m
    # ==============================================================

    # أ) الميزان الحساس
    scale_icon = make_scale_with_weight(color=GOLD_LIGHT, scale=0.92)
    weight_text = MathTex(r"3.5\text{ kg}", tex_template=mach_math_template, font_size=27, color=IVORY_WHITE)
    row_weight = VGroup(scale_icon, weight_text).arrange(RIGHT, buff=0.25).move_to([X_LEFT, Y_ROW1, 0])

    # ب) الـ 4 تفاحات
    apples_group = VGroup(*[make_apple(color=COPPER_TERRA, scale=0.88) for _ in range(4)]).arrange(RIGHT, buff=0.15)
    apples_label = MarkupText("4 تفاحات", font="Cairo", font_size=19, color=IVORY_WHITE)
    row_apples = VGroup(apples_group, apples_label).arrange(DOWN, buff=0.18).move_to([X_CENTER, Y_ROW1, 0])

    # ج) مسطرة قياس هندسية مدرجة
    ruler_len = 2.5
    measure_line = Line(LEFT * (ruler_len / 2), RIGHT * (ruler_len / 2), stroke_width=2.4, color=GOLD_LIGHT)
    cap_l = Line(UP * 0.14, DOWN * 0.14, stroke_width=2, color=GOLD_LIGHT).move_to(measure_line.get_left())
    cap_r = Line(UP * 0.14, DOWN * 0.14, stroke_width=2, color=GOLD_LIGHT).move_to(measure_line.get_right())

    ruler_ticks = VGroup()
    num_ticks = 7
    for i in range(1, num_ticks - 1):
        x_val = interpolate(-ruler_len / 2, ruler_len / 2, i / (num_ticks - 1))
        t_height = 0.09 if i % 2 == 0 else 0.05
        t_w = 1.6 if i % 2 == 0 else 1.0
        tick = Line([x_val, -t_height / 2, 0], [x_val, t_height / 2, 0], stroke_width=t_w, color=GOLD_LIGHT)
        ruler_ticks.add(tick)

    length_text = MathTex(r"3\text{ m}", tex_template=mach_math_template, font_size=26, color=IVORY_WHITE)\
        .next_to(measure_line, UP, buff=0.16)
    row_length = VGroup(measure_line, cap_l, cap_r, ruler_ticks, length_text).move_to([X_RIGHT, Y_ROW1, 0])

    # ==============================================================
    # 3. الصف السفلي (Row 2): الساعة 7s - المبنى - المنقلة الهندسية 180°
    # ==============================================================

    # أ) ساعة التوقيت الدقيقة
    clock_icon = make_realistic_clock(color=GOLD_LIGHT, scale=0.95)
    time_text = MathTex(r"7\text{ s}", tex_template=mach_math_template, font_size=27, color=IVORY_WHITE)
    row_time = VGroup(clock_icon, time_text).arrange(RIGHT, buff=0.28).move_to([X_LEFT, Y_ROW2, 0])

    # ب) المبنى المعماري
    building_icon = make_building(color=COPPER_TERRA, scale=0.82)
    floor_label = MarkupText("الدور العاشر", font="Cairo", font_size=19, color=IVORY_WHITE)
    row_floor = VGroup(building_icon, floor_label).arrange(DOWN, buff=0.15).move_to([X_CENTER, Y_ROW2, 0])

    # ج) المنقلة الهندسية المدرجة
    r_prot = 0.76
    angle_base = Line(LEFT * 1.25, RIGHT * 1.25, stroke_width=1.8, color=STONE_AXIS)
    angle_arc = Arc(radius=r_prot, start_angle=0, angle=PI, color=GOLD_LIGHT, stroke_width=2.2)
    angle_center_dot = Dot(angle_base.get_center(), radius=0.035, color=GOLD_LIGHT)

    prot_ticks = VGroup()
    for deg in range(15, 180, 15):
        rad = deg * DEGREES
        is_major = (deg % 45 == 0)
        len_t = 0.08 if is_major else 0.04
        p_out = np.array([r_prot * np.cos(rad), r_prot * np.sin(rad), 0])
        p_in  = np.array([(r_prot - len_t) * np.cos(rad), (r_prot - len_t) * np.sin(rad), 0])
        prot_ticks.add(Line(p_out, p_in, stroke_width=1.4 if is_major else 0.9, color=GOLD_LIGHT))

    angle_text = MathTex(r"180^\circ", tex_template=mach_math_template, font_size=26, color=IVORY_WHITE)\
        .next_to(angle_arc.get_top(), UP, buff=0.14)
    row_angle = VGroup(angle_base, angle_arc, angle_center_dot, prot_ticks, angle_text).move_to([X_RIGHT, Y_ROW2, 0])

    # ==============================================================
    # 4. التزامن الصوتي المحسوب للمشهد الرابع
    # ==============================================================

    # أ) ظهور البطاقة الأولى مع إضاءتها الأرضية (الفيزياء)
    scene.play(
        FadeIn(card_phys, shift=UP * 0.2),
        FadeIn(glow_phys),
        FadeIn(title_phys),
        run_time=0.8,
    )
    scene.play(
        FadeIn(row_weight, shift=RIGHT * 0.2),
        run_time=0.7,
    )
    scene.play(
        FadeIn(row_time, shift=RIGHT * 0.2),
        run_time=0.7,
    )

    # ب) ظهور البطاقة الثانية مع إضاءتها الأرضية (أشياء معدودة)
    scene.play(
        FadeIn(card_count, shift=UP * 0.2),
        FadeIn(glow_count),
        FadeIn(title_count),
        run_time=0.8,
    )
    scene.play(
        FadeIn(row_apples, shift=UP * 0.15),
        run_time=0.8,
    )
    scene.play(
        FadeIn(row_floor, shift=UP * 0.15),
        run_time=0.7,
    )

    # ج) ظهور البطاقة الثالثة مع إضاءتها الأرضية (كميات هندسية)
    scene.play(
        FadeIn(card_geom, shift=UP * 0.2),
        FadeIn(glow_geom),
        FadeIn(title_geom),
        run_time=0.8,
    )
    scene.play(
        Create(measure_line),
        FadeIn(cap_l, cap_r),
        Create(ruler_ticks),
        FadeIn(length_text),
        run_time=0.9,
    )
    scene.play(
        Create(angle_base),
        Create(angle_arc),
        Create(prot_ticks),
        FadeIn(angle_center_dot),
        FadeIn(angle_text),
        run_time=0.9,
    )

    # د) استقرار المشهد للتأمل (3.5s)
    scene.wait(3.5)

    # هـ) تفريغ المشهد بالكامل
    all_content = Group(
        card_phys, glow_phys, title_phys, row_weight, row_time,
        card_count, glow_count, title_count, row_apples, row_floor,
        card_geom, glow_geom, title_geom, row_length, row_angle,
    )

    scene.play(
        FadeOut(all_content),
        run_time=0.9,
    )
    scene.wait(0.5)