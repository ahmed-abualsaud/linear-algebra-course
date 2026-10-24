from manim import *
import numpy as np

from common.palette import (
    STONE_AXIS,
    GOLD_LIGHT,
    GOLD_BRIGHT,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.mobjects.characters import mach_stick_figure
from common.mobjects.coordinate_systems import MachAxes1D, MachAxes2D, MachAxes3D
from common.mobjects.vectors import MachVector, MachVector3D
from common.mobjects.dialogue import thought_bubble


# ======================================================================
# أدوات مساعدة للأمان الهندسي والإخراج
# ======================================================================
def _clear(scene, *mobs):
    """حذف جذري ونظيف للكائنات وكل عائلتها المتشعبة من المشهد."""
    fam = []
    for m in mobs:
        if m is not None:
            fam += m.get_family()
    scene.remove(*fam)


def _hud(scene, *mobs):
    """سجّل العناصر كـ HUD ثابتة على الشاشة بدون إضافتها للمشهد."""
    if isinstance(scene, ThreeDScene):
        scene.renderer.camera.add_fixed_in_frame_mobjects(*mobs)
    return mobs[0] if len(mobs) == 1 else mobs


def _shake_camera(scene, run_time, amp=0.012):
    """اهتزاز خفيف لعدسة الكاميرا لحظة صدمة فشل البعد الرابع."""
    cam = scene.renderer.camera
    base_t, base_p = cam.get_theta(), cam.get_phi()
    dummy = Mobject()

    def f(_m, a):
        env = np.sin(np.pi * a)
        scene.set_camera_orientation(
            phi=base_p + amp * env * np.sin(70 * a),
            theta=base_t + amp * env * np.sin(53 * a + 1.0),
        )

    return UpdateFromAlphaFunc(dummy, f, run_time=run_time, rate_func=linear)


def play_scene06(scene: Scene):
    """
    المشهد السادس: كسر حاجز الأبعاد (المدة: 36.0 ثانية من 02:19.0 إلى 02:55.0)
    """
    is_3d = isinstance(scene, ThreeDScene)

    _frame_mobs = [
        m for m in (getattr(scene, "frame", None), getattr(scene, "neon_overlay", None))
        if m is not None
    ]
    if is_3d and _frame_mobs:
        _hud(scene, *_frame_mobs)

    BUFF_TITLE = 0.35
    AXES_CENTER_2D = DOWN * 0.45
    AXES_CENTER_3D = RIGHT * 1.15 + DOWN * 0.35

    # ==============================================================
    # 1. فضاء البعد الواحد (1D) (3.0s إجمالي)
    # ==============================================================
    # [02:19.0 - 02:22.0]: "لان في المثال الاول انا مضطر اما ارسملك سهم في بعد واحد..."
    title_1d = MarkupText("1D  |  بُعد خطي واحد", font="Cairo", font_size=23, color=GOLD_LIGHT)
    title_1d.to_edge(UP, buff=BUFF_TITLE)

    axes_1d = MachAxes1D(
        center=AXES_CENTER_2D,
        x_length=6.5,
        grid_step=0.6,
    )

    origin_pt = axes_1d.c2p(0)
    spark_core = Dot(origin_pt, radius=0.06, color=GOLD_BRIGHT)
    spark_halo = Dot(origin_pt, radius=0.24, color=GOLD_BRIGHT).set_opacity(0.18)
    spark = VGroup(spark_halo, spark_core)

    vec_1d = MachVector(
        start=origin_pt,
        end=axes_1d.c2p(2.5),
        color=COPPER_TERRA,
        stroke_width=3.6,
        tip_length=0.22,
    )

    _hud(scene, title_1d)

    scene.play(FadeIn(spark, scale=0.3), FadeIn(title_1d, shift=DOWN * 0.15), run_time=0.5)
    axes_1d.animate_creation(scene, run_time=1.2)

    scene.play(
        GrowFromPoint(vec_1d, point=origin_pt),
        FadeOut(spark, scale=2.0),
        run_time=0.8,
        rate_func=rush_from,
    )
    scene.wait(0.5)

    # ==============================================================
    # 2. الانبثاق الهندسي للبعد الثاني (2D) (2.5s إجمالي)
    # ==============================================================
    # [02:22.0 - 02:24.5]: "...او بعدين متعامدين..."
    title_2d = MarkupText("2D  |  مستوى ثنائي الأبعاد", font="Cairo", font_size=23, color=GOLD_LIGHT)
    title_2d.to_edge(UP, buff=BUFF_TITLE)

    axes_2d = MachAxes2D(
        center=AXES_CENTER_2D,
        x_length=6.5,
        y_length=6.0,
        grid_step=0.6,
    )
    o2 = axes_2d.c2p(0, 0)

    vec_2d_target = MachVector(
        start=o2,
        end=axes_2d.c2p(2.5, 2.0),
        color=COPPER_TERRA,
        stroke_width=3.6,
    )

    ripple = Circle(radius=0.08, color=GOLD_BRIGHT, stroke_width=3.0).move_to(o2)
    scene.add(ripple)

    _hud(scene, title_2d)

    axes_2d_all = VGroup(
        axes_2d.axes,
        axes_2d.grid,
        axes_2d.ticks,
        axes_2d.minor_ticks,
        axes_2d.labels,
        getattr(axes_2d, "origin", VMobject()),
        getattr(axes_2d, "axis_labels", VMobject()),
    )

    scene.play(
        FadeOut(title_1d, shift=UP * 0.12),
        FadeIn(title_2d, shift=UP * 0.12),
        FadeOut(axes_1d),
        ripple.animate.scale(18).set_stroke(opacity=0),
        GrowFromPoint(axes_2d.axes, point=o2),
        LaggedStart(
            FadeIn(axes_2d.grid, scale=0.94),
            FadeIn(axes_2d.ticks),
            FadeIn(axes_2d.minor_ticks),
            FadeIn(axes_2d.labels),
            FadeIn(getattr(axes_2d, "origin", VMobject())),
            FadeIn(getattr(axes_2d, "axis_labels", VMobject())),
            lag_ratio=0.08,
        ),
        Transform(vec_1d, vec_2d_target),
        run_time=1.8,
        rate_func=smooth,
    )
    _clear(scene, ripple, axes_1d, title_1d)
    scene.wait(0.7)

    # ==============================================================
    # 3. التحليق ثلاثي الأبعاد (3D) (3.5s إجمالي)
    # ==============================================================
    # [02:24.5 - 02:28.0]: "...او تلات ابعاد متعامدة عشان مخك يقدر يتخيله"
    title_3d = MarkupText("3D  |  فضاء ثلاثي الأبعاد", font="Cairo", font_size=23, color=GOLD_LIGHT)
    title_3d.to_edge(UP, buff=BUFF_TITLE)

    axes_3d = MachAxes3D(
        center=AXES_CENTER_3D,
        x_length=6.5,
        y_length=6.0,
        z_length=4.5,
        grid_step=0.6,
        show_xz_grid=False,
        show_yz_grid=False,
    )

    VEC_3D_TARGET = (2.2, 1.6, 3.0)
    vec_3d = MachVector3D(
        start=axes_3d.c2p(0, 0, 0),
        end=axes_3d.c2p(*VEC_3D_TARGET),
        color=COPPER_TERRA,
        stroke_width=4.2,
        tip_length=0.34,
    )

    ground_proj = axes_3d.c2p(VEC_3D_TARGET[0], VEC_3D_TARGET[1], 0)
    lift_line = DashedLine(
        ground_proj,
        axes_3d.c2p(*VEC_3D_TARGET),
        dash_length=0.07,
        color=GOLD_LIGHT,
        stroke_width=1.8,
        stroke_opacity=0.85,
    )
    tip_dot_3d = Dot3D(axes_3d.c2p(*VEC_3D_TARGET), radius=0.065, color=COPPER_TERRA)

    if hasattr(axes_3d, "face_camera"):
        axes_3d.face_camera(scene)
    _hud(scene, title_3d)

    if is_3d:
        scene.move_camera(
            phi=64 * DEGREES,
            theta=-42 * DEGREES,
            added_anims=[
                FadeOut(title_2d, shift=UP * 0.12),
                FadeIn(title_3d, shift=UP * 0.12),
                FadeOut(axes_2d_all),
                FadeIn(axes_3d),
                Transform(vec_1d, vec_3d),
            ],
            run_time=2.0,
            rate_func=smooth,
        )
    else:
        scene.play(
            FadeOut(title_2d, shift=UP * 0.12),
            FadeIn(title_3d, shift=UP * 0.12),
            FadeOut(axes_2d_all),
            FadeIn(axes_3d),
            Transform(vec_1d, vec_3d),
            run_time=2.0,
            rate_func=smooth,
        )

    _clear(scene, axes_2d_all, axes_2d, title_2d)

    scene.play(
        Create(lift_line),
        FadeIn(tip_dot_3d, scale=0.5),
        run_time=0.8,
    )

    if is_3d:
        scene.begin_ambient_camera_rotation(rate=0.06)
    scene.wait(0.7)

    # ==============================================================
    # 4. مأزق البعد الرابع (4D) (5.5s إجمالي)
    # ==============================================================
    # [02:28.0 - 02:33.5]: "لكن لو زاد عدد الابعاد اكتر من كدة مخك هيخليك تلف حوالين نفسك!"
    o3 = axes_3d.c2p(0, 0, 0)
    end4 = axes_3d.c2p(2.2, -2.2, 2.2)
    impossible_axis = Line(o3, end4, color=RED_B, stroke_width=3.2)

    avatar = mach_stick_figure(pose="thinking", scale=0.75)
    final_avatar_pos = LEFT * 4.4 + UP * 0.2
    avatar.move_to(final_avatar_pos).shift(LEFT * 3.5)

    _hud(scene, avatar)
    scene.add(avatar)

    scene.play(
        avatar.animate.move_to(final_avatar_pos),
        Create(impossible_axis),
        run_time=0.9,
        rate_func=rush_from,
    )

    box, dots, mark, d_s, d_e = thought_bubble(
        r"4D\ ?",
        anchor_head=avatar.head,
        color=GOLD_LIGHT,
        text_color=GOLD_BRIGHT,
        font_size=28,
        buff=0.35,
        use_math=True,
    )

    _hud(scene, box, dots, mark)

    scene.play(
        LaggedStart(
            FadeIn(dots, lag_ratio=0.2),
            FadeIn(box, scale=0.85),
            Write(mark),
            lag_ratio=0.15,
        ),
        run_time=0.8,
    )

    scene.play(
        Rotate(impossible_axis, angle=PI * 1.2, axis=UP + RIGHT, about_point=o3),
        run_time=1.5,
        rate_func=smooth,
    )

    if is_3d:
        scene.stop_ambient_camera_rotation()

    anims_shake = [
        Wiggle(impossible_axis, scale_value=1.18, rotation_angle=0.08 * TAU),
    ]
    if is_3d:
        anims_shake.append(_shake_camera(scene, run_time=0.8, amp=0.014))
    scene.play(*anims_shake, run_time=0.8)

    n_shards = 10
    rng = np.random.default_rng(12)
    end_now = impossible_axis.get_end()
    pts = [o3 + (end_now - o3) * (i / n_shards) for i in range(n_shards + 1)]
    shards = VGroup(*[
        Line(pts[i], pts[i + 1], color=RED_B, stroke_width=3.2) for i in range(n_shards)
    ])
    scene.remove(impossible_axis)
    scene.add(shards)

    scene.play(
        LaggedStart(*[
            s.animate.shift(rng.normal(size=3) * 0.45).rotate(rng.uniform(-1.5, 1.5)).set_stroke(opacity=0)
            for s in shards
        ], lag_ratio=0.04),
        box.animate.set_stroke(RED_B),
        run_time=1.0,
    )
    _clear(scene, shards, impossible_axis)
    scene.wait(0.5)

    # ==============================================================
    # 5. التلاشي وضبط الكاميرا في العتمة (1.5s إجمالي)
    # ==============================================================
    # [02:33.5 - 02:35.0]: "وعجزي عن الرسم وعجز مخنا في تخيل ده..."
    all_3d_objects = [
        axes_3d,
        vec_1d,
        vec_3d,
        lift_line,
        tip_dot_3d,
        title_3d,
        avatar,
        box,
        dots,
        mark,
    ]

    scene.play(
        LaggedStart(*[FadeOut(m, scale=0.9) for m in all_3d_objects if m in scene.mobjects], lag_ratio=0.04),
        run_time=1.0,
    )

    if is_3d:
        scene.remove_fixed_in_frame_mobjects(title_3d, avatar, box, dots, mark)
        scene.set_camera_orientation(phi=0, theta=-90 * DEGREES)

    _clear(scene, *all_3d_objects)
    scene.wait(0.5)

    # ==============================================================
    # 6. الحل الجبري: التمدد الفيزيائي الناعم للقائمة (16.5s إجمالي)
    # ==============================================================
    title_algebra = MarkupText(
        "الحل الجبري: كسر قيود الفضاء الحسي",
        font="Cairo",
        font_size=25,
        color=GOLD_LIGHT,
    ).to_edge(UP, buff=0.75)

    avatar_algebra = mach_stick_figure(pose="explaining", scale=0.78)
    avatar_algebra.move_to(LEFT * 1.9 + UP * 0.25)

    def make_brackets(top_y, bot_y, x_left, x_right):
        tick_len = 0.16
        left_b = VMobject(color=IVORY_WHITE, stroke_width=2.5)
        left_b.set_points_as_corners([
            [x_left + tick_len, top_y, 0],
            [x_left, top_y, 0],
            [x_left, bot_y, 0],
            [x_left + tick_len, bot_y, 0]
        ])
        right_b = VMobject(color=IVORY_WHITE, stroke_width=2.5)
        right_b.set_points_as_corners([
            [x_right - tick_len, top_y, 0],
            [x_right, top_y, 0],
            [x_right, bot_y, 0],
            [x_right - tick_len, bot_y, 0]
        ])
        return VGroup(left_b, right_b)

    X_CENTER = 1.35
    X_L = X_CENTER - 0.32
    X_R = X_CENTER + 0.32
    TOP_Y = 2.05
    ROW_SPACING = 0.54

    y1 = TOP_Y - 0.36
    y2 = y1 - ROW_SPACING
    y3 = y2 - ROW_SPACING
    y4 = y3 - ROW_SPACING
    y_dots = y4 - ROW_SPACING * 0.85
    yn = y_dots - ROW_SPACING * 0.95

    bot_1d = y1 - 0.36
    bot_2d = y2 - 0.36
    bot_3d = y3 - 0.36
    bot_nd = yn - 0.36

    brackets_1d = make_brackets(TOP_Y, bot_1d, X_L, X_R)
    brackets_2d = make_brackets(TOP_Y, bot_2d, X_L, X_R)
    brackets_3d = make_brackets(TOP_Y, bot_3d, X_L, X_R)
    brackets_nd = make_brackets(TOP_Y, bot_nd, X_L, X_R)

    eq_sign = MathTex(r"\mathbf{v} =", font_size=36, color=IVORY_WHITE)
    eq_sign.next_to(brackets_1d[0], LEFT, buff=0.25).set_y((TOP_Y + bot_1d) / 2)

    eq_y_2d = (TOP_Y + bot_2d) / 2
    eq_y_3d = (TOP_Y + bot_3d) / 2
    eq_y_nd = (TOP_Y + bot_nd) / 2

    elem_x1 = MathTex(r"x_1", font_size=34, color=IVORY_WHITE).move_to([X_CENTER, y1, 0])
    elem_x2 = MathTex(r"x_2", font_size=34, color=IVORY_WHITE).move_to([X_CENTER, y2, 0])
    elem_x3 = MathTex(r"x_3", font_size=34, color=IVORY_WHITE).move_to([X_CENTER, y3, 0])
    elem_x4 = MathTex(r"x_4", font_size=34, color=IVORY_WHITE).move_to([X_CENTER, y4, 0])
    elem_dots = MathTex(r"\vdots", font_size=34, color=IVORY_WHITE).move_to([X_CENTER, y_dots + 0.05, 0])
    elem_xn = MathTex(r"x_n", font_size=34, color=IVORY_WHITE).move_to([X_CENTER, yn, 0])

    badge_1d = Text("1-Dimension", font="Cairo", font_size=19, color=GOLD_LIGHT).next_to(brackets_1d, DOWN, buff=0.35)
    badge_2d = Text("2-Dimensions", font="Cairo", font_size=19, color=GOLD_LIGHT).next_to(brackets_2d, DOWN, buff=0.35)
    badge_3d = Text("3-Dimensions", font="Cairo", font_size=19, color=GOLD_LIGHT).next_to(brackets_3d, DOWN, buff=0.35)
    badge_nd = Text("n-Dimensions", font="Cairo", font_size=19, color=GOLD_LIGHT).next_to(brackets_nd, DOWN, buff=0.35)

    # 1. الظهور الأولي (1D)
    # [02:35.0 - 02:36.8]: "...لا يمنع اطلاقاً..."
    scene.play(
        FadeIn(title_algebra, shift=DOWN * 0.2),
        FadeIn(avatar_algebra, shift=RIGHT * 0.25),
        Write(eq_sign),
        Create(brackets_1d),
        Write(elem_x1),
        FadeIn(badge_1d, shift=UP * 0.1),
        run_time=1.0,
    )
    scene.wait(0.8)

    # 2. تمدد القائمة لـ 2D
    # [02:36.8 - 02:38.3]: "...وجود متجهات..."
    scene.play(
        Transform(brackets_1d, brackets_2d),
        eq_sign.animate.set_y(eq_y_2d),
        Transform(badge_1d, badge_2d),
        FadeIn(elem_x2, shift=DOWN * 0.2),
        run_time=0.9,
        rate_func=smooth,
    )
    scene.wait(0.6)

    # 3. تمدد القائمة لـ 3D
    # [02:38.3 - 02:40.0]: "...في 4 ابعاد او اي عدد من الابعاد"
    scene.play(
        Transform(brackets_1d, brackets_3d),
        eq_sign.animate.set_y(eq_y_3d),
        Transform(badge_1d, badge_3d),
        FadeIn(elem_x3, shift=DOWN * 0.2),
        run_time=0.9,
        rate_func=smooth,
    )
    # وقفة مع نهاية جملة الأبعاد وقبل بدء جملة القائمة (02:40.0 - 02:42.5)
    scene.wait(2.5)

    # 4. التمدد الأكبر لـ n-Dimensions
    # [02:42.5 - 02:45.3]: "علشان كده طريقة تقديم المتجه كليست او قائمة من الارقام..."
    scene.play(
        Transform(brackets_1d, brackets_nd),
        eq_sign.animate.set_y(eq_y_nd),
        Transform(badge_1d, badge_nd),
        LaggedStart(
            FadeIn(elem_x4, shift=DOWN * 0.15),
            FadeIn(elem_dots, shift=DOWN * 0.15),
            FadeIn(elem_xn, shift=DOWN * 0.15),
            lag_ratio=0.15,
        ),
        run_time=1.8,
        rate_func=smooth,
    )
    scene.wait(1.0)

    # 5. بطاقة الاستنتاج في الأسفل
    # [02:45.3 - 02:51.5]: "...هتخليني اقدر اوصف متجهات بأي عدد من الابعاد انا عاوزه"
    summary_box = RoundedRectangle(
        corner_radius=0.18,
        width=7.2,
        height=0.85,
        color=GOLD_LIGHT,
        stroke_width=1.2,
        fill_color="#1E1A16",
        fill_opacity=0.88,
    ).to_edge(DOWN, buff=1.15).shift(RIGHT * 0.6)

    summary_text = MarkupText(
        "ميزة قائمة الأرقام: حرية مطلقة تمتد إلى ما لا نهاية من الأبعاد!",
        font="Cairo",
        font_size=18,
        color=GOLD_LIGHT,
    ).move_to(summary_box)

    scene.play(
        FadeIn(summary_box, shift=UP * 0.2),
        FadeIn(summary_text, shift=UP * 0.2),
        run_time=1.0,
        rate_func=rush_from,
    )
    # مهلة استيعاب كاملة خلال السكتة الطويلة في الصوت (02:46.3 - 02:51.5)
    scene.wait(5.2)

    # ==============================================================
    # 7. تلاشي المشهد السادس بالكامل (2.0s إجمالي)
    # ==============================================================
    # [02:51.5 - 02:55.0]: تفريغ المشهد بهدوء قبل بدء المشهد السابع عند 02:55.0
    scene06_final_mobs = [
        title_algebra,
        avatar_algebra,
        eq_sign,
        brackets_1d,
        brackets_2d,
        brackets_3d,
        brackets_nd,
        elem_x1,
        elem_x2,
        elem_x3,
        elem_x4,
        elem_dots,
        elem_xn,
        badge_1d,
        summary_box,
        summary_text,
    ]

    scene.play(
        LaggedStart(
            *[FadeOut(m, scale=0.92) for m in scene06_final_mobs if m in scene.mobjects],
            lag_ratio=0.03,
        ),
        run_time=1.2,
    )
    _clear(scene, *scene06_final_mobs)
    scene.wait(0.8)

    if is_3d and _frame_mobs:
        scene.renderer.camera.remove_fixed_in_frame_mobjects(*_frame_mobs)

    # المجموع: 3.0 + 2.5 + 3.5 + 5.5 + 1.5 + 16.5 + 2.0 = 36.0 ثانية بالتمام والكمال!