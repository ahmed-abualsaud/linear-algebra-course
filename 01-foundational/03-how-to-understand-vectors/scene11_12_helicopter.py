"""
المشهدان 11 و12 — يكملان على نفس رسمة الطيارة (scene.mach_drawing) من المشهد العاشر.

play_scene11(scene, keep_drawing=True)   # 3 قوائم لنفس الحركة (31.0 ثانية)
play_scene12(scene, keep_drawing=False)  # قوائم لا نهائية، والمتجه الحقيقي = الإزاحة (38.0 ثانية)
"""
from manim import *
import numpy as np

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    COPPER_TERRA,
    IVORY_WHITE,
)

MOVE = (3, 4, 5)
DURATION = 10
SCALE = 100
PLANK = 3.9

TIME_COLOR = COPPER_TERRA
M_COLOR = GOLD_BRIGHT          # المتر
CM_COLOR = "#F0B27A"           # السنتيمتر
PLANK_COLOR = "#7FD6C2"        # الخشبة (نفس لون المشهد العاشر)

SCREEN_RIGHT = np.array([np.cos(np.radians(35)), np.sin(np.radians(35)), 0.0])


# ======================================================================
# أدوات مساعدة
# ======================================================================
def _clear(scene, *mobs):
    fam = []
    for m in mobs:
        if m is not None:
            fam += m.get_family()
    scene.remove(*fam)


def _hud(scene, *mobs):
    if isinstance(scene, ThreeDScene):
        scene.renderer.camera.add_fixed_in_frame_mobjects(*mobs)
    return mobs[0] if len(mobs) == 1 else mobs


def _ar(txt, size=22, color=IVORY_WHITE, bold=False):
    body = f"<b>{txt}</b>" if bold else txt
    return MarkupText(body, font="Cairo", font_size=size, color=color)


def _make_list(vals, space_color, fs=40, cx=3.7, cy=0.0):
    """قائمة (a , b , c , 10) بنفس تنسيق المشهد العاشر."""
    tex = [MathTex(v, font_size=fs, color=space_color) for v in vals[:3]]
    tex.append(MathTex(vals[3], font_size=fs, color=TIME_COLOR))
    parts = VGroup(
        MathTex(r"(", font_size=fs + 14),
        tex[0], MathTex(r",", font_size=fs),
        tex[1], MathTex(r",", font_size=fs),
        tex[2], MathTex(r",", font_size=fs),
        tex[3],
        MathTex(r")", font_size=fs + 14),
    ).arrange(RIGHT, buff=0.2, aligned_edge=DOWN).move_to([cx, cy, 0])
    for p in parts:
        if p not in tex:
            p.set_color(IVORY_WHITE)
    return parts


def _fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _ensure_drawing(scene):
    if not hasattr(scene, "mach_drawing"):
        try:
            from scene08_09_10_helicopter import play_scene10
        except ImportError as e:
            raise RuntimeError(
                "لا توجد رسمة سابقة (scene.mach_drawing). شغّل المشاهد 8→10 على نفس الـ scene أولاً، "
                "أو عدّل سطر الاستيراد أعلاه ليشير إلى ملف المشاهد 8-10 عندك."
            ) from e
        play_scene10(scene, keep_drawing=True)
    return scene.mach_drawing


def _path_flash(scene, O, goal, run_time=0.9):
    flash = Line(O, goal, color=GOLD_BRIGHT, stroke_width=9)
    flash.set_shade_in_3d(True)
    scene.play(ShowPassingFlash(flash, time_width=0.7), run_time=run_time)


