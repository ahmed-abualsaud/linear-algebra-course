from manim import *
import os
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
from episode_04_common import _ar, _tex, ERR_RED, _hud_fix


# ==============================================================
# الحلقة 04 — المشهد 6 (ثلاثي الأبعاد): فضاء المتجهات = مسرح، فضاء الإحداثيات = سقالات
# لازم يتشغل داخل ThreeDScene.
# ==============================================================

TEAL = "#4FA7A0"
DIR_COL = [GOLD_BRIGHT, COPPER_TERRA, TEAL]
GS = 1.0                                   # طول وحدة الشبكة (= طول متجه الأساس الافتراضي)
RNG = (3, 3, 2)                            # مدى الفهرس على كل محور: -n..n
RNG_FAST = (2, 2, 1)                       # وضع المعاينة السريعة
BEND = 1.3                                 # شدة انحناء الفضاء (1.0 = القديم)


# ---------- أدوات رسم (كل حاجة في VMobject واحد = سريع) ----------

def _segs(P0, P1, color, width=2.0, opacity=1.0):
    vm = VMobject()
    vm.set_fill(opacity=0)
    vm.set_stroke(color, width, opacity)
    P0 = np.asarray(P0, float).reshape(-1, 3)
    P1 = np.asarray(P1, float).reshape(-1, 3)
    if len(P0) == 0:
        P0 = np.zeros((1, 3))
        P1 = np.zeros((1, 3))
    d = P1 - P0
    pts = np.stack([P0, P0 + d / 3, P0 + 2 * d / 3, P1], axis=1).reshape(-1, 3)
    vm.set_points(pts)
    return vm


def _rot_from_z(u):
    c = float(u[2])
    if c > 0.999999:
        return np.eye(3)
    if c < -0.999999:
        return np.diag([1.0, -1.0, -1.0])
    v = np.cross([0, 0, 1.0], u)
    s2 = float(v @ v)
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx * ((1 - c) / s2)


class _Pool:
    """
    أسهم مانيم ثلاثية الأبعاد (Line3D + Cone). السمك وحجم الرأس ثابتين،
    والطول بس هو اللي بيتغير (الساق بتتمدد/بتنكمش والرأس بيتحرك مع طرفها).
    """

    def __init__(self, colors, th=0.012, hl=0.16, r=0.05, rc=(1, 6), rk=(1, 8)):
        self.hl = hl
        self.arrows, self.cyl, self.cone, self.cyl_b, self.cone_b = [], [], [], [], []
        for c in colors:
            cyl = Line3D(ORIGIN, OUT, thickness=th, color=c, resolution=rc)
            cone = Cone(direction=OUT, base_radius=r, height=hl, show_base=False, resolution=rk, fill_color=c)
            g = VGroup(cyl, cone).set_color(c)
            cf = [m for m in cyl.get_family() if len(m.points) > 0]
            kf = [m for m in cone.get_family() if len(m.points) > 0]
            self.arrows.append(g)
            self.cyl.append(cf)
            self.cone.append(kf)
            self.cyl_b.append([m.points.copy() for m in cf])
            self.cone_b.append([m.points.copy() for m in kf])
        self.group = VGroup(*self.arrows)

    def pose(self, k, start, end):
        st = np.asarray(start, float)
        d = np.asarray(end, float) - st
        L = float(np.linalg.norm(d))
        if L < 1e-4:
            for sm in self.cyl[k] + self.cone[k]:
                sm.points = np.tile(st, (len(sm.points), 1))
            return
        R = _rot_from_z(d / L)
        hs = min(1.0, L / (1.3 * self.hl))
        sl = L - self.hl * hs
        for sm, B in zip(self.cyl[k], self.cyl_b[k]):
            B2 = B.copy()
            B2[:, 0] *= hs
            B2[:, 1] *= hs
            B2[:, 2] *= sl
            sm.points = st + B2 @ R.T
        for sm, B in zip(self.cone[k], self.cone_b[k]):
            B2 = B * hs
            B2[:, 2] += L
            sm.points = st + B2 @ R.T


def _static_arrow(start, end, color, **kw):
    p = _Pool([color], **kw)
    p.pose(0, start, end)
    return p.group


def _tri_color(t):
    """تدرج: قصير=تركواز، متوسط=ذهبي، طويل=نحاسي."""
    t = float(np.clip(t, 0, 1))
    if t < 0.5:
        return interpolate_color(ManimColor(TEAL), ManimColor(GOLD_BRIGHT), t * 2)
    return interpolate_color(ManimColor(GOLD_BRIGHT), ManimColor(COPPER_TERRA), (t - 0.5) * 2)


