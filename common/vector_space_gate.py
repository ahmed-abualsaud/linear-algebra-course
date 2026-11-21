"""
vector_space_gate.py
====================
لقطة "فضاء المتجهات مش مكان فيزيائي":
شخص راكب عربية ملاكي على طريق أسفلت وسط أرض رملية، آخر الطريق بوابة قصر مصمتة عليها يافطة
«فضاء المتجهات» وسور عالي مقفول على الجانبين، ولوحة إرشادية «أهلا بكم في فضاء المتجهات»،
وبعدين علامة X حمرا تظهر عشان تقول إن الموقف ده مش موجود في الواقع.

مكان الملف:  common/mobjects/vector_space_gate.py

الاستخدام داخل أي مشهد:

    from common.mobjects.vector_space_gate import play_vector_space_gate
    play_vector_space_gate(scene, cap=cap, caption="...")

الملف مستقل: بيعتمد على manim و numpy بس.
المساحة المستخدمة: y من -3.0 إلى 2.6 (شريط الشروط فوق والترجمة تحت).
"""
from manim import *
import numpy as np

FONT = "Cairo"

# ---------------------------------------------------------------- ألوان
_SAND_FAR, _SAND_NEAR = "#C98A55", "#3F2F22"
_ASPHALT_FAR, _ASPHALT_NEAR = "#4A464A", "#141418"
_STONE, _STONE_DK, _STONE_LT = "#A58C68", "#76624A", "#C0A982"
_GOLD, _GOLD_DK = "#E0B645", "#9A7A22"
_WOOD, _WOOD_LT = "#3F2618", "#5A3822"
_RED = "#E5484D"

HORIZON_Y = 0.6      # قاعدة السور والبوابة (نهاية الطريق)
BOTTOM_Y = -3.3      # أسفل الأرض
_DY = HORIZON_Y - 0.2   # إزاحة العناصر المرسومة بالنسبة لأفق 0.2
ROAD_HW_BOTTOM = 3.6
ROAD_HW_TOP = 1.0    # = نصف عرض فتحة البوابة
SIDE = 7.3


def _mix(a, b, t):
    return interpolate_color(ManimColor(a), ManimColor(b), float(np.clip(t, 0, 1)))


def _ar(text, size, color, width=None, weight=BOLD):
    t = MarkupText(text, font=FONT, font_size=size, color=color, weight=weight)
    if width is not None and t.width > width:
        t.set_width(width)
    return t


def _poly(pts, fill, op=1.0, stroke=None, sw=0):
    p = Polygon(*[[x, y, 0] for x, y in pts], fill_color=fill, fill_opacity=op, stroke_width=sw)
    if stroke:
        p.set_stroke(stroke, sw)
    return p


def _rect(x0, x1, y0, y1, fill, op=1.0, stroke=None, sw=0):
    return _poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, op, stroke, sw)


def road_half_width(y):
    k = (y - BOTTOM_Y) / (HORIZON_Y - BOTTOM_Y)
    return ROAD_HW_BOTTOM + (ROAD_HW_TOP - ROAD_HW_BOTTOM) * k


# ======================================================== السماء والكثبان والنخيل
def _frond(base, ang, L, droop, w, color):
    s = np.linspace(0, 1, 14)
    cx = base[0] + L * s * np.cos(ang)
    cy = base[1] + L * s * np.sin(ang) - droop * L * s ** 2
    wd = w * np.sin(np.pi * np.clip(s, 0, 1)) ** 0.7 + 0.004
    up = [(cx[i], cy[i] + wd[i]) for i in range(len(s))]
    dn = [(cx[i], cy[i] - wd[i]) for i in range(len(s) - 1, -1, -1)]
    return _poly(up + dn, color, 1.0)