# ======================================================================
# المشهد الحادي عشر: 3 قوائم لنفس الحركة (المدة: 31.0 ثانية: 05:36 إلى 06:07)
# ======================================================================
def play_scene11(scene: Scene, keep_drawing: bool = True):
    is_3d = isinstance(scene, ThreeDScene)
    st = _ensure_drawing(scene)
    O, goal, ticks = st["O"], st["goal"], st.get("ticks")

    # [05:36.0 - 05:39.0]: (3.0s) "طيب انا دلوقتي عندي تلات قوائم بصف بيهم نفس الحركة..."
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

    # 1. قائمة المتر [05:39.0 - 05:41.5]: (2.5s) "تلاتة اربعة خمسة عشرة"
    grp0, lst0, mode0 = rows[0]
    if ticks is not None:
        tick_anim0, tick_commit0 = ticks.retarget(mode0)
    else:
        tick_anim0, tick_commit0 = Wait(0.01), (lambda: None)
    scene.play(FadeIn(grp0, shift=LEFT * 0.2), tick_anim0, run_time=1.2)
    tick_commit0()
    _path_flash(scene, O, goal, run_time=0.8)
    scene.wait(0.5)

    # 2. قائمة السنتيمتر [05:41.5 - 05:44.5]: (3.0s) "300 400 500 10"
    grp1, lst1, mode1 = rows[1]
    if ticks is not None:
        tick_anim1, tick_commit1 = ticks.retarget(mode1)
    else:
        tick_anim1, tick_commit1 = Wait(0.01), (lambda: None)
    scene.play(FadeIn(grp1, shift=LEFT * 0.2), tick_anim1, run_time=1.2)
    tick_commit1()
    _path_flash(scene, O, goal, run_time=0.8)
    scene.wait(1.0)

    # 3. قائمة الخشبة [05:44.5 - 05:50.5]: (6.0s) "والقايمة الخاصة بوحدة القياس الجديدة اللي اسمها الخشبة"
    grp2, lst2, mode2 = rows[2]
    if ticks is not None:
        tick_anim2, tick_commit2 = ticks.retarget(mode2)
    else:
        tick_anim2, tick_commit2 = Wait(0.01), (lambda: None)
    scene.play(FadeIn(grp2, shift=LEFT * 0.2), tick_anim2, run_time=1.2)
    tick_commit2()
    _path_flash(scene, O, goal, run_time=0.8)
    scene.wait(4.0)

    # [05:50.5 - 05:56.5]: (6.0s) "هنا المفروض اسال نفسي: انهي قايمة فيهم هي المتجه اللي بيصف الحركة فعلا؟"
    scene.play(FadeIn(q, shift=UP * 0.1), run_time=1.0)
    scene.play(*[Indicate(r[1], scale_factor=1.08, color=c) for r, c in
                 zip(rows, (M_COLOR, CM_COLOR, PLANK_COLOR))], run_time=1.5)
    scene.wait(3.5)

    # [05:56.5 - 06:04.5]: (8.0s) "الحقيقة هما التلاتة بيصفو نفس متجه الحركة.. لكن كل قايمة من دول بتصف الحركة من وجهة نظر مختلفة!"
    scene.play(FadeOut(q, shift=UP * 0.1), FadeIn(ans, shift=UP * 0.1), run_time=1.2)
    scene.wait(6.8)

    # [06:04.5 - 06:07.0]: (2.5s) سكتة تسليم للمشهد الثاني عشر
    hud_outs = [title, ans] + [r[0] for r in rows]
    if keep_drawing and is_3d:
        scene.play(*[FadeOut(m) for m in hud_outs], run_time=1.5)
        _clear(scene, *hud_outs, q)
        scene.wait(1.0)
        return

    _exit_all(scene, st, hud_outs + [q])
    # المجموع: 3.0 + 2.5 + 3.0 + 6.0 + 6.0 + 8.0 + 2.5 = 31.0 ثانية بالتمام والكمال!


