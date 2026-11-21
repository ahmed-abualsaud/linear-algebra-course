"""
الفصل 9 — السطح المنحني: مستوى ← جزء كرة ← سرج حصان.
"""
from functools import lru_cache
from manim import *
import numpy as np

from common.palette import GOLD_LIGHT, GOLD_BRIGHT, GOLD_MUTED, COPPER_TERRA, IVORY_WHITE, STONE_AXIS
from episode_05_common import *
try:
    from common.palette import LABEL_MUTED
except ImportError:
    LABEL_MUTED = "#DCD6CD"

KAPPA = 0.55
SC = 1.05
WX0, WX1, WY0, WY1 = -6.8, 2.9, -2.35, 3.1
CEN = np.array([0.5 * (WX0 + WX1), 0.5 * (WY0 + WY1), 0.0])
DOM_X, DOM_Y = (-0.8, 3.2), (-0.8, 3.0)
U0 = np.array([2.0, 0.4])
V0 = np.array([0.4, 1.7])
NSTEP = 48
CX, CY = 0.5 * (DOM_X[0] + DOM_X[1]), 0.5 * (DOM_Y[0] + DOM_Y[1])

CAM = dict(az=np.radians(35.0), el=np.radians(60.0), zoom=1.0, f=0.0)
LIGHT = np.array([-0.45, -0.55, 0.70])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


def _coef(s):
    a = min(1.0, max(0.0, s))
    b = min(1.0, max(0.0, s - 1.0))
    A = -(1 - b) * a + b
    B = -(1 - b) * a - b
    return A, B


def _z(x, y, s):
    A, B = _coef(s)
    return 0.5 * KAPPA * (A * x * x + B * y * y)


def _leg(p, d, w, s):
    A, B = _coef(s)
    H = KAPPA * np.array([[A, 0.0], [0.0, B]])

    def f(st):
        p_, d_, w_ = st[0:2], st[2:4], st[4:6]
        g = KAPPA * np.array([A * p_[0], B * p_[1]])
        den = 1.0 + g @ g
        return np.concatenate([d_, -(d_ @ H @ d_) / den * g, -(d_ @ H @ w_) / den * g])

    st = np.concatenate([p, d, w]).astype(float)
    out = [st.copy()]
    h = 1.0 / NSTEP
    for _ in range(NSTEP):
        k1 = f(st)
        k2 = f(st + h / 2 * k1)
        k3 = f(st + h / 2 * k2)
        k4 = f(st + h * k3)
        st = st + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out.append(st.copy())
    return np.array(out)


def _routes(s):
    o = np.zeros(2)
    a1 = _leg(o, U0, V0, s)
    a2 = _leg(a1[-1, 0:2], a1[-1, 4:6], np.zeros(2), s)
    b1 = _leg(o, V0, U0, s)
    b2 = _leg(b1[-1, 0:2], b1[-1, 4:6], np.zeros(2), s)
    return a1, a2, b1, b2


_routes_raw = _routes


@lru_cache(maxsize=8)
def _routes_c(s):
    return tuple(_routes_raw(s))


def _w3(x, y, s):
    return np.array([x, y, _z(x, y, s)])


def _focus(s):
    c = _w3(CX, CY, s)
    a1, a2, b1, b2 = _routes_c(s)
    m = 0.5 * (_w3(*a2[-1, 0:2], s) + _w3(*b2[-1, 0:2], s))
    f = CAM["f"]
    return (1 - f) * c + f * m


def _rot(p, s, foc=None):
    az, el = CAM["az"], CAM["el"]
    foc = _focus(s) if foc is None else foc
    x, y, z = p - foc
    sx = x * np.cos(az) - y * np.sin(az)
    ty = x * np.sin(az) + y * np.cos(az)
    sy = ty * np.sin(el) + z * np.cos(el)
    dep = ty * np.cos(el) - z * np.sin(el)
    return sx, sy, dep


def _proj(x, y, s, lift=0.0):
    sx, sy, _ = _rot(_w3(x, y, s) + np.array([0, 0, lift]), s)
    return CEN + SC * CAM["zoom"] * np.array([sx, sy, 0.0])


def _scr(leg, s, lift=0.03):
    foc = _focus(s)
    out = []
    for r in leg:
        sx, sy, _ = _rot(_w3(r[0], r[1], s) + np.array([0, 0, lift]), s, foc)
        out.append(CEN + SC * CAM["zoom"] * np.array([sx, sy, 0.0]))
    return np.array(out)


def _poly(pts, color, width, opacity=1.0):
    m = VMobject()
    m.set_points_as_corners(pts)
    m.set_stroke(color, width, opacity)
    return m


