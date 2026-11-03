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
from common.mobjects.helicopter import make_helicopter  # noqa: F401
from common.mobjects.hand import hand_pointing_at, hand_enter, add_hand_bob
from episode_04_common import _ar, _tex, _hud_fix, ERR_RED
from scene06_scaffolding import _Pool, _segs, _static_arrow, TEAL

# ==============================================================
# الحلقة 04 — المشهد 9 (امتداد المشهد 8 بدون قطع، ثلاثي الأبعاد):
#   e_path على مسار الطيارة + e_pisa مايل زي برج بيزا + إلغاء e3
#   v = 4.7 e_path + 5 e_pisa + 10 e4   (نفس المتجه)
# ==============================================================

SPD = 0.12 if __import__("os").environ.get("MACH_FAST") else 1.0
G = 0.5
AL = 3.99 * DEGREES                          # ميل برج بيزا
TAN = float(np.tan(AL))
DIR = np.array([0.6, 0.8, 0.0])              # اتجاه مسار الطيارة على الأرض (53° تقريباً)
HP = np.array([3.0, 4.0, 5.0])               # الطيارة (شرق، شمال، ارتفاع) بالمتر
HOR = 5.0                                    # المسافة الأفقية 5 متر
N = 8


def _get_state(scene):
    D = getattr(scene, "mach_drawing", None)
    if D is None or "v_grp" not in D:
        print("[scene09] تحذير: مفيش رسمة من المشهد 8، هشغّل المشهدين 7 و 8 الأول (render أبطأ).")
        from scene08_change_basis import play_scene08
        play_scene08(scene, keep_drawing=True)
        D = scene.mach_drawing
    return D


def play_scene09(scene):
    _hud_fix(scene)
    D = _get_state(scene)
    cam = scene.camera
    cap, COLS = D["cap"], D["COLS"]
    nums = list(D["nums"])
    hud_es = list(D["hud_es"])
    units = list(D["units"])
    signs = list(D["signs"])
    v_grp, lens = D["v_grp"], D["lens"]
    U, DY, PX, PY, PZ = D["U"], D["DY"], D["PX"], D["PY"], D["PZ"]
    pool, dense, plane = D["pool"], D["dense"], D["plane"]
    comps, hud_add, mk_unit, track = D["comps"], D["hud_add"], D["mk_unit"], D["track"]
    ROWS, X_E, X_NUM = D["ROWS"], D["X_E"], D["X_NUM"]
    ofs2, ofs3, la2, la3, lbl2, lbl3 = D["ofs2"], D["ofs3"], D["la2"], D["la3"], D["lbl2"], D["lbl3"]

    AB, TB, PLA, VA = (ValueTracker(0.0) for _ in range(4))

    def tt():
        return TAN * TB.get_value()

    def a_path():
        return HOR - HP[2] * tt()

    def note(txt, color=GOLD_LIGHT):
        cap.set(txt, color, 18)

    def bind_num(n_, fn):
        n_.clear_updaters()
        n_.add_updater(lambda m: (m.set_value(fn()), cam.add_fixed_in_frame_mobjects(m)))

    def swap_hud(old, new):
        hud_add(new)
        scene.remove(new)
        scene.play(FadeOut(old), run_time=0.45)
        scene.play(FadeIn(new), run_time=0.5)

    # ==========================================================
    # 0) نرجع لوحدة المتر (13:28.0 - 13:39.5)
    # ==========================================================
    # 13:28.0 - 13:39.5 | "بل إنه مش شرط إنك تخلي متجهات الأساس الخاصة بالمسافة إنها تعبر عن الحركة في اتجاه الشرق أو الشمال أو الارتفاع..."
    note("مش شرط نستخدم نفس المساطر:\nهنرجع لوحدة المتر الأول", GOLD_LIGHT)
    e2n = _tex(r"\mathbf{e}_2", 32, COLS[1])
    e2n.move_to([X_E + e2n.width / 2, ROWS[1], 0])
    u2n = mk_unit("متر — شمال", 1)
    e3n = _tex(r"\mathbf{e}_3", 32, COLS[2])
    e3n.move_to([X_E + e3n.width / 2, ROWS[2], 0])
    u3n = mk_unit("متر — ارتفاع", 2)
    hud_add(e2n, u2n, e3n, u3n)
    scene.remove(e2n, u2n, e3n, u3n)
    scene.play(FadeOut(hud_es[1]), FadeOut(units[1]), FadeOut(hud_es[2]), FadeOut(units[2]), run_time=0.5)
    scene.play(FadeIn(e2n), FadeIn(u2n), FadeIn(e3n), FadeIn(u3n), run_time=0.5)
    hud_es[1], units[1], hud_es[2], units[2] = e2n, u2n, e3n, u3n
    D["nums"][2].num_decimal_places = 3
    scene.play(U[1].animate(rate_func=smooth).set_value(1.0), ofs2.animate(rate_func=smooth).set_value(0.0),
               U[2].animate(rate_func=smooth).set_value(1.0), ofs3.animate(rate_func=smooth).set_value(0.0),
               run_time=4.0)
    D["nums"][2].num_decimal_places = 0
    scene.play(DY.animate(rate_func=smooth).set_value(0.0), la2.animate.set_value(0.0),
               D["lbl_a"][1].animate.set_value(1.0), la3.animate.set_value(0.0), D["lbl_a"][2].animate.set_value(1.0),
               run_time=0.8)
    scene.wait(5.7 * SPD)

    # ==========================================================
    # 1) مسار الطيارة على الأرض: خط بيميل 53° تقريباً (13:39.5 - 13:49.0)
    # ==========================================================
    # 13:39.5 - 13:49.0 | "يعني لو رجعنا للطيارة، هتلاقيها بتتحرك في خط مستقيم على الأرض بيميل بزاوية 53 درجة تقريباً..."
    note("الطيارة بتتحرك على الأرض\nفي خط مائل 53° تقريباً", COPPER_TERRA)
    ground = DashedLine([0, 0, 0.02], [*(DIR * 3.4)[:2], 0.02], dash_length=0.12, color=GOLD_LIGHT, stroke_width=2.2)
    th = float(np.arctan2(DIR[1], DIR[0]))
    arc = Arc(radius=0.75, start_angle=0, angle=th, arc_center=ORIGIN, color=GOLD_LIGHT, stroke_width=3)
    a_lbl = _tex(r"53^\circ", 26, GOLD_LIGHT)
    a_lbl.move_to([1.15 * np.cos(th / 2), 1.15 * np.sin(th / 2) - 0.1, 0.02])
    scene.add_fixed_orientation_mobjects(a_lbl)
    a_lbl.set_opacity(0)
    scene.play(Create(ground), Create(arc), a_lbl.animate.set_opacity(1.0), run_time=1.8)
    scene.wait(7.7 * SPD)

    # ==========================================================
    # 2) e1 و e2 ← e_path (متجه أساس واحد على مسار الطيارة) (13:49.0 - 14:01.0)
    # ==========================================================
    # 13:49.0 - 14:01.0 | "فبدل ما استخدم مسطرة للشرق ومسطرة للشمال، أنا ممكن استبدلهم بمتجه أساس واحد ماشي على مسار الطيارة وأسميه e_path..."
    pp = _Pool([COLS[0]] * N, th=0.02, hl=0.15, r=0.055, rc=(1, 8), rk=(1, 10))
    off = np.array([0.0, 0.0, 0.07])

    def upd_pool9(_m=None):
        ab, t = AB.get_value(), tt()
        c = comps()
        X, Y = c[0] * G, c[1] * G
        for k in range(N):
            f = float(np.clip(c[0] - k, 0, 1)) * (1 - ab)
            s0 = np.array([k * G, 0, 0.0]) + off
            pool.pose(k, s0, s0 + [f * G, 0, 0])
            f = float(np.clip(c[1] - k, 0, 1)) * (1 - ab)
            s0 = np.array([X, k * G, 0.0]) + off
            pool.pose(N + k, s0, s0 + [0, f * G, 0])
        base = a_path() * G * DIR
        step = G * np.array([t * DIR[0], t * DIR[1], 1.0])
        for k in range(N):
            f = float(np.clip(c[2] - k, 0, 1))
            s0 = base + off + k * step
            pool.pose(2 * N + k, s0, s0 + f * step)

    def upd_path(_m=None):
        cp = a_path() * AB.get_value()
        for k in range(N):
            f = float(np.clip(cp - k, 0, 1))
            s0 = k * G * DIR + off
            pp.pose(k, s0, s0 + f * G * DIR)

    pool.group.clear_updaters()
    pool.group.add_updater(upd_pool9)
    pp.group.add_updater(upd_path)
    scene.add(pp.group)

    LB_PATH = _tex(r"\mathbf{e}_{\text{path}}", 28, COLS[0])
    nrm = np.array([DIR[1], -DIR[0], 0.0])
    lp = ValueTracker(0.0)

    def up_lp(m):
        m.move_to(0.66 * a_path() * G * DIR + 0.62 * nrm + [0, 0, 0.12])
        m.set_opacity(float(np.clip(AB.get_value() * 3 - 1.2, 0, 1)) * lp.get_value())

    LB_PATH.add_updater(up_lp)
    LB_PATH.set_opacity(0)
    scene.add_fixed_orientation_mobjects(LB_PATH)

    e_1p = _tex(r"\mathbf{e}_{\text{path}}", 32, COLS[0])
    e_1p.move_to([X_E + e_1p.width / 2, ROWS[0], 0])
    u_1p = mk_unit("متر — اتجاه الحركة", 0)
    hud_add(e_1p, u_1p)
    scene.remove(e_1p, u_1p)

    def val_a():
        return 3 * (1 - AB.get_value()) + AB.get_value() * a_path()

    note("بدل مسطرتي الشرق والشمال:\nمسطرة واحدة على المسار", GOLD_BRIGHT)
    for n_ in nums:
        n_.clear_updaters()
    rowB = (nums[2], hud_es[2], units[2])
    rowC = (nums[3], hud_es[3], units[3])
    scene.play(FadeOut(nums[1]), FadeOut(hud_es[1]), FadeOut(units[1]), FadeOut(signs[3]),
               FadeOut(hud_es[0]), FadeOut(units[0]), run_time=0.5)
    scene.remove(nums[1], hud_es[1], units[1], signs[3], hud_es[0], units[0])
    anims = []
    for (n_, e, u), y_new, y_old in zip((rowB, rowC), (ROWS[1], ROWS[2]), (ROWS[2], ROWS[3])):
        dy = y_new - y_old
        anims += [n_.animate.shift(UP * dy), e.animate.shift(UP * dy), u.animate.shift(UP * dy)]
    scene.play(*anims, run_time=0.8)
    scene.play(FadeIn(e_1p), FadeIn(u_1p), run_time=0.6)
    nums = [nums[0], nums[2], nums[3]]
    hud_es = [e_1p, hud_es[2], hud_es[3]]
    units = [u_1p, units[2], units[3]]
    signs = signs[:3]
    bind_num(nums[0], val_a)
    bind_num(nums[1], lambda: comps()[2])
    bind_num(nums[2], lambda: comps()[3])
    scene.play(AB.animate(rate_func=smooth).set_value(1.0), D["lbl_a"][0].animate.set_value(0.0),
               D["lbl_a"][1].animate.set_value(0.0), lp.animate.set_value(1.0), run_time=3.5)
    scene.wait(6.6 * SPD)

    # ==========================================================
    # 3) e3 ← e_pisa : برج بيزا والمحور المائل (14:01.0 - 14:31.0)
    # ==========================================================
    # 14:01.0 - 14:13.0 | "وممكن بدل مسطرة الارتفاع العمودي، نقدر نستخدم مسطرة مايلة في الفضاء زي اتجاه ميل برج بيزا المايل في إيطاليا ونسميه e_pisa..."
    pz = np.array([TAN * DIR[0], TAN * DIR[1], 1.0])
    pzu = pz / np.linalg.norm(pz)
    axz = _Pool([GOLD_MUTED], th=0.012, hl=0.2, r=0.06, rc=(1, 8), rk=(1, 10))

    def upd_axz(_m=None):
        t = tt()
        axz.pose(0, [0, 0, 0], (N + 1) * G * np.array([t * DIR[0], t * DIR[1], 1.0]))

    upd_axz()
    axz.group.add_updater(upd_axz)
    D["axes"].remove(D["axes"][2])
    scene.add(axz.group)

    for m in D["fx"]:
        c = m.get_center()
        if abs(c[1]) < 1e-6 and ((abs(c[0] + 0.28) < 1e-6 and c[2] > 0.1) or (abs(c[0]) < 1e-6 and c[2] > 4.0)):
            m.add_updater(lambda mm, b=c.copy(): mm.move_to(b + [b[2] * tt() * DIR[0], b[2] * tt() * DIR[1], 0]))

    vref = DashedLine([0, 0, 0.03], [0, 0, 4.3], dash_length=0.12, color=STONE_AXIS, stroke_width=1.8)
    vref.set_opacity(0)

    tiers = VGroup()
    H, R0 = 3.5, 0.42
    for i in range(8):
        h = H / 8
        rad = R0 if i < 7 else R0 * 0.72
        cyl = Cylinder(radius=rad, height=h * 0.94, direction=pzu, resolution=(2, 28), show_ends=True)
        cyl.move_to((i + 0.5) * h * pzu)
        cyl.set_fill(IVORY_WHITE if i % 2 == 0 else GOLD_LIGHT, opacity=0.5)
        cyl.set_stroke(GOLD_MUTED, width=0.6, opacity=0.5)
        tiers.add(cyl)
    t_lbl = _tex(r"\approx 4^\circ", 28, GOLD_LIGHT)
    t_lbl.move_to([-1.55, 0.0, 3.35])
    t_ar = _ar("ميل برج بيزا", 18, GOLD_MUTED).move_to(t_lbl.get_center() + [0.0, 0.0, 0.45])
    for m in (t_lbl, t_ar):
        m.set_opacity(0)
        scene.add_fixed_orientation_mobjects(m)

    Lp, Hp = 3.5, 3.5

    def plane_pts(t):
        p = np.array([t * DIR[0], t * DIR[1], 1.0])
        return DIR * Lp, p * Hp

    plane_fill = VMobject()
    plane_fill.set_fill(GOLD_LIGHT, 0.0).set_stroke(GOLD_LIGHT, 1.4, 0.0)
    plane_grid = VMobject()
    plane_grid.set_fill(opacity=0).set_stroke(GOLD_LIGHT, 1.0, 0.0)

    def upd_plane(_m=None):
        a = PLA.get_value()
        t = tt()
        A, B = plane_pts(t)
        plane_fill.set_points_as_corners([ORIGIN, A, A + B, B, ORIGIN])
        plane_fill.set_fill(GOLD_LIGHT, 0.075 * a).set_stroke(GOLD_LIGHT, 1.4, 0.35 * a)
        n = 7
        P0 = [A * i / n for i in range(1, n)] + [B * i / n for i in range(1, n)]
        P1 = [B + A * i / n for i in range(1, n)] + [A + B * i / n for i in range(1, n)]
        pts = np.array(P0), np.array(P1)
        vs = _segs(pts[0], pts[1], GOLD_LIGHT, 1.0, 0.16 * a)
        plane_grid.set_points(vs.points)
        plane_grid.set_stroke(GOLD_LIGHT, 1.0, 0.16 * a)

    upd_plane()
    plane_fill.add_updater(upd_plane)
    scene.add(plane_fill, plane_grid)

    def a_pisa():
        return a_path() * G * DIR + np.array([0.27, 0.17, 0.5 * G]) + ofs_p.get_value() * np.array([0.5, 0.1, 0.25])

    ofs_p = ValueTracker(0.0)
    w_new = _tex(r"\mathbf{e}_{\text{pisa}}", 28, COLS[2]).width
    LB_PISA, la_p = D["make_label"](r"\mathbf{e}_{\text{pisa}}", COLS[2], a_pisa, PZ, size=28,
                                    dx=(w_new - D["elbl"][2].width) / 2)
    la_p.set_value(0.0)

    e_2p = _tex(r"\mathbf{e}_{\text{pisa}}", 32, COLS[2])
    e_2p.move_to([X_E + e_2p.width / 2, ROWS[1], 0])
    u_2p = mk_unit("متر — ميل بيزا", 1)
    hud_add(e_2p, u_2p)
    scene.remove(e_2p, u_2p)

    note("وبدل مسطرة الارتفاع: مسطرة\nمايلة زي برج بيزا في إيطاليا", TEAL)
    scene.play(FadeIn(tiers), vref.animate.set_opacity(0.85), run_time=1.0)
    scene.play(t_lbl.animate.set_opacity(1.0), t_ar.animate.set_opacity(1.0), run_time=0.6)
    scene.wait(1.0 * SPD)
    nums[0].num_decimal_places = 1
    scene.play(FadeOut(hud_es[1]), FadeOut(units[1]), D["lbl_a"][2].animate.set_value(0.0),
               la_p.animate.set_value(1.0), run_time=0.5)
    scene.play(FadeIn(e_2p), FadeIn(u_2p), run_time=0.5)
    hud_es[1], units[1] = e_2p, u_2p
    scene.play(TB.animate(rate_func=smooth).set_value(1.0), PLA.animate(rate_func=smooth).set_value(1.0),
               run_time=2.4)
    scene.wait(1.0 * SPD)
    scene.play(FadeOut(tiers), FadeOut(t_lbl), FadeOut(t_ar), run_time=0.9)
    scene.remove(tiers, t_lbl, t_ar)
    scene.wait(4.1 * SPD)

    # 14:13.0 - 14:31.0 | "وهنا هنلغي e3 خالص، لأن حركة الطيارة في الفراغ محصورة في مستوى واحد يمر بالمسار وبرج بيزا... فـ اتنين متجه أساس بقوا كافيين جداً لوصف الحركة"
    note("الحركة محصورة في مستوى واحد\nيجمع المسار وبرج بيزا", GOLD_LIGHT)
    scene.wait(2.0 * SPD)

    HOME_PHI, HOME_TH = 58 * DEGREES, -58 * DEGREES
    SHY, ZOOM0 = D["SHY"], cam.get_zoom()
    ZOOM_SIDE, SHY_SIDE = ZOOM0 * 0.8, -0.45
    note("نفس المستوى من أكتر من زاوية:\nأول حاجة بنشوفه وش لوش", GOLD_BRIGHT)
    scene.move_camera(phi=74 * DEGREES, theta=-37 * DEGREES, zoom=ZOOM_SIDE, run_time=3.0, rate_func=smooth,
                      added_anims=[SHY.animate(rate_func=smooth).set_value(SHY_SIDE)])
    scene.wait(1.0 * SPD)
    note("ومن جنبه تمامًا: المستوى يبان خط\nوميل بيزا واضح فيه", TEAL)
    scene.move_camera(phi=80 * DEGREES, theta=53 * DEGREES, run_time=3.0, rate_func=smooth)
    scene.wait(1.0 * SPD)
    note("ومن فوق: بنشوف مساره على الأرض\nمع امتداد المستوى", COPPER_TERRA)
    scene.move_camera(phi=30 * DEGREES, theta=-20 * DEGREES, run_time=3.0, rate_func=smooth)
    scene.wait(1.0 * SPD)
    note("وبنرجع لزاوية المشهد الأصلية", GOLD_LIGHT)
    scene.move_camera(phi=HOME_PHI, theta=HOME_TH, zoom=ZOOM0, run_time=3.0, rate_func=smooth,
                      added_anims=[SHY.animate(rate_func=smooth).set_value(0.0)])
    scene.wait(1.0 * SPD)

    # ==========================================================
    # 4) e3 اتلغى — متجهين كفاية (14:31.0 - 15:08.0)
    # ==========================================================
    # 14:31.0 - 14:50.0 | "لكن لو الطيارة اتحركت في اتجاه تاني وقتها هحتاج إني أسيب متجه الأساس e3 زي ما هو عشان يقدر هو وباقي متجهات الأساس يصفولي حركة الطيارة بشكل كامل..."
    xm = _tex(r"\times", 70, ERR_RED)
    xm.move_to([0, 0, 2.6])
    xm.set_opacity(0)
    scene.add_fixed_orientation_mobjects(xm)
    note("فنلغي متجه الأساس الثالث:\nمتجهين كفاية لوصف الحركة", ERR_RED)
    scene.play(xm.animate.set_opacity(1.0), run_time=0.8)
    scene.wait(4.0 * SPD)
    scene.play(xm.animate.set_opacity(0.0), vref.animate.set_opacity(0.0), run_time=0.8)
    scene.remove(xm, vref)
    scene.wait(13.4 * SPD)

    # 14:50.0 - 15:08.0 | "ونتيجة لده صيغة المتجه هتكون بالشكل ده: v = 4.7 e_path + 5 e_pisa + 10 e4... ولاحظ هنا إن الرقم الخاص بـ e_path بقى 4.7 بدل 5"
    note("رقم المسار بقى 4.7 بدل 5\nلأن الميل غطّى جزء من الأرض", COPPER_TERRA)
    hand_n = hand_pointing_at(VGroup(nums[0], hud_es[0]), side=RIGHT, gap=0.15)
    hud_add(hand_n)
    scene.remove(hand_n)
    scene.play(hand_enter(hand_n, RIGHT), run_time=1.0)
    add_hand_bob(hand_n, LEFT)
    scene.wait(12.0 * SPD)
    scene.play(FadeOut(hand_n), run_time=0.5)
    hand_n.clear_updaters()
    scene.wait(4.5 * SPD)

    # ==========================================================
    # 5) المتجه نفسه ما اتغيرش وتجريد الخصائص (15:08.0 - 16:08.0)
    # ==========================================================
    # 15:08.0 - 15:25.0 | "يبقى كل اللي أنا عملته هنا هو إني غيرت السقالات... لكن المتجه نفسه كحركة حقيقية في الفراغ ما اتغيرش إطلاقاً..."
    va = _Pool([GOLD_BRIGHT], th=0.032, hl=0.2, r=0.085, rc=(1, 8), rk=(1, 10))
    P = HP * G
    va.pose(0, [0, 0, 0.12], P + [0, 0, 0.12])
    for sm in va.cyl[0] + va.cone[0]:
        sm.set_opacity(0.0)
    scene.add(va.group)
    vl = _tex(r"\mathbf{v}", 40, GOLD_BRIGHT)
    vl.move_to(P * 0.5 + [-0.45, 0.35, 0.3])
    vl.set_opacity(0)
    scene.add_fixed_orientation_mobjects(vl)

    note("المتجه نفسه متغيرش —\nاللي اتغير بس صيغته وكتابته", GOLD_BRIGHT)
    scene.play(UpdateFromAlphaFunc(va.group, lambda m, a: [sm.set_opacity(a) for sm in va.cyl[0] + va.cone[0]]),
               vl.animate.set_opacity(1.0), Indicate(v_grp, color=GOLD_BRIGHT, scale_factor=1.15),
               run_time=1.8)
    scene.wait(15.2 * SPD)

    # 15:25.0 - 15:39.5 | "وخد بالك إن الخصائص اللي بتختارها دي ومتجهات الأساس بتاعتها تكون فعلاً بتصف حركة الطيارة وصف يكاد يكون كامل من غير أي فقد للمعلومات..."
    note("الخصائص ومتجهاتها لازم توصف\nالحركة بأقل فقد ممكن", GOLD_LIGHT)
    scene.wait(14.5 * SPD)

    # 15:39.5 - 15:52.0 | "يعني بمعنى تاني أكثر تجريداً: لازم متجهات الأساس اللي هتختارها دي تبني نظام إحداثيات يقدر يغطي أكبر قدر ممكن داخل فضاء المتجهات..."
    note("يعني نبني نظام إحداثيات يغطي\nأكبر قدر ممكن من الفضاء", COPPER_TERRA)
    scene.wait(12.5 * SPD)

    # 15:52.0 - 16:06.0 | "عشان كدة أنا لما ذكرت النقطة بتاعة اختيار الخصائص في الحلقة اللي فاتت، قلتلك وقتها إنها حاجة مش سهلة إطلاقاً..."
    note("وعشان كده اختيار الخصائص\nمش سهل أبدًا", GOLD_BRIGHT)
    scene.wait(14.0 * SPD)

    # ==========================================================
    # خروج (16:06.0 - 16:08.0)
    # ==========================================================
    for m in (plane, pool.group, pp.group, axz.group, dense, D["slider"], D["rig"], *D["nums"], *D["elbl"], lbl2, lbl3,
              lens, LB_PATH, LB_PISA, plane_fill, *D["fx"]):
        m.clear_updaters()
    plane.stop_rotors(scene)
    D["keeper"].clear_updaters()
    outs = [D["world"], D["axes"], D["chips"], axz.group, pool.group, pp.group, dense, D["slider"], D["shafts"],
            D["heads"], D["e4_tag"], v_grp, *signs, *nums, *hud_es, *units,
            *D["fx"], *D["elbl"], lbl2, lbl3, lens, LB_PATH, LB_PISA, plane_fill, plane_grid, ground, arc, a_lbl,
            va.group, vl]
    scene.play(FadeOut(VGroup(*[o for o in outs if o is not None])),
               UpdateFromAlphaFunc(plane, lambda m, a: m.set_fade(1 - a)), FadeOut(cap.cur), run_time=1.7)
    scene.remove(plane, D["rig"], D["keeper"])
    scene.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ORIGIN)
    scene.mach_drawing = None
    scene.wait(0.3)


class Dev(ThreeDScene):
    def construct(self):
        play_scene09(self)