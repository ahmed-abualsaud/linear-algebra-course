from manim import *
import numpy as np

from episode_03_common import (
    MOVE, DURATION, PLANK_VALUES, UNIT_NAME,
    GOLD_LIGHT, GOLD_BRIGHT, NEW_COLOR, TIME_COLOR, SPACE_COLOR, IVORY_WHITE,
    _clear, _hud, _ar, _TickLabels
)
from scene09_helicopter import play_scene09


def play_scene10(scene: Scene, keep_drawing: bool = True):
    is_3d = isinstance(scene, ThreeDScene)
    frame_mobs = [m for m in (getattr(scene, "frame", None), getattr(scene, "neon_overlay", None)) if m is not None]

    if not hasattr(scene, "mach_drawing"):
        play_scene09(scene, keep_drawing=True)

    st = scene.mach_drawing
    axes, heli, ar_labels = st["axes"], st["heli"], st["ar_labels"]
    rulers, trail, drops, O = st["rulers"], st["trail"], st["drops"], st["O"]
    goal = st["goal"]
    timer_static = st["timer_static"]
    ticks = st.get("ticks")
    if ticks is None:
        ticks = _TickLabels(scene, axes, O)
        st["ticks"] = ticks

    # 1. عناصر الشاشة بتنسيق متسع للأرقام العشرية
    title = _ar("بل أقدر أخترع وحدة قياس على مزاجي!", 22, GOLD_LIGHT).to_edge(UP, buff=0.5).shift(RIGHT * 1.6)
    _hud(scene, title)

    chip_ring = RoundedRectangle(
        corner_radius=0.2, width=3.9, height=0.72,
        stroke_color=GOLD_LIGHT, stroke_width=2.2, fill_color="#17100A", fill_opacity=0.9,
    ).move_to([4.3, 0.50, 0])
    chip_title = _ar("وحدة المسافة:", 19, GOLD_LIGHT).move_to(chip_ring.get_center() + np.array([0.95, 0, 0]))
    chip_value = _ar("متر", 24, SPACE_COLOR, True).move_to(chip_ring.get_center() + np.array([-0.85, 0, 0]))
    chip_static = VGroup(chip_ring, chip_title)
    _hud(scene, chip_static, chip_value)

    FS = 40
    new_tex = [MathTex(v, font_size=FS) for v in PLANK_VALUES] + [MathTex(str(DURATION), font_size=FS)]
    parts = VGroup(
        MathTex(r"(", font_size=FS + 14),
        new_tex[0], MathTex(r",", font_size=FS),
        new_tex[1], MathTex(r",", font_size=FS),
        new_tex[2], MathTex(r",", font_size=FS),
        new_tex[3],
        MathTex(r")", font_size=FS + 14),
    ).arrange(RIGHT, buff=0.2, aligned_edge=DOWN).move_to([3.7, -1.0, 0])
    slot_centers = [t.get_center() for t in new_tex]
    slot_colors = (SPACE_COLOR, SPACE_COLOR, SPACE_COLOR, TIME_COLOR)
    paren_and_commas = VGroup(*[p for p in parts if p not in new_tex])
    for p in paren_and_commas:
        p.set_color(IVORY_WHITE)

    m_nums = [MathTex(str(v), font_size=FS, color=c).move_to(sc)
              for v, sc, c in zip(list(MOVE) + [DURATION], slot_centers, slot_colors)]
    n_nums = [t.set_color(NEW_COLOR if i < 3 else TIME_COLOR) for i, t in enumerate(new_tex)]

    names = ["شرق", "شمال", "أرتفاع", "زمن"]
    name_txt = VGroup(*[
        _ar(n, 20, c, True).next_to(MathTex("0").move_to(sc), DOWN, buff=0.35)
        for n, c, sc in zip(names, slot_colors, slot_centers)
    ])

    plank_bar = Rectangle(width=1.5, height=0.2, stroke_color=NEW_COLOR, stroke_width=2.5,
                          fill_color=NEW_COLOR, fill_opacity=0.28)
    plank_ticks = VGroup(*[Line(plank_bar.get_left() + RIGHT * 1.5 * k / 3.9 * 1.0 + UP * 0.1,
                                plank_bar.get_left() + RIGHT * 1.5 * k / 3.9 * 1.0 + DOWN * 0.1,
                                color=NEW_COLOR, stroke_width=1.5, stroke_opacity=0.7)
                           for k in (1, 2, 3)])
    plank_lbl = _ar("1 " + UNIT_NAME, 22, NEW_COLOR, True)
    eq_lbl = VGroup(
        _ar("3.9 متر", 22, IVORY_WHITE, True),
        MathTex("=", font_size=34, color=IVORY_WHITE),
    ).arrange(RIGHT, buff=0.15)
    plank_card = VGroup(plank_bar, plank_ticks)
    plank_row = VGroup(eq_lbl, plank_lbl).arrange(RIGHT, buff=0.15)
    plank_all = VGroup(plank_card, plank_row).arrange(DOWN, buff=0.22).move_to([4.3, -2.85, 0])

    _hud(scene, title, chip_static, chip_value, paren_and_commas, name_txt,
         *m_nums, *n_nums, plank_all)

    scene.play(
        FadeIn(title, shift=DOWN * 0.15),
        FadeIn(chip_static, shift=UP * 0.1),
        FadeIn(chip_value, shift=UP * 0.1),
        FadeIn(paren_and_commas),
        *[FadeIn(n) for n in m_nums],
        FadeIn(name_txt),
        run_time=1.2,
    )
    scene.wait(5.8)

    # 3. تعريف الوحدة الجديدة ("الخشبة")
    scene.play(FadeIn(plank_all, shift=UP * 0.15), run_time=1.5)
    scene.wait(8.5)

    # 4. التحويل: متر → الخشبة
    chip_value_new = _ar(UNIT_NAME, 24, NEW_COLOR, True).move_to(chip_value)
    _hud(scene, chip_value_new)

    tags = VGroup(*[
        MathTex(r"\div 3.9", font_size=26, color=NEW_COLOR).move_to(sc + np.array([0, 0.72, 0]))
        for sc in slot_centers[:3]
    ])
    _hud(scene, tags)

    scene.play(
        FadeOut(chip_value, shift=UP * 0.2), FadeIn(chip_value_new, shift=UP * 0.2),
        chip_ring.animate.set_stroke(NEW_COLOR),
        run_time=0.8,
    )
    scene.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tags], lag_ratio=0.25), run_time=0.8)
    
    tick_anim, tick_commit = ticks.retarget("plank")
    scene.play(
        *[FadeOut(m_nums[i], shift=UP * 0.18) for i in range(3)],
        *[FadeIn(n_nums[i], shift=UP * 0.18) for i in range(3)],
        tick_anim,
        run_time=1.8,
    )
    tick_commit()
    scene.play(FadeOut(tags), run_time=0.4)
    scene.play(FadeOut(m_nums[3]), FadeIn(n_nums[3]), run_time=0.4)

    flash = Line(O, goal, color=GOLD_BRIGHT, stroke_width=9).set_shade_in_3d(True)
    scene.play(ShowPassingFlash(flash, time_width=0.7), run_time=1.0)

    box_t = SurroundingRectangle(n_nums[3], buff=0.16, color=TIME_COLOR, stroke_width=3, corner_radius=0.12)
    _hud(scene, box_t)
    scene.play(Create(box_t), run_time=0.8)
    scene.wait(2.0)

    scene.wait(11.0)

    # 5. الخروج النهائي للمشهد العاشر
    hud_outs = [title, timer_static, chip_static, chip_value_new, paren_and_commas,
                VGroup(*n_nums), name_txt, plank_all, box_t]

    if keep_drawing and is_3d:
        scene.play(*[FadeOut(m) for m in hud_outs], run_time=1.8)
        _clear(scene, *hud_outs, chip_value, tags, *m_nums)
        scene.wait(1.2)
        return

    outs = [axes, heli, ar_labels, rulers, trail, drops] + hud_outs + ticks.mobs()
    if is_3d:
        scene.move_camera(phi=0, theta=-90 * DEGREES, gamma=0, run_time=1.8,
                          added_anims=[FadeOut(m) for m in outs])
    else:
        scene.play(*[FadeOut(m) for m in outs], run_time=1.8)

    heli.stop_rotors(scene)
    ticks.dispose()
    _clear(scene, *outs, chip_value, tags, *m_nums)
    if hasattr(scene, "mach_drawing"):
        del scene.mach_drawing
    if is_3d and frame_mobs:
        scene.renderer.camera.remove_fixed_in_frame_mobjects(*frame_mobs)
    scene.wait(1.2)


class Scene10(ThreeDScene):
    def construct(self):
        play_scene10(self, keep_drawing=False)