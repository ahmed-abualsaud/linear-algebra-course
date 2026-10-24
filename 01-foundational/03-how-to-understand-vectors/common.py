import weakref
import numpy as np
from manim import *

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_MUTED,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.mobjects.coordinate_systems import MachAxes3D
from common.mobjects.helicopter import make_helicopter, fly_along_3d
from common.mobjects.time_slider import MachTimeSlider

# ======================================================================
# الإعدادات الموحدة والمشتركة للمشاهد
# ======================================================================
MOVE = (3, 4, 5)          # الإزاحة: شرق، شمال، أرتفاع (بالمتر)
DURATION = 10             # الزمن (بالثواني)
FLIGHT_TIME = 7.5         # مدة الطيران المتزامنة مع الصوت
UNIT = 0.46               # طول الوحدة في الرسم
SCALE = 100               # متر → سنتيمتر

# إعدادات وحدة الخشبة
PLANK = 3.9
PLANK_VALUES = ("0.769", "1.025", "1.282")
UNIT_NAME = "الخشبة"

AXES_CENTER = np.array([-3.8, -2.5, -0.90])

# لوحة الألوان المشتركة
SPACE_COLOR = GOLD_BRIGHT
TIME_COLOR = COPPER_TERRA
NEW_COLOR = "#7FD6C2"
M_COLOR = GOLD_BRIGHT
CM_COLOR = "#F0B27A"
PLANK_COLOR = "#7FD6C2"

SCREEN_RIGHT = np.array([np.cos(np.radians(35)), np.sin(np.radians(35)), 0.0])


# ======================================================================
# الدوال المساعدة المشتركة
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


def _seg(a, b, **kw):
    if np.linalg.norm(np.asarray(b) - np.asarray(a)) < 1e-3:
        return VGroup()
    return DashedLine(a, b, **kw)


def _fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _make_list(vals, space_color, fs=40, cx=3.7, cy=0.0):
    """قائمة (a , b , c , 10) متوافقة التنسيق."""
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


def _path_flash(scene, O, goal, run_time=0.9):
    flash = Line(O, goal, color=GOLD_BRIGHT, stroke_width=9)
    flash.set_shade_in_3d(True)
    scene.play(ShowPassingFlash(flash, time_width=0.7), run_time=run_time)


def _exit_all(scene, st, hud_outs, extra=()):
    """خروج كامل وتفريغ نهائي للرسمة والكاميرا."""
    is_3d = isinstance(scene, ThreeDScene)
    frame_mobs = [m for m in (getattr(scene, "frame", None), getattr(scene, "neon_overlay", None)) if m is not None]
    ticks = st.get("ticks")
    outs = (
        [st["axes"], st["heli"], st["ar_labels"], st["rulers"], st["trail"], st["drops"]]
        + list(hud_outs)
        + list(extra)
        + (ticks.mobs() if ticks is not None else [])
    )
    if is_3d:
        scene.move_camera(
            phi=0, theta=-90 * DEGREES, gamma=0, run_time=1.5,
            added_anims=[FadeOut(m) for m in outs]
        )
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


# ======================================================================
# الكلاسات المشتركة
# ======================================================================
class _LiveNumber(VGroup):
    """عداد رقمي حي بدون ترك كائنات متراكمة في الذاكرة."""
    def __init__(self, scene, getter, center_fn, decimals=0, font_size=64, color=IVORY_WHITE):
        super().__init__()
        self._scene_ref = weakref.ref(scene)
        self._getter, self._center_fn = getter, center_fn
        self._dec, self._fs, self._col = decimals, font_size, color
        self._last = None
        self._cur = None
        self._old = []
        self._rebuild(force=True)
        self.add_updater(lambda m: m._rebuild())

    def _rebuild(self, force=False):
        v = round(max(0.0, float(self._getter())), self._dec)
        if not force and v == self._last:
            return
        self._last = v
        sc = self._scene_ref()
        cam = sc.renderer.camera if isinstance(sc, ThreeDScene) else None
        
        if self._cur is not None:
            self._cur.set_opacity(0)
            self._old.append(self._cur)
        txt = f"{v:.{self._dec}f}"
        new = MathTex(txt, font_size=self._fs, color=self._col)
        new.move_to(self._center_fn())
        if cam is not None:
            cam.add_fixed_in_frame_mobjects(new)
        self.add(new)
        self._cur = new

    def dispose(self, scene):
        self.clear_updaters()
        items = list(self._old) + ([self._cur] if self._cur is not None else [])
        if isinstance(scene, ThreeDScene):
            scene.renderer.camera.remove_fixed_in_frame_mobjects(*items)
        scene.remove(*items, self)
        self._old, self._cur = [], None


class _TickLabels:
    """يدير أرقام تدريج المحاور بحيث تتغير في مكانها دون تحريك الرسمة."""
    def __init__(self, scene, axes, O):
        self.scene = scene
        self.is_3d = isinstance(scene, ThreeDScene)
        self.mode = "m"
        self.items = []
        labs = []
        for m in axes._label_mobjects():
            if isinstance(m, Text):
                raw = m.text.strip()
                if raw.isdigit() and int(raw) > 0:
                    labs.append(m)
        for m in labs:
            c = m.get_center()
            kind = "z" if c[2] > O[2] + 0.1 else ("y" if c[0] < O[0] - 1e-3 else "x")
            self.items.append(dict(mob=m, kind=kind, k=int(m.text.strip()), ref=m.copy()))
        for g in axes.get_family():
            g.remove(*labs)
        scene.add(*labs)

    @staticmethod
    def text_for(mode, k):
        if mode == "cm":
            return str(k * SCALE)
        if mode == "plank":
            return f"{k / PLANK:.2f}"
        return str(k)

    def mobs(self):
        return [it["mob"] for it in self.items if it["mob"] is not None]

    @staticmethod
    def _visible(mode, it):
        return mode == "m" or it["k"] % 2 == 0

    def retarget(self, mode, font_size=13):
        if mode == self.mode:
            return Wait(0.01), (lambda: None)
        cam = self.scene.renderer.camera if self.is_3d else None
        pairs = []
        for it in self.items:
            old = it["mob"]
            new = None
            if self._visible(mode, it):
                ref = it["ref"]
                new = Text(self.text_for(mode, it["k"]), font_size=font_size, color=IVORY_WHITE).set_opacity(0.9)
                new.move_to(ref.get_center())
                if it["kind"] == "x":
                    new.align_to(ref, UP)
                elif it["kind"] == "y":
                    new.align_to(ref, RIGHT)
                else:
                    new.align_to(ref, LEFT)
                if cam is not None:
                    cam.add_fixed_orientation_mobjects(new)
            pairs.append((it, old, new))

        anims = []
        for _, o, n in pairs:
            parts = ([FadeOut(o)] if o is not None else []) + ([FadeIn(n)] if n is not None else [])
            if parts:
                anims.append(AnimationGroup(*parts))
        anim = LaggedStart(*anims, lag_ratio=0.04)

        def commit():
            for it, o, n in pairs:
                if o is not None:
                    self.scene.remove(o)
                    if cam is not None:
                        cam.remove_fixed_orientation_mobjects(o)
                it["mob"] = n
            self.mode = mode

        return anim, commit

    def dispose(self):
        cam = self.scene.renderer.camera if self.is_3d else None
        for m in self.mobs():
            self.scene.remove(m)
            if cam is not None:
                cam.remove_fixed_orientation_mobjects(m)
        self.items = []