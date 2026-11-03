from manim import *
import numpy as np

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_MUTED,
    GOLD_DARK,
    COPPER_TERRA,
    IVORY_WHITE,
    STONE_AXIS,
)
from common.latex import mach_math_template
from common.mobjects.hand import hand_pointing_at, hand_enter, add_hand_bob
from episode_04_common import _ar, _tex, _hud_fix
from scene07_measuring import CEN as CEN0

# ==============================================================
# الحلقة 04 — المشهد 8 (امتداد المشهد 7 بدون قطع):
#   v = 3e1 + 4e2 + 5e3 + 10e4 ثم تغيير متجهات الأساس (متر ← سنتيمتر، متر ← خشبة)
# بيكمل على نفس رسمة الطيارة: متجهات الأساس نفسها هي اللي بتتبدّل قدّام العين.
# ==============================================================

SPD = 0.12 if __import__("os").environ.get("MACH_FAST") else 1.0
KH = 3.9                                   # طول الخشبة بالمتر (5 ÷ 3.9 = 1.282)

# مواضع قايمة الصيغة (يمين الشاشة)
ROWS = [2.25, 1.40, 0.55, -0.30]           # y لكل مركّبة
X_SIGN = 2.55                              # عمود  = و +
X_NUM = 3.95                               # الحافة اليمنى للأرقام
X_E = 4.25                                 # بداية رموز e (محاذاة لليسار)
RING = np.array([1.45, ROWS[0], 0.0])      # دايرة v


def _get_state(scene):
    D = getattr(scene, "mach_drawing", None)
    if D is None:
        print("[scene08] تحذير: مفيش رسمة من المشهد 7، هشغّل المشهد 7 الأول (render أبطأ).")
        from scene07_measuring import play_scene07
        play_scene07(scene, keep_drawing=True)
        D = scene.mach_drawing
    return D