def _palm(x, base_y, h, lean):
    g = VGroup()
    pts = [(x + lean * (t ** 1.6), base_y + h * t) for t in np.linspace(0, 1, 10)]
    trunk = VMobject(stroke_color="#1A1510", stroke_width=7).set_points_as_corners([[a, b, 0] for a, b in pts])
    g.add(trunk)
    top = pts[-1]
    cols = ["#1B2418", "#151C14", "#202B1B"]
    for i, a in enumerate(np.linspace(0.15, np.pi - 0.15, 9)):
        g.add(_frond(top, a, 0.62, 0.55 if abs(a - np.pi / 2) > 0.5 else 0.2, 0.07, cols[i % 3]))
    return g


def build_scenery():
    g = VGroup()
    # سماء غروب: برتقالي دافي عند الأفق ثم بنفسجي ثم أزرق غامق
    n = 40
    y_top = 3.15
    stops = [(0.0, "#F7A24B"), (0.42, "#E0703F"), (0.6, "#94485A"), (0.8, "#303659"), (1.0, "#080B16")]
    for i in range(n):
        y0 = HORIZON_Y + (y_top - HORIZON_Y) * i / n
        y1 = HORIZON_Y + (y_top - HORIZON_Y) * (i + 1) / n + 0.01
        t = i / (n - 1)
        for (ta, ca), (tb, cb) in zip(stops[:-1], stops[1:]):
            if ta <= t <= tb:
                c = _mix(ca, cb, (t - ta) / (tb - ta))
                break
        g.add(_rect(-SIDE, SIDE, y0, y1, c))
    # شمس واطية بهالة
    for r, o in [(1.3, 0.07), (0.9, 0.11), (0.6, 0.18)]:
        g.add(Circle(radius=r, fill_color="#FF8A3D", fill_opacity=o, stroke_width=0).move_to([-4.7, 1.95 + _DY, 0]))
    g.add(Circle(radius=0.34, fill_color="#FFD08A", fill_opacity=1, stroke_width=0).move_to([-4.7, 1.95 + _DY, 0]))
    # كثبان بعيدة
    xs = np.linspace(-SIDE, SIDE, 60)
    for amp, ph, base, col in [(0.32, 0.8, 1.35 + _DY, "#7A4A35"), (0.22, 2.6, 1.05 + _DY, "#5E3A2C")]:
        top = [(x, base + amp * np.sin(0.55 * x + ph) + 0.1 * np.sin(1.3 * x)) for x in xs]
        g.add(_poly([(-SIDE, HORIZON_Y)] + top + [(SIDE, HORIZON_Y)], col))
    # نخيل وراء السور
    for x, h, l in [(-5.9, 1.0, 0.18), (-3.4, 0.8, -0.12), (3.5, 0.85, 0.14), (5.9, 1.05, -0.16)]:
        g.add(_palm(x, 1.2 + _DY, h * 0.85, l))
    # الأرض الرملية
    n = 26
    rs = np.random.RandomState(7)
    for i in range(n):
        y0 = BOTTOM_Y + (HORIZON_Y - BOTTOM_Y) * i / n
        y1 = BOTTOM_Y + (HORIZON_Y - BOTTOM_Y) * (i + 1) / n + 0.01
        t = i / (n - 1)
        g.add(_rect(-SIDE, SIDE, y0, y1, _mix(_SAND_NEAR, _SAND_FAR, t ** 0.9)))
    # حبيبات ورمل مموج
    for _ in range(260):
        y = rs.uniform(BOTTOM_Y, HORIZON_Y - 0.03)
        x = rs.uniform(-SIDE, SIDE)
        if abs(x) < road_half_width(y) + 0.1:
            continue
        sc = 0.35 + 0.65 * (HORIZON_Y - y) / (HORIZON_Y - BOTTOM_Y)
        dark = rs.rand() < 0.5
        g.add(Dot([x, y, 0], radius=0.012 + 0.02 * sc, color="#7A5B30" if dark else "#F1DAA2",
                  fill_opacity=0.35).set_stroke(width=0))
    for _ in range(9):
        y = rs.uniform(-2.8, -0.15)
        x0 = rs.uniform(-6.5, 5.5)
        L = rs.uniform(0.7, 1.6) * (0.5 + 0.5 * (HORIZON_Y - y) / 3.2)
        arc = ArcBetweenPoints([x0, y, 0], [x0 + L, y + 0.02, 0], angle=0.25,
                               stroke_color="#8B6A3A", stroke_width=2, stroke_opacity=0.35)
        if abs(x0) > road_half_width(y) + 0.1 and abs(x0 + L) > road_half_width(y) + 0.1 and x0 * (x0 + L) > 0:
            g.add(arc)
    # حجارة وشجيرات جافة
    for x, y, s in [(-5.3, -1.6, 1.0), (-3.9, -0.5, 0.6), (5.6, -2.0, 1.1), (6.2, -0.7, 0.55), (-6.3, -2.5, 1.3)]:
        g.add(Ellipse(width=0.34 * s, height=0.2 * s, fill_color="#8D7650", fill_opacity=1,
                      stroke_width=0).move_to([x, y, 0]))
        g.add(Ellipse(width=0.2 * s, height=0.09 * s, fill_color="#B49A6C", fill_opacity=0.9,
                      stroke_width=0).move_to([x - 0.03 * s, y + 0.04 * s, 0]))
    # الأسفلت (شرائح متدرجة)
    n = 26
    for i in range(n):
        y0 = BOTTOM_Y + (HORIZON_Y - BOTTOM_Y) * i / n
        y1 = BOTTOM_Y + (HORIZON_Y - BOTTOM_Y) * (i + 1) / n + 0.01
        t = i / (n - 1)
        h0, h1 = road_half_width(y0), road_half_width(y1)
        g.add(_poly([(-h0, y0), (h0, y0), (h1, y1), (-h1, y1)], _mix(_ASPHALT_NEAR, _ASPHALT_FAR, t ** 0.9)))
    # كتف الطريق (حافة رملية غامقة) وخطوط الحافة البيضا
    for s in (-1, 1):
        g.add(Line([s * (ROAD_HW_BOTTOM + 0.05), BOTTOM_Y, 0], [s * (ROAD_HW_TOP + 0.01), HORIZON_Y, 0],
                   color="#7B6038", stroke_width=5, stroke_opacity=0.7))
        k = 0.1
        g.add(Line([s * (ROAD_HW_BOTTOM - 0.22), BOTTOM_Y, 0], [s * (ROAD_HW_TOP - 0.06), HORIZON_Y, 0],
                   color="#E9E6DC", stroke_width=3, stroke_opacity=0.85))
    # خط المنتصف المتقطع بمنظور صحيح
    for i in range(7):
        t0, t1 = (i + 0.1) / 7, (i + 0.5) / 7
        y0 = HORIZON_Y - (HORIZON_Y - BOTTOM_Y) * (1 - t0) ** 2
        y1 = HORIZON_Y - (HORIZON_Y - BOTTOM_Y) * (1 - t1) ** 2
        w0 = 0.075 * road_half_width(y0) / 2.0
        w1 = 0.075 * road_half_width(y1) / 2.0
        g.add(_poly([(-w0, y0), (w0, y0), (w1, y1), (-w1, y1)], "#F1EEE2", 0.92))
    # حصى على الأسفلت
    for _ in range(90):
        y = rs.uniform(BOTTOM_Y + 0.05, HORIZON_Y - 0.03)
        hw = road_half_width(y) - 0.3
        x = rs.uniform(-hw, hw)
        g.add(Dot([x, y, 0], radius=0.012, color="#9A9DA2" if rs.rand() < 0.5 else "#16171A",
                  fill_opacity=0.35).set_stroke(width=0))
    # ظل السور على الأرض (شريط ناعم) — شلنا ظل العمودين لأنه كان بيبان غريب على الطريق
    H = HORIZON_Y
    for i in range(7):
        g.add(_rect(-SIDE, SIDE, H - 0.12 * (i + 1), H - 0.12 * i + 0.005, "#070A14", op=0.42 * (1 - i / 7)))
    # تعتيم ناعم أسفل الأرض
    n = 8
    for i in range(n):
        y0 = BOTTOM_Y + 0.5 * (1 - (i + 1) / n)
        y1 = BOTTOM_Y + 0.5 * (1 - i / n) + 0.01
        g.add(_rect(-SIDE, SIDE, y0, y1, "#000000", op=0.12 * (i + 1) * 0.9).set_z_index(3))
    return g


