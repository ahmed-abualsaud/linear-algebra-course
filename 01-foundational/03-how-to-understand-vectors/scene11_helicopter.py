from manim import *

from common import (
    M_COLOR, CM_COLOR, PLANK_COLOR, GOLD_LIGHT, TIME_COLOR,
    _clear, _hud, _ar, _make_list, _path_flash, _exit_all
)
from scene10_helicopter import play_scene10


def _ensure_drawing(scene):
    if not hasattr(scene, "mach_drawing"):
        play_scene10(scene, keep_drawing=True)
    return scene.mach_drawing


def play_scene11(scene: Scene, keep_drawing: bool = True):
    is_3d = isinstance(scene, ThreeDScene)
    st = _ensure_drawing(scene)
    O, goal, ticks = st["O"], st["goal"], st.get("ticks")

    # [05:36.0 - 05:39.0]
    title = _ar("3 قوائم.. نفس الحركة بالظبط", 22, GOLD_LIGHT).to_edge(UP, buff=0.5).shift(RIGHT * 1.6)

    specs = [
        ("بالمتر", M_COLOR, ["3", "4", "5", "10"], "m", 1.45),
        ("بالسنتيمتر", CM_COLOR, ["300", "400", "500", "10"], "cm", 0.05),
        ("بالخشبة", PLANK_COLOR, ["0.769", "1.025", "1.282", "10"], "plank", -1.35),
    ]
    rows = []
    for name, col, vals, mode, y in specs:
        lst = _make_list(vals, col, cy=y)
        lbl = _ar(name, 20, col, True)
        lbl.next_to(lst, UP, buff=0.16).align_to(lst, RIGHT)
        rows.append((VGroup(lbl, lst), lst, mode))
    _hud(scene, title, *[r[0] for r in rows])

    q = _ar("أنهي قايمة فيهم هي المتجه\nاللي بيصف الحركة فعلاً؟", 21, GOLD_LIGHT, True).move_to([3.7, -2.6, 0])
    ans = _ar("التلاتة بيصفوا نفس الحركة\nكل قايمة من وجهة نظر مختلفة!", 21, TIME_COLOR, True).move_to([3.7, -2.6, 0])
    _hud(scene, q, ans)

    scene.play(FadeIn(title, shift=DOWN * 0.15), run_time=1.0)
    scene.wait(2.0)

    # 1. قائمة المتر [05:39.0 - 05:41.5]
    grp0, lst0, mode0 = rows[0]
    if ticks is not None:
        tick_anim0, tick_commit0 = ticks.retarget(mode0)
    else:
        tick_anim0, tick_commit0 = Wait(0.01), (lambda: None)
    scene.play(FadeIn(grp0, shift=LEFT * 0.2), tick_anim0, run_time=1.2)
    tick_commit0()
    _path_flash(scene, O, goal, run_time=0.8)
    scene.wait(0.5)

    # 2. قائمة السنتيمتر [05:41.5 - 05:44.5]
    grp1, lst1, mode1 = rows[1]
    if ticks is not None:
        tick_anim1, tick_commit1 = ticks.retarget(mode1)
    else:
        tick_anim1, tick_commit1 = Wait(0.01), (lambda: None)
    scene.play(FadeIn(grp1, shift=LEFT * 0.2), tick_anim1, run_time=1.2)
    tick_commit1()
    _path_flash(scene, O, goal, run_time=0.8)
    scene.wait(1.0)

    # 3. قائمة الخشبة [05:44.5 - 05:50.5]
    grp2, lst2, mode2 = rows[2]
    if ticks is not None:
        tick_anim2, tick_commit2 = ticks.retarget(mode2)
    else:
        tick_anim2, tick_commit2 = Wait(0.01), (lambda: None)
    scene.play(FadeIn(grp2, shift=LEFT * 0.2), tick_anim2, run_time=1.2)
    tick_commit2()
    _path_flash(scene, O, goal, run_time=0.8)
    scene.wait(4.0)

    # [05:50.5 - 05:56.5]
    scene.play(FadeIn(q, shift=UP * 0.1), run_time=1.0)
    scene.play(*[Indicate(r[1], scale_factor=1.08, color=c) for r, c in
                 zip(rows, (M_COLOR, CM_COLOR, PLANK_COLOR))], run_time=1.5)
    scene.wait(3.5)

    # [05:56.5 - 06:04.5]
    scene.play(FadeOut(q, shift=UP * 0.1), FadeIn(ans, shift=UP * 0.1), run_time=1.2)
    scene.wait(6.8)

    # [06:04.5 - 06:07.0]
    hud_outs = [title, ans] + [r[0] for r in rows]
    if keep_drawing and is_3d:
        scene.play(*[FadeOut(m) for m in hud_outs], run_time=1.5)
        _clear(scene, *hud_outs, q)
        scene.wait(1.0)
        return

    _exit_all(scene, st, hud_outs + [q])


class Scene11(ThreeDScene):
    def construct(self):
        play_scene11(self, keep_drawing=False)