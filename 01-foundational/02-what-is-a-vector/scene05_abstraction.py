from manim import *
import numpy as np
from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_MUTED,
    STONE_AXIS,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.identity import turn_on_neon, turn_off_neon
from common.mobjects.characters import mach_mathematician
from common.latex import mach_math_template


def play_scene05(scene):

    # ==============================================================
    # 1. المرحلة الأولى: إشعال فريم النيون وتفكيك المعنى المادي (12.4 ث)
    # [02:04.0 -> 02:16.4 في الفيديو | 01:58.0 -> 02:09.4 في الصوت]
    # ==============================================================
    X_GAP = 1.95
    Y_ROW = 0.65

    POS_WEIGHT = np.array([-X_GAP,  Y_ROW, 0])
    POS_APPLES = np.array([  0.0,   Y_ROW, 0])
    POS_LENGTH = np.array([ X_GAP,  Y_ROW, 0])

    POS_TIME   = np.array([-X_GAP, -Y_ROW, 0])
    POS_FLOOR  = np.array([  0.0,  -Y_ROW, 0])
    POS_ANGLE  = np.array([ X_GAP, -Y_ROW, 0])

    # العناصر مع وحداتها الفيزيائية
    item_weight = MathTex(r"3.5\text{ kg}", tex_template=mach_math_template, font_size=30, color=IVORY_WHITE).move_to(POS_WEIGHT)
    item_apples = MarkupText("4 تفاحات", font="Cairo", font_size=20, color=IVORY_WHITE).move_to(POS_APPLES)
    item_length = MathTex(r"3\text{ m}", tex_template=mach_math_template, font_size=30, color=IVORY_WHITE).move_to(POS_LENGTH)

    item_time   = MathTex(r"7\text{ s}", tex_template=mach_math_template, font_size=30, color=IVORY_WHITE).move_to(POS_TIME)
    item_floor  = MarkupText("الدور 10", font="Cairo", font_size=20, color=IVORY_WHITE).move_to(POS_FLOOR)
    item_angle  = MathTex(r"180^\circ", tex_template=mach_math_template, font_size=30, color=IVORY_WHITE).move_to(POS_ANGLE)

    all_items = [item_weight, item_apples, item_length, item_time, item_floor, item_angle]

    # الأرقام الصافية المجردة في نفس المواقع
    num_weight = MathTex(r"3.5", tex_template=mach_math_template, font_size=34, color=GOLD_LIGHT).move_to(POS_WEIGHT)
    num_apples = MathTex(r"4",   tex_template=mach_math_template, font_size=34, color=GOLD_LIGHT).move_to(POS_APPLES)
    num_length = MathTex(r"3",   tex_template=mach_math_template, font_size=34, color=GOLD_LIGHT).move_to(POS_LENGTH)

    num_time   = MathTex(r"7",   tex_template=mach_math_template, font_size=34, color=GOLD_LIGHT).move_to(POS_TIME)
    num_floor  = MathTex(r"10",  tex_template=mach_math_template, font_size=34, color=GOLD_LIGHT).move_to(POS_FLOOR)
    num_angle  = MathTex(r"180", tex_template=mach_math_template, font_size=34, color=GOLD_LIGHT).move_to(POS_ANGLE)

    abstract_numbers = VGroup(num_weight, num_apples, num_length, num_time, num_floor, num_angle)

    # أ) إشعال فريم النيون وظهور العناصر مع بداية جملة:
    # "لكن إجابة عالم الرياضيات..."
    turn_on_neon(scene, run_time=0.8)

    scene.play(
        LaggedStart(*[FadeIn(it, shift=UP * 0.15) for it in all_items], lag_ratio=0.08),
        run_time=0.8,
    )
    # استماع أثناء "...هتبينلك إن العدد نفسه لا يمثل أي شيء من ده إطلاقاً..."
    scene.wait(2.8)

    # ب) خطوط الشطب على الوحدات مع جملة "...لا يمثل أي شيء من ده إطلاقاً"
    slash_lines = VGroup(*[
        Line(
            it.get_center() + LEFT * 0.42 + DOWN * 0.18,
            it.get_center() + RIGHT * 0.42 + UP * 0.18,
            stroke_width=2.4, color=COPPER_TERRA, stroke_opacity=0.85,
        )
        for it in all_items
    ])

    scene.play(Create(slash_lines), run_time=0.8)
    
    # "...كل دي عبارة عن أمثلة ومواقف بنستخدم فيها الأعداد"
    scene.wait(2.2)

    # ج) تلاشي الوحدات وبقاء الأرقام الذهبية المجردة الصافية
    scene.play(
        FadeOut(VGroup(*all_items)),
        FadeOut(slash_lines),
        FadeIn(abstract_numbers, scale=1.05),
        run_time=0.8,
    )
    # ثبات الأرقام الذهبية المجردة ليراها المشاهد بوضوح
    scene.wait(3.4)

    # إطفاء فريم النيون بهدوء
    turn_off_neon(scene, run_time=0.8)

    # ==============================================================
    # 2. المرحلة الثانية: ظهور عالم الرياضيات وكارت التجريد وخط الأعداد (8.4 ث)
    # [02:16.4 -> 02:24.8 في الفيديو | 02:09.4 -> 02:17.8 في الصوت]
    # ==============================================================
    mathematician = mach_mathematician(
        color=COPPER_TERRA,
        accent_color=GOLD_LIGHT,
        pose="explaining",
        scale=0.92,
        blink=True,
        breathing=True,
        glasses=True,
        tie_type="bowtie",
    ).shift(LEFT * 4.2 + DOWN * 0.3)

    card_bg = RoundedRectangle(
        corner_radius=0.18, width=5.0, height=1.35,
        stroke_width=1.5, color=GOLD_LIGHT,
        fill_color="#18140E", fill_opacity=0.90,
    )
    t_main = MarkupText("مفهوم مجرد", font="Cairo", font_size=25, color=GOLD_LIGHT)
    t_sub  = MarkupText("خالٍ من أي معنى فيزيائي أو هندسي", font="Cairo", font_size=15, color=IVORY_WHITE)
    badge_content = VGroup(t_main, t_sub).arrange(DOWN, buff=0.16).move_to(card_bg.get_center())
    abstract_badge = VGroup(card_bg, badge_content).move_to([0.8, 1.9, 0])

    # خط الأعداد الرسمي
    number_line = NumberLine(
        x_range=[0, 11, 1],
        length=7.0,
        color=STONE_AXIS,
        stroke_width=1.8,
        include_numbers=True,
        include_ticks=True,
        tick_size=0.08,
        font_size=18,
    ).move_to([1.0, -0.4, 0])

    p_line_start = number_line.n2p(0)
    p_line_end   = number_line.n2p(11)

    tip_len, tip_w = 0.16, 0.06

    tip_l = Polygon(
        p_line_start + LEFT * 0.22,
        p_line_start + LEFT * (0.22 - tip_len) + UP * tip_w,
        p_line_start + LEFT * (0.22 - tip_len) + DOWN * tip_w,
        color=STONE_AXIS, fill_color=STONE_AXIS, fill_opacity=1.0, stroke_width=0,
    )

    tip_r = Polygon(
        p_line_end + RIGHT * 0.22,
        p_line_end + RIGHT * (0.22 - tip_len) + UP * tip_w,
        p_line_end + RIGHT * (0.22 - tip_len) + DOWN * tip_w,
        color=STONE_AXIS, fill_color=STONE_AXIS, fill_opacity=1.0, stroke_width=0,
    )

    ext_l = Line(p_line_start, p_line_start + LEFT * 0.22, stroke_width=1.8, color=STONE_AXIS)
    ext_r = Line(p_line_end, p_line_end + RIGHT * 0.22, stroke_width=1.8, color=STONE_AXIS)

    numline_group = VGroup(number_line, ext_l, ext_r, tip_l, tip_r)

    # المواضع على خط الأعداد
    p_3   = number_line.n2p(3)   + UP * 0.40
    p_4   = number_line.n2p(4)   + UP * 0.40
    p_7   = number_line.n2p(7)   + UP * 0.40
    p_10  = number_line.n2p(10)  + UP * 0.40
    p_3_5 = number_line.n2p(3.5) + DOWN * 0.55
    p_180 = p_line_end + RIGHT * 0.75 + UP * 0.38

    dots_on_line = VGroup(*[
        Dot(number_line.n2p(val), radius=0.055, color=GOLD_BRIGHT)
        for val in [3, 3.5, 4, 7, 10]
    ])

    guide_line_3_5 = Line(
        number_line.n2p(3.5) + DOWN * 0.05,
        number_line.n2p(3.5) + DOWN * 0.32,
        stroke_width=1.2,
        color=GOLD_LIGHT,
        stroke_opacity=0.6,
    )

    ellipsis_text = MathTex(r"\dots", font_size=28, color=GOLD_LIGHT)\
        .move_to(p_line_end + RIGHT * 0.35 + UP * 0.38)

    # "لكن العدد بالنسبة لعالم الرياضيات هو إنه عبارة عن فكرة..."
    scene.play(
        FadeIn(mathematician, shift=RIGHT * 0.3),
        FadeIn(abstract_badge, shift=UP * 0.2),
        Create(numline_group),
        num_length.animate.move_to(p_3).scale(0.85),
        num_apples.animate.move_to(p_4).scale(0.85),
        num_weight.animate.move_to(p_3_5).scale(0.85),
        num_time.animate.move_to(p_7).scale(0.85),
        num_floor.animate.move_to(p_10).scale(0.85),
        num_angle.animate.move_to(p_180).scale(0.85),
        run_time=1.8,
        rate_func=smooth,
    )

    # اشتعال النقاط الذهبية
    scene.play(
        FadeIn(dots_on_line),
        FadeIn(guide_line_3_5),
        FadeIn(ellipsis_text),
        run_time=0.6,
    )

    # استماع وتأمل أثناء "...أو مفهوم مجرد من أي مثال أو موقف"
    scene.wait(4.6)

    # تفريغ خط الأعداد وكارت التجريد (عالم الرياضيات يبقى في المشهد)
    scene.play(
        FadeOut(abstract_badge),
        FadeOut(numline_group),
        FadeOut(abstract_numbers),
        FadeOut(dots_on_line),
        FadeOut(guide_line_3_5),
        FadeOut(ellipsis_text),
        run_time=0.8,
    )
    scene.wait(0.6)

    # ==============================================================
    # 3. المرحلة الثالثة: البوابة الكونية للأعداد (عالم الأعداد) (10.2 ث)
    # [02:24.8 -> 02:35.0 في الفيديو | 02:17.8 -> 02:28.0 في الصوت]
    # ==============================================================
    portal_center = np.array([1.6, 0.0, 0])

    realm_glow = Circle(radius=2.35, stroke_width=0, fill_color=GOLD_LIGHT, fill_opacity=0.04).move_to(portal_center)
    realm_ring_outer = Circle(radius=2.10, stroke_width=1.4, color=GOLD_LIGHT, stroke_opacity=0.55).move_to(portal_center)
    realm_ring_dash = DashedVMobject(
        Circle(radius=1.85, stroke_width=1.0, color=GOLD_MUTED, stroke_opacity=0.4),
        num_dashes=48,
    ).move_to(portal_center)

    realm_title = MarkupText("عالم الأعداد", font="Cairo", font_size=23, color=GOLD_LIGHT)\
        .next_to(realm_ring_outer.get_top(), UP, buff=0.18)

    num_coords = [
        ([-0.8,  0.9, 0], r"3.5",      24),
        ([ 0.9,  1.1, 0], r"\pi",      28),
        ([-1.1, -0.4, 0], r"-10",      24),
        ([ 0.0,  0.2, 0], r"0",        28),
        ([ 1.1, -0.6, 0], r"\sqrt{2}", 26),
        ([-0.3, -1.2, 0], r"7",        24),
        ([ 0.7, -1.3, 0], r"180",      22),
    ]

    floating_nums = VGroup(*[
        MathTex(tex, tex_template=mach_math_template, font_size=fs, color=GOLD_LIGHT)\
            .move_to(portal_center + np.array(pos))
        for pos, tex, fs in num_coords
    ])

    realm_group = VGroup(realm_glow, realm_ring_outer, realm_ring_dash, realm_title, floating_nums)

    # ظهور بوابة عالم الأعداد مع جملة:
    # "وإن الأرقام أو الأعداد دي هي جزء من عالم بتعيش فيه وبيحتويها..."
    scene.play(
        FadeIn(realm_glow),
        Create(realm_ring_outer),
        Create(realm_ring_dash),
        FadeIn(realm_title),
        FadeIn(floating_nums, scale=0.8),
        run_time=1.4,
    )

    # دوران فلكي هادئ للأرقام أثناء جملة:
    # "...زي ما احنا كبشر جزء من الكون وعايشين فيه بالظبط."
    scene.play(
        Rotate(floating_nums, angle=0.10 * TAU, about_point=portal_center, rate_func=linear),
        run_time=6.4,
    )

    # ==============================================================
    # 4. تفريغ المشهد للانتقال للمشهد السادس (2.4 ث)
    # [02:32.6 -> 02:35.0 في الفيديو]
    # ==============================================================
    all_scene = Group(mathematician, realm_group)

    scene.play(
        FadeOut(all_scene),
        run_time=1.2,
    )
    # سكون الانتقال النظيف ليسلّم المشهد بدقة عند 02:35.0
    scene.wait(1.2)