# ======================================================== السور والبوابة
def _arch_y(x, ys=1.3, rise=0.4, hw=1.0):
    R = (hw ** 2 + rise ** 2) / (2 * rise)
    cy = ys + rise - R
    return cy + np.sqrt(R ** 2 - x ** 2)


def _brick_lines(x0, x1, y0, y1, row=0.22, bw=0.5, color="#8E7B52", op=0.5):
    g = VGroup()
    ys = np.arange(y0 + row, y1 - 0.01, row)
    for r, y in enumerate(ys):
        g.add(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=1.6, stroke_opacity=op))
    rows = np.arange(y0, y1 - 0.01, row)
    for r, y in enumerate(rows):
        off = (bw / 2) if r % 2 else 0
        for x in np.arange(x0 + off + bw * 0.5, x1, bw):
            g.add(Line([x, y, 0], [x, min(y + row, y1), 0], color=color, stroke_width=1.4, stroke_opacity=op))
    return g


def build_gate():
    y0 = 0.2
    gate = VGroup()
    # ----- السور العالي المقفول
    wall_top = 1.38
    for s in (-1, 1):
        xa, xb = sorted([s * 1.45, s * SIDE])
        gate.add(_rect(xa, xb, y0, wall_top, _STONE))
        gate.add(_brick_lines(xa, xb, y0, wall_top, row=0.23, bw=0.55))
        gate.add(_rect(xa, xb, y0, y0 + 0.12, "#000000", 0.18))         # ظل أسفل السور
        gate.add(_rect(xa, xb, wall_top - 0.02, wall_top + 0.09, _STONE_DK))   # كورنيش
        gate.add(_rect(xa, xb, wall_top + 0.07, wall_top + 0.1, _STONE_LT))
        for px in (3.2, 5.2, 7.0):
            cx = s * px
            gate.add(_rect(cx - 0.17, cx + 0.17, y0, wall_top + 0.28, _STONE_LT))
            gate.add(_rect(cx + 0.03, cx + 0.17, y0, wall_top + 0.28, "#000000", 0.1))
            gate.add(_rect(cx - 0.25, cx + 0.25, wall_top + 0.28, wall_top + 0.38, _STONE_DK))
            gate.add(_rect(cx - 0.2, cx + 0.2, wall_top + 0.38, wall_top + 0.44, _STONE_LT))
            gate.add(Circle(radius=0.1, fill_color=_GOLD, fill_opacity=1, stroke_color=_GOLD_DK,
                            stroke_width=1.5).move_to([cx, wall_top + 0.56, 0]))
    # ----- العمودين الحجريين الكبار
    for s in (-1, 1):
        xa, xb = sorted([s * 1.0, s * 1.5])
        gate.add(_rect(xa, xb, y0, 1.9, _STONE_LT))
        gate.add(_brick_lines(xa, xb, y0 + 0.1, 1.9, row=0.2, bw=10, color="#9C8860", op=0.6))
        shade_a, shade_b = (xa, xa + 0.14) if s > 0 else (xb - 0.14, xb)
        gate.add(_rect(shade_a, shade_b, y0, 1.9, "#000000", 0.14))
        gate.add(_rect(s * 0.95 if s > 0 else -1.58, 1.58 if s > 0 else -0.95, y0, y0 + 0.2, _STONE_DK))  # قاعدة
        gate.add(_rect(s * 0.95 if s > 0 else -1.58, 1.58 if s > 0 else -0.95, 1.82, 1.94, _STONE_DK))     # تاج
    # ----- قوس الحجر
    arch_pts = [[x, _arch_y(x) + 0.0, 0] for x in np.linspace(-1.0, 1.0, 40)]
    # الضلفتين (مصمتة) – خشب غامق بزخارف دهب
    door_pts = [(-1.0, y0), (-1.0, 1.3)] + [(x, _arch_y(x)) for x in np.linspace(-1.0, 1.0, 40)] + [(1.0, 1.3), (1.0, y0)]
    gate.add(_poly(door_pts, _WOOD))
    # سطح الضلفة اليسار أفتح شوية للإحساس بالإضاءة
    left_pts = [(-1.0, y0), (-1.0, 1.3)] + [(x, _arch_y(x)) for x in np.linspace(-1.0, 0.0, 20)] + [(0.0, y0)]
    gate.add(_poly(left_pts, _WOOD_LT, 0.45))
    for s in (-1, 1):
        # كوفرة (باناوات) سفلية وعلوية
        for (ya, yb) in [(0.36, 0.98), (1.08, 1.34)]:
            xa, xb = sorted([s * 0.16, s * 0.84])
            gate.add(_rect(xa, xb, ya, yb, _WOOD_LT if s < 0 else "#4C301D", 0.95, _GOLD, 2.2))
            gate.add(_rect(xa + 0.05 * (1 if s < 0 else -1) * -1 if False else min(xa, xb) + 0.05,
                           max(xa, xb) - 0.05, ya + 0.05, yb - 0.05, "#000000", 0.0, _GOLD_DK, 1.2))
        # مسامير دهبية على حافة الضلفة
        for y in np.arange(0.35, 1.3, 0.13):
            gate.add(Dot([s * 0.93, y, 0], radius=0.022, color=_GOLD).set_stroke(width=0))
        # حلقة مقبض
        gate.add(Circle(radius=0.075, stroke_color=_GOLD, stroke_width=4, fill_opacity=0).move_to([s * 0.12, 0.72, 0]))
        gate.add(Circle(radius=0.035, fill_color=_GOLD, fill_opacity=1, stroke_width=0).move_to([s * 0.12, 0.8, 0]))
    # الخط الأوسط
    gate.add(Line([0, y0, 0], [0, _arch_y(0), 0], color=_GOLD, stroke_width=3.5))
    # مروحة ذهبية في أعلى القوس
    for a in np.linspace(0.35, np.pi - 0.35, 9):
        gate.add(Line([0, 1.38, 0], [0.32 * np.cos(a), 1.38 + 0.3 * np.sin(a), 0], color=_GOLD, stroke_width=2.2))
    gate.add(Circle(radius=0.14, fill_color=_GOLD, fill_opacity=1, stroke_color=_GOLD_DK,
                    stroke_width=2).move_to([0, 1.38, 0]))
    gate.add(Circle(radius=0.07, fill_color=_WOOD, fill_opacity=1, stroke_width=0).move_to([0, 1.38, 0]))
    # حلقة قوس الحجر + حجر المفتاح
    gate.add(VMobject(stroke_color=_STONE_DK, stroke_width=13).set_points_as_corners(
        [[x, y + 0.04, 0] for x, y, _ in arch_pts]))
    gate.add(VMobject(stroke_color=_STONE_LT, stroke_width=6).set_points_as_corners(
        [[x, y + 0.08, 0] for x, y, _ in arch_pts]))
    gate.add(_poly([(-0.13, 1.64), (0.13, 1.64), (0.1, 1.86), (-0.1, 1.86)], _STONE_DK))
    # إضاءة حافة دافية من الشمس الخلفية
    RIM = "#FFB56B"
    for s_ in (-1, 1):
        xa, xb = sorted([s_ * 1.45, s_ * SIDE])
        gate.add(Line([xa, wall_top + 0.1, 0], [xb, wall_top + 0.1, 0], color=RIM, stroke_width=2.2, stroke_opacity=0.9))
        for px in (3.2, 5.2, 7.0):
            gate.add(Line([s_ * px - 0.25, wall_top + 0.44, 0], [s_ * px + 0.25, wall_top + 0.44, 0],
                          color=RIM, stroke_width=2, stroke_opacity=0.85))
    gate.add(Line([1.0, y0 + 0.2, 0], [1.0, 1.9, 0], color=RIM, stroke_width=2.5, stroke_opacity=0.8))
    gate.add(Line([-1.5, y0 + 0.2, 0], [-1.5, 1.9, 0], color=RIM, stroke_width=2.5, stroke_opacity=0.8))
    gate.add(VMobject(stroke_color=RIM, stroke_width=2.5, stroke_opacity=0.85).set_points_as_corners(
        [[x, y + 0.11, 0] for x, y, _ in arch_pts]))
    # عتبة
    gate.add(_rect(-1.0, 1.0, y0, y0 + 0.05, "#1A120C"))
    # ----- اليافطة (لوح حجر + لوحة داكنة وحروف دهبية)
    beam = RoundedRectangle(corner_radius=0.07, width=3.5, height=0.64, fill_color=_STONE_DK,
                            fill_opacity=1, stroke_color=_GOLD, stroke_width=3).move_to([0, 2.2, 0])
    panel = RoundedRectangle(corner_radius=0.05, width=3.3, height=0.46, fill_color="#241810",
                             fill_opacity=1, stroke_color=_GOLD_DK, stroke_width=1.8).move_to([0, 2.2, 0])
    txt = _ar("فضاء المتجهات", 27, "#F6D77A", width=2.9).move_to(panel)
    rim_top = Line([-1.72, 2.52, 0], [1.72, 2.52, 0], color="#FFB56B", stroke_width=2.4, stroke_opacity=0.9)
    sign = VGroup(beam, panel, txt, rim_top)
    gate.shift(UP * _DY)
    sign.shift(UP * _DY)
    return gate, sign