def play_scene08(scene, keep_drawing=False):
    _hud_fix(scene)
    D = _get_state(scene)
    cam = scene.camera
    cap = D["cap"]
    nums, hud_es, hud = D["nums"], D["hud_es"], D["hud"]
    S_, BL, SHX, SHY, U, DY, PT = D["S"], D["BL"], D["SHX"], D["SHY"], D["U"], D["DY"], D["PT"]
    comps, COLS = D["comps"], D["COLS"]
    G = 0.5
    plane = D["plane"]
    D["chips"] = VGroup(*D["chips"])

    track = [D["chips"], hud, D["hud_cap"], D["slider"], D["shafts"], D["heads"], D["e4_tag"]]
    keeper = Mobject()
    keeper.add_updater(lambda m: cam.add_fixed_in_frame_mobjects(*track))
    scene.add(keeper)

    def hud_add(*ms):
        for m in ms:
            track.append(m)
        scene.add_fixed_in_frame_mobjects(*ms)

    def swap_note(txt, color=GOLD_LIGHT):
        cap.set(txt, color, 18)

    # ---------- 0) لقطة: الطيارة عند (3، 4، 5) بعد 10 ثواني (11:46.0 - 11:55.0) ----------
    # 11:46.0 - 11:55.0 | "احنا في الآخر بعد ما بنحدد قايمة الأرقام الخاصة بمركبات متجه زي المتجه الخاص بحركة الطيارة مثلاً..."
    swap_note("نثبّت لقطة: الطيارة عند\n(3، 4، 5) بعد 10 ثواني", GOLD_BRIGHT)
    scene.play(BL.animate(rate_func=smooth).set_value(1.0),
               SHX.animate(rate_func=smooth).set_value(-3.75),
               FadeOut(D["hud_cap"]),
               run_time=3.5)
    scene.remove(D["hud_cap"])
    scene.wait(5.5 * SPD)

    # ---------- 1) عمود الأرقام يتحوّل لصيغة المجموع (11:55.0 - 12:03.0) ----------
    # 11:55.0 - 12:03.0 | "وقتها هنقدر إننا نكتبه بالصيغة الرياضية للمتجهات بالشكل ده: v = 3e1 + 4e2 + 5e3 + 10e4"
    for n_ in nums:
        n_.clear_updaters()
    vals = [3, 4, 5, 10]
    for n_, v in zip(nums, vals):
        n_.num_decimal_places = 0
        n_.set_value(v)

    def keep_nums(n_, i):
        n_.add_updater(lambda m, i=i: (m.set_value(comps()[i]), cam.add_fixed_in_frame_mobjects(m)))

    v_ring = Circle(radius=0.42, color=GOLD_LIGHT, stroke_width=2.2)
    v_glow = Circle(radius=0.6, stroke_width=0, fill_color=GOLD_LIGHT, fill_opacity=0.07)
    v_core = _tex(r"\mathbf{v}", 36, GOLD_BRIGHT)
    v_grp = VGroup(v_glow, v_ring, v_core).move_to(RING)
    signs = [_tex("=", 40, IVORY_WHITE)] + [_tex("+", 40, IVORY_WHITE) for _ in range(3)]
    for sg, y in zip(signs, ROWS):
        sg.move_to([X_SIGN, y, 0])
    hud_add(v_grp, *signs)

    anims = []
    for n_, y in zip(nums, ROWS):
        n_.generate_target()
        n_.target.move_to([X_NUM - n_.width / 2, y, 0])
        anims.append(MoveToTarget(n_))
    for e, y in zip(hud_es, ROWS):
        anims.append(e.animate.move_to([X_E + e.width / 2, y, 0]))
    swap_note("نفس الأرقام بتتكتب\nكمجموع متجهات", GOLD_LIGHT)
    scene.play(FadeOut(hud[0]), FadeIn(v_grp, scale=0.8), *[FadeIn(sg, shift=LEFT * 0.15) for sg in signs],
               *anims, run_time=2.2)
    for i, n_ in enumerate(nums):
        keep_nums(n_, i)
    scene.wait(5.8 * SPD)

    # ---------- 2) نضرب كل مركّبة في متجه الأساس بتاعها ثم نجمع (12:03.0 - 12:14.0) ----------
    # 12:03.0 - 12:14.0 | "لاحظ هنا زي ما قلتلك إننا بنضرب كل رقم أو كل مركبة من مركبات المتجه في متجه الأساس بتاعها، وبعدين بنجمعهم على بعض..."
    rects = VGroup(*[SurroundingRectangle(VGroup(n_, e), color=GOLD_BRIGHT, buff=0.1, corner_radius=0.1,
                                          stroke_width=2) for n_, e in zip(nums, hud_es)])
    hud_add(rects)
    swap_note("بنضرب كل مركبة في متجه\nالأساس بتاعها وبعدين نجمع", GOLD_BRIGHT)
    scene.play(LaggedStart(*[Create(r) for r in rects], lag_ratio=0.25), run_time=1.8)
    scene.wait(8.7 * SPD)
    scene.play(FadeOut(rects), run_time=0.5)
    track.remove(rects)

    # ---------- 3) وحدة كل متجه أساس (12:14.0 - 12:24.0) ----------
    # 12:14.0 - 12:24.0 | "دلوقتي أنا عايز أقول ملحوظة هنا: انت ممكن تستخدم متجهات أساس مختلفة لكل خاصية من التلات خصائص اللي بيقيسوا المسافة..."
    def mk_unit(t, i):
        l = _ar(t, 15, GOLD_MUTED)
        l.move_to([X_E + l.width / 2, ROWS[i] - 0.4, 0])
        return l

    units = [mk_unit(t, i) for i, t in enumerate(["متر — شرق", "متر — شمال", "متر — ارتفاع", "ثانية — زمن"])]
    hud_add(*units)
    swap_note("نفس المتجه… بس هغيّر\nمتجهات الأساس بتاعت المسافة", GOLD_LIGHT)
    scene.play(*[FadeIn(u, shift=UP * 0.1) for u in units], run_time=1.0)
    scene.wait(9.0 * SPD)

    # ---------- 4) e2: متر ← سنتيمتر ، والرقم 4 ← 400 (12:24.0 - 12:47.0) ----------
    # 12:24.0 - 12:31.0 | "يعني ممكن e1 تخليه زي ما هو بيعبر عن وحدة قياس المسافة بالمتر في اتجاه الشرق..."
    scene.wait(7.0 * SPD)

    # 12:31.0 - 12:47.0 | "لكن e2 مثلاً نستبدلها بمتجه أساس تاني بيعبر عن وحدة قياس المسافة بالسنتيمتر في اتجاه الشمال، وخلينا نرمز له بـ e_centimeter..."
    e_cm = _tex(r"\mathbf{e}_{\text{centimeter}}", 32, COLS[1])
    e_cm.move_to([X_E + e_cm.width / 2, ROWS[1], 0])
    u_cm = mk_unit("سنتيمتر — شمال", 1)
    hud_add(e_cm, u_cm)
    scene.remove(e_cm, u_cm)
    ofs2 = ValueTracker(0.0)
    w_new = _tex(r"\mathbf{e}_{\text{centimeter}}", 28, COLS[1]).width
    lbl2, la2 = D["make_label"](r"\mathbf{e}_{\text{centimeter}}", COLS[1],
                                lambda: D["a_e2"]() + ofs2.get_value() * np.array([0.55, 0.15, 0.0]), D["PY"], size=28,
                                dx=(w_new - D["elbl"][1].width) / 2)
    la2.set_value(0.0)

    # عدسة التكبير
    cx, cy, R_BIG, R_SM, ln = 1.55, -2.35, 0.82, 0.2, 0.26
    funnel = Polygon([0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], stroke_width=0)
    funnel.set_fill(GOLD_LIGHT, 0.07)
    edge1 = Line(ORIGIN, RIGHT, color=GOLD_LIGHT, stroke_width=1.5)
    edge2 = Line(ORIGIN, RIGHT, color=GOLD_LIGHT, stroke_width=1.5)
    ring_sm = Circle(radius=R_SM, color=GOLD_BRIGHT, stroke_width=2.2)
    ring_sm.set_fill(opacity=0)
    ring_big = Circle(radius=R_BIG, color=GOLD_LIGHT, stroke_width=2.6).move_to([cx, cy, 0])
    ring_big.set_fill("#0B0905", 0.96)
    shine = Arc(radius=R_BIG - 0.09, start_angle=PI * 0.62, angle=PI * 0.28, arc_center=[cx, cy, 0],
                color=IVORY_WHITE, stroke_width=3.0)
    lens = VGroup(funnel, edge1, edge2, ring_big, ring_sm, shine)
    for k in range(5):
        x0 = cx - 2.5 * ln + k * ln
        lens.add(Line([x0, cy + 0.05, 0], [x0 + ln - 0.05, cy + 0.05, 0], color=COLS[1], stroke_width=3.4))
        lens.add(Triangle(fill_color=COLS[1], fill_opacity=1, stroke_width=0).scale(0.055).rotate(-PI / 2)
                 .move_to([x0 + ln - 0.03, cy + 0.05, 0]))
    for k in range(6):
        xt = cx - 2.5 * ln + k * ln
        lens.add(Line([xt, cy - 0.16, 0], [xt, cy - 0.27, 0], color=GOLD_MUTED, stroke_width=1.3))
    lens.add(Line([cx - 2.5 * ln, cy - 0.16, 0], [cx + 2.5 * ln, cy - 0.16, 0], color=GOLD_MUTED, stroke_width=1.3))
    lens_cap = _ar("تكبير: كل سهم = سنتيمتر", 14, GOLD_MUTED).move_to([cx, cy - R_BIG - 0.25, 0])
    lens.add(lens_cap)
    big_c = np.array([cx, cy])

    def lens_up(m):
        v = float(np.clip((0.45 - U[1].get_value()) / 0.2, 0, 1))
        c = comps()
        mid = np.array([c[0] * U[0].get_value() * G, 0.5 * c[1] * U[1].get_value() * G, 0.07])
        fcn = np.asarray(cam.frame_center, float)
        q = cam.generate_rotation_matrix() @ (mid - fcn)
        p = q[:2] * (cam.get_focal_distance() / (cam.get_focal_distance() - q[2])) * cam.get_zoom() - CEN0[:2]
        ring_sm.move_to([*p, 0])
        d = big_c - p
        L = float(np.linalg.norm(d))
        if L > R_BIG - R_SM + 0.05:
            al = float(np.arctan2(d[1], d[0]))
            be = float(np.arccos(np.clip((R_SM - R_BIG) / L, -1, 1)))
            pts = []
            for g in (al + be, al - be):
                u_ = np.array([np.cos(g), np.sin(g)])
                pts.append((p + R_SM * u_, big_c + R_BIG * u_))
            (a0, a1), (b0, b1) = pts
            funnel.set_points_as_corners([[*a0, 0], [*a1, 0], [*b1, 0], [*b0, 0], [*a0, 0]])
            edge1.put_start_and_end_on([*a0, 0], [*a1, 0])
            edge2.put_start_and_end_on([*b0, 0], [*b1, 0])
        for sub in m:
            if sub is funnel:
                sub.set_fill(GOLD_LIGHT, 0.07 * v)
            elif sub in (ring_sm, edge1, edge2, shine):
                sub.set_stroke(opacity=v * (0.55 if sub in (edge1, edge2) else 0.9))
            elif sub is ring_big:
                sub.set_stroke(opacity=v)
                sub.set_fill("#0B0905", 0.96 * v)
            else:
                sub.set_opacity(v)

    lens_up(lens)
    lens.add_updater(lens_up)
    hud_add(lens)

    swap_note("نغيّر متجه الأساس الثاني\nمن متر لسنتيمتر: 400 بدل 4", COPPER_TERRA)
    scene.play(DY.animate(rate_func=smooth).set_value(1.0), run_time=0.7)
    scene.play(FadeOut(hud_es[1]), FadeOut(units[1]), D["lbl_a"][1].animate.set_value(0.0),
               la2.animate.set_value(1.0), run_time=0.5)
    scene.play(FadeIn(e_cm), FadeIn(u_cm), run_time=0.5)
    hud_es[1], units[1] = e_cm, u_cm
    scene.play(U[1].animate(rate_func=smooth).set_value(0.01), run_time=5.0)
    scene.wait(9.3 * SPD)

    # ---------- 5) e3: متر ← خشبة ، والرقم 5 ← 1.282 (12:47.0 - 12:57.0) ----------
    # 12:47.0 - 12:57.0 | "و e3 نستبدلها بمتجه أساس تاني بيعبر عن الارتفاع بوحدة قياس الخشبة... وخلينا نرمز له بالرمز e_khashaba"
    e_kh = _tex(r"\mathbf{e}_{\text{khashaba}}", 32, COLS[2])
    e_kh.move_to([X_E + e_kh.width / 2, ROWS[2], 0])
    u_kh = mk_unit("خشبة — ارتفاع", 2)
    hud_add(e_kh, u_kh)
    scene.remove(e_kh, u_kh)
    ofs3 = ValueTracker(0.0)
    w_new3 = _tex(r"\mathbf{e}_{\text{khashaba}}", 28, COLS[2]).width
    lbl3, la3 = D["make_label"](r"\mathbf{e}_{\text{khashaba}}", COLS[2],
                                lambda: D["a_e3"]() + ofs3.get_value() * np.array([0.75, 0.0, 0.5 * 0.5 * (KH - 1)]),
                                D["PZ"], size=28, dx=(w_new3 - D["elbl"][2].width) / 2)
    la3.set_value(0.0)
    nums[2].num_decimal_places = 3
    swap_note("نغيّر متجه الأساس الثالث\nمن متر لخشبة (3.9 متر)", COLS[2])
    scene.play(FadeOut(hud_es[2]), FadeOut(units[2]), D["lbl_a"][2].animate.set_value(0.0),
               la3.animate.set_value(1.0), run_time=0.5)
    scene.play(FadeIn(e_kh), FadeIn(u_kh), run_time=0.5)
    hud_es[2], units[2] = e_kh, u_kh
    scene.play(U[2].animate(rate_func=smooth).set_value(KH), run_time=4.5)
    scene.wait(4.5 * SPD)

    # ---------- 6) المتجه نفسه ما اتغيرش (12:57.0 - 13:28.0) ----------
    # 12:57.0 - 13:09.0 | "ونفس الكلام لو هتخلي متجه الأساس بتاع الزمن e4... وبعد ما عملنا التغييرات دي الصيغة الرياضية للمتجه هتتغير وهتكون بالشكل ده..."
    scene.wait(12.0 * SPD)

    # 13:09.0 - 13:28.0 | "لاحظ هنا إن المتجه نفسه ما اتغيرش، لكن كل اللي اتغير هي صيغته الرياضية وطريقة كتابته بس"
    hand_v = hand_pointing_at(v_grp, side=LEFT, gap=0.1)
    hud_add(hand_v)
    scene.remove(hand_v)
    swap_note("المتجه نفسه متغيرش —\nاللي اتغير بس صيغته وكتابته", GOLD_BRIGHT)
    scene.play(hand_enter(hand_v, LEFT), run_time=1.0)
    add_hand_bob(hand_v, RIGHT)
    scene.wait(14.5 * SPD)
    scene.play(FadeOut(hand_v), run_time=0.5)
    hand_v.clear_updaters()
    scene.remove(hand_v)
    track.remove(hand_v)
    scene.wait(1.5 * SPD)

    if keep_drawing:
        # تسليم الرسمة للمشهد 9 (من غير قطع)
        D.update(v_grp=v_grp, signs=signs, units=units, lens=lens, lbl2=lbl2, lbl3=lbl3, la2=la2,
                 la3=la3, ofs2=ofs2, ofs3=ofs3, track=track, hud_add=hud_add, keeper=keeper, ROWS=ROWS,
                 X_NUM=X_NUM, X_E=X_E, X_SIGN=X_SIGN, KH=KH, mk_unit=mk_unit)
        scene.mach_drawing = D
        return

    # ---------- خروج (13:26.5 - 13:28.0) ----------
    for m in (plane, D["pool"].group, D["dense"], D["slider"], D["rig"], *nums, *D["elbl"], lbl2, lbl3, lens):
        m.clear_updaters()
    plane.stop_rotors(scene)
    keeper.clear_updaters()
    scene.play(FadeOut(VGroup(D["world"], D["axes"], D["pool"].group, D["dense"], D["slider"], D["shafts"],
                              D["heads"], D["e4_tag"], D["chips"], v_grp, *signs, *nums, *hud_es, *units,
                              *D["fx"], *D["elbl"], lbl2, lbl3, lens)),
               UpdateFromAlphaFunc(plane, lambda m, a: m.set_fade(1 - a)),
               FadeOut(cap.cur), run_time=1.2)
    scene.remove(plane, D["rig"], keeper)
    scene.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ORIGIN)
    scene.mach_drawing = None
    scene.wait(0.3)


class Dev(ThreeDScene):
    def construct(self):
        play_scene08(self)