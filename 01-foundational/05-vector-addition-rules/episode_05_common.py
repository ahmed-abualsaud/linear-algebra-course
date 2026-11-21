from contextlib import contextmanager
import os

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


def _load_mach_axes():
    """
    بيدوّر في نص ملفات مجلد common (من غير ما يستورد أي ملف تاني) على الملف اللي فيه
    class MachAxes1D و class MachAxes2D، وبعدين بيستورده هو بس.
    (استيراد كل ملفات common كان ممكن يغيّر إعدادات manim ويبوّظ الصورة.)
    """
    import importlib
    from pathlib import Path
    try:                                                   # المكان الفعلي عند المستخدم
        return importlib.import_module("common.mobjects.coordinate_systems")
    except ImportError:
        pass
    import common
    root = Path(common.__file__).resolve().parent
    for p in sorted(root.rglob("*.py")):
        try:
            txt = p.read_text(encoding="utf-8")
        except Exception:
            continue
        if "class MachAxes2D" in txt and "class MachAxes1D" in txt:
            parts = list(p.relative_to(root.parent).with_suffix("").parts)
            if parts[-1] == "__init__":
                parts = parts[:-1]
            return importlib.import_module(".".join(parts))
    raise ImportError("مش لاقي ملف فيه MachAxes1D و MachAxes2D جوه مجلد common")


_axes_mod = _load_mach_axes()
MachAxes1D = _axes_mod.MachAxes1D
MachAxes2D = _axes_mod.MachAxes2D

# ==============================================================
# الحلقة 05 — الأدوات المشتركة بين كل المشاهد (قواعد جمع المتجهات)
# ملف مستقل: مفيش استيراد من مجلد الحلقة 04، فتقدر تشغّل الحلقة 05 لوحدها.
# ==============================================================

SPD = 0.12 if os.environ.get("MACH_FAST") else 1.0        # معاينة سريعة فقط (بتقصّر الانتظار)
TEAL = "#4FA7A0"
ERR_RED = "#C0443A"
C_U = COPPER_TERRA                                         # لون المتجه u
C_V = GOLD_LIGHT                                           # لون المتجه v
C_SUM = GOLD_BRIGHT                                        # لون المحصلة u + v
C_W = TEAL                                                 # لون المتجه w

# الشروط الخمسة: (الاسم البسيط القصير، الاسم العلمي)
RULES = [("البقاء في نفس الفضاء", "الإغلاق الجمعي"),
         ("وجود نقطة الأصل ", "المحايد الجمعي"),
         ("القدرة على العودة", "المعكوس الجمعي"),
         ("استقامة الفضاء", "الإبدال الجمعي"),
         ("اتساق الفضاء", "التجميع")]
RULES_SHORT = ["البقاء في الفضاء", "نقطة الأصل", "القدرة على العودة", "استقامة الفضاء", "اتساق الفضاء"]


# ---------------------------------------------------------------- نصوص ومعادلات
def _ar(txt, size=22, color=IVORY_WHITE, bold=False):
    """نص عربي بـ MarkupText (Text بيقص العربي المختلط). متبدأش سطر بحرف لاتيني."""
    body = f"<b>{txt}</b>" if bold else txt
    return MarkupText(body, font="Cairo", font_size=size, color=color)


def _tex(s, size=44, color=IVORY_WHITE):
    return MathTex(s, tex_template=mach_math_template, font_size=size, color=color)


def _chip(txt, color, w=2.7, h=0.55, size=17, filled=False):
    box = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=1.8,
                           fill_color=color if filled else "#14100A", fill_opacity=0.22 if filled else 0.9)
    t = _ar(txt, size, color, True).move_to(box)
    return VGroup(box, t)


# ---------------------------------------------------------------- توقيت المشهد
@contextmanager
def beat(scene, dur):
    """
    فقرة من السرد ميزانيتها dur ثانية (تقدير من عدد الكلمات — عدّلها بعد التسجيل الفعلي).
    الأنيميشن جوّه الـ with بياخد الوقت اللي يحتاجه، والباقي بينتظره تلقائيًا عشان المشهد يمشي مع الصوت.
    """
    t0 = scene.renderer.time
    yield
    rem = dur * SPD - (scene.renderer.time - t0)
    if rem > 0.05:
        scene.wait(rem)