def _dashed(u, v, center, half, step, color, op, dash=0.3, width=1.0, n_bands=4, band_w=3):
    """شبكة متقطعة على مستوى (u,v) بتخفت مع البعد: بترجّع VGroup من bands."""
    center = np.asarray(center, float)
    m = int(half / step)
    out = VGroup()
    for band in range(n_bands):
        P0, P1 = [], []
        for fam, other in ((u, v), (v, u)):
            for i in range(-m, m + 1):
                if min(abs(i) // band_w, n_bands - 1) != band:
                    continue
                c = center + i * step * other
                n = int(2 * half / (2 * dash))
                t0 = -half + np.arange(n) * 2 * dash
                P0.append(c + t0[:, None] * fam)
                P1.append(c + (t0 + dash)[:, None] * fam)
        if P0:
            out.add(_segs(np.concatenate(P0), np.concatenate(P1), color, width, op * (0.55 ** band)))
    return out


def _window(aperture=1.0):
    """نافذة: إطار معتم بفتحة مستديرة الحواف + حدود ذهبية."""
    w, h = 14.0 * aperture, 7.8 * aperture
    hole = RoundedRectangle(corner_radius=0.45, width=w, height=h)
    mask = Difference(Rectangle(width=22, height=14), hole, fill_color="#000000", fill_opacity=1, stroke_width=0)
    rim1 = RoundedRectangle(corner_radius=0.45, width=w, height=h, stroke_color=GOLD_LIGHT, stroke_width=3.0,
                            stroke_opacity=0.9, fill_opacity=0)
    rim2 = RoundedRectangle(corner_radius=0.45, width=w + 0.18, height=h + 0.18, stroke_color=GOLD_MUTED,
                            stroke_width=1.2, stroke_opacity=0.5, fill_opacity=0)
    glow = RoundedRectangle(corner_radius=0.45, width=w - 0.1, height=h - 0.1, stroke_color=GOLD_LIGHT,
                            stroke_width=14, stroke_opacity=0.06, fill_opacity=0)
    return VGroup(mask, glow, rim1, rim2)


class _Note3D:
    """مربع ملاحظة صغير فوق اليمين: بيظهر عند النقاط المهمة بس."""

    def __init__(self, scene, x=4.45, y=2.85):
        self.scene, self.x, self.y, self.cur = scene, x, y, None

    def show(self, txt, color=GOLD_LIGHT, size=19, run_time=0.6):
        color = GOLD_LIGHT                      # كل الملاحظات بنفس اللون
        t = _ar(txt, size, color, True)
        bg = RoundedRectangle(corner_radius=0.14, width=t.width + 0.5, height=t.height + 0.36,
                              stroke_color=color, stroke_width=1.4, stroke_opacity=0.8,
                              fill_color="#0B0905", fill_opacity=0.82)
        g = VGroup(bg, t)
        g.move_to(ORIGIN).align_to([6.72, 3.62, 0], UR)   # ملزوق في كورنر النافذة
        self.scene.add_fixed_in_frame_mobjects(g)
        old = self.cur
        self.scene.play(FadeIn(g, shift=LEFT * 0.15), *([FadeOut(old)] if old is not None else []), run_time=run_time)
        if old is not None:
            self.scene.remove(old)
        self.cur = g

    def hide(self, run_time=0.5):
        if self.cur is not None:
            self.scene.play(FadeOut(self.cur), run_time=run_time)
            self.scene.remove(self.cur)
            self.cur = None


def _smooth(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def play_scene06(scene, part=None, fast=None):
    """
    part: None = المشهد كله | 1 = البناء والتحويل لمتجهات | 2 = الانهيار والتحولات الحرة | 3 = الانحناء والانهيار لـ 2D
    fast: True = معاينة سريعة (أسهم أقل). لو None بيتقرأ من متغيرات البيئة FAST و PART.
    الأجزاء بتتوصل من غير قفزات لأن كل جزء بينتهي بوضع كاميرا ثابت ومتجهات حالة معروفة.
    """
    if part is None:
        part = int(os.environ.get("PART", "0")) or None
    if fast is None:
        fast = os.environ.get("FAST", "0") == "1"
    RN = RNG_FAST if fast else RNG
    do = lambda p: part is None or part == p

    _hud_fix(scene)
    note = _Note3D(scene)

    # ---------- حالة الشبكة (كل التحولات عن طريق trackers) ----------
    T = {k: ValueTracker(v) for k, v in dict(
        b=0.0,      # بناء السقالات (من تحت لفوق)
        f=0.0,      # السقالات ← متجهات أساس (0..2)
        R=0.0,      # موجة ظهور متجهات الأساس
        S=1.0,      # الانتشار (0 = كلهم عند المركز)
        W=0.0,      # الانحناء
        GL=0.0,     # ظهور خطوط الشبكة
        ZL=0.0,     # إبراز خطوط/مستويات z وقت الانهيار
        rot=0.0, sx=1.0, sy=1.0, sh=0.0, zc=1.0,
    ).items()}

    def basis():
        th = T["rot"].get_value()
        c, s = np.cos(th), np.sin(th)
        Rz = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        a = Rz @ np.array([GS * T["sx"].get_value(), 0, 0])
        b = Rz @ np.array([GS * T["sh"].get_value(), GS * T["sy"].get_value(), 0])
        cc = np.array([0, 0, GS * T["zc"].get_value()])
        return np.array([a, b, cc])

    def warp(P):
        w = T["W"].get_value()
        if abs(w) < 1e-9:
            return P
        w = w * BEND
        Q = P.copy()
        Q[:, 0] += w * 0.72 * np.sin(0.45 * P[:, 1] + 0.3 * P[:, 2])
        Q[:, 1] += w * 0.72 * np.sin(0.45 * P[:, 2] + 0.3 * P[:, 0])
        Q[:, 2] += w * 0.45 * np.sin(0.45 * P[:, 0] + 0.2 * P[:, 1])
        return Q

    I, J, K = np.meshgrid(np.arange(-RN[0], RN[0] + 1), np.arange(-RN[1], RN[1] + 1),
                          np.arange(-RN[2], RN[2] + 1), indexing="ij")
    NODES = np.stack([I, J, K], -1).reshape(-1, 3).astype(float)
    STARTS = [NODES[NODES[:, d] < RN[d]] for d in range(3)]
    RHO_MAX = np.sqrt(RN[0] ** 2 + RN[1] ** 2 + 2.25 * RN[2] ** 2)

    def rho(ijk):
        return np.sqrt(ijk[:, 0] ** 2 + ijk[:, 1] ** 2 + 2.25 * ijk[:, 2] ** 2) / RHO_MAX

    def empty():
        return _segs([[0, 0, 0]], [[0, 0, 0]], GOLD_LIGHT, 0, 0)

    # ---------- متجهات الأساس المتراصة (أسهم مانيم 3D) على خطوط الشبكة ----------
    A_ijk, A_dir = [], []
    for d in range(3):
        for st_ in STARTS[d]:
            A_ijk.append(st_)
            A_dir.append(d)
    A_ijk = np.array(A_ijk, float)
    A_dir = np.array(A_dir)
    A_phase = np.sin(1.3 * A_ijk[:, 0] + 0.9 * A_ijk[:, 1] + 0.7 * A_ijk[:, 2] + 1.7 * A_dir)
    A_rho = rho(A_ijk)
    stack_pool = _Pool([DIR_COL[d] for d in A_dir], th=0.014, hl=0.17, r=0.055, rc=(1, 6), rk=(1, 8))
    core_pool = _Pool(DIR_COL, th=0.03, hl=0.26, r=0.09, rc=(2, 16), rk=(2, 20))
    last = {"W": None, "S": None, "z": None}

    def upd_stack(_m=None):
        M = basis()
        Rv, S, W = T["R"].get_value(), T["S"].get_value(), T["W"].get_value()
        Wc = float(np.clip(W, 0, 1))
        vecs = M[A_dir]
        P = A_ijk @ M
        Pw = warp(P)
        Tg = warp(P + 0.05 * vecs) - warp(P - 0.05 * vecs)
        u = Tg / np.maximum(np.linalg.norm(Tg, axis=1, keepdims=True), 1e-9)
        ln = np.linalg.norm(vecs, axis=1)
        prog = _smooth((Rv * 1.5 - A_rho) / 0.5)
        lf = 1.0 + Wc * (0.4 * A_phase - 0.1)             # أطوال مختلفة وهي بتنحني
        zc = T["zc"].get_value()
        fz = np.where(A_dir == 2, np.clip(zc * 3, 0, 1), 1.0)
        A = S * Pw
        L = ln * prog * lf * fz
        if S < 0.03:
            L = L * 0
        E = A + u * L[:, None]
        for k in range(len(A_dir)):
            stack_pool.pose(k, A[k], E[k])
        if last["W"] is None or abs(W - last["W"]) > 1e-4:
            last["W"] = W
            for k in range(len(A_dir)):
                base = DIR_COL[A_dir[k]]
                col = base if Wc < 1e-3 else interpolate_color(
                    ManimColor(base), _tri_color((lf[k] - 0.45) / 1.0), Wc)
                stack_pool.arrows[k].set_color(col)

    def upd_core(_m=None):
        M = basis()
        S = T["S"].get_value()
        zc = T["zc"].get_value()
        for d in range(3):
            vec = M[d]
            ln = np.linalg.norm(vec)
            O = np.zeros((1, 3))
            Tg = warp(O + 0.05 * vec) - warp(O - 0.05 * vec)
            u = (Tg / max(np.linalg.norm(Tg), 1e-9))[0]
            fz = float(np.clip(zc * 3, 0, 1)) if d == 2 else 1.0
            op = float(np.clip(1.0 - 2.2 * S, 0, 1)) * fz
            if op < 1e-3 or ln < 1e-4:
                core_pool.pose(d, [0, 0, 0], [0, 0, 0])
            else:
                core_pool.pose(d, [0, 0, 0], u * ln)
            key = (round(op, 3), d)
            if last.get(("op", d)) != key:
                last[("op", d)] = key
                core_pool.arrows[d].set_opacity(op)

    stack_pool.group.add_updater(upd_stack)
    core_pool.group.add_updater(upd_core)

    # ---------- شبكة الإحداثيات ثلاثية الأبعاد: 3 مستويات (xy أقوى) + المحاور ----------
    NS = 14 if fast else 26
    EXT = (5, 5, 3) if fast else (7, 7, 4)

    def planes():
        M = basis()
        gl = T["GL"].get_value()
        out = VGroup()
        if gl < 1e-3:
            return VGroup(empty())
        buckets = {}
        for (a_, b_) in ((0, 1), (0, 2), (1, 2)):
            main = (a_, b_) == (0, 1)
            for fam, oth in ((a_, b_), (b_, a_)):
                idx = np.array([i for i in range(-EXT[oth], EXT[oth] + 1) if i != 0])
                t = np.linspace(-(EXT[fam] + 0.5), EXT[fam] + 0.5, NS)
                ijk = np.zeros((len(idx), NS, 3))
                ijk[:, :, oth] = idx[:, None]
                ijk[:, :, fam] = t[None, :]
                pts = warp(ijk.reshape(-1, 3) @ M).reshape(len(idx), NS, 3)
                buckets.setdefault((fam, main), []).append((pts[:, :-1].reshape(-1, 3), pts[:, 1:].reshape(-1, 3)))
        for (fam, main), lst in buckets.items():
            if np.linalg.norm(M[fam]) < 1e-6:
                continue
            P0 = np.concatenate([x[0] for x in lst])
            P1 = np.concatenate([x[1] for x in lst])
            zl = T["ZL"].get_value()
            op = 0.5 if main else 0.2 + 0.6 * zl
            w_ = 1.2 if main else 1.0 + 1.0 * zl
            out.add(_segs(P0, P1, DIR_COL[fam], w_, op * gl))
        for d in range(3):
            if np.linalg.norm(M[d]) < 1e-6:
                continue
            t = np.linspace(-(EXT[d] + 0.5), EXT[d] + 0.5, NS)
            ijk = np.zeros((NS, 3))
            ijk[:, d] = t
            pts = warp(ijk @ M)
            out.add(_segs(pts[:-1], pts[1:], DIR_COL[d], 3.0, 0.9 * gl))
        return out

    # ---------- السقالات: أعمدة + روافد + وصلات (بدون تكتيف قطري ولا ألواح) ----------
    A0 = np.diag([GS, GS, GS])
    KN = 2 * RN[2]
    TT = KN + 1.5

    def scaffold():
        t = T["b"].get_value() * TT
        f = T["f"].get_value()
        mix = float(np.clip(f, 0, 1))
        eo = float(1 - np.clip(f - 1, 0, 1))
        xo = float(1 - np.clip(f, 0, 1))
        if t <= 1e-6:
            return VGroup(empty())
        out = VGroup()
        steel = [GOLD_MUTED, STONE_AXIS, STONE_AXIS]
        wid = [2.6, 1.8, 1.8]
        wins = [lambda k: k + 0.5, lambda k: k + 0.5, lambda k: k]
        for d in (2, 0, 1):
            st = STARTS[d]
            kid = st[:, 2] + RN[2]
            prog = np.clip(t - wins[d](kid), 0, 1)
            m = prog > 1e-4
            if not m.any():
                continue
            P = st[m] @ A0
            col = interpolate_color(ManimColor(steel[d]), ManimColor(DIR_COL[d]), mix)
            out.add(_segs(P, P + prog[m][:, None] * A0[d], col, wid[d], eo))
        jp0, jp1 = [], []
        for kid in range(KN + 1):
            sz = float(np.clip(t - (kid + 1.0), 0, 1)) * 0.1
            if sz <= 1e-3:
                continue
            lv = NODES[NODES[:, 2] == kid - RN[2]] @ A0
            for ax in range(3):
                e = np.zeros(3)
                e[ax] = sz
                jp0.append(lv - e), jp1.append(lv + e)
        if jp0:
            out.add(_segs(np.concatenate(jp0), np.concatenate(jp1), GOLD_BRIGHT, 2.0, xo))
        return out

    # ---------- عالم فضاء المتجهات (مش غرفة): شبكات متقطعة + غبار + متجهات حرة ----------
    world = VGroup()
    world.add(*_dashed(RIGHT, UP, [0, 0, -3.0], 15, 1.5, STONE_AXIS, 0.7, dash=0.3, width=1.0))
    ang = 30 * DEGREES
    u2 = np.array([np.cos(ang), np.sin(ang), 0])
    v2 = np.array([-np.sin(ang), np.cos(ang), 0])
    world.add(*_dashed(u2, v2, [0, 0, -3.0], 13, 2.0, COPPER_TERRA, 0.28, dash=0.3, width=0.9))
    world.add(*_dashed(RIGHT, np.array([0.75, 1, 0]) / 1.0, [0, 0, -3.0], 12, 2.0, TEAL, 0.22, dash=0.3, width=0.9))
    world.add(*_dashed(RIGHT, OUT, [0, 0, 0], 14, 3.0, STONE_AXIS, 0.2, dash=0.3, width=0.8, n_bands=3))
    world.add(*_dashed(UP, OUT, [0, 0, 0], 14, 3.0, STONE_AXIS, 0.2, dash=0.3, width=0.8, n_bands=3))
    rs = np.random.RandomState(7)
    dust_c = rs.uniform(-15, 15, size=(520, 3))
    dust_c[:, 2] = rs.uniform(-8, 12, size=520)
    dd = rs.normal(size=(520, 3))
    dd /= np.linalg.norm(dd, axis=1, keepdims=True)
    world.add(_segs(dust_c, dust_c + dd * 0.07, IVORY_WHITE, 1.6, 0.3))

    free = VGroup()
    near = [(2.6, 1.8, 1.4), (-2.2, 2.4, 0.8), (-1.6, -2.4, 1.9), (2.0, -2.2, -0.9), (0.5, 3.0, -1.4),
            (-3.0, -0.6, -1.3)]
    cols = [GOLD_BRIGHT, COPPER_TERRA, IVORY_WHITE, GOLD_LIGHT, TEAL, GOLD_MUTED]
    for dv, c in zip(near, cols):
        free.add(_static_arrow([0, 0, 0], dv, c, th=0.02, hl=0.3, r=0.09, rc=(2, 10), rk=(2, 12)))
    far = VGroup()
    for n in range(9):
        p = rs.uniform(-1, 1, 3)
        p = p / np.linalg.norm(p) * rs.uniform(7, 13)
        dv = rs.normal(size=3)
        dv = dv / np.linalg.norm(dv) * rs.uniform(1.5, 2.6)
        far.add(_static_arrow(p, p + dv, cols[n % 6], th=0.02, hl=0.3, r=0.09, rc=(2, 10), rk=(2, 12)))

    # ---------- النافذة ----------
    ap = ValueTracker(0.12)
    win = always_redraw(lambda: _window(ap.get_value()))

    gridm = always_redraw(planes)
    scaf = always_redraw(scaffold)
    stk = stack_pool.group
    cor = core_pool.group
    # ---------- 3) ننهار عند المركز ----------
    labels = VGroup(*[_tex(s, 46, c) for s, c in zip((r"\mathbf{e}_1", r"\mathbf{e}_2", r"\mathbf{e}_3"), DIR_COL)])

    def lbl_updater(i):
        def up(m):
            M = basis()
            ln = np.linalg.norm(M[i])
            u = M[i] / max(ln, 1e-9)
            o = M[{0: 1, 1: 0, 2: 0}[i]]
            on = o / max(np.linalg.norm(o), 1e-9)
            m.move_to(M[i] + 0.22 * u - 0.42 * on)          # الرمز بعيد عن الخط
            if i == 2:
                m.set_opacity(float(np.clip(T["zc"].get_value() * 3, 0, 1)))
        return up

    for i, l in enumerate(labels):
        l.add_updater(lbl_updater(i))
        l.move_to(basis()[i] * 1.1)


    if do(1):
        # ---------- لقطة 1: بنفتح النافذة على فضاء المتجهات (07:54.0 - 08:00.0) ----------
        scene.set_camera_orientation(phi=74 * DEGREES, theta=-38 * DEGREES, zoom=0.6, frame_center=[0, 0, 0])
        scene.add(world)
        scene.add(free, far)
        scene.add_fixed_in_frame_mobjects(win)
        scene.add_foreground_mobject(win)
        scene.begin_ambient_camera_rotation(rate=0.07)
        # 07:54.0 - 07:56.5 | "بعد كدة هستخدم متجهات الأساس دي في بناء شيء اسمه نظام الإحداثيات، أو فضاء الإحداثيات..."
        scene.play(ap.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        win.clear_updaters()
        note.show("فضاء المتجهات = عالم كامل", GOLD_LIGHT, run_time=0.5)
        # 07:56.5 - 08:00.0 | استقرار النافذة
        scene.wait(3.0)
        note.hide(run_time=0.5)

        # ---------- النافذة بتتحرك لمناطق تانية من العالم (08:00.0 - 08:07.5) ----------
        # 08:00.0 - 08:07.5 | "فضاء الإحداثيات ده بيكون موجود داخل فضاء المتجهات..."
        scene.stop_ambient_camera_rotation()
        scene.move_camera(phi=82 * DEGREES, theta=-8 * DEGREES, zoom=0.75, frame_center=[5, -4, 1], run_time=2.5)
        scene.move_camera(phi=66 * DEGREES, theta=-95 * DEGREES, zoom=0.7, frame_center=[-5, 4, 2], run_time=2.5)
        scene.move_camera(phi=68 * DEGREES, theta=-52 * DEGREES, zoom=1.25, frame_center=[0, 0, 0], run_time=2.5)
        scene.begin_ambient_camera_rotation(rate=0.08)

        # ---------- 1) السقالات بتتنصب (08:07.5 - 08:15.0) ----------
        # 08:07.5 - 08:15.0 | "يعني فضاء المتجهات ده تقدر تعتبره مسرح الأحداث وفضاء الإحداثيات ده هي سقالات منصوبة داخل فضاء المتجهات..."
        scene.add(gridm, scaf, stk, cor)
        note.show("فضاء الإحداثيات = سقالات\nمنصوبة جوه فضاء المتجهات", COPPER_TERRA, run_time=0.5)
        scene.play(T["b"].animate.set_value(1.0), FadeOut(far), FadeOut(free), run_time=6.0, rate_func=linear)
        scene.remove(far, free)
        note.hide(run_time=0.5)
        scene.wait(0.5)

        # ---------- 2) كل سقالة ← متجه أساس (08:15.0 - 08:23.5) ----------
        # 08:15.0 - 08:23.5 | "...عشان تقدر تستخدم السقالات دي في إنك توصل بيها لأكبر مساحة ممكنة داخل فضاء المتجهات"
        note.show("كل سقالة بتتحول\nلمتجه أساس", GOLD_BRIGHT, run_time=0.5)
        scene.play(T["f"].animate.set_value(1.0), T["GL"].animate.set_value(1.0), run_time=1.5)
        scene.play(T["R"].animate.set_value(1.0), run_time=4.5, rate_func=linear)
        scene.play(T["f"].animate.set_value(2.0), run_time=1.0)
        note.hide(run_time=0.5)
        scene.wait(0.5)

        # ---- نهاية الجزء 1: وضع كاميرا ثابت (08:23.5 - 08:25.5) ----
        scene.stop_ambient_camera_rotation()
        scene.move_camera(phi=68 * DEGREES, theta=-50 * DEGREES, zoom=1.25, frame_center=[0, 0, 0], run_time=1.5)
        scene.wait(0.5)

    if do(2):
        if part == 2:
            # حالة بداية الجزء 2 = نهاية الجزء 1
            win = _window(1.0)
            for k_, v_ in dict(b=1.0, f=2.0, R=1.0, S=1.0, GL=1.0).items():
                T[k_].set_value(v_)
            scene.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES, zoom=1.25, frame_center=[0, 0, 0])
            scene.add(world)
            scene.add_fixed_in_frame_mobjects(win)
            scene.add_foreground_mobject(win)
            scene.add(gridm, scaf, stk, cor)
            scene.begin_ambient_camera_rotation(rate=0.08)

        # ---------- 3) تنصب السقالات بأي طريقة (08:25.5 - 08:44.5) ----------
        # 08:25.5 - 08:35.5 | "وتقدر تركب السقالات دي وتنصبها بأي طريقة انت عاوزها جوة فضاء المتجهات، طبعاً بعد ما بتحدد متجهات الأساس اللي انت هتستخدمها..."
        scene.stop_ambient_camera_rotation()
        scene.move_camera(phi=46 * DEGREES, theta=-50 * DEGREES, zoom=1.0, frame_center=[0, 0, 0], run_time=2.5)
        note.show("تقدر تنصب السقالات\nبأي طريقة تحبها", GOLD_BRIGHT, run_time=0.5)
        scene.wait(2.0)
        note.show("دوران", GOLD_LIGHT, run_time=0.4)
        scene.play(T["rot"].animate.set_value(50 * DEGREES), run_time=3.0, rate_func=smooth)
        note.show("مط", GOLD_LIGHT, run_time=0.4)
        scene.play(T["sx"].animate.set_value(1.6), run_time=2.5, rate_func=smooth)
        note.show("انكماش", GOLD_LIGHT, run_time=0.4)
        scene.play(T["sy"].animate.set_value(0.6), T["sx"].animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        note.show("قص — Shear", GOLD_LIGHT, run_time=0.4)
        scene.play(T["sh"].animate.set_value(0.7), T["sy"].animate.set_value(0.9), run_time=2.5, rate_func=smooth)

        # 08:35.5 - 08:44.5 | "يعني مثلاً لو أنا في البداية حددت إن متجهات الأساس اللي هبني بيها فضاء الإحداثيات دي إنها تكون متعامدة على بعض..."
        scene.wait(1.5)
        note.show("كل تحويل = متجهات أساس\nجديدة ملزوقة في بعض", GOLD_LIGHT, run_time=0.5)
        scene.wait(2.5)
        note.hide(run_time=0.4)
        scene.play(T["rot"].animate.set_value(0.0), T["sx"].animate.set_value(1.0), T["sy"].animate.set_value(1.0),
                   T["sh"].animate.set_value(0.0), run_time=3.5, rate_func=smooth)
        scene.wait(1.0)

        # ---------- 4) ننهار عند المركز (08:44.5 - 09:10.5) ----------
        # 08:44.5 - 09:01.5 | "وقتها بعرف إني هستخدم فضاء أو نظام إحداثيات اسمه نظام الإحداثيات الكارتيزية أو الديكارتية المتعامد... وده نظام الإحداثيات اللي شرحتلك بيه مثال الطيارة"
        scene.move_camera(phi=62 * DEGREES, theta=-50 * DEGREES, zoom=1.25, frame_center=[0, 0, 0],
                          added_anims=[T["S"].animate.set_value(0.0)], run_time=5.0)
        scene.begin_ambient_camera_rotation(rate=0.08)
        for l in labels:
            scene.add_fixed_orientation_mobjects(l)
        scene.play(FadeIn(labels), run_time=0.8)
        note.show("متجه أساس لكل بُعد\nوخطوط الشبكة بتفضل", GOLD_LIGHT, run_time=0.5)

        # 09:01.5 - 09:10.5 | "ونظام الإحداثيات بعد كدة هيحدد قايمة واحدة محددة لكل متجه في فضاء المتجهات زي ما هنشوف كمان شوية..."
        scene.wait(8.0)
        note.hide(run_time=0.5)
        scene.play(*[m.animate.set_stroke(opacity=m.get_stroke_opacity() * 0.3) for m in world], run_time=1.5)

        # ---------- 5) متجهات الأساس تنبثق من المركز على الخطوط (09:10.5 - 09:22.5) ----------
        # 09:10.5 - 09:20.5 | "يعني اللي أنا عايز أقوله هنا إنك ممكن تستخدم أي نظام إحداثيات كارتيزية انت عاوزه سواء كانت إحداثيات متعامدة أو حتى إحداثيات مائلة بأي متجه أساس..."
        scene.play(T["S"].animate.set_value(1.0), run_time=6.5, rate_func=smooth)
        scene.wait(3.5)

        # ---- نهاية الجزء 2: وضع كاميرا ثابت (09:20.5 - 09:22.5) ----
        scene.stop_ambient_camera_rotation()
        scene.move_camera(phi=46 * DEGREES, theta=-40 * DEGREES, zoom=1.3, frame_center=[0, 0, 0], run_time=1.5)
        scene.wait(0.5)

    if do(3):
        if part == 3:
            # حالة بداية الجزء 3 = نهاية الجزء 2
            win = _window(1.0)
            for k_, v_ in dict(b=1.0, f=2.0, R=1.0, S=1.0, GL=1.0).items():
                T[k_].set_value(v_)
            scene.set_camera_orientation(phi=46 * DEGREES, theta=-40 * DEGREES, zoom=1.3, frame_center=[0, 0, 0])
            for m in world:
                m.set_stroke(opacity=m.get_stroke_opacity() * 0.3)
            scene.add(world)
            scene.add_fixed_in_frame_mobjects(win)
            scene.add_foreground_mobject(win)
            scene.add(gridm, scaf, stk, cor)
            for l in labels:
                scene.add_fixed_orientation_mobjects(l)
            scene.add(labels)

        # ---------- 6) الانحناء ← خطأ (من عدة زوايا) (09:22.5 - 09:34.5) ----------
        scene.stop_ambient_camera_rotation()
        cross = VGroup(Line([-2.4, -1.6, 0], [2.4, 1.6, 0]), Line([-2.4, 1.6, 0], [2.4, -1.6, 0])).set_stroke(
            ERR_RED, 14, opacity=0.9)
        cross.move_to([0, -0.2, 0])
        scene.add_fixed_in_frame_mobjects(cross)
        scene.remove(cross)                      # متسجلة ثابتة في الشاشة بس مش ظاهرة لحد ما تتعمل Create

        # 09:22.5 - 09:27.0 | "لكن المهم إن متجهات الأساس دي تكون ثابتة ومش بتتغير من مكان للتاني داخل فضاء المتجهات..."
        note.show("متجهات الأساس لازم تكون\nثابتة في كل مكان", GOLD_BRIGHT, run_time=0.5)
        scene.wait(3.5)
        note.hide(run_time=0.4)

        # 09:27.0 - 09:34.5 | "...وإلا وقتها مش هنكون بنشرح جبر خطي أصلاً"
        scene.move_camera(phi=64 * DEGREES, theta=-60 * DEGREES, zoom=1.3, frame_center=[0, 0, 0],
                          added_anims=[T["W"].animate.set_value(1.0)], run_time=6.0)
        note.show("الشبكة بتنحني ← خرجنا\nمن الجبر الخطي", ERR_RED, run_time=0.5)
        scene.play(Create(cross), run_time=0.8)
        scene.wait(2.5)
        scene.play(FadeOut(cross), run_time=0.5)
        note.hide(run_time=0.4)

        # زوايا مختلفة للشبكة المنحنية: من فوق، من الجنب، ومن زاوية تانية
        scene.move_camera(phi=12 * DEGREES, theta=-90 * DEGREES, zoom=1.2, frame_center=[0, 0, 0], run_time=1.5)
        scene.wait(0.5)
        scene.move_camera(phi=88 * DEGREES, theta=-90 * DEGREES, zoom=1.2, frame_center=[0, 0, 0], run_time=1.5)
        scene.wait(0.5)
        scene.move_camera(phi=60 * DEGREES, theta=-15 * DEGREES, zoom=1.3, frame_center=[0, 0, 0], run_time=1.5)
        scene.wait(0.5)

        # ---------- 7) تعتدل ← تنهار (09:34.5 - 09:44.5) ----------
        # 09:34.5 - 09:44.5 | "وخلي بالك من نقطة مهمة: إنه مش شرط فضاء الإحداثيات أو السقالات دي تكون موجودة جوة كل جزء داخل فضاء المتجهات..."
        scene.move_camera(phi=62 * DEGREES, theta=-50 * DEGREES, zoom=1.25, frame_center=[0, 0, 0],
                          added_anims=[T["W"].animate.set_value(0.0)], run_time=3.5)
        scene.wait(1.0)
        scene.play(T["S"].animate.set_value(0.0), run_time=2.5, rate_func=smooth)
        scene.wait(0.5)

        # ---------- 8) انهيار 3D ← 2D (09:44.5 - 09:58.5) ----------
        # 09:44.5 - 09:58.5 | "ممكن فضاء الإحداثيات ده يكون بيغطي جزء محدد من فضاء المتجهات وباقي الأجزاء انت مش قادر توصلها أصلاً... لأن متجهات الأساس اللي انت اخترتها من البداية مش بتساعدك على كدة"
        scene.stop_ambient_camera_rotation()
        scene.move_camera(phi=76 * DEGREES, theta=-34 * DEGREES, zoom=1.15, frame_center=[0, 0, 0], run_time=2.0)
        note.show("مش شرط السقالات تغطي\nكل أبعاد فضاء المتجهات", GOLD_LIGHT, run_time=0.4)
        scene.play(T["ZL"].animate.set_value(1.0), run_time=1.0)
        scene.wait(1.0)
        note.hide(run_time=0.3)
        scene.begin_ambient_camera_rotation(rate=0.05)
        scene.play(T["zc"].animate.set_value(0.0), run_time=5.5, rate_func=smooth)
        scene.wait(0.8)

        # ---------- 9) فضاء جزئي Subspace & Span (09:58.5 - 10:25.5) ----------
        # 09:58.5 - 10:05.5 | "يعني مش شرط إن عدد متجهات الأساس اللي بنختارها يغطي كل أبعاد فضاء المتجهات..."
        scene.stop_ambient_camera_rotation()
        scene.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.3, run_time=2.5)

        # 10:05.5 - 10:16.5 | "لأننا ممكن نكتفي بمتجهات أساس تبنيلنا 'فضاء إحداثيات جزئي' أو Subspace بيغطي جزء محدد بس من الأبعاد..."
        note.show("فضاء إحداثيات جزئي — Subspace", GOLD_LIGHT, run_time=0.4)
        scene.wait(10.6)

        # 10:16.5 - 10:25.5 | "والجزئية دي هنرجع لها تاني إن شاء الله لما نتكلم عن حاجة اسمها الامتداد أو الـ span والاستقلال الخطي أو الـ linear independence"
        note.show("هنرجعله مع الـ span\nوالـ linear independence", GOLD_LIGHT, run_time=0.5)
        scene.wait(8.0)
        note.hide(run_time=0.5)

        # ---------- خروج (10:25.5 - 10:27.0) ----------
        for m in (gridm, scaf, stk, cor):
            m.clear_updaters()
        for l in labels:
            l.clear_updaters()
        scene.play(FadeOut(VGroup(world, gridm, scaf, stk, cor, labels, win)), run_time=1.2)
        scene.remove_foreground_mobject(win)
        scene.remove(win)
        scene.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=[0, 0, 0])
        scene.wait(0.3)


class Dev(ThreeDScene):
    def construct(self):
        play_scene06(self)