from manim import *
import numpy as np

from common.palette import (
    GOLD_DARK,
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_MUTED,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.mobjects.card import MachCard
from common.mobjects.characters import mach_stick_figure
from common.mobjects.helicopter import make_helicopter, fly_along_3d


# ======================================================================
# أدوات مساعدة للأمان الهندسي والإخراج
# ======================================================================
def _clear(scene, *mobs):
    """حذف جذري ونظيف للكائنات وكل عائلتها من المشهد."""
    fam = []
    for m in mobs:
        if m is not None:
            fam += m.get_family()
    scene.remove(*fam)


def _hud(scene, *mobs):
    """تثبيت العناصر كـ HUD للشاشات ثنائية وثلاثية الأبعاد."""
    if isinstance(scene, ThreeDScene):
        scene.renderer.camera.add_fixed_in_frame_mobjects(*mobs)
    return mobs[0] if len(mobs) == 1 else mobs


def play_scene07(scene: Scene):
    """
    المشهد السابع: الطائرة، البعد الرابع، وهندسة الصفات (المدة: 40.0 ثانية من 02:55.0 إلى 03:35.0)
    """
    is_3d = isinstance(scene, ThreeDScene)

    # ضبط الكاميرا في المنظور المسطح الثابت (HUD 2D)
    if is_3d:
        scene.set_camera_orientation(phi=0, theta=-90 * DEGREES)

    BUFF_TITLE = 0.55

    # ==============================================================
    # 1. العنوان وحركة الطائرة (5.5s إجمالي)
    # ==============================================================
    title = Text(
        "تطبيق عملي: وصف حركة طائرة في الفضاء",
        font="Cairo",
        font_size=24,
        color=GOLD_LIGHT,
    ).to_edge(UP, buff=BUFF_TITLE)
    _hud(scene, title)

    _frame_mobs = [
        m for m in (getattr(scene, "frame", None), getattr(scene, "neon_overlay", None))
        if m is not None
    ]
    if is_3d and _frame_mobs:
        _hud(scene, *_frame_mobs)

    flight_path = CubicBezier(
        np.array([-3.9, -2.3, 0.25]),
        np.array([-1.2, -2.9, 0.7]),
        np.array([1.0, 0.6, 1.5]),
        np.array([4.4, 1.7, 1.2]),
    )

    heli = make_helicopter(scale=0.85)
    heli.set_pose(flight_path.point_from_proportion(0), heading=0.0)
    heli.start_rotors(scene)

    jet_trail = DashedVMobject(flight_path, num_dashes=30, dashed_ratio=0.55)
    jet_trail.set_color(GOLD_MUTED).set_stroke(width=1.8, opacity=0.6)
    jet_trail.set_shade_in_3d(True)

    ground = VGroup()
    for gx in range(-7, 8):
        ground.add(Line([gx, -5, 0], [gx, 5, 0], stroke_width=0.7, color=GOLD_MUTED, stroke_opacity=0.10))
    for gy in range(-5, 6):
        ground.add(Line([-7, gy, 0], [7, gy, 0], stroke_width=0.7, color=GOLD_MUTED, stroke_opacity=0.10))
    ground.set_shade_in_3d(True)

    shadow = Ellipse(width=1.5, height=0.75, stroke_width=0).set_fill(GOLD_MUTED, 0.16)
    shadow.set_shade_in_3d(True)

    def _follow_shadow(m):
        p = heli._pos
        m.move_to([p[0], p[1], 0.0])
        m.set_opacity(0.0 + 0.16 * max(0.25, 1.0 - 0.18 * p[2]))

    shadow.add_updater(_follow_shadow)

    # [02:55.0 - 02:56.5]: "تعال بقى نستخدم الطريقة دي..."
    if is_3d:
        scene.add(ground, shadow)
        scene.move_camera(
            phi=66 * DEGREES,
            theta=-60 * DEGREES,
            run_time=1.5,
            added_anims=[FadeIn(title, shift=DOWN * 0.2), FadeIn(heli), FadeIn(ground)],
        )
    else:
        scene.play(FadeIn(title, shift=DOWN * 0.2), FadeIn(heli), run_time=1.5)

    # [02:56.5 - 03:00.5]: "...واديلك مثال اوصفلك فيه حركة طيارة"
    scene.play(
        fly_along_3d(heli, flight_path, run_time=3.5, rate_func=smooth),
        Create(jet_trail),
    )
    scene.wait(0.5)

    # ==============================================================
    # 2. بناء مصفوفة الطائرة الرباعية وأقواسها الدقيقة (8.0s إجمالي)
    # ==============================================================
    shadow.clear_updaters()

    def _park(m, alpha):
        m.set_pose(scale=0.85 + (0.6 - 0.85) * alpha)
        m.set_fade(1.0 + (0.35 - 1.0) * alpha)

    park_anims = [
        UpdateFromAlphaFunc(heli, _park, suspend_mobject_updating=False),
        jet_trail.animate.set_stroke(opacity=0.2),
        FadeOut(shadow),
        FadeOut(ground),
    ]

    # [03:00.5 - 03:02.5]: "انا اخترت بطريقة ما اني اوصفها..."
    if is_3d:
        scene.move_camera(
            phi=0, theta=-90 * DEGREES,
            run_time=1.5, rate_func=smooth,
            added_anims=park_anims,
        )
    else:
        scene.play(*park_anims, run_time=1.5)
    scene.wait(0.5)

    v_flight_tex = MathTex(
        r"\mathbf{x}_{\text{flight}} = \begin{bmatrix} x \\ y \\ z \\ t \end{bmatrix}",
        font_size=38,
        color=IVORY_WHITE,
    ).move_to(LEFT * 1.5 + UP * 0.1)

    right_x = v_flight_tex.get_right()[0] + 0.08
    top_y = v_flight_tex.get_top()[1] - 0.06
    bot_y = v_flight_tex.get_bottom()[1] + 0.06
    split_y = top_y - 0.73 * (top_y - bot_y)

    line_space = Line([right_x, top_y, 0], [right_x, split_y, 0])
    line_time = Line([right_x, split_y, 0], [right_x, bot_y, 0])

    bracket_space = Brace(line_space, direction=RIGHT, buff=0.12, color=GOLD_MUTED)
    bracket_time = Brace(line_time, direction=RIGHT, buff=0.12, color=COPPER_TERRA)

    label_space = Text("3 أبعاد للمكان (الموقع الفضائي)", font="Cairo", font_size=16, color=GOLD_LIGHT)
    label_time = Text("بُعد واحد للزمن (اللحظة الحالية)", font="Cairo", font_size=16, color=COPPER_TERRA)

    label_space.next_to(bracket_space, RIGHT, buff=0.2)
    label_time.next_to(bracket_time, RIGHT, buff=0.2)

    vec_4d_tag = Text(
        "3 مكان + 1 زمن",
        font="Cairo",
        font_size=18,
        color=GOLD_BRIGHT,
    ).next_to(v_flight_tex, DOWN, buff=0.45)

    # [03:02.5 - 03:04.5]: "...بتلات ابعاد للمكان..."
    scene.play(
        Write(v_flight_tex),
        run_time=1.0,
    )
    scene.play(
        Create(bracket_space),
        FadeIn(label_space, shift=RIGHT * 0.2),
        run_time=1.0,
    )

    # [03:04.5 - 03:07.5]: "...وبعد واحد للزمن"
    scene.play(
        Create(bracket_time),
        FadeIn(label_time, shift=RIGHT * 0.2),
        FadeIn(vec_4d_tag, shift=UP * 0.1),
        run_time=1.0,
    )
    scene.wait(2.0)

    # [03:07.5 - 03:08.5]: مسح تمهيد الطائرة بالكامل
    flight_elements = [
        heli, jet_trail, v_flight_tex, bracket_space,
        bracket_time, label_space, label_time, vec_4d_tag, title
    ]
    scene.play(
        LaggedStart(*[FadeOut(m, scale=0.92) for m in flight_elements], lag_ratio=0.04),
        run_time=1.0,
    )
    heli.stop_rotors(scene)
    _clear(scene, *flight_elements, ground, shadow)
    if is_3d and _frame_mobs:
        scene.renderer.camera.remove_fixed_in_frame_mobjects(*_frame_mobs)

    # ==============================================================
    # 3. التركيز على كلمة "اخترت" (11.0s إجمالي)
    # ==============================================================
    avatar = mach_stick_figure(pose="explaining", scale=0.82)
    avatar.move_to(LEFT * 4.4 + UP * 0.05)
    _hud(scene, avatar)

    gold_hex = ManimColor(GOLD_DARK).to_hex()
    quote_text = MarkupText(
        f'أنا الذي <span foreground="{gold_hex}"><b>اخترت</b></span> هذه الصفات الأربع لوصف الطائرة!',
        font="Cairo",
        font_size=23,
        color=IVORY_WHITE,
    )
    quote_text.to_edge(UP, buff=0.48).shift(RIGHT * 0.8)
    _hud(scene, quote_text)

    target_hex = gold_hex.upper()
    chosen_chars = [
        m for m in quote_text.family_members_with_points()
        if m.get_color().to_hex().upper() == target_hex or m.get_fill_color().to_hex().upper() == target_hex
    ]

    if chosen_chars:
        chosen_box = VGroup(*chosen_chars)
        line_start = chosen_box.get_left()[0] - 0.04
        line_end = chosen_box.get_right()[0] + 0.04
        line_y = chosen_box.get_bottom()[1] - 0.12
    else:
        x_ref = quote_text.get_right()[0]
        line_start = x_ref - 1.45
        line_end = x_ref - 0.75
        line_y = quote_text.get_bottom()[1] - 0.12

    underline = Line(
        [line_start, line_y, 0],
        [line_end, line_y, 0],
        color=COPPER_TERRA,
        stroke_width=3.2,
    )
    underline_glow = Line(
        [line_start, line_y, 0],
        [line_end, line_y, 0],
        color=GOLD_BRIGHT,
        stroke_width=6.0,
        stroke_opacity=0.35,
    )
    _hud(scene, underline, underline_glow)

    # [03:08.5 - 03:10.5]: "وحط خط تحت كلمة اخترت دي!"
    scene.play(
        FadeIn(avatar, shift=RIGHT * 0.3),
        FadeIn(quote_text, shift=DOWN * 0.15),
        run_time=1.0,
    )

    # إشعال الخط المشع تحت كلمة "اخترت" بالتزامن المباشر مع الكلمة
    scene.play(
        Create(underline),
        FadeIn(underline_glow),
        run_time=0.8,
        rate_func=rush_from,
    )
    scene.wait(0.2)

    # [03:10.5 - 03:19.5]: "لان الخصائص او الصفات اللي بختارها عشان ابني بيها متجه... دي مسألة مش سهلة اطلاقاً"
    # مهلة كاملة للتأكيد على صعوبة وأهمية هذه الخطوة
    scene.wait(9.0)

    # ==============================================================
    # 4. جسر تعلم الآلة: Feature Engineering (13.5s إجمالي)
    # ==============================================================
    tech_card = MachCard(
        width=8.8,
        height=4.1,
        center=RIGHT * 1.0 + DOWN * 0.20,
        title="Feature Engineering  |  هندسة الصفات",
        show_divider=True,
        divider_style="horizontal",
        accent_color=GOLD_LIGHT,
        background_color="#100D07",
    )
    _hud(scene, tech_card)

    # [03:19.5 - 03:24.5]: "والا ما كانوش خصصولها فرع اسمه هندسة الصفات او feature engineering في الـ machine learning..."
    scene.play(
        tech_card.animate_shell(run_time=1.5),
    )

    card_content_y = tech_card.get_content_center()[1]
    card_cx = tech_card.get_center()[0]

    ml_vector_tex = MathTex(
        r"\mathbf{x} = \begin{bmatrix} x \\ y \\ z \\ t \\ \text{speed} \\ \text{fuel} \\ \vdots \end{bmatrix}",
        font_size=25,
        color=IVORY_WHITE,
    ).move_to([card_cx - 2.5, card_content_y, 0])

    ml_intro = Text(
        "في علم تعلم الآلة (Machine Learning):",
        font="Cairo",
        font_size=15,
        color=GOLD_LIGHT,
    )
    ml_desc_1 = Text(
        "• المتجه ليس مجرد سهم في الفراغ!",
        font="Cairo",
        font_size=14,
        color=IVORY_WHITE,
    )
    ml_desc_2 = Text(
        "• بل هو «بطاقة هوية رقمية» تجمع خصائص أي كائن.",
        font="Cairo",
        font_size=14,
        color=IVORY_WHITE,
    )
    ml_desc_3 = Text(
        "• كل بُعد = خاصية إضافية تصف الكائن (Feature).",
        font="Cairo",
        font_size=14,
        color=COPPER_TERRA,
    )

    text_column = VGroup(ml_intro, ml_desc_1, ml_desc_2, ml_desc_3).arrange(
        DOWN, aligned_edge=RIGHT, buff=0.18
    )
    text_column.move_to([card_cx + 1.4, card_content_y, 0])

    card_content = VGroup(ml_vector_tex, text_column)
    _hud(scene, card_content, ml_vector_tex, text_column)

    scene.play(
        Write(ml_vector_tex),
        LaggedStart(
            FadeIn(ml_intro, shift=LEFT * 0.15),
            FadeIn(ml_desc_1, shift=LEFT * 0.15),
            FadeIn(ml_desc_2, shift=LEFT * 0.15),
            FadeIn(ml_desc_3, shift=LEFT * 0.15),
            lag_ratio=0.15,
        ),
        run_time=2.0,
    )
    scene.wait(1.5)

    # [03:24.5 - 03:33.0]: "...وكل اللي شغال في الـ machine learning فاهم كلامي" + سكتة للتأمل
    scene.wait(8.5)

    # ==============================================================
    # 5. تلاشي المشهد السابع بالكامل (2.0s إجمالي)
    # ==============================================================
    # [03:33.0 - 03:35.0]: تفريغ المشهد بهدوء قبل بداية المشهد الثامن عند 03:35.0
    all_final = [
        avatar, quote_text, underline, underline_glow,
        tech_card, card_content, ml_vector_tex, text_column
    ]
    scene.play(
        LaggedStart(*[FadeOut(m, scale=0.94) for m in all_final if m in scene.mobjects], lag_ratio=0.03),
        run_time=1.2,
    )
    _clear(scene, *all_final)
    scene.wait(0.8)

    # المجموع: 5.5 + 8.0 + 11.0 + 13.5 + 2.0 = 40.0 ثانية بالتمام والكمال!