# ======================================================================
# المشهد الثاني عشر: قوائم لا نهائية، والمتجه الحقيقي = الإزاحة (المدة: 38.0 ثانية: 06:07 إلى 06:45)
# ======================================================================
def play_scene12(scene: Scene, keep_drawing: bool = False):
    is_3d = isinstance(scene, ThreeDScene)
    st = _ensure_drawing(scene)
    O, goal, ticks = st["O"], st["goal"], st.get("ticks")
    mx, my, mz = MOVE

    # [06:07.0 - 06:18.0]: (11.0s) "وخليني اقولك اني ممكن اصف نفس حركة الطيارة بقايمة رابعة وخامسة وعدد لا نهائي من القوائم..."
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

    # [06:18.0 - 06:22.0]: (4.0s) "...لكن كل قايمة من الارقام دي بتعتمد على وحدات القياس اللي بقيس بيها"
    scene.play(FadeOut(cur["list"]), FadeOut(cur["bar"]), FadeOut(cur["cap"]), FadeOut(ruler_title), run_time=1.0)
    _clear(scene, cur["list"], cur["bar"], cur["cap"], ruler_title)
    scene.wait(3.0)

    # [06:22.0 - 06:31.5]: (9.5s) "عشان كده الارقام اللي جوه القايمة مش شيء مطلق.. دي مجرد قراءة بتعتمد على المساطر ووحدات القياس اللي اخترناها"
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

    # [06:31.5 - 06:36.5]: (5.0s) "لكن المتجه الحقيقي هو الازاحة او حركة الطيارة نفسها"
    scene.play(FadeIn(t2, shift=UP * 0.1), Create(box), FadeIn(disp_lbl), FadeIn(glow), run_time=1.5)
    _path_flash(scene, O, goal, run_time=1.2)
    scene.wait(2.3)

    # [06:36.5 - 06:42.5]: (6.0s) "وهو شيء مطلق ومستقل وثابت مهما غيرت المساطر او وحدات القياس"
    scene.play(FadeIn(t3, shift=UP * 0.1), run_time=1.2)
    scene.wait(4.8)

    # [06:42.5 - 06:45.0]: (2.5s) خروج كامل وتفريغ نهائي قبل المشهد الثالث عشر عند 06:45.0
    hud_outs = [title, t1, t2, t3, box]
    extra = [disp_lbl, glow]
    if keep_drawing and is_3d:
        scene.play(*[FadeOut(m) for m in hud_outs + extra], run_time=1.5)
        scene.renderer.camera.remove_fixed_orientation_mobjects(disp_lbl)
        _clear(scene, *hud_outs, *extra)
        scene.wait(1.0)
        return

    _exit_all(scene, st, hud_outs, extra=extra)
    # المجموع: 11.0 + 4.0 + 9.5 + 5.0 + 6.0 + 2.5 = 38.0 ثانية بالتمام والكمال!


# ======================================================================
# خروج كامل: الرسمة + الكاميرا
# ======================================================================
def _exit_all(scene, st, hud_outs, extra=()):
    is_3d = isinstance(scene, ThreeDScene)
    frame_mobs = [m for m in (getattr(scene, "frame", None), getattr(scene, "neon_overlay", None)) if m is not None]
    ticks = st.get("ticks")
    outs = [st["axes"], st["heli"], st["ar_labels"], st["rulers"], st["trail"], st["drops"]] \
        + list(hud_outs) + list(extra) + (ticks.mobs() if ticks is not None else [])
    if is_3d:
        scene.move_camera(phi=0, theta=-90 * DEGREES, gamma=0, run_time=1.5,
                          added_anims=[FadeOut(m) for m in outs])
    else:
        scene.play(*[FadeOut(m) for m in outs], run_time=1.5)
    st["heli"].stop_rotors(scene)
    if ticks is not None:
        ticks.dispose()
    for m in extra:
        if is_3d and m in scene.renderer.camera.fixed_orientation_mobjects:
            scene.renderer.camera.remove_fixed_orientation_mobjects(m)
    _clear(scene, *outs)
    if hasattr(scene, "mach_drawing"):
        del scene.mach_drawing
    if is_3d and frame_mobs:
        scene.renderer.camera.remove_fixed_in_frame_mobjects(*frame_mobs)
    scene.wait(1.0)