_LO = np.array([0x1F, 0x5E, 0x66]) / 255.0
_HI = np.array([0xA8, 0xE6, 0xD8]) / 255.0


def _mesh(s, n=14):
    xs = np.linspace(*DOM_X, n + 1)
    ys = np.linspace(*DOM_Y, n + 1)
    foc = _focus(s)
    A, B = _coef(s)
    quads = []
    for i in range(n):
        for j in range(n):
            x0, x1, y0, y1 = xs[i], xs[i + 1], ys[j], ys[j + 1]
            xm, ym = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
            nrm = np.array([-KAPPA * A * xm, -KAPPA * B * ym, 1.0])
            nrm /= np.linalg.norm(nrm)
            lam = float(np.clip(0.35 + 0.65 * (nrm @ LIGHT), 0, 1))
            col = rgb_to_color(_LO + (_HI - _LO) * lam)
            pts3 = [_rot(_w3(x, y, s), s, foc) for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
            dep = sum(p[2] for p in pts3) / 4
            pts = [CEN + SC * CAM["zoom"] * np.array([p[0], p[1], 0.0]) for p in pts3]
            quads.append((dep, pts, col))
    quads.sort(key=lambda q: -q[0])
    g = VGroup()
    for _, pts, col in quads:
        p = Polygon(
            *pts,
            stroke_width=0.8,
            stroke_color=IVORY_WHITE,
            stroke_opacity=0.28,
            fill_color=col,
            fill_opacity=0.96,
        )
        g.add(p)
    return g


def _gap_az(s, near=35.0):
    a1, a2, b1, b2 = _routes_c(s)
    d = b2[-1, 0:2] - a2[-1, 0:2]
    az = -np.degrees(np.arctan2(d[1], d[0]))
    while az - near > 90:
        az -= 180
    while az - near < -90:
        az += 180
    return float(az)


def play_curved_surface(scene, cap):
    CAM.update(az=np.radians(35.0), el=np.radians(60.0), zoom=1.0, f=0.0)
    st = ValueTracker(0.0)
    S = st.get_value
    trk = dict(az=ValueTracker(35.0), el=ValueTracker(60.0), zoom=ValueTracker(1.0), f=ValueTracker(0.0))

    def _cam_up(_m):
        CAM["az"] = np.radians(trk["az"].get_value())
        CAM["el"] = np.radians(trk["el"].get_value())
        CAM["zoom"] = trk["zoom"].get_value()
        CAM["f"] = trk["f"].get_value()

    hook = Mobject()
    hook.add_updater(_cam_up)
    scene.add(hook)

    def cam(az=None, el=None, zoom=None, f=None, t=2.0):
        anims = []
        for k, v in (("az", az), ("el", el), ("zoom", zoom), ("f", f)):
            if v is not None:
                anims.append(trk[k].animate.set_value(v))
        scene.play(*anims, run_time=t, rate_func=smooth)

    bgc = scene.camera.background_color

    def _band(x0, x1, y0, y1):
        r = Rectangle(width=x1 - x0, height=y1 - y0, stroke_width=0, fill_color=bgc, fill_opacity=1)
        return r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0]).set_z_index(40)

    masks = VGroup(_band(-9, WX0, -5, 5), _band(WX1, 9, -5, 5), _band(WX0, WX1, -5, WY0), _band(WX0, WX1, WY1, 5))
    frame = Rectangle(
        width=WX1 - WX0, height=WY1 - WY0,
        stroke_color=COPPER_TERRA, stroke_width=1.6, fill_opacity=0,
    ).move_to([CEN[0], CEN[1], 0]).set_z_index(45)
    for m_ in scene.mobjects:
        if abs(m_.get_center()[1] - 3.55) < 0.1:
            m_.set_z_index(80)

    # 1) إدخال الفريم والماسك بنعومة أولاً (0.6s)
    scene.play(Create(frame), FadeIn(masks), run_time=0.6)

    def _cap_set(txt, color=GOLD_LIGHT, size=22, run_time=0.6, extra=()):
        new = _ar(txt, size, color, True).move_to([0, cap.y, 0]).set_z_index(80)
        if cap.cur is None:
            scene.play(FadeIn(new, shift=UP * 0.1), *extra, run_time=run_time)
        else:
            scene.play(ReplacementTransform(cap.cur, new), *extra, run_time=run_time)
        cap.cur = new
        return new

    cap.set = _cap_set

    def say(txt, col):
        cap.set(txt, col, run_time=0.6)

    mesh = always_redraw(lambda: _mesh(S()))

    def paths():
        a1, a2, b1, b2 = _routes_c(S())
        s = S()
        return VGroup(
            _poly(_scr(a1, s), C_U, 6.5),
            _poly(_scr(a2, s), C_V, 6.5),
            _poly(_scr(b1, s), C_V, 6.5, 0.95),
            _poly(_scr(b2, s), C_U, 6.5, 0.95),
        )

    paths_m = always_redraw(paths)

    def endpts():
        a1, a2, b1, b2 = _routes_c(S())
        s = S()
        return _proj(*a2[-1, 0:2], s, 0.03), _proj(*b2[-1, 0:2], s, 0.03)

    dA = Dot(radius=0.11, color=IVORY_WHITE).add_updater(lambda m: m.move_to(endpts()[0]))
    dB = Dot(radius=0.11, color=C_SUM).add_updater(lambda m: m.move_to(endpts()[1]))
    for d in (dA, dB):
        d.set_stroke(BLACK, 2.5)
    tA = _tex("A", 34, IVORY_WHITE)
    tB = _tex("B", 34, C_SUM)

    def _lab_pos():
        A_, B_ = endpts()
        d = B_ - A_
        n = float(np.linalg.norm(d))
        u = d / n if n > 1e-3 else np.array([1.0, 0, 0])
        return A_ - u * 0.42, B_ + u * 0.42

    tA.add_updater(lambda m: m.move_to(_lab_pos()[0]))
    tB.add_updater(lambda m: m.move_to(_lab_pos()[1]))

    def gap():
        A_, B_ = endpts()
        d = np.linalg.norm(A_ - B_)
        op = float(min(1.0, d / 0.35))
        under = Line(A_, B_, color=BLACK, stroke_width=11).set_stroke(opacity=0.55 * op)
        ln = DashedLine(A_, B_, color=ERR_RED, stroke_width=7, dash_length=0.09)
        ln.set_stroke(opacity=op)
        return VGroup(under, ln)

    gap_m = always_redraw(gap)

    lu = _tex(r"\mathbf{u}", 34, C_U)
    lv = _tex(r"\mathbf{v}", 34, C_V)
    lu.add_updater(lambda m: m.move_to(_scr(_routes_c(S())[0], S())[NSTEP // 2] + np.array([0.12, -0.42, 0.0])))
    lv.add_updater(lambda m: m.move_to(_scr(_routes_c(S())[2], S())[NSTEP // 2] + np.array([-0.45, 0.1, 0.0])))
    for m_, z in ((mesh, 1), (paths_m, 5), (gap_m, 6), (dA, 7), (dB, 7), (tA, 8), (tB, 8), (lu, 8), (lv, 8)):
        m_.set_z_index(z)

    PXC = 4.6
    _names = [
        ("مسطح  ·  انحناء صفر", IVORY_WHITE),
        ("كرة  ·  انحناء موجب", GOLD_LIGHT),
        ("سرج  ·  انحناء سالب", COPPER_TERRA),
    ]

    def _pc(i, on):
        return _chip(_names[i][0], _names[i][1], w=3.0, h=0.62, size=18, filled=on)

    ph = _ar("نوع الانحناء", 20, LABEL_MUTED, True).move_to([PXC, 2.65, 0])
    off = [_pc(i, False).set_opacity(0.45) for i in range(3)]
    on = [_pc(i, True) for i in range(3)]
    YS = (1.85, 1.1, 0.35)
    for i in range(3):
        off[i].move_to([PXC, YS[i], 0]).set_z_index(60)
        on[i].move_to([PXC, YS[i], 0]).set_z_index(60)
    cur = [0]
    mlab = _ar("حجم الفجوة بين A و B", 20, LABEL_MUTED, True).move_to([PXC, -0.55, 0])
    TRK_W = 2.8
    track = Rectangle(width=TRK_W, height=0.3, stroke_color=STONE_AXIS, stroke_width=2, fill_opacity=0).move_to([PXC, -1.2, 0])

    def _gapw():
        a1, a2, b1, b2 = _routes_c(S())
        s_ = S()
        return float(np.linalg.norm(_w3(*a2[-1, 0:2], s_) - _w3(*b2[-1, 0:2], s_)))

    def meter():
        w = max(0.001, min(TRK_W, 2.4 * _gapw()))
        r = Rectangle(width=w, height=0.3, stroke_width=0, fill_color=ERR_RED, fill_opacity=0.95)
        return r.move_to([PXC - TRK_W / 2 + w / 2, -1.2, 0])

    bar_m = always_redraw(meter)
    for m_ in (ph, mlab, track, bar_m):
        m_.set_z_index(60)

    def hl(i):
        k = cur[0]
        cur[0] = i
        return [FadeOut(on[k]), FadeIn(off[k]), FadeOut(off[i]), FadeIn(on[i])]

    # ---------- 1) دخول ناعم للسطح المسطح ثم انحناء سريع للكرة (23:14 - 23:24.5) ----------
    say("نبدأ بفضاء مسطح — وبعدين نخلّيه ينحني", GOLD_BRIGHT)
    scene.play(
        FadeIn(mesh, scale=0.96), FadeIn(paths_m),
        FadeIn(ph), FadeIn(on[0]), FadeIn(off[1]), FadeIn(off[2]),
        FadeIn(mlab), FadeIn(track),
        FadeIn(lu), FadeIn(lv), FadeIn(dA), FadeIn(dB), FadeIn(tA), FadeIn(tB),
        run_time=1.2,
    )
    scene.add(bar_m, gap_m)

    # ---------- 2) كرة (23:17 - 23:24.5) ----------
    say("نحنّي السطح لجزء من كرة…", GOLD_BRIGHT)
    scene.play(st.animate.set_value(1.0), *hl(1), run_time=3.0, rate_func=smooth)
    say("على الكرة: المسارين مش بيتقابلوا في نفس النقطة", GOLD_LIGHT)
    cam(zoom=1.8, f=1.0, az=_gap_az(1.0), el=78.0, t=2.0)
    scene.wait(0.4 * SPD)
    cam(zoom=1.0, f=0.0, az=35.0, el=60.0, t=1.5)

    # ---------- 3) سرج حصان (23:24.5 - 23:33) ----------
    say("وبعدين نحني السطح على شكل سرج حصان…", GOLD_BRIGHT)
    scene.play(st.animate.set_value(2.0), *hl(2), run_time=3.2, rate_func=smooth)
    say("على السرج: المسارين بيتباعدوا عن بعض", GOLD_LIGHT)
    cam(zoom=1.8, f=1.0, az=_gap_az(2.0), el=78.0, t=2.0)
    scene.wait(0.4 * SPD)
    cam(zoom=1.0, f=0.0, az=35.0, el=60.0, t=1.5)

    # ---------- 4) توضيح الفجوة وتباعد المسارين (23:33 - 23:50) ----------
    fg = _ar("فجوة", 20, ERR_RED, True).set_z_index(9)
    fg.add_updater(lambda m: m.move_to((endpts()[0] + endpts()[1]) / 2 + np.array([0.0, 0.62, 0.0])))
    scene.play(FadeIn(fg), run_time=0.6)

    a1, a2, b1, b2 = _routes_c(2.0)
    pa = np.concatenate([_scr(a1, 2.0), _scr(a2, 2.0)])
    pb = np.concatenate([_scr(b1, 2.0), _scr(b2, 2.0)])
    wa = Dot(radius=0.09, color=GOLD_BRIGHT).set_z_index(9)
    wb = Dot(radius=0.09, color=GOLD_BRIGHT).set_z_index(9)

    def place(alpha):
        k = int(round(alpha * (len(pa) - 1)))
        wa.move_to(pa[k])
        wb.move_to(pb[k])

    wa.move_to(pa[0])
    wb.move_to(pb[0])
    scene.play(FadeIn(wa), FadeIn(wb), run_time=0.3)
    scene.play(UpdateFromAlphaFunc(VGroup(wa, wb), lambda m, a: place(a)), run_time=2.0, rate_func=smooth)
    scene.play(FadeOut(VGroup(wa, wb)), run_time=0.4)

    side = VGroup(
        _chip("A = u ثم v", IVORY_WHITE, w=2.9, h=0.6, size=18),
        _chip("B = v ثم u", C_SUM, w=2.9, h=0.6, size=18),
        _chip("A ≠ B", ERR_RED, w=2.9, h=0.6, size=18, filled=True),
    ).arrange(DOWN, buff=0.22).move_to([4.6, 0.4, 0]).set_z_index(60)
    scene.play(
        FadeOut(VGroup(ph, mlab, track, bar_m, on[cur[0]], *[off[k] for k in range(3) if k != cur[0]])),
        run_time=0.5,
    )
    scene.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in side], lag_ratio=0.25), run_time=1.2)
    scene.wait(9.0 * SPD)

    hook.clear_updaters()
    scene.remove(hook)
    for m in (mesh, paths_m, gap_m, bar_m, dA, dB, tA, tB, lu, lv, fg):
        m.clear_updaters()
    return VGroup(mesh, paths_m, gap_m, dA, dB, tA, tB, lu, lv, fg, side, masks, frame)