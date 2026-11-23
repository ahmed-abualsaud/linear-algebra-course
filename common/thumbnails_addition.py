"""
مشهد "كيف نجمع المتجهات؟" (الحلقة 05): u ثم v رأس لذيل = u+v، [6,2] + [3,4] = [9,6]،
+ خمس أيقونات لقواعد الجمع تحت الرسمة، والمعادلة بالمصفوفات تحت العنوان.
الاستخدام (داخل Scene عادي):
    from common.thumbnails_addition import *
    build_vector_addition(self, ltr=False, line1=..., line2=..., badge_text=..., line1_width=..., line2_width=...)

المنطق (نفس لغة الحلقة 04):
  - الشخصية اتشالت؛ الرسمة بتتحجّم وتتمركز تلقائياً في المساحة اللي فوق صف الأيقونات (REGION_*).
  - الشبكة بتملأ الإطار كله وبتخفت مع البعد (من غير هالة سودة ورا العناوين).
  - المحاور محدودة وبسهم في الطرفين، وأرقام المركبات 9 و6 على المحورين بتربط الرسمة بالمصفوفة [9,6].
  - الأيقونات الخمس تحت الرسمة (الشرط 1 أول اتجاه القراءة: يمين في RTL، يسار في LTR).
  - المصفوفات تحت العنوان متوسطة رأسياً في المساحة الفاضية ومحاذية لحافة العنوان.
"""
from manim import *
import numpy as np

from common.palette import (
    GOLD_BRIGHT, GOLD_LIGHT, GOLD, TEAL, STONE_AXIS, COPPER_TERRA, IVORY_WHITE,
)
from common.latex import mach_math_template
from common.thumbnails import *
from common.thumbnails import _axis_arrow
from common.thumbnails_basis import lattice, E1, E2

C_U, C_V, C_SUM = COPPER_TERRA, GOLD_LIGHT, IVORY_WHITE      # u نحاسي، v ذهبي فاتح، u+v عاجي
U_VEC = np.array([6.0, 2.0])                                  # u = [6, 2]
V_VEC = np.array([3.0, 4.0])                                  # v = [3, 4]
SUM_VEC = U_VEC + V_VEC                                       # u + v = [9, 6]

U0 = 0.42                                                     # الوحدة اللي اتصممت عليها إزاحات التسميات
PILL_SCALE = 1.00                                             # حجم صف الأيقونات
PILL_GAP = 0.12
MROW_W = 4.4                                                  # عرض صف المصفوفات تحت العنوان
RULES_GAP = 0.65                                              # مسافة بين صف الأيقونات والرسمة (أرقام المحور السفلي والسهم)

# المساحة الأفقية للرسمة (x0, x1) — الرأسية بتتحسب من صف الأيقونات. القمة 2.75 عشان محور y يفضل بعيد عن اسم القناة.
REGION_X_RTL = (-6.40, 0.10)
REGION_X_LTR = (-0.10, 6.40)
REGION_TOP = 2.75
EXT = dict(left=0.60, right=0.80, bottom=0.45, top=0.70)      # امتداد المحاورين خارج الرسمة (وحدات الشاشة)

RULE_COLS = [GOLD_LIGHT, GOLD_BRIGHT, COPPER_TERRA, IVORY_WHITE, TEAL]


# ---------------- الأيقونات ----------------
def small_arrow(a, b, color, width=5.0):
    return Arrow(a, b, buff=0, stroke_width=width, color=color,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def rule_icon(i, col):
    """أيقونة هندسية لكل شرط (من غير كلام عشان تتقري حتى لو الصورة صغيرة)."""
    c = ORIGIN
    if i == 1:        # الإغلاق: متجه جوه فقاعة الفضاء
        ring = Circle(radius=0.30, color=col, stroke_width=3.2).set_fill(col, 0.08)
        return VGroup(ring, small_arrow(c + np.array([-0.14, -0.12, 0]), c + np.array([0.14, 0.14, 0]), IVORY_WHITE))
    if i == 2:        # المحايد: صفر متوهج
        glow = Circle(radius=0.24, stroke_width=0, fill_color=col, fill_opacity=0.18)
        z = MathTex("0", tex_template=mach_math_template, font_size=52, color=col)
        return VGroup(glow, z)
    if i == 3:        # المعكوس: سهمين متعاكسين من نفس النقطة
        return VGroup(small_arrow(c + np.array([0.03, 0, 0]), c + np.array([0.36, 0, 0]), C_U),
                      small_arrow(c + np.array([-0.03, 0, 0]), c + np.array([-0.36, 0, 0]), TEAL),
                      Dot(c, radius=0.045, color=IVORY_WHITE))
    if i == 4:        # الإبدال: متوازي أضلاع
        pts = [np.array(p) for p in ((-0.30, -0.19, 0), (0.10, -0.19, 0), (0.30, 0.19, 0), (-0.10, 0.19, 0))]
        para = Polygon(*pts, stroke_color=col, stroke_width=3.0, fill_color=col, fill_opacity=0.12)
        return VGroup(para, Line(pts[0], pts[2], color=col, stroke_width=2.2, stroke_opacity=0.8))
    # 5 التجميع: ثلاثة أسهم ورا بعض
    a, b, d, e = (np.array(p) for p in ((-0.34, -0.17, 0), (-0.06, 0.08, 0), (0.12, -0.12, 0), (0.36, 0.14, 0)))
    return VGroup(small_arrow(a, b, C_U), small_arrow(b, d, C_V), small_arrow(d, e, col))


def rule_pill(i, col):
    pill = RoundedRectangle(corner_radius=0.16, width=0.98, height=1.12, stroke_color=col, stroke_width=2.2,
                            fill_color="#14100A", fill_opacity=0.92)
    icon = rule_icon(i, col).move_to(pill.get_center() + UP * 0.14)
    num = MathTex(str(i), tex_template=mach_math_template, font_size=28, color=col)
    num.move_to(pill.get_bottom() + UP * 0.20)
    return VGroup(pill, icon, num)


def build_rules_row(ltr):
    """صف الأيقونات الخمس: الشرط 1 أول اتجاه القراءة (يمين في RTL، يسار في LTR)."""
    pills = [rule_pill(i + 1, c) for i, c in enumerate(RULE_COLS)]
    rules = VGroup(*(pills if ltr else reversed(pills))).arrange(RIGHT, buff=PILL_GAP)
    rules.scale(PILL_SCALE)
    return rules


# ---------------- الهندسة ----------------
def addition_geometry(ltr, rules_height):
    """يرجّع (U, O): وحدة الشبكة ونقطة الأصل، بحيث الرسمة تملا المساحة فوق صف الأيقونات وتتمركز فيها."""
    x0, x1 = REGION_X_LTR if ltr else REGION_X_RTL
    y0 = -(FRAME_TOP - MARGIN) + rules_height + RULES_GAP
    y1 = REGION_TOP
    u_h = ((y1 - y0) - EXT["bottom"] - EXT["top"]) / SUM_VEC[1]
    u_w = ((x1 - x0) - EXT["left"] - EXT["right"]) / SUM_VEC[0]
    U = min(u_h, u_w)
    ox = (x0 + x1) / 2 - (-EXT["left"] + SUM_VEC[0] * U + EXT["right"]) / 2
    oy = (y0 + y1) / 2 - (SUM_VEC[1] * U + EXT["top"] - EXT["bottom"]) / 2
    return U, np.array([ox, oy, 0.0])


def starburst(center, n=12, r0=0.30, r1=0.62, color=GOLD_BRIGHT):
    g = VGroup()
    for i in range(n):
        a = 2 * PI * i / n + 0.13
        r_out = r1 * (1.0 if i % 2 == 0 else 0.72)
        d = np.array([np.cos(a), np.sin(a), 0])
        g.add(Line(center + d * r0, center + d * r_out, color=color, stroke_width=3.2 if i % 2 == 0 else 2.0,
                   stroke_opacity=0.85 if i % 2 == 0 else 0.55).set_cap_style(CapStyleType.ROUND))
    return g


def build_vector_addition(scene, ltr, line1, line2, badge_text, line1_width, line2_width, badge_width=3.5):
    scene.camera.background_color = THUMB_BG

    rules = build_rules_row(ltr)
    U, O = addition_geometry(ltr, rules.height)
    s = U / U0                       # تكبير الرسمة عن التصميم الأصلي
    fs = min(s, 1.25)                # تكبير الخطوط أقل شوية عشان ما تبقاش ضخمة
    P = lambda x, y: np.array([O[0] + U * x, O[1] + U * y, 0.0])

    A = P(*U_VEC)                    # نهاية u
    TIP = P(*SUM_VEC)                # نهاية u + v = [9, 6]
    mid = (O + TIP) / 2

    # ---------------- 1. الخلفية والتوهج والشبكة (بالعرض الكامل)
    warm = vignette_bg(center=(2.5 if ltr else -2.5, -0.5, 0))
    hot = soft_glow(mid, 3.4, GOLD, layers=22, peak=0.06)
    tip_glow = soft_glow(TIP, 1.9, GOLD_BRIGHT, layers=16, peak=0.20)
    grid = lattice(O, U, E1, E2, STONE_AXIS, width=1.4, base=0.45, fade_rate=0.035, min_op=0.08)

    # ---------------- 2. المحاور (محدودة وبسهم في الطرفين)
    axes = VGroup(
        _axis_arrow(O + np.array([-EXT["left"], 0, 0]), O + np.array([SUM_VEC[0] * U + EXT["right"], 0, 0]),
                    color=GOLD_LIGHT),
        _axis_arrow(O + np.array([0, -EXT["bottom"], 0]), O + np.array([0, SUM_VEC[1] * U + EXT["top"], 0]),
                    color=GOLD_LIGHT),
    )

    # ---------------- 3. البطل: u ثم v ثم u+v (رأس لذيل)
    def dash(p, q, col):
        return DashedLine(p, q, dash_length=0.10, color=col, stroke_width=1.8, stroke_opacity=0.42)

    ux, uy = U_VEC
    vx, vy = V_VEC
    sx, sy = SUM_VEC
    drops = VGroup(
        # u = [6, 2]: من نهاية u للمحورين
        dash(A, P(ux, 0), C_U), dash(A, P(0, uy), C_U),
        # u + v = [9, 6]
        dash(TIP, P(sx, 0), C_SUM), dash(TIP, P(0, sy), C_SUM),
    )

    u_arrow = glow_arrow(O, A, C_U, 9 * fs, COPPER_TERRA, tip_ratio=0.16)
    v_arrow = glow_arrow(A, TIP, C_V, 9 * fs, GOLD_LIGHT, tip_ratio=0.16)
    sum_arrow = glow_arrow(O, TIP, C_SUM, 12 * fs, GOLD, tip_ratio=0.13)
    joint = VGroup(Dot(A, radius=0.15 * fs, color=GOLD_LIGHT).set_opacity(0.25),
                   Dot(A, radius=0.07 * fs, color=IVORY_WHITE))
    burst = starburst(TIP, r0=0.30 * fs, r1=0.62 * fs)
    tip_dot = VGroup(Dot(TIP, radius=0.20 * fs, color=GOLD_BRIGHT).set_opacity(0.30),
                     Dot(TIP, radius=0.09 * fs, color=IVORY_WHITE))

    def tx(tex, size, col, w=8):
        return stroked(MathTex(tex, tex_template=mach_math_template, font_size=size * fs, color=col), width=w)

    v_dir = (TIP - A) / np.linalg.norm(TIP - A)
    s_dir = (TIP - O) / np.linalg.norm(TIP - O)
    # u: جنب المتجه بتاعه (تحته ويمينه، فوق المحور الأفقي) زي v
    u_dir = (A - O) / np.linalg.norm(A - O)
    lu = tx(r"\mathbf{u}", 72, C_U).move_to(O + (A - O) * 0.72 + np.array([u_dir[1], -u_dir[0], 0]) * 0.34 * s)
    lv = tx(r"\mathbf{v}", 72, C_V).move_to((A + TIP) / 2 + np.array([v_dir[1], -v_dir[0], 0]) * 0.55 * s)
    lsum = tx(r"\mathbf{u}+\mathbf{v}", 72, C_SUM)
    lsum[0][0:1].set_color(C_U)
    lsum[0][2:3].set_color(C_V)
    lsum.move_to(O + (TIP - O) * 0.62 + np.array([-s_dir[1], s_dir[0], 0]) * 0.78 * s)

    # أرقام المركبات على المحورين (صغيرة): u نحاسي، v ذهبي فاتح، u+v عاجي — نفس ألوان المصفوفات
    def num(val, col, pos):
        return tx(str(int(val)), 34, col, w=6).move_to(pos)

    nums = VGroup(
        num(vx, C_V, [P(vx, 0)[0], O[1] - 0.30, 0]), num(ux, C_U, [P(ux, 0)[0], O[1] - 0.30, 0]),
        num(sx, C_SUM, [P(sx, 0)[0], O[1] - 0.30, 0]),
        num(uy, C_U, [O[0] - 0.44, P(0, uy)[1], 0]), num(vy, C_V, [O[0] - 0.44, P(0, vy)[1], 0]),
        num(sy, C_SUM, [O[0] - 0.44, P(0, sy)[1], 0]),
    )

    hero = layer([tip_glow, drops, u_arrow, v_arrow, sum_arrow, joint, burst, tip_dot, glow_dot(O),
                  lu, lv, lsum, nums], 12)

    # ---------------- 4. العنوان والبادج (padding موحد من الإطار)
    title = title_block(
        line1, line2, badge_text,
        ltr=ltr, margin=MARGIN,
        line1_width=line1_width, line2_width=line2_width, badge_width=badge_width,
        line2_y=0.82 if ltr else 0.55, badge_gap=0.24,
        ltr_offsets=(1.05, -0.75),
    )
    title.shift(UP * ((FRAME_TOP - MARGIN) - title[3].get_top()[1]))    # حافة البادج العليا بالظبط على MARGIN
    brand = brand_mark_at(UR if ltr else UL)

    # ---------------- 5. المعادلة بالمصفوفات تحت العنوان (متوسطة رأسياً في المساحة الفاضية)
    def mat(a, b, col):
        return MathTex(rf"\begin{{bmatrix}}{a}\\[3pt]{b}\end{{bmatrix}}", tex_template=mach_math_template,
                       font_size=74, color=col)

    def op(tex):
        return MathTex(tex, tex_template=mach_math_template, font_size=74, color=IVORY_WHITE)

    mrow = VGroup(mat(6, 2, C_U), op("+"), mat(3, 4, C_V), op("="), mat(9, 6, C_SUM)).arrange(RIGHT, buff=0.30)
    stroked(mrow, width=6)
    mrow.set_width(MROW_W)
    top_y = title[2].get_bottom()[1] - 0.35
    bottom_limit = -(FRAME_TOP - MARGIN)
    avail = top_y - bottom_limit
    if mrow.height > avail:
        mrow.scale(avail / mrow.height)
    edge = -FRAME_FX + MARGIN if ltr else FRAME_FX - MARGIN
    mrow.align_to(np.array([edge, 0.0, 0.0]), LEFT if ltr else RIGHT)
    mrow.shift(UP * ((top_y + bottom_limit) / 2 - mrow.get_center()[1]))
    mrow.set_z_index(30)

    # ---------------- 6. صف الأيقونات تحت الرسمة (متمركز مع الرسمة، حافته السفلية على MARGIN)
    x0, x1 = REGION_X_LTR if ltr else REGION_X_RTL
    rules.move_to([(x0 + x1) / 2, bottom_limit + rules.height / 2, 0])
    rules.set_z_index(30)

    scene.add(warm, hot, grid, axes, channel_frame().set_z_index(25), hero, title, brand, mrow, rules)