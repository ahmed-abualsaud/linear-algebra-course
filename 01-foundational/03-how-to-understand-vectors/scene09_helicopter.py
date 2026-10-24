from manim import *
import numpy as np

from episode_03_common import (
    MOVE, DURATION, SCALE,
    GOLD_LIGHT, GOLD_BRIGHT, COPPER_TERRA, IVORY_WHITE, SPACE_COLOR, TIME_COLOR,
    _clear, _hud, _ar, _TickLabels
)
from scene08_helicopter import play_scene08


def play_scene09(scene: Scene, keep_drawing: bool = True):
    is_3d = isinstance(scene, ThreeDScene)
    frame_mobs = [m for m in (getattr(scene, "frame", None), getattr(scene, "neon_overlay", None)) if m is not None]

    if not hasattr(scene, "mach_drawing"):
        play_scene08(scene)

    st = scene.mach_drawing
    axes, O, goal = st["axes"], st["O"], st["goal"]
    heli, ar_labels = st["heli"], st["ar_labels"]
    rulers, trail, drops = st["rulers"], st["trail"], st["drops"]
    timer_static = st["timer_static"]
    paren_and_commas = st["paren_and_commas"]
    slot_centers = st["slot_centers"]
    slot_colors = st["slot_colors"]
    name_txt = st["name_txt"]
    m_nums = st["m_nums"]

    # 1. العنوان + شريحة وحدة المسافة
    title = _ar("نفس الطيارة • نفس الحركة بالظبط — بس غيّرنا وحدة قياس المسافة", 22, GOLD_LIGHT).to_edge(UP, buff=0.5).shift(RIGHT * 1.6)
    _hud(scene, title)

    chip_ring = RoundedRectangle(
        corner_radius=0.2, width=3.9, height=0.72,
        stroke_color=GOLD_LIGHT, stroke_width=2.2, fill_color="#17100A", fill_opacity=0.9,
    ).move_to([4.3, 0.50, 0])
    chip_title = _ar("وحدة المسافة:", 19, GOLD_LIGHT).move_to(chip_ring.get_center() + np.array([0.95, 0, 0]))
    chip_value = _ar("متر", 24, SPACE_COLOR, True).move_to(chip_ring.get_center() + np.array([-0.85, 0, 0]))
    chip_static = VGroup(chip_ring, chip_title)
    _hud(scene, chip_static, chip_value)

    CF = 64
    cm_vals = [str(v * SCALE) for v in MOVE] + [str(DURATION)]
    cm_tex = [MathTex(v, font_size=CF, color=c) for v, c in zip(cm_vals, slot_colors)]
    cm_parts = VGroup(
        MathTex(r"(", font_size=CF + 16),
        cm_tex[0], MathTex(r",", font_size=CF),
        cm_tex[1], MathTex(r",", font_size=CF),
        cm_tex[2], MathTex(r",", font_size=CF),
        cm_tex[3],
        MathTex(r")", font_size=CF + 16),
    ).arrange(RIGHT, buff=0.34, aligned_edge=DOWN).move_to([3.45, -0.85, 0])
    cm_centers = [t.get_center() for t in cm_tex]
    cm_pc = VGroup(*[p for p in cm_parts if p not in cm_tex])
    for p in cm_pc:
        p.set_color(IVORY_WHITE)
    cm_names = VGroup(*[
        _ar(n, 22, c, True).next_to(MathTex("0").move_to(sc), DOWN, buff=0.35)
        for n, c, sc in zip(["شرق", "شمال", "أرتفاع", "زمن"], slot_colors, cm_centers)
    ])
    _hud(scene, *cm_tex)

    ticks = st.get("ticks")
    if ticks is None:
        ticks = _TickLabels(scene, axes, O)
        st["ticks"] = ticks

    scene.play(
        FadeIn(title, shift=DOWN * 0.15),
        FadeIn(chip_static, shift=UP * 0.1),
        FadeIn(chip_value, shift=UP * 0.1),
        run_time=1.2,
    )
    scene.wait(2.8)

    flash_path = Line(O, goal, color=GOLD_BRIGHT, stroke_width=9).set_shade_in_3d(True)
    scene.play(ShowPassingFlash(flash_path, time_width=0.7), run_time=1.5)
    scene.wait(7.5)

    # 3. التحويل إلى سنتيمتر
    chip_value_new = _ar("سنتيمتر", 24, COPPER_TERRA, True).move_to(chip_value)
    _hud(scene, chip_value_new)

    tags = VGroup(*[
        MathTex(r"\times 100", font_size=30, color=COPPER_TERRA).move_to(sc + np.array([0, 0.78, 0]))
        for sc in slot_centers[:3]
    ])
    _hud(scene, tags)

    scene.play(
        FadeOut(chip_value, shift=UP * 0.2),
        FadeIn(chip_value_new, shift=UP * 0.2),
        chip_ring.animate.set_stroke(COPPER_TERRA),
        run_time=1.0,
    )
    scene.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tags], lag_ratio=0.25), run_time=1.0)

    tick_anim, tick_commit = ticks.retarget("cm")
    scene.play(
        *[FadeOut(m_nums[i], shift=UP * 0.18) for i in range(3)],
        *[FadeIn(cm_tex[i], shift=UP * 0.18) for i in range(3)],
        Transform(paren_and_commas, cm_pc),
        Transform(name_txt, cm_names),
        m_nums[3].animate.move_to(cm_centers[3]),
        tick_anim,
        run_time=2.0,
    )
    tick_commit()
    scene.play(FadeOut(tags), run_time=0.4)
    scene.play(FadeOut(m_nums[3]), FadeIn(cm_tex[3]), run_time=0.4)

    flash_path2 = Line(O, goal, color=GOLD_BRIGHT, stroke_width=9).set_shade_in_3d(True)
    scene.play(ShowPassingFlash(flash_path2, time_width=0.7), run_time=1.2)
    scene.wait(1.0)

    # 4. تثبيت الزمن
    box_t = SurroundingRectangle(cm_tex[3], buff=0.18, color=TIME_COLOR, stroke_width=3, corner_radius=0.12)
    note = _ar("الزمن زي ما هو — غيّرنا وحدة المسافة بس", 20, TIME_COLOR, True).move_to([3.45, -2.55, 0])
    _hud(scene, box_t, note)
    scene.play(Create(box_t), FadeIn(note, shift=UP * 0.1), run_time=1.2)
    scene.wait(12.8)

    # 5. الخروج
    hud_outs = [title, chip_static, chip_value_new, paren_and_commas, VGroup(*cm_tex), name_txt, box_t, note]

    if keep_drawing:
        tick_anim, tick_commit = ticks.retarget("m")
        scene.play(*[FadeOut(m) for m in hud_outs], tick_anim, run_time=1.8)
        tick_commit()
        _clear(scene, *hud_outs, chip_value, tags, *m_nums)
        scene.wait(1.2)
        return

    outs = [title, axes, heli, ar_labels, rulers, trail, drops, timer_static, chip_static, chip_value_new,
            paren_and_commas, VGroup(*cm_tex), name_txt, box_t, note] + ticks.mobs()
    if is_3d:
        scene.move_camera(phi=0, theta=-90 * DEGREES, gamma=0, run_time=1.8,
                          added_anims=[FadeOut(m) for m in outs])
    else:
        scene.play(*[FadeOut(m) for m in outs], run_time=1.8)
    heli.stop_rotors(scene)
    ticks.dispose()
    _clear(scene, *outs, chip_value, tags, *m_nums)
    del scene.mach_drawing
    if is_3d and frame_mobs:
        scene.renderer.camera.remove_fixed_in_frame_mobjects(*frame_mobs)
    scene.wait(1.2)


class Scene09(ThreeDScene):
    def construct(self):
        play_scene09(self, keep_drawing=False)