class _Cap:
    """سطر التعليق السفلي: بيبدّل النص بنعومة."""

    def __init__(self, scene, y=-3.4):
        self.scene, self.y, self.cur = scene, y, None

    def set(self, txt, color=GOLD_LIGHT, size=22, run_time=0.7, extra=()):
        new = _ar(txt, size, color, True).move_to([0, self.y, 0])
        if self.cur is None:
            self.scene.play(FadeIn(new, shift=UP * 0.1), *extra, run_time=run_time)
        else:
            self.scene.play(ReplacementTransform(self.cur, new), *extra, run_time=run_time)
        self.cur = new
        return new

    def clear(self, run_time=0.5):
        if self.cur is not None:
            self.scene.play(FadeOut(self.cur), run_time=run_time)
            self.cur = None


# ---------------------------------------------------------------- عناصر عامة
def _rules_bar(active=None, y=3.55):
    """شريط الشروط الخمسة أعلى الشاشة (الشرط الحالي مضيء). بيتحط في المشاهد 6–10."""
    chips = VGroup()
    for i, t in enumerate(RULES_SHORT):
        on = (i == active)
        c = _chip(f"{i + 1}- {t}", GOLD_BRIGHT if on else GOLD_MUTED, w=2.55, h=0.46, size=13, filled=on)
        if not on:
            c.set_opacity(0.55)
        chips.add(c)
    chips.arrange(LEFT, buff=0.12).move_to([0, y, 0])        # الشرط الأول على اليمين (RTL)
    return chips


def _scene_head(txt, color=GOLD_LIGHT, y=2.85):
    return _ar(txt, 30, color, True).move_to([0, y, 0])


def _dot(p, color=GOLD_BRIGHT, r=0.1):
    p = np.array([p[0], p[1], 0.0])
    return VGroup(Dot(p, radius=r * 2.6, color=color).set_opacity(0.18), Dot(p, radius=r, color=color))


def _cross(pos, size=0.32, color=ERR_RED):
    pos = np.array([pos[0], pos[1], 0.0])
    return VGroup(Line(pos + [-size, -size, 0], pos + [size, size, 0], color=color, stroke_width=6),
                  Line(pos + [-size, size, 0], pos + [size, -size, 0], color=color, stroke_width=6))


def _check(pos, size=0.3, color=TEAL):
    pos = np.array([pos[0], pos[1], 0.0])
    return VMobject().set_points_as_corners([pos + [-size, 0, 0], pos + [-size * 0.35, -size * 0.7, 0],
                                             pos + [size, size * 0.8, 0]]).set_stroke(color, 7)


def _arrow(start, end, color, width=5, tip=0.25):
    return Arrow([start[0], start[1], 0], [end[0], end[1], 0], buff=0, color=color, stroke_width=width,
                 max_tip_length_to_length_ratio=tip, max_stroke_width_to_length_ratio=12)


def _stack(start, step, n, color, width=5):
    """رصّة n متجه أساس ورا بعض، كل واحد بطول step (متجه 2D)."""
    s = np.array(start, float)[:2]
    d = np.array(step, float)[:2]
    return VGroup(*[_arrow(s + i * d, s + (i + 1) * d, color, width, tip=0.38) for i in range(n)])


def _placeholder(title, desc, w=6.0, h=2.6, color=GOLD_MUTED):
    """مكان رسمة لسه متنفذتش (للهيكل بس): مستطيل منقّط + عنوان + وصف المطلوب."""
    box = DashedVMobject(Rectangle(width=w, height=h, color=color, stroke_width=2), num_dashes=40)
    t = _ar("TODO — " + title, 20, color, True).move_to([0, h / 2 - 0.4, 0])
    d = _ar(desc, 16, color).next_to(t, DOWN, buff=0.2)
    return VGroup(box, t, d)


# ---------------------------------------------------------------- شبكة إحداثيات 2D
def _clip(p, q, box):
    """Liang–Barsky: قص القطعة p→q داخل box=(x0,x1,y0,y1)."""
    x0, x1, y0, y1 = box
    p, q = np.asarray(p, float), np.asarray(q, float)
    d = q - p
    t0, t1 = 0.0, 1.0
    for pk, qk in ((-d[0], p[0] - x0), (d[0], x1 - p[0]), (-d[1], p[1] - y0), (d[1], y1 - p[1])):
        if abs(pk) < 1e-9:
            if qk < 0:
                return None
            continue
        r = qk / pk
        if pk < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return None
    return p + t0 * d, p + t1 * d


