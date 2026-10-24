from manim import *
import numpy as np

from episode_03_common import (
    MOVE, DURATION, FLIGHT_TIME, UNIT, AXES_CENTER,
    SPACE_COLOR, TIME_COLOR, GOLD_LIGHT, GOLD_BRIGHT, COPPER_TERRA, IVORY_WHITE,
    MachAxes3D, make_helicopter, fly_along_3d, MachTimeSlider,
    _clear, _hud, _ar, _seg, _LiveNumber
)


def play_scene08(scene: Scene):
    is_3d = isinstance(scene, ThreeDScene)
    if is_3d:
        scene.set_camera_orientation(phi=0, theta=-90 * DEGREES)

    mx, my, mz = MOVE

    frame_mobs = [m for m in (getattr(scene, "frame", None), getattr(scene, "neon_overlay", None)) if m is not None]
    if is_3d and frame_mobs:
        _hud(scene, *frame_mobs)

    # 1. التأسيس (2.0s إجمالي)
    title = _ar("الطيارة اتحركت: 3 متر شرق • 4 متر شمال • 5 متر أرتفاع — في 10 ثواني", 22, GOLD_LIGHT).to_edge(UP, buff=0.5).shift(RIGHT * 1.6)
    _hud(scene, title)

    axes = MachAxes3D(
        center=AXES_CENTER, grid_step=UNIT,
        x_range=(0, 6), y_range=(0, 6), z_range=(0, 6), show_negative_arrows=False,
        show_minor_ticks=False, number_font_size=13,
    )
    O = axes.get_origin()

    def P(x, y, z):
        return O + np.array([x, y, z]) * UNIT

    SCREEN_RIGHT = np.array([np.cos(np.radians(35)), np.sin(np.radians(35)), 0.0])

    def ar_label(txt, letter_mob, gap=0.42, color=GOLD_LIGHT):
        t = _ar(txt, 18, color, True)
        t.set_opacity(0.92)
        t.move_to(letter_mob.get_center() + SCREEN_RIGHT * gap)
        return t

    ar_labels = VGroup(
        ar_label("شرق", axes.x_label),
        ar_label("شمال", axes.y_label, gap=0.66),
        ar_label("أرتفاع", axes.z_label, gap=0.40),
    )

    heli = make_helicopter(scale=0.55)
    heli.set_pose(P(0, 0, 0.0), heading=float(np.arctan2(my, mx)))
    heli.start_rotors(scene)

    def rel():
        return (heli._pos - O) / UNIT

    def frac():
        return float(np.clip(rel()[0] / mx, 0, 1))

    # العداد الموحد
    t_label = _ar("الزمن", 22, TIME_COLOR, True)
    t_unit = _ar("ثانية", 22, TIME_COLOR)
    timer_ring = RoundedRectangle(
        corner_radius=0.18, width=2.9, height=1.5,
        stroke_color=TIME_COLOR, stroke_width=2.2, fill_color="#17100A", fill_opacity=0.9,
    ).move_to([4.3, 1.95, 0])
    t_label.move_to(timer_ring.get_top() + DOWN * 0.32)
    t_unit.move_to(timer_ring.get_center() + np.array([0.85, -0.2, 0]))
    timer_static = VGroup(timer_ring, t_label, t_unit)

    slider = MachTimeSlider(center=[4.3, 0.50, 0], width=3.9, t_max=DURATION, number_font_size=18, track_width=7)
    slider.register_hud(scene)
    timer_center = timer_ring.get_center() + np.array([-0.45, -0.17, 0])
    t_live = _LiveNumber(scene, lambda: DURATION * frac(), lambda: timer_center,
                         decimals=1, font_size=56, color=IVORY_WHITE)

    finals = ["3", "4", "5", "10"]
    final_tex = [MathTex(f, font_size=64) for f in finals]
    parts = VGroup(
        MathTex(r"(", font_size=80),
        final_tex[0], MathTex(r",", font_size=64),
        final_tex[1], MathTex(r",", font_size=64),
        final_tex[2], MathTex(r",", font_size=64),
        final_tex[3],
        MathTex(r")", font_size=80),
    ).arrange(RIGHT, buff=0.42, aligned_edge=DOWN).move_to([3.45, -0.85, 0])
    slot_centers = [ft.get_center() for ft in final_tex]
    slot_colors = (SPACE_COLOR, SPACE_COLOR, SPACE_COLOR, TIME_COLOR)

    paren_and_commas = VGroup(*[p for p in parts if p not in final_tex])
    for p in paren_and_commas:
        p.set_color(IVORY_WHITE)

    getters = [lambda: rel()[0], lambda: rel()[1], lambda: rel()[2], lambda: DURATION * frac()]
    slots = [
        _LiveNumber(scene, g, (lambda c=c: c), decimals=0, font_size=64, color=col)
        for g, c, col in zip(getters, slot_centers, slot_colors)
    ]
    slots_group = VGroup(*slots)

    _hud(scene, timer_static, paren_and_commas, slots_group, t_live)

    # [03:35.0 - 03:37.0]
    if is_3d:
        scene.add(axes)
        axes.face_camera(scene)
        scene.renderer.camera.add_fixed_orientation_mobjects(*ar_labels)
        scene.move_camera(
            phi=68 * DEGREES, theta=-55 * DEGREES, gamma=-4 * DEGREES, run_time=1.5,
            added_anims=[
                FadeIn(title, shift=DOWN * 0.2),
                FadeIn(heli),
                FadeIn(ar_labels),
                FadeIn(timer_static, shift=LEFT * 0.2),
                FadeIn(t_live),
                FadeIn(slider),
                FadeIn(paren_and_commas),
                FadeIn(slots_group),
            ],
        )
    else:
        scene.add(axes)
        scene.play(FadeIn(title), FadeIn(heli), FadeIn(ar_labels), FadeIn(timer_static), FadeIn(t_live), FadeIn(slider),
                   FadeIn(paren_and_commas), FadeIn(slots_group), run_time=1.5)
    scene.wait(0.5)

    # 2. الطيران وتحليق الهليكوبتر (13.5s إجمالي)
    def drop_lines():
        p = heli._pos
        foot = np.array([p[0], p[1], O[2]])
        fx = np.array([p[0], O[1], O[2]])
        fy = np.array([O[0], p[1], O[2]])
        kw = dict(dash_length=0.08, stroke_width=1.8, stroke_opacity=0.85)
        g = VGroup(
            _seg(p, foot, color=GOLD_LIGHT, **kw),
            _seg(foot, fx, color=GOLD_LIGHT, **kw),
            _seg(foot, fy, color=GOLD_LIGHT, **kw),
        )
        g.set_shade_in_3d(True)
        return g

    def rulers():
        p = heli._pos
        g = VGroup()
        for a, b, col in (
            (O, np.array([p[0], O[1], O[2]]), GOLD_BRIGHT),
            (O, np.array([O[0], p[1], O[2]]), GOLD_BRIGHT),
            (O, np.array([O[0], O[1], p[2]]), GOLD_BRIGHT),
        ):
            if np.linalg.norm(b - a) > 1e-3:
                g.add(Line(a, b, color=col, stroke_width=6, stroke_opacity=0.9))
                g.add(Line(a, b, color=GOLD_LIGHT, stroke_width=14, stroke_opacity=0.15))
        g.set_shade_in_3d(True)
        return g

    def trail():
        p = heli._pos
        if np.linalg.norm(p - O) < 1e-3:
            return VGroup()
        g = VGroup(
            Line(O, p, color=COPPER_TERRA, stroke_width=3.2, stroke_opacity=0.9),
            Line(O, p, color=COPPER_TERRA, stroke_width=9, stroke_opacity=0.14),
        )
        g.set_shade_in_3d(True)
        return g

    drops = always_redraw(drop_lines)
    ruler_mob = always_redraw(rulers)
    trail_mob = always_redraw(trail)
    scene.add(ruler_mob, trail_mob, drops)

    slider.attach(lambda: DURATION * frac())
    goal = P(mx, my, mz)
    path = Line(P(0, 0, 0), goal)

    # [03:37.0 - 03:44.5]
    scene.play(
        fly_along_3d(heli, path, run_time=FLIGHT_TIME, rate_func=smooth, nose_down=0.12),
    )
    
    for sl in slots:
        sl.clear_updaters()
    t_live.clear_updaters()
    slider.detach()
    slider.set_time(DURATION)
    scene.play(slider.finish_animation(), run_time=0.8)
    scene.wait(1.2)

    m_nums = VGroup(*[
        MathTex(str(v), font_size=64, color=col).move_to(sc)
        for v, sc, col in zip(list(MOVE) + [DURATION], slot_centers, slot_colors)
    ])
    _hud(scene, m_nums)
    
    scene.remove(slots_group, t_live)
    for sl in slots:
        sl.dispose(scene)
    t_live.dispose(scene)

    scene.add(m_nums)
    
    t_num_static = MathTex("10.0", font_size=56, color=IVORY_WHITE).move_to(timer_center)
    _hud(scene, t_num_static)
    timer_static.add(t_num_static)
    scene.add(t_num_static)

    # [03:46.5 - 03:50.5]
    scene.play(*[Indicate(m, scale_factor=1.25, color=col) for m, col in zip(m_nums, slot_colors)], run_time=1.0)
    scene.wait(3.0)

    # 3. معنى كل خانة (18.5s إجمالي)
    heli.stop_rotors(scene)

    names = ["شرق", "شمال", "أرتفاع", "زمن"]
    name_cols = [SPACE_COLOR, SPACE_COLOR, SPACE_COLOR, TIME_COLOR]
    name_txt = VGroup(*[
        _ar(n, 22, c, True).next_to(ft, DOWN, buff=0.35)
        for n, c, ft in zip(names, name_cols, final_tex)
    ])
    _hud(scene, name_txt)

    # [03:50.5 - 04:01.0]
    scene.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in name_txt], lag_ratio=0.35), run_time=2.0)
    scene.wait(8.5)

    left_x = final_tex[0].get_left()[0] - 0.05
    mid_x = final_tex[2].get_right()[0] + 0.05
    y_b = name_txt.get_bottom()[1] - 0.12
    br_space = Brace(Line([left_x, y_b, 0], [mid_x, y_b, 0]), direction=DOWN, color=SPACE_COLOR, buff=0.05)
    br_time = Brace(Line([final_tex[3].get_left()[0] - 0.05, y_b, 0], [final_tex[3].get_right()[0] + 0.05, y_b, 0]),
                    direction=DOWN, color=TIME_COLOR, buff=0.05)
    cap_space = _ar("3 أرقام للمكان", 19, SPACE_COLOR).next_to(br_space, DOWN, buff=0.12)
    cap_time = _ar("رقم للزمن", 19, TIME_COLOR).next_to(br_time, DOWN, buff=0.12)
    brs = VGroup(br_space, br_time, cap_space, cap_time)
    _hud(scene, brs)

    # [04:01.0 - 04:09.0]
    scene.play(Create(br_space), Create(br_time), FadeIn(cap_space), FadeIn(cap_time), run_time=1.5)
    scene.wait(6.5)

    # 4. الرقم الرابع (9.0s إجمالي)
    # [04:09.0 - 04:18.0]
    box4 = SurroundingRectangle(m_nums[3], buff=0.18, color=TIME_COLOR, stroke_width=3, corner_radius=0.12)
    q = _ar("مفيش محور رابع أرسمه!", 21, TIME_COLOR, True)
    q.move_to([4.3, 0.40, 0])
    pointer = Arrow(q.get_bottom() + DOWN * 0.05, box4.get_top() + UP * 0.05, buff=0.05,
                    color=TIME_COLOR, stroke_width=3, max_tip_length_to_length_ratio=0.25)
    _hud(scene, box4, q, pointer)
    
    scene.play(FadeOut(slider), Create(box4), FadeIn(q, shift=DOWN * 0.1), GrowArrow(pointer), run_time=1.2)
    _clear(scene, slider)
    if is_3d:
        scene.renderer.camera.remove_fixed_in_frame_mobjects(slider)
        for sub in slider.get_family():
            scene.renderer.camera.remove_fixed_in_frame_mobjects(sub)

    scene.wait(7.8)

    # 5. تسليم المشهد
    ruler_mob.clear_updaters()
    trail_mob.clear_updaters()
    drops.clear_updaters()

    leaving_mobs = [title, brs, box4, q, pointer]
    scene.play(*[FadeOut(m) for m in leaving_mobs], run_time=1.0)
    _clear(scene, *leaving_mobs)
    scene.wait(1.0)

    scene.mach_drawing = {
        "axes": axes,
        "O": O,
        "P_func": P,
        "goal": goal,
        "heli": heli,
        "ar_labels": ar_labels,
        "rulers": ruler_mob,
        "trail": trail_mob,
        "drops": drops,
        "timer_static": timer_static,
        "paren_and_commas": paren_and_commas,
        "slot_centers": slot_centers,
        "slot_colors": slot_colors,
        "name_txt": name_txt,
        "m_nums": m_nums,
    }


class Scene08(ThreeDScene):
    def construct(self):
        play_scene08(self)