# ======================================================== تدريج لوني سينمائي (غروب بنَفَس "سنايدر")
def build_grade():
    g = VGroup()
    # 1) سُحب ألوان: ظلال زرقاء/تيل مكتومة فوق كل حاجة
    g.add(_rect(-SIDE, SIDE, BOTTOM_Y - 0.2, 3.3, "#0A1020", 0.30))
    # 2) ضباب/غبار دافي عند الأفق
    n = 12
    for i in range(n):
        t = i / n
        h = 0.07
        g.add(_rect(-SIDE, SIDE, HORIZON_Y - 0.5 + 0.5 * t, HORIZON_Y - 0.5 + 0.5 * (t + 1 / n) + 0.005,
                    "#FF9A4D", 0.22 * t))
        g.add(_rect(-SIDE, SIDE, HORIZON_Y + 0.5 * (1 - t) - 0.5 / n, HORIZON_Y + 0.5 * (1 - t),
                    "#FF9A4D", 0.16 * t))
    # 3) فينييت جانبي
    for i in range(10):
        w = 1.6 / 10
        o = 0.5 * ((i + 1) / 10) ** 1.6
        g.add(_rect(-SIDE + 1.6 - w * (i + 1), -SIDE + 1.6 - w * i + 0.005, BOTTOM_Y - 0.2, 3.3, "#000000", o * 0.9))
        g.add(_rect(SIDE - 1.6 + w * i - 0.005, SIDE - 1.6 + w * (i + 1), BOTTOM_Y - 0.2, 3.3, "#000000", o * 0.9))
    g.set_z_index(6)
    return g


# ======================================================== اللوحة الإرشادية
def build_guide_board(x=4.5, y=0.12 + _DY):
    shadow = _poly([(x - 0.85, y - 1.35), (x + 0.85, y - 1.35), (x + 1.9, y - 1.8), (x + 0.2, y - 1.8)], "#070A14", 0.38)
    posts = VGroup(*[Rectangle(width=0.1, height=1.35, fill_color="#8B8F95", fill_opacity=1,
                               stroke_width=0).move_to([x + dx, y - 0.7, 0]) for dx in (-0.8, 0.8)])
    board = RoundedRectangle(corner_radius=0.08, width=2.9, height=1.2, fill_color="#17704D",
                             fill_opacity=1, stroke_color="#FFFFFF", stroke_width=4).move_to([x, y + 0.35, 0])
    sheen = _rect(x - 1.4, x + 1.4, y + 0.62, y + 0.9, "#FFFFFF", 0.06)
    l1 = _ar("أهلا بكم في", 20, "#FFFFFF", width=2.4)
    l2 = _ar("فضاء المتجهات", 25, "#FFE08A", width=2.6)
    lines = VGroup(l1, l2).arrange(DOWN, buff=0.12).move_to(board)
    return VGroup(shadow, posts, board, sheen, lines), VGroup(board, lines)


# ======================================================== العربية
def build_car():
    """سيدان من الخلف وفيها السواق باين من الإزاز الخلفي. المركز (0,0) والعرض ~1.9."""
    g = VGroup()
    g.add(Ellipse(width=2.8, height=0.3, fill_color="#05070E", fill_opacity=0.55,
                  stroke_width=0).move_to([0.25, -0.5, 0]))
    g.add(Ellipse(width=2.4, height=0.34, fill_color="#FF2A20", fill_opacity=0.16,
                  stroke_width=0).move_to([0, -0.5, 0]))
    for s in (-1, 1):
        g.add(RoundedRectangle(corner_radius=0.05, width=0.3, height=0.36, fill_color="#0F1013",
                               fill_opacity=1, stroke_width=0).move_to([s * 0.74, -0.3, 0]))
    # الصدام والجسم
    g.add(RoundedRectangle(corner_radius=0.1, width=1.94, height=0.3, fill_color="#7E2420",
                           fill_opacity=1, stroke_width=0).move_to([0, -0.17, 0]))
    g.add(RoundedRectangle(corner_radius=0.16, width=1.9, height=0.62, fill_color="#B7352D",
                           fill_opacity=1, stroke_color="#7E2420", stroke_width=1.5).move_to([0, 0.1, 0]))
    g.add(_rect(-0.9, 0.9, 0.31, 0.37, "#D5564C", 0.8))                 # لمعة غطاء الشنطة
    g.add(Line([-0.86, 0.12, 0], [0.86, 0.12, 0], color="#8C2923", stroke_width=2))
    # الكابينة
    g.add(_poly([(-0.72, 0.36), (0.72, 0.36), (0.55, 0.88), (-0.55, 0.88)], "#A92E27", 1, "#7E2420", 1.5))
    g.add(_poly([(-0.62, 0.4), (0.62, 0.4), (0.48, 0.82), (-0.48, 0.82)], "#1E2A38"))
    g.add(_poly([(-0.2, 0.4), (0.05, 0.4), (0.22, 0.82), (-0.03, 0.82)], "#3B5068", 0.55))   # انعكاس
    # مسند الراس + السواق (من الخلف) + مسند الراكب
    for dx in (-0.27, 0.27):
        g.add(RoundedRectangle(corner_radius=0.05, width=0.2, height=0.2, fill_color="#14181F",
                               fill_opacity=1, stroke_width=0).move_to([dx, 0.55, 0]))
    g.add(_poly([(-0.37, 0.4), (-0.17, 0.4), (-0.19, 0.5), (-0.35, 0.5)], "#EDE7D3"))  # كتف الشخص
    g.add(_poly([(-0.4, 0.4), (-0.14, 0.4), (-0.17, 0.5), (-0.37, 0.5)], "#EDE7D3"))
    g.add(Circle(radius=0.12, fill_color="#2A1D15", fill_opacity=1, stroke_width=0).move_to([-0.27, 0.62, 0]))
    for dx in (-0.395, -0.145):
        g.add(Circle(radius=0.02, fill_color="#E6B98C", fill_opacity=1, stroke_width=0).move_to([dx, 0.6, 0]))
    # الفوانيس الخلفية
    for s in (-1, 1):
        g.add(Circle(radius=0.4, fill_color="#FF3B30", fill_opacity=0.09, stroke_width=0).move_to([s * 0.7, 0.16, 0]))
        g.add(_poly([(s * 0.5, 0.06), (s * 0.93, 0.06), (s * 0.93, 0.27), (s * 0.55, 0.27)], "#D32222", 1, "#7E1410", 1))
        g.add(_poly([(s * 0.58, 0.1), (s * 0.88, 0.1), (s * 0.88, 0.2), (s * 0.6, 0.2)], "#FF6A5E", 0.85))
    # اللوحة المعدنية
    g.add(RoundedRectangle(corner_radius=0.03, width=0.5, height=0.17, fill_color="#F3EFE0",
                           fill_opacity=1, stroke_color="#222", stroke_width=1.2).move_to([0, 0.0, 0]))
    for k in range(5):
        g.add(_rect(-0.19 + 0.08 * k, -0.15 + 0.08 * k, -0.04, 0.04, "#222"))
    g.add(Circle(radius=0.035, fill_color="#0B0B0D", fill_opacity=1, stroke_width=0).move_to([0.6, -0.27, 0]))
    return g


def build_red_x(center=(0, 0.4, 0), half=1.5):
    cx, cy = center[0], center[1]
    kw = dict(color=_RED, stroke_width=26)
    l1 = Line([cx - half, cy + half, 0], [cx + half, cy - half, 0], **kw)
    l2 = Line([cx + half, cy + half, 0], [cx - half, cy - half, 0], **kw)
    for l in (l1, l2):
        try:
            l.set_stroke(capstyle=CapStyleType.ROUND)
        except Exception:
            pass
    return l1, l2


def play_vector_space_gate(scene, cap=None, drive_time=6.0, hold=3.0, fade_out=True,
                           note="مش موجود في الواقع!", caption=None):
    """
    يشغّل اللقطة كاملة. المدة الإجمالية تقريبًا = drive_time + 7.6 + hold (+0.7 لو fade_out).
    cap: كائن الترجمة (اختياري) — لو اتمرّر هيظهر عليه caption عند ظهور علامة الـ X.
    """
    world = build_scenery()
    gate, sign = build_gate()
    guide_all, guide_board = build_guide_board()
    grade = build_grade()
    car = build_car().scale(1.25).move_to([0, -2.35, 0])
    car.set_z_index(5)
    everything = VGroup(world, gate, sign, guide_all, car, grade)

    # الأرض والسور والبوابة بيظهروا مع بعض (السور ظاهر من أول لحظة)، وبعدين اليافطة
    scene.play(FadeIn(VGroup(world, gate, grade)), run_time=1.2)
    scene.play(FadeIn(sign, shift=DOWN * 0.15), run_time=0.8)
    scene.play(FadeIn(guide_all, shift=LEFT * 0.2), run_time=0.8)
    scene.play(FadeIn(car), run_time=0.6)
    scene.play(car.animate.scale(0.56).move_to([0, -0.1, 0]), run_time=drive_time,
               rate_func=rate_functions.ease_in_out_sine)
    scene.play(Indicate(sign, color=None, scale_factor=1.06), Indicate(guide_board, color=None, scale_factor=1.06),
               run_time=1.2)
    dim = Rectangle(width=14.4, height=8.2, fill_color="#000000", fill_opacity=0.55,
                    stroke_width=0).set_z_index(20)
    l1, l2 = build_red_x()
    l1.set_z_index(21); l2.set_z_index(21)
    scene.play(FadeIn(dim), run_time=0.5)
    scene.play(Create(l1), run_time=0.4)
    scene.play(Create(l2), run_time=0.4)
    extras = VGroup()
    if note:
        chip = RoundedRectangle(corner_radius=0.15, width=4.6, height=0.8, fill_color="#1A0E0E",
                                fill_opacity=0.95, stroke_color=_RED, stroke_width=3).move_to([0, -1.75, 0])   # مرفوعة عشان متتداخلش مع الترجمة الحمرا تحتها
        chip_t = _ar(note, 26, "#FFB3B5", width=4.2).move_to(chip)
        extras = VGroup(chip, chip_t).set_z_index(22)
        scene.play(FadeIn(extras, shift=UP * 0.15), run_time=0.6)
    if cap is not None and caption:
        cap.set(caption, _RED)
        if getattr(cap, "cur", None) is not None:
            cap.cur.set_z_index(50)   # الترجمة فوق التعتيم وفوق ظل أسفل الأرض (كانت نصفها متداري)
    scene.wait(hold)

    group = VGroup(everything, dim, l1, l2, extras)
    if fade_out:
        scene.play(FadeOut(group), run_time=0.7)
    return group