def _grid_lines(a, b, box, origin=(0, 0, 0), n=14, color=STONE_AXIS, width=1.0, opacity=0.25):
    a, b, o = np.array(a, float), np.array(b, float), np.array(origin, float)
    g = VGroup()
    for fam, step in ((b, a), (a, b)):
        for i in range(-n, n + 1):
            c = o + i * step
            seg = _clip(c - 60 * fam, c + 60 * fam, box)
            if seg is None or np.linalg.norm(seg[1] - seg[0]) < 1e-3:
                continue
            g.add(Line([*seg[0][:2], 0], [*seg[1][:2], 0]).set_stroke(color, width, opacity))
    return g


class Plane:
    """
    فضاء متجهات 2D بسيط: شبكة باهتة + محورين. P(x, y) بيحوّل إحداثيات (بوحدة e1 و e2) لنقطة على الشاشة.
    .grid و .axes و .labels كلها VGroup تقدر تظهرها كل واحدة لوحدها.
    """

    def __init__(self, origin=(-4.2, -2.3), step=0.62, box=(-6.6, 2.9, -3.1, 3.0), with_labels=True):
        self.O = np.array([origin[0], origin[1], 0.0])
        self.s = step
        self.box = box
        self.grid = _grid_lines([step, 0], [0, step], box, self.O[:2], n=30)
        ex, ey = box[1] - 0.15, box[3] - 0.1
        self.axes = VGroup(
            Line([box[0] + 0.3, self.O[1], 0], [ex, self.O[1], 0], color=GOLD_LIGHT, stroke_width=2.6),
            Line([self.O[0], box[2] + 0.1, 0], [self.O[0], ey, 0], color=GOLD_LIGHT, stroke_width=2.6),
            Triangle(fill_color=GOLD_LIGHT, fill_opacity=1, stroke_width=0).scale(0.1).rotate(-PI / 2).move_to([ex, self.O[1], 0]),
            Triangle(fill_color=GOLD_LIGHT, fill_opacity=1, stroke_width=0).scale(0.1).move_to([self.O[0], ey, 0]),
        )
        self.labels = VGroup()
        if with_labels:
            self.labels.add(_tex("x", 28, GOLD_LIGHT).move_to([ex - 0.1, self.O[1] - 0.3, 0]),
                            _tex("y", 28, GOLD_LIGHT).move_to([self.O[0] + 0.3, ey - 0.05, 0]),
                            _tex("0", 26, GOLD_LIGHT).move_to(self.O + [-0.25, -0.25, 0]))
        self.group = VGroup(self.grid, self.axes, self.labels)

    def P(self, x, y=None):
        if y is None:
            x, y = x
        return self.O + self.s * np.array([x, y, 0.0])

    def vec(self, comps, color, start=(0, 0), width=6):
        a = self.P(*start)
        return _arrow(a, a + self.s * np.array([comps[0], comps[1], 0.0]), color, width, tip=0.14)


ORD = ["الأول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس", "السابع", "الثامن", "التاسع", "العاشر", "الحادي عشر"]


def _chapter(scene, num, title, hold=2.6):
    """كارت عنوان الفصل (أسلوب Justice League): «الفصل الأول» + العنوان. مدته الكلية ≈ hold + 1.6 ثانية."""
    kicker = _ar(f"الفصل {ORD[num - 1]}", 24, COPPER_TERRA, True).move_to([0, 1.25, 0])
    rule = Line([-1.6, 0.75, 0], [1.6, 0.75, 0], color=GOLD_MUTED, stroke_width=2)
    main = _ar(title, 40, GOLD_BRIGHT, True)
    if main.width > 12.2:
        main.scale_to_fit_width(12.2)
    main.next_to(rule, DOWN, buff=0.55)          # مسافة كافية بين الخط والعنوان
    card = VGroup(kicker, rule, main)
    scene.play(FadeIn(kicker, shift=DOWN * 0.1), Create(rule), FadeIn(main, shift=UP * 0.1), run_time=0.9)
    scene.wait(hold * SPD)
    scene.play(FadeOut(card), run_time=0.7)


def _exit(scene, run_time=0.8):
    """خروج المشهد: بيطفّي كل اللي على الشاشة."""
    if scene.mobjects:
        scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=run_time)
    scene.wait(0.3)


# بنصدّر كل الأسماء (بما فيها اللي بتبدأ بـ _) عشان `from episode_05_common import *`
__all__ = [n for n in dir() if not n.startswith("__")]