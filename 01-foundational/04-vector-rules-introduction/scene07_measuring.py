from manim import *
import os
import numpy as np

from common.palette import (
    GOLD,
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_MUTED,
    COPPER_TERRA,
    IVORY_WHITE,
    STONE_AXIS,
)
from common.latex import mach_math_template
from common.mobjects.helicopter import make_helicopter
from common.mobjects.time_slider import MachTimeSlider
from episode_04_common import _ar, _tex, _chip, _hud_fix
from scene06_scaffolding import _Pool, _segs, _static_arrow, TEAL

# ==============================================================
# الحلقة 04 — المشهد 7 (ثلاثي الأبعاد): القياس بنظام الإحداثيات ← أرقام المركبات
# ==============================================================

G = 0.5                                        # طول وحدة الشبكة (= طول متجه الأساس)
CEN = np.array([2.0, 1.9, 0.3])                # مركز المشهد
N = 8                                          # أقصى عدد متجهات أساس على كل محور
T0, T1 = 10.0, 22.0                            # زمن بداية ونهاية الرحلة
T_MAX = 24
SPD = 0.12 if os.environ.get('MACH_FAST') else 1.0      # معاينة سريعة فقط (بتقصّر الانتظار)
TARGET = np.array([3.0, 4.0, 5.0])             # لقطة المشهد 8: (3, 4, 5) بعد 10 ثواني
T_SNAP = 10.0
ZF = 0.95                                      # معامل تكبير عام للكاميرا
COLS = [GOLD_BRIGHT, COPPER_TERRA, TEAL, IVORY_WHITE]   # e1 e2 e3 e4

# ---------- مسار الطيارة ----------
def _raw(u):
    ph = 2 * np.pi * u / 3.0
    return np.array([4.0 + 2.2 * np.cos(ph), 4.0 + 2.2 * np.sin(ph), 4.6 + 1.1 * np.sin(2 * ph)])


_U = np.linspace(0, 3, 1201)
_P = np.array([_raw(u) for u in _U])
_V = np.gradient(_P, _U, axis=0)


