from manim import *
import numpy as np

from common import (
    MOVE, DURATION, PLANK_COLOR, GOLD_LIGHT, GOLD_BRIGHT, TIME_COLOR, IVORY_WHITE,
    SCREEN_RIGHT, _clear, _hud, _ar, _make_list, _fmt, _path_flash, _exit_all
)
from scene11_helicopter import play_scene11


def _ensure_drawing(scene):
    if not hasattr(scene, "mach_drawing"):
        play_scene11(scene, keep_drawing=True)
    return scene.mach_drawing


def play_scene12(scene: Scene, keep_drawing: bool = False):
    is_3d = isinstance(scene, ThreeDScene)
    st = _ensure_drawing(scene)
    O, goal, ticks = st["O"], st["goal"], st.get("ticks")

    # [06:07.0 - 06:18.0]
    title = _ar("وأقدر أوصف نفس الحركة بقوايم لا نهائية", 22, GOLD_LIGHT) \
        .to_edge(UP, buff=0.5).shift(RIGHT * 1.6)
    _hud(scene, title)

    if ticks is not None:
        tick_anim, tick_commit = ticks.retarget("m")
    else:
        tick_anim, tick_commit = Wait(0.01), (lambda: None)
    scene.play(FadeIn(title, shift=DOWN * 0.15), tick_anim, run_time=1.2)
    tick_commit()
    scene.wait(0.5)

    cur = {"list": None, "bar": None, "cap": None}
    units = [2.0, 0.5, 0.3048, 1.5, 3.0]
    ruler_title = _ar("المسطرة اللي اخترتها", 20, GOLD_LIGHT, True).move_to([3.7, -0.55, 0])
    _hud(scene, ruler_title)

    def build(u):
        vals = [_fmt(m / u) for m in MOVE] + [str(DURATION)]
        lst = _make_list(vals, PLANK_COLOR, cy=0.55)
        w = float(np.clip(0.9 * u, 0.3, 2.8))
        bar = Rectangle(width=w, height=0.2, stroke_color=PLANK_COLOR, stroke_width=2.5,
                        fill_color=PLANK_COLOR, fill_opacity=0.28).move_to([3.7, -1.15, 0])
        cap = _ar(f"1 وحدة = {_fmt(u)} متر", 20, IVORY_WHITE, True).move_to([3.7, -1.65, 0])
        _hud(scene, lst, bar, cap)
        return lst, bar, cap

    first = True
    for u in units:
        lst, bar, cap = build(u)
        if first:
            scene.play(FadeIn(lst), FadeIn(bar), FadeIn(cap), FadeIn(ruler_title), run_time=0.9)
            _path_flash(scene, O, goal, run_time=0.8)
            first = False
        else:
            scene.play(
                FadeOut(cur["list"]), FadeOut(cur["bar"]), FadeOut(cur["cap"]),
                FadeIn(lst), FadeIn(bar), FadeIn(cap), run_time=0.8,
            )
            _clear(scene, cur["list"], cur["bar"], cur["cap"])
            _path_flash(scene, O, goal, run_time=0.8)
        cur.update(list=lst, bar=bar, cap=cap)

    scene.wait(1.2)

    # [06:18.0 - 06:22.0]
    scene.play(FadeOut(cur["list"]), FadeOut(cur["bar"]), FadeOut(cur["cap"]), FadeOut(ruler_title), run_time=1.0)
    _clear(scene, cur["list"], cur["bar"], cur["cap"], ruler_title)
    scene.wait(3.0)

    # [06:22.0 - 06:31.5]
    t1 = _ar("الأرقام اللي في القايمة\nمجرد قراءة بتتغير مع المسطرة", 21, IVORY_WHITE).move_to([3.7, 1.2, 0])
    t2 = _ar("المتجه الحقيقي = الإزاحة نفسها", 24, GOLD_BRIGHT, True).move_to([3.7, -0.05, 0])
    t3 = _ar("مطلق ومستقل وثابت\nمهما غيرت المسطرة", 21, TIME_COLOR, True).move_to([3.7, -1.4, 0])
    box = SurroundingRectangle(t2, buff=0.22, color=GOLD_BRIGHT, stroke_width=2.5, corner_radius=0.14)
    _hud(scene, t1, t2, t3, box)

    mid = (np.array(O) + np.array(goal)) / 2
    disp_lbl = _ar("الإزاحة", 22, GOLD_BRIGHT, True)
    disp_lbl.move_to(mid + SCREEN_RIGHT * 0.95 + np.array([0, 0, 0.45]))
    if is_3d:
        scene.renderer.camera.add_fixed_orientation_mobjects(disp_lbl)
    glow = Line(O, goal, color=GOLD_BRIGHT, stroke_width=14, stroke_opacity=0.45)
    glow.set_shade_in_3d(True)

    scene.play(FadeIn(t1, shift=UP * 0.1), run_time=1.2)
    scene.wait(8.3)

    # [06:31.5 - 06:36.5]
    scene.play(FadeIn(t2, shift=UP * 0.1), Create(box), FadeIn(disp_lbl), FadeIn(glow), run_time=1.5)
    _path_flash(scene, O, goal, run_time=1.2)
    scene.wait(2.3)

    # [06:36.5 - 06:42.5]
    scene.play(FadeIn(t3, shift=UP * 0.1), run_time=1.2)
    scene.wait(4.8)

    # [06:42.5 - 06:45.0]
    hud_outs = [title, t1, t2, t3, box]
    extra = [disp_lbl, glow]
    if keep_drawing and is_3d:
        scene.play(*[FadeOut(m) for m in hud_outs + extra], run_time=1.5)
        scene.renderer.camera.remove_fixed_orientation_mobjects(disp_lbl)
        _clear(scene, *hud_outs, *extra)
        scene.wait(1.0)
        return

    _exit_all(scene, st, hud_outs, extra=extra)


class Scene12(ThreeDScene):
    def construct(self):
        play_scene12(self, keep_drawing=False)