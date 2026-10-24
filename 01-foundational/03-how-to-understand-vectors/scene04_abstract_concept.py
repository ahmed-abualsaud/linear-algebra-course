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
from common.mobjects.characters import mach_mathematician
from common.mobjects.vector_space import MachVectorSpace


# ==============================================================
# دالة دمج لوني آمنة ومتوافقة مع جميع إصدارات Manim
# ==============================================================

def blend_colors(c1, c2, alpha):
    """دمج لوني انسيابي ودقيق عبر فضاء RGB يتفادى أي أخطاء في ManimColor."""
    rgb1 = np.array(color_to_rgb(c1))
    rgb2 = np.array(color_to_rgb(c2))
    return rgb_to_color(interpolate(rgb1, rgb2, alpha))


# ==============================================================
# 1. دوال بناء القرص الزجاجي والتوهج الساطع فائق النعومة
# ==============================================================

def make_radiant_rays(center_point, inner_radius=0.78, n_rays=32):
    """أشعة نور أكثر سطوعاً مع تدرج غاوسي حريري متصل فائق النعومة."""
    rays_group = VGroup()

    n_bloom = 70
    r_max_offset = 1.65
    peak_glow = 0.68

    for i in range(n_bloom):
        t_curr = i / n_bloom
        t_next = (i + 1) / n_bloom

        r_bloom = inner_radius + r_max_offset * t_curr

        g_curr = peak_glow * ((1.0 - t_curr) ** 2.1)
        g_next = peak_glow * ((1.0 - t_next) ** 2.1)

        delta_op = max(0.0006, g_curr - g_next)

        if t_curr < 0.30:
            color = blend_colors(GOLD_BRIGHT, GOLD_LIGHT, t_curr / 0.30)
        else:
            color = blend_colors(GOLD_LIGHT, GOLD_DARK, (t_curr - 0.30) / 0.70)

        bloom_circle = Circle(
            radius=r_bloom,
            stroke_width=0,
            fill_color=color,
            fill_opacity=delta_op,
        ).move_to(center_point)
        rays_group.add(bloom_circle)

    for i in range(n_rays):
        angle = i * (TAU / n_rays)
        pattern = i % 4
        if pattern == 0:
            ray_len, sw, op = 0.70, 1.4, 0.58
        elif pattern == 2:
            ray_len, sw, op = 0.46, 1.0, 0.40
        else:
            ray_len, sw, op = 0.28, 0.7, 0.25

        dir_vec = np.array([np.cos(angle), np.sin(angle), 0])
        p_start = center_point + dir_vec * (inner_radius + 0.02)
        p_end   = center_point + dir_vec * (inner_radius + ray_len)

        ray_line = Line(
            p_start, p_end,
            stroke_width=sw,
            stroke_opacity=op,
            color=GOLD_BRIGHT if pattern == 0 else GOLD_LIGHT,
        )
        rays_group.add(ray_line)

    return rays_group


def make_glass_orb(center_point, radius=0.78):
    """قرص زجاجي كريستالي مشرق مع إضاءة حافة ذهبية متألقة."""
    orb = VGroup()

    for i in range(5):
        t = i / 4
        r_glow = radius * (1.0 - 0.18 * t)
        glow_in = Circle(
            radius=r_glow,
            stroke_width=0,
            fill_color=GOLD_LIGHT,
            fill_opacity=0.06 * (1.0 - t),
        ).move_to(center_point)
        orb.add(glow_in)

    outer_rim = Circle(
        radius=radius,
        stroke_color=GOLD_LIGHT,
        stroke_width=1.8,
        stroke_opacity=0.90,
        fill_color="#100D07",
        fill_opacity=0.88,
    ).move_to(center_point)

    inner_rim = Circle(
        radius=radius - 0.05,
        stroke_color=GOLD_LIGHT,
        stroke_width=0.6,
        stroke_opacity=0.40,
        fill_color=GOLD_LIGHT,
        fill_opacity=0.035,
    ).move_to(center_point)

    halo_edge = Circle(
        radius=radius + 0.02,
        stroke_color=GOLD_BRIGHT,
        stroke_width=2.2,
        stroke_opacity=0.45,
    ).move_to(center_point)

    orb.add(outer_rim, inner_rim, halo_edge)
    return orb


# ==============================================================
# 2. المشهد الرابع (Scene 04) - المدة: 19.0 ثانية (01:30.0 إلى 01:49.0)
# ==============================================================

def play_scene04(scene):

    X_RIGHT = 1.90
    X_MATH   = -4.35
    hero_point = np.array([X_RIGHT, 2.30, 0.0])

    mathematician = mach_mathematician(
        color=COPPER_TERRA,
        accent_color=GOLD_LIGHT,
        pose="explaining",
        scale=0.92,
        blink=True,
        breathing=True,
        glasses=True,
        tie_type="necktie",
    ).shift(RIGHT * X_MATH + DOWN * 0.40).set_z_index(5)

    faint_vectors_data = [
        ((3.2, 0.95, 0), GOLD_BRIGHT, r"\mathbf{v}_1"),
        ((-2.2, 1.9, 0), COPPER_TERRA, r"\mathbf{v}_2"),
        ((-1.7, -0.9, 0), STONE_AXIS, r"\mathbf{v}_3"),
        ((1.3, -2.4, 0), GOLD_LIGHT, r"\mathbf{v}_4"),
        ((3.4, -0.6, 0), IVORY_WHITE, r"\mathbf{v}_5"),
        ((-1.0, -2.5, 0), GOLD_MUTED, r"\mathbf{v}_6"),
    ]

    bg_vector_space = MachVectorSpace(
        center=ORIGIN,
        width=14.4,
        height=8.0,
        grid_step=0.75,
        vectors=faint_vectors_data,
        show_title=False,
        show_origin=True,
        grid_color=STONE_AXIS,
        axis_color=GOLD_LIGHT,
        grid_width=0.75,
        grid_opacity=0.08,
        axis_width=1.2,
        axis_opacity=0.18,
        vector_width=1.8,
        vector_opacity=0.14,
        origin_opacity=0.20,
        tip_length=0.16,
        label_font_size=16,
        dash_length=0.08,
        dashed_ratio=0.50,
    )
    bg_vector_space.set_z_index(-10)

    initial_center = ORIGIN
    glass_orb = make_glass_orb(initial_center, radius=0.78)

    v_part = MathTex(r"\mathbf{v}", tex_template=mach_math_template, font_size=46, color=GOLD_BRIGHT)
    in_part = MathTex(r"\in", tex_template=mach_math_template, font_size=40, color=IVORY_WHITE)
    V_part = MathTex(r"V", tex_template=mach_math_template, font_size=46, color=COPPER_TERRA)
    v_in_V = VGroup(v_part, in_part, V_part).arrange(RIGHT, buff=0.20).move_to(initial_center)

    orb_core = VGroup(glass_orb, v_in_V).set_z_index(6)
    radiant_rays = make_radiant_rays(initial_center, inner_radius=0.78).set_z_index(4)
    celestial_group = VGroup(radiant_rays, orb_core).move_to(UP * 5.2)

    concept_card = MachCard(
        width=7.40,
        height=2.80,
        center=[X_RIGHT, -1.25, 0],
        title="عقيدتك الرياضية عن المتجهات",
        title_font_size=19,
        title_color=GOLD_LIGHT,
        title_buff=0.18,
        content_padding=0.25,
        corner_radius=0.22,
        background_opacity=0.88,
    )

    content_center = concept_card.get_content_center()
    col_divider = DashedLine(
        UP * 0.70, DOWN * 0.70,
        dash_length=0.07, dashed_ratio=0.5,
        stroke_width=1.0, color=GOLD_DARK, stroke_opacity=0.45,
    ).move_to(content_center).set_z_index(2)

    col_r_title = MarkupText("1. جزء من فضاء المتجهات", font="Cairo", font_size=16, color=COPPER_TERRA)
    col_r_sub = Text("(Vector Space)", font="DejaVu Sans", font_size=12.5, color=GOLD_MUTED)
    col_r_line1 = Text("كيان يخضع لقواعد", font="Cairo", font_size=13, color=IVORY_WHITE)
    col_r_line2 = Text("وبديهيات رياضية صارمة", font="Cairo", font_size=13, color=IVORY_WHITE)
    col_r_desc = VGroup(col_r_line1, col_r_line2).arrange(DOWN, buff=0.07)
    col_right = VGroup(col_r_title, col_r_sub, col_r_desc).arrange(DOWN, buff=0.10).set_z_index(3)

    col_l_title = MarkupText("2. مفهوم مجرد", font="Cairo", font_size=16, color=GOLD_LIGHT)
    col_l_sub = Text("(Abstract Concept)", font="DejaVu Sans", font_size=12.5, color=GOLD_MUTED)
    col_l_line1 = Text("مستقل تماماً عن السهم", font="Cairo", font_size=13, color=IVORY_WHITE)
    col_l_line2 = Text("أو أي تمثيل حسي آخر", font="Cairo", font_size=13, color=IVORY_WHITE)
    col_l_desc = VGroup(col_l_line1, col_l_line2).arrange(DOWN, buff=0.07)
    col_left = VGroup(col_l_title, col_l_sub, col_l_desc).arrange(DOWN, buff=0.10).set_z_index(3)

    col_right.move_to([content_center[0] + 1.82, content_center[1], 0])
    col_left.move_to([content_center[0] - 1.82, content_center[1], 0])

    target_top_y = content_center[1] + 0.62
    col_right.align_to([0, target_top_y, 0], UP)
    col_left.align_to([0, target_top_y, 0], UP)

    # ==========================================================
    # خط زمني دقيق للمشهد الرابع (19.0 ثانية: 01:30.0 إلى 01:49.0)
    # ==========================================================

    # 1. هبوط القرص الزجاجي المشع (2.5s إجمالي)
    # [01:30.0 - 01:32.5]: "لكن معلش انا هعيد واكرر تاني..."
    scene.play(
        celestial_group.animate.move_to(ORIGIN),
        run_time=1.5,
        rate_func=smooth,
    )
    scene.wait(1.0)

    # 2. الاستقرار في الموضع المرتفع وظهور عالم الرياضيات والفضاء (2.5s إجمالي)
    # [01:32.5 - 01:35.0]: "...ان اللي لازم يكون ثابت في عقيدتك الرياضية..."
    scene.play(
        orb_core.animate.move_to(hero_point),
        FadeOut(radiant_rays, scale=0.6),
        FadeIn(bg_vector_space, run_time=1.5),
        FadeIn(mathematician, shift=RIGHT * 0.35, run_time=1.2),
        run_time=1.5,
        rate_func=smooth,
    )
    scene.wait(1.0)

    # 3. مؤشرات الشرح تنطلق مباشرة من أسفل الرموز (2.5s إجمالي)
    # [01:35.0 - 01:37.5]: "...هو ان المتجه عبارة عن جزء من فضاء..."
    p_top_v  = v_part.get_bottom() + DOWN * 0.05
    p_top_in = in_part.get_bottom() + DOWN * 0.05
    p_top_V  = V_part.get_bottom() + DOWN * 0.05

    p_bot_v  = np.array([hero_point[0] - 1.45, 1.45, 0])
    p_bot_in = np.array([hero_point[0],        1.45, 0])
    p_bot_V  = np.array([hero_point[0] + 1.45, 1.45, 0])

    line_v  = Line(p_top_v,  p_bot_v,  stroke_width=1.0, color=GOLD_LIGHT,   stroke_opacity=0.65)
    line_in = Line(p_top_in, p_bot_in, stroke_width=1.0, color=IVORY_WHITE,  stroke_opacity=0.55)
    line_V  = Line(p_top_V,  p_bot_V,  stroke_width=1.0, color=COPPER_TERRA, stroke_opacity=0.65)

    dot_v  = Dot(p_top_v,  radius=0.022, color=GOLD_BRIGHT)
    dot_in = Dot(p_top_in, radius=0.022, color=IVORY_WHITE)
    dot_V  = Dot(p_top_V,  radius=0.022, color=COPPER_TERRA)

    txt_v  = MarkupText("المتجه", font="Cairo", font_size=12.5, color=GOLD_BRIGHT).next_to(p_bot_v, DOWN, buff=0.08)
    txt_in = MarkupText("ينتمي إلى", font="Cairo", font_size=11.5, color=IVORY_WHITE).next_to(p_bot_in, DOWN, buff=0.08)
    txt_V  = MarkupText("فضاء المتجهات", font="Cairo", font_size=12.5, color=COPPER_TERRA).next_to(p_bot_V, DOWN, buff=0.08)

    callouts_group = VGroup(
        VGroup(line_v, dot_v, txt_v),
        VGroup(line_in, dot_in, txt_in),
        VGroup(line_V, dot_V, txt_V),
    ).set_z_index(7)

    scene.play(
        Create(line_v),  Create(line_in),  Create(line_V),
        FadeIn(dot_v),   FadeIn(dot_in),   FadeIn(dot_V),
        FadeIn(txt_v, shift=DOWN * 0.06),
        FadeIn(txt_in, shift=DOWN * 0.06),
        FadeIn(txt_V, shift=DOWN * 0.06),
        run_time=1.0,
    )
    scene.wait(1.5)

    # 4. بناء البطاقة والعمودين (9.5s إجمالي)
    # [01:37.5 - 01:42.5]: "...ليه قواعد وقوانين والفضاء ده اسمه فضاء المتجهات" (ظهور العمود الأيمن)
    scene.play(
        concept_card.animate_shell(run_time=1.4),
        Create(col_divider, run_time=0.8),
    )
    scene.play(
        FadeIn(col_right, shift=LEFT * 0.20),
        run_time=1.0,
    )
    scene.wait(2.6)

    # [01:42.5 - 01:47.0]: "...وانه مفهوم مجرد من اي مثال او موقف بيحاول يشرحه" (ظهور العمود الأيسر)
    scene.play(
        FadeIn(col_left, shift=RIGHT * 0.20),
        run_time=1.0,
    )
    scene.wait(3.5)

    # 5. تفريغ المشهد (2.0s إجمالي)
    # [01:47.0 - 01:49.0]: سكتة قبل بداية المشهد الخامس عند 01:49.0
    all_scene = VGroup(
        mathematician,
        bg_vector_space,
        orb_core,
        callouts_group,
        concept_card,
        col_divider,
        col_right,
        col_left,
    )
    scene.play(
        FadeOut(all_scene),
        run_time=1.2,
    )
    scene.wait(0.8)

    # المجموع: 2.5 + 2.5 + 2.5 + 5.0 + 4.5 + 2.0 = 19.0 ثانية بالتمام والكمال!