def _smooth_arr(a, w=61):
    pad = np.pad(a, (w // 2, w // 2), mode="edge")
    return np.convolve(pad, np.ones(w) / w, mode="valid")


_H = _smooth_arr(np.unwrap(np.arctan2(_V[:, 1], _V[:, 0])))
_BANK = _smooth_arr(np.clip(-0.16 * np.gradient(_H, _U), -0.4, 0.4))
_PITCH = _smooth_arr(np.clip(0.5 * np.arctan2(_V[:, 2], np.hypot(_V[:, 0], _V[:, 1])), -0.3, 0.3))


def _state(t):
    u = float(np.clip((t - T0) / (T1 - T0) * 3.0, 0, 3))
    pos = np.array([np.interp(u, _U, _P[:, i]) for i in range(3)])
    return pos, np.interp(u, _U, _H), np.interp(u, _U, _BANK), np.interp(u, _U, _PITCH)


def _pose3(heli, pos, heading, bank, pitch):
    heli.set_pose(np.asarray(pos, float) * G, heading, bank, 0.12 - 0.8 * pitch)


# ---------- أدوات ----------

class _Cap3:
    def __init__(self, scene, x=4.95, y=-3.0):
        self.scene, self.x, self.y, self.cur = scene, x, y, None

    def _fade(self, m, start, end, dur=0.7, remove=False, delay=0.0):
        t = [0.0]

        def up(mob, dt):
            t[0] += dt
            a = float(np.clip((t[0] - delay) / dur, 0.0, 1.0))
            mob.set_opacity(start + (end - start) * a)
            if a >= 1.0:
                mob.remove_updater(up)
                if remove:
                    self.scene.remove(mob)

        m.add_updater(up)

    def set(self, txt, color=GOLD_LIGHT, size=18):
        new = _ar(txt, size, color, True).move_to([self.x, self.y, 0])
        new.set_opacity(0)
        self.scene.add_fixed_in_frame_mobjects(new)
        self.scene.add(new)
        if self.cur is not None:
            self._fade(self.cur, 1.0, 0.0, dur=0.45, remove=True)
            self._fade(new, 0.0, 1.0, dur=0.7, delay=0.4)
        else:
            self._fade(new, 0.0, 1.0)
        self.cur = new
        return new


def _floor_and_walls():
    n = N
    L = n * G
    out = VGroup()
    P0, P1 = [], []
    for j in range(n + 1):
        P0.append([0, j * G, 0]); P1.append([L, j * G, 0])
        P0.append([j * G, 0, 0]); P1.append([j * G, L, 0])
    out.add(_segs(P0, P1, GOLD_LIGHT, 1.0, 0.20))
    P0, P1 = [], []
    for k in range(n + 1):
        P0.append([0, 0, k * G]); P1.append([L, 0, k * G])
        P0.append([k * G, 0, 0]); P1.append([k * G, 0, L])
        P0.append([0, 0, k * G]); P1.append([0, L, k * G])
        P0.append([0, k * G, 0]); P1.append([0, k * G, L])
    out.add(_segs(P0, P1, STONE_AXIS, 0.9, 0.11))
    return out


def _hud_column():
    nums = VGroup(*[DecimalNumber(10.0, num_decimal_places=1, font_size=38, color=IVORY_WHITE,
                                  edge_to_fix=RIGHT) for _ in range(4)]).arrange(DOWN, buff=0.3, aligned_edge=RIGHT)
    es = VGroup(*[_tex(rf"\mathbf{{e}}_{i}", 32, c) for i, c in zip((1, 2, 3, 4), COLS)])
    for e, n in zip(es, nums):
        e.next_to(n, RIGHT, buff=0.3)
    inner = VGroup(nums, es)
    h = inner.height + 0.3
    c = inner.get_center()
    lx, rx = inner.get_left()[0] - 0.25, inner.get_right()[0] + 0.25
    top, bot = c[1] + h / 2, c[1] - h / 2
    left = VMobject().set_points_as_corners([[lx + 0.12, top, 0], [lx, top, 0], [lx, bot, 0], [lx + 0.12, bot, 0]])
    right = VMobject().set_points_as_corners([[rx - 0.12, top, 0], [rx, top, 0], [rx, bot, 0], [rx - 0.12, bot, 0]])
    br = VGroup(left, right).set_stroke(IVORY_WHITE, 2.4)
    return VGroup(br, inner), nums, es


def _set_segs(vm, P0, P1):
    P0 = np.asarray(P0, float).reshape(-1, 3)
    P1 = np.asarray(P1, float).reshape(-1, 3)
    if len(P0) == 0:
        P0 = np.zeros((1, 3)); P1 = np.zeros((1, 3))
    d = P1 - P0
    vm.set_points(np.stack([P0, P0 + d / 3, P0 + 2 * d / 3, P1], axis=1).reshape(-1, 3))


def play_scene07(scene, keep_drawing=False):
    """keep_drawing=True: مفيش خروج في النهاية، والرسمة بتتسلّم للمشهد 8 في scene.mach_drawing."""
    _hud_fix(scene)
    cap = _Cap3(scene)

    S = ValueTracker(0.0)
    PX, PY, PZ, PT = (ValueTracker(0.0) for _ in range(4))
    FW = ValueTracker(0.0)
    BL = ValueTracker(0.0)
    SHX, SHY = ValueTracker(-1.9), ValueTracker(0.0)
    U = [ValueTracker(1.0) for _ in range(3)]
    DY = ValueTracker(0.0)

    def tnow():
        return T0 + S.get_value()

    def hpos():
        b = BL.get_value()
        return _state(tnow())[0] * (1 - b) + TARGET * b

    def htime():
        b = BL.get_value()
        return tnow() * (1 - b) + T_SNAP * b

    def comps():
        pos = hpos()
        return np.array([pos[0] * PX.get_value() / U[0].get_value(), pos[1] * PY.get_value() / U[1].get_value(),
                         pos[2] * PZ.get_value() / U[2].get_value(), htime() * PT.get_value()])

    # ---------- الخطوات (10:27.0 - 10:44.5) ----------
    # 10:27.0 - 10:44.5 | سرد الخطوات الثلاث الأولى: "طيب أنا بعد ما: 1- بحدد الخصائص.. 2- متجهات الأساس.. 3- نبني نظام الإحداثيات"
    steps = ["1- نحدد الخصائص", "2- نحدد متجهات الأساس + رموزها", "3- نبني نظام الإحداثيات", "4- نقيس بيه كل خاصية"]
    cols = [GOLD, COPPER_TERRA, GOLD_LIGHT, GOLD_BRIGHT]
    xs = [5.55, 2.2, -1.7, -5.0]
    ws = [2.5, 3.7, 3.0, 3.0]
    chips = [_chip(t, c, w=w, size=15).move_to([x, 3.3, 0]) for t, c, w, x in zip(steps, cols, ws, xs)]
    for c in chips[:3]:
        c.set_opacity(0.55)
    scene.set_camera_orientation(phi=58 * DEGREES, theta=-58 * DEGREES, zoom=1.0 * ZF, frame_center=CEN, focal_distance=1e5)
    scene.add_fixed_in_frame_mobjects(*chips)
    scene.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in chips], lag_ratio=0.25), run_time=2.0)
    scene.wait(15.5 * SPD)

    # 10:44.5 - 10:45.1 | تكبير الخطوة 4 بالتزامن مع: "4- هستخدم بقى نظام الإحداثيات نفسه في قياس وتحديد قيمة لكل خاصية..."
    scene.play(chips[3].animate.scale(1.08), run_time=0.6)

    # ---------- الكاميرا ----------
    lag = {"p": CEN.copy()}
    rig = Mobject()

    cam0 = scene.camera
    R_HOME = cam0.generate_rotation_matrix()

    def _fc_home(T, sh):
        zm, fd = cam0.get_zoom(), cam0.get_focal_distance()
        fc = T.copy()
        for _ in range(3):
            zs = (R_HOME @ (T - fc))[2]
            fac = fd / (fd - zs) if fd - zs > 1e-3 else 1.0
            A2 = zm * fac * R_HOME[:2, :2]
            fc[:2] = np.linalg.solve(A2 + np.eye(2), A2 @ T[:2] - sh)
            fc[2] = T[2]
        return fc

    def rig_up(m, dt):
        pos = hpos() * G
        lag["p"] = lag["p"] + (pos - lag["p"]) * min(1.0, dt * 3.0)
        T = CEN + (lag["p"] - CEN) * FW.get_value()
        cam = scene.camera
        R = cam.generate_rotation_matrix()
        zm, fd = cam.get_zoom(), cam.get_focal_distance()
        sh = np.array([SHX.get_value(), SHY.get_value()])
        target = sh + _fc_home(T, sh)[:2] - CEN[:2]
        fc = T.copy()
        for _ in range(3):
            zs = (R @ (T - fc))[2]
            fac = fd / (fd - zs) if fd - zs > 1e-3 else 1.0
            A2 = zm * fac * R[:2, :2]
            fc[:2] = T[:2] - np.linalg.solve(A2, target + CEN[:2])
            fc[2] = T[2]
        cam.frame_center = fc

    rig.add_updater(rig_up)
    scene.add(rig)

    # ---------- العالم والمحاور (10:45.1 - 10:48.4) ----------
    world = _floor_and_walls()
    axes = VGroup(*[_static_arrow([0, 0, 0], v, GOLD_MUTED, th=0.012, hl=0.2, r=0.06, rc=(1, 8), rk=(1, 10))
                    for v in ([(N + 1) * G, 0, 0], [0, (N + 1) * G, 0], [0, 0, (N + 1) * G])])
    names = [(_ar("شرق", 18, GOLD_MUTED), [(N + 1.9) * G, 0, 0]),
             (_ar("شمال", 18, GOLD_MUTED), [0, (N + 1.9) * G, 0]),
             (_ar("الارتفاع", 18, GOLD_MUTED), [0, 0, (N + 2) * G])]
    ticks = []
    for k in range(0, N + 1, 2):
        for pos in ([k * G, -0.28, 0], [-0.28, k * G, 0], [-0.28, 0, k * G]):
            if k == 0 and pos != [k * G, -0.28, 0]:
                continue
            ticks.append((_tex(str(k), 24, STONE_AXIS), pos))
    scene.add(world)
    scene.add(axes)
    scene.play(FadeIn(world), FadeIn(axes), run_time=2.5)
    fx = []
    for m, pos in names + ticks:
        m.move_to(pos)
        fx.append(m)
        scene.add_fixed_orientation_mobjects(m)
    scene.play(*[FadeIn(m) for m in fx], run_time=0.8)

    # ---------- الطائرة (10:48.4 - 10:52.0) ----------
    plane = make_helicopter(scale=0.42)
    _pose3(plane, *_state(T0))
    plane.set_fade(0.0)
    plane.add_updater(lambda m: _pose3(m, hpos(), *_state(tnow())[1:]))
    plane.start_rotors(scene)
    plane_lbl = _ar("الطيارة", 20, GOLD_BRIGHT, True)
    plane_lbl.move_to(_state(T0)[0] * G + OUT * 0.55)
    plane_lbl.add_updater(lambda m: m.move_to(hpos() * G + OUT * 0.55))
    scene.add_fixed_orientation_mobjects(plane_lbl)
    scene.add(plane)
    scene.play(UpdateFromAlphaFunc(plane, lambda m, a: m.set_fade(a)), FadeIn(plane_lbl), run_time=1.4)
    scene.wait(2.2 * SPD)

    # ---------- رصّ متجهات الأساس ----------
    pool = _Pool([COLS[0]] * N + [COLS[1]] * N + [COLS[2]] * N,
                 th=0.02, hl=0.15, r=0.055, rc=(1, 8), rk=(1, 10))

    yfade = {"a": 1.0}

    def upd_pool(_m=None):
        c = comps()
        u1, u2, u3 = (u.get_value() * G for u in U)
        X, Y, Z = c[0] * u1, c[1] * u2, c[2] * u3
        off = np.array([0.0, 0.0, 0.07])
        for k in range(N):
            f = float(np.clip(c[0] - k, 0, 1))
            s0 = np.array([k * u1, 0, 0.0]) + off
            pool.pose(k, s0, s0 + [f * u1, 0, 0])
            if DY.get_value() > 0.999:
                pool.pose(N + k, off, off)
            else:
                f = float(np.clip(c[1] - k, 0, 1))
                s0 = np.array([X, k * u2, 0.0]) + off
                pool.pose(N + k, s0, s0 + [0, f * u2, 0])
            f = float(np.clip((Z - off[2]) / u3 - k, 0, 1))
            s0 = np.array([X, Y, k * u3]) + off
            pool.pose(2 * N + k, s0, s0 + [0, 0, f * u3])
        a = 1.0 - DY.get_value()
        if abs(a - yfade["a"]) > 1e-3:
            yfade["a"] = a
            for k in range(N, 2 * N):
                for sm in pool.cyl[k] + pool.cone[k]:
                    sm.set_opacity(a)

    pool.group.add_updater(upd_pool)
    scene.add(pool.group)

    # متجهات e2 الكثيفة
    dense = VMobject()
    dense.set_fill(opacity=0)
    dense.set_stroke(COLS[1], 2.4, 0.0)
    _set_segs(dense, [[0, 0, 0]], [[0, 0, 0]])

    def upd_dense(m):
        a = DY.get_value()
        if a < 1e-3:
            m.set_stroke(opacity=0)
            return
        c = comps()
        u = U[1].get_value() * G
        X = c[0] * U[0].get_value() * G
        n = int(min(600, np.ceil(c[1] - 1e-9)))
        if n <= 0:
            m.set_stroke(opacity=0)
            return
        k = np.arange(n)
        L = np.clip(c[1] - k, 0, 1) * u
        hs = np.minimum(1.0, L / (1.3 * 0.15))
        hl, w = 0.15 * hs, 0.055 * hs
        z = np.full(n, 0.07)
        xs = np.full(n, X)
        a0 = np.stack([xs, k * u, z], 1)
        tip = np.stack([xs, k * u + L, z], 1)
        bk = np.stack([xs, k * u + L - hl, z], 1)
        P0 = np.concatenate([a0, tip, tip])
        P1 = np.concatenate([bk, bk + np.stack([w, 0 * w, 0 * w], 1), bk - np.stack([w, 0 * w, 0 * w], 1)])
        _set_segs(m, P0, P1)
        m.set_stroke(COLS[1], 2.4, a)

    dense.add_updater(upd_dense)
    scene.add(dense)

    # رموز e1 e2 e3
    def make_label(tex, color, anchor, vis, size=34, dx=0.0):
        t = _tex(tex, size, color)
        if dx:
            t.shift(RIGHT * dx)
            pad = Rectangle(width=2 * (abs(dx) + t.width / 2 + 0.05), height=0.02, stroke_width=0, fill_opacity=0)
            pad.move_to(ORIGIN)
            m = VGroup(t, pad)
        else:
            m = t
        la = ValueTracker(1.0)

        def up(mm):
            mm.move_to(anchor())
            t.set_opacity(float(np.clip(vis.get_value() * 4, 0, 1)) * la.get_value())

        m.add_updater(up)
        t.set_opacity(0)
        scene.add_fixed_orientation_mobjects(m)
        return m, la

    def a_e1():
        return np.array([1.2 * G, -0.65, 0.0])

    def a_e2():
        return np.array([comps()[0] * U[0].get_value() * G + 0.42, 0.55 * G, 0.15])

    def a_e3():
        c = comps()
        return np.array([c[0] * U[0].get_value() * G + 0.27, c[1] * U[1].get_value() * G + 0.17, 0.5 * G])

    elbl, lbl_a = [], []
    for i, an, vis in zip(range(3), (a_e1, a_e2, a_e3), (PX, PY, PZ)):
        m, la = make_label(rf"\mathbf{{e}}_{i + 1}", COLS[i], an, vis)
        elbl.append(m)
        lbl_a.append(la)

    sl_c = [5.0, -1.60, 0]
    slider = MachTimeSlider(center=sl_c, width=3.6, t_max=T_MAX, number_every=4, number_font_size=12, track_width=5.0)
    slider.attach(lambda: htime() * PT.get_value())
    unit = 3.6 / T_MAX
    x0 = sl_c[0] - 1.8
    ya = sl_c[1] + 0.34
    shafts = VGroup(*[Line([x0 + k * unit, ya, 0], [x0 + (k + 1) * unit, ya, 0], color=COLS[3], stroke_width=3.2)
                      for k in range(T_MAX)])
    heads = VGroup(*[Triangle(fill_color=COLS[3], fill_opacity=1, stroke_width=0).scale(0.042).rotate(-PI / 2)
                     .move_to([x0 + (k + 1) * unit, ya, 0]) for k in range(T_MAX)])
    head_base = heads[0].copy()
    e4_tag = _tex(r"\mathbf{e}_4", 30, COLS[3]).move_to([x0 - 0.4, ya, 0])

    def upd_e4(_m=None):
        ct = htime() * PT.get_value()
        for k in range(T_MAX):
            f = float(np.clip(ct - k, 0, 1))
            a = np.array([x0 + k * unit, ya, 0.0])
            b = a + [f * unit, 0, 0]
            if f < 0.04:
                shafts[k].set_stroke(opacity=0)
                heads[k].set_fill(opacity=0)
                continue
            hl = min(0.07, f * unit * 0.9)
            shafts[k].put_start_and_end_on(a, b - [hl * 0.8, 0, 0] if f * unit > hl else b)
            shafts[k].set_stroke(opacity=1)
            heads[k].become(head_base.copy().scale(hl / 0.07)).move_to(b - [hl * 0.5, 0, 0])
            heads[k].set_fill(opacity=1)

    slider.add_updater(upd_e4)
    upd_e4()
    scene.add_fixed_in_frame_mobjects(slider, shafts, heads, e4_tag)
    scene.remove(slider, e4_tag)

    hud, nums, hud_es = _hud_column()
    hud.move_to([5.35, 0.45, 0])
    for n_, i in zip(nums, range(4)):
        n_.set_value(comps()[i])
    hud_cap = _ar("أرقام التمثيل الإحداثي\nهي مركبات المتجه", 18, GOLD_LIGHT, True).move_to([5.3, 2.3, 0])
    scene.add_fixed_in_frame_mobjects(hud, hud_cap)
    scene.remove(hud, hud_cap)

    # ---------- الرحلة التفاعلية (10:52.0 - 11:39.0) ----------
    FLY = 27.5
    V = (T1 - T0) / FLY
    st = {"s": 0.0}

    def go(d, *anims, note=None, move=True):
        if move:
            st["s"] = min(T1 - T0, st["s"] + V * d)
            anims = (*anims, S.animate(rate_func=linear).set_value(st["s"]))
        if note is not None:
            cap.set(note[0], note[1], 18)
        scene.play(*anims, run_time=max(0.3, d * (0.5 if SPD < 1 else 1.0)))

    # 10:52.0 - 11:05.0 | "وهينتج عن عملية القياس دي أرقام، والأرقام دي هتكون هي أرقام التمثيل الإحداثي... مركبات المتجه"
    go(2.0, PX.animate.set_value(1.0), move=False, note=("بنرص متجهات الأساس\nعلى المحاور لحد الطيارة", COLS[1]))
    go(2.0, PY.animate.set_value(1.0), move=False)
    go(2.0, PZ.animate.set_value(1.0), FadeOut(plane_lbl), move=False)
    scene.remove(plane_lbl)
    go(2.5, PT.animate.set_value(1.0), FadeIn(slider), FadeIn(e4_tag), move=False,
       note=("والزمن بعد رابع:\nمتجهات e₄ على السلايدر", COLS[3]))
    scene.wait(4.5 * SPD)

    # 11:05.0 - 11:11.5 | "اللي هي في مثال الطيارة هتكون قايمة الأرقام دي: (3, 4, 5, 10)..."
    for n_, i in zip(nums, range(4)):
        n_.set_value(comps()[i])
    scene.camera.add_fixed_in_frame_mobjects(hud)
    go(1.2, FadeIn(hud, shift=LEFT * 0.2), FadeIn(hud_cap), move=False,
       note=("القياس بيدّينا أرقام\nهي مركبات المتجه", GOLD_LIGHT))
    for n_, i in zip(nums, range(4)):
        n_.add_updater(lambda m, i=i: (m.set_value(comps()[i]), scene.camera.add_fixed_in_frame_mobjects(m)))
    scene.wait(5.3 * SPD)

    # 11:11.5 - 11:23.0 | "يعني بشكل عام، فضاء أو نظام الإحداثيات ده بيدي لكل متجه جوة فضاء المتجهات قايمة واحدة محددة..."
    go(4.0, note=("لكل متجه قايمة واحدة\nمحددة من الأرقام", GOLD_BRIGHT))
    go(7.5)

    # 11:23.0 - 11:29.0 | "وقايمة الأرقام دي هي اللي بتصف المتجه جوة نظام الإحداثيات اللي احنا شغالين بيه..."
    go(6.0, note=("كل ما الطيارة تتحرك،\nالرصّة والأرقام بتختلف", GOLD_LIGHT))

    # 11:29.0 - 11:39.0 | "وهي اللي أنا بتعامل معاها وأنا بطبق قواعد جمع المتجهات، وقواعد ضرب المتجهات في رقم قياسي..."
    go(10.0, note=("الأرقام دي هي اللي هنجمعها\nونضربها في رقم قياسي", GOLD_BRIGHT))

    rem = (T1 - T0 - st["s"]) / V
    if rem > 0.1:
        go(rem)

    # 11:39.0 - 11:44.5 | "وماتقلقش، هتفهم أنا قصدي إيه في الجزئية دي تحديداً وأنا بشرحلك طريقة جمع المتجهات"
    scene.wait(5.5 * SPD)

    if keep_drawing:
        # تسليم الرسمة للمشهد 8 (من غير خروج ولا قطع)
        scene.mach_drawing = dict(
            chips=chips, world=world, axes=axes, fx=fx, plane=plane, pool=pool, dense=dense, slider=slider,
            shafts=shafts, heads=heads, e4_tag=e4_tag, hud=hud, nums=nums, hud_es=hud_es, hud_cap=hud_cap,
            elbl=elbl, lbl_a=lbl_a, make_label=make_label, cap=cap, rig=rig, comps=comps,
            S=S, PX=PX, PY=PY, PZ=PZ, PT=PT, FW=FW, BL=BL, SHX=SHX, SHY=SHY, U=U, DY=DY,
            a_e2=a_e2, a_e3=a_e3, COLS=COLS, upd_pool=upd_pool, a_e1=a_e1)
        return

    # ---------- خروج (11:44.5 - 11:46.0) ----------
    for m in (plane, pool.group, dense, slider, rig, *nums, *elbl):
        m.clear_updaters()
    plane.stop_rotors(scene)
    scene.play(FadeOut(VGroup(chips, world, axes, pool.group, dense, slider, shafts, heads, e4_tag, hud, hud_cap,
                              *fx, *elbl)),
               UpdateFromAlphaFunc(plane, lambda m, a: m.set_fade(1 - a)),
               FadeOut(cap.cur), run_time=1.3)
    scene.remove(plane)
    scene.remove(rig)
    scene.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ORIGIN)
    scene.wait(0.2)


class Dev(ThreeDScene):
    def construct(self):
        play_scene07(self)