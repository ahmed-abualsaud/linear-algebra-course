from manim import *
import numpy as np

from common.palette import (
    GOLD_BRIGHT, GOLD_LIGHT, GOLD, TEAL,
    STONE_AXIS, COPPER_TERRA, IVORY_WHITE,
)
from common.latex import mach_math_template
from common.thumbnails import *

# ==============================================================
# Thumbnail — الحلقة 05: قواعد جمع المتجهات
# الفكرة: جمع متجهين (u ثم v) بالأرقام الحقيقية من الحلقة: [6,2] + [3,4] = [9,6]
# تحت العنوان: المعادلة بالمصفوفات الملونة + خمس أيقونات = الشروط الخمسة (بدون تفضيل شرط على التاني).
# نفس لغة الحلقة 04: شبكة بتخفت، متجهات متوهجة، رموز ملونة، عنوان من غير تشققات.
# ==============================================================

# ---------------- إعدادات سريعة ----------------
TITLE_LINE1 = "كيف"
TITLE_LINE2 = "نجمع المتجهات؟"
BADGE_TEXT = "الجبر الخطي • الحلقة 05"

C_U, C_V, C_SUM = COPPER_TERRA, GOLD_LIGHT, IVORY_WHITE      # u نحاسي، v ذهبي فاتح، u+v عاجي

U = 0.42                                                      # طول وحدة الشبكة
O = np.array([-3.30, -2.90, 0.0])                             # نقطة الأصل
U_VEC = np.array([6.0, 2.0])                                  # u = [6, 2]
V_VEC = np.array([3.0, 4.0])                                  # v = [3, 4]
GRID_BOX = (-3.3, 6.75, -3.68, 3.68)                          # جوه إطار القناة (±3.78) بهامش صغير
FADE_W = 0.001                                                # الشبكة تبدأ من السهم الراسي مباشرة (من غير منطقة سودا جنبه)
TEXT_SHIFT_X = 0.30
AXIS_X_LEN = 4.25                                             # المحور الأفقي بيخلص قبل صف الأيقونات الخمسة


def P(x, y):
    return np.array([O[0] + U * x, O[1] + U * y, 0.0])


# ---------------- أدوات ----------------
def edge_fade(x):
    t = np.clip((x - GRID_BOX[0]) / FADE_W, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def add_faded(g, p, q, color, width, opacity):
    p, q = np.asarray(p, float)[:2], np.asarray(q, float)[:2]
    if min(p[0], q[0]) >= GRID_BOX[0] + FADE_W:
        g.add(Line([*p, 0], [*q, 0], color=color, stroke_width=width, stroke_opacity=opacity))
        return
    n = max(2, int(np.ceil(np.linalg.norm(q - p) / 0.4)))
    for i in range(n):
        a = p + (q - p) * i / n
        b = p + (q - p) * (i + 1) / n
        f = edge_fade((a[0] + b[0]) / 2)
        if f * opacity < 0.01:
            continue
        g.add(Line([*a, 0], [*b, 0], color=color, stroke_width=width, stroke_opacity=opacity * f))


def lattice(color, width, base, fade_rate=0.034, min_op=0.07, k0=-18, k1=24):
    g = VGroup()
    for fam, step in ((np.array([1.0, 0.0]), np.array([0.0, 1.0])), (np.array([0.0, 1.0]), np.array([1.0, 0.0]))):
        for k in range(k0, k1 + 1):
            if k == 0:
                continue
            c0 = O[:2] + U * k * step
            c = clip_line(c0 - 45 * U * fam, c0 + 45 * U * fam, GRID_BOX)
            if c is None:
                continue
            d = np.linalg.norm((c[0] + c[1]) / 2 - O[:2])
            add_faded(g, c[0], c[1], color, width, max(min_op, base - fade_rate * d))
    return g


def starburst(center, n=12, r0=0.30, r1=0.62, color=GOLD_BRIGHT):
    g = VGroup()
    for i in range(n):
        a = 2 * PI * i / n + 0.13
        r_out = r1 * (1.0 if i % 2 == 0 else 0.72)
        d = np.array([np.cos(a), np.sin(a), 0])
        g.add(Line(center + d * r0, center + d * r_out, color=color, stroke_width=3.2 if i % 2 == 0 else 2.0,
                   stroke_opacity=0.85 if i % 2 == 0 else 0.55).set_cap_style(CapStyleType.ROUND))
    return g


def _round_joints(mob):
    for sm in mob.family_members_with_points():
        sm.joint_type = LineJointType.ROUND
    return mob


def solid_text(text, width, color_a=IVORY_WHITE, color_b=GOLD_BRIGHT, glow=GOLD_LIGHT, outline_w=4,
               halo_w=(14, 7)):
    """نص عربي عريض بدون تشققات ولا نتوءات (مع fallback لو MarkupText رجعت فاضية)."""
    main = MarkupText(f"<b>{text}</b>", font=THUMB_FONT, font_size=96)
    if len(main.family_members_with_points()) == 0:
        main = Text(text, font=THUMB_FONT, font_size=96, weight=BOLD)
    if len(main.family_members_with_points()) == 0:
        main = Text(text, font_size=96, weight=BOLD)
    main.set(width=width)
    main.set_color_by_gradient(color_a, color_b)
    for sm in main.family_members_with_points():
        sm.set_stroke(sm.get_fill_color(), width=1.6, opacity=1)
    _round_joints(main)
    outline = _round_joints(main.copy().set_fill(opacity=0).set_stroke(THUMB_BG, width=outline_w, opacity=0.9))
    halo = VGroup(
        main.copy().set_fill(opacity=0).set_stroke(glow, width=halo_w[0], opacity=0.07),
        main.copy().set_fill(opacity=0).set_stroke(glow, width=halo_w[1], opacity=0.11),
    )
    _round_joints(halo)
    return VGroup(halo, outline, main)


def small_arrow(a, b, color, width=5.0):
    return Arrow(a, b, buff=0, stroke_width=width, color=color,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


RULE_COLS = [GOLD_LIGHT, GOLD_BRIGHT, COPPER_TERRA, IVORY_WHITE, TEAL]


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


class Episode05Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = THUMB_BG

        A = P(*U_VEC)                         # نهاية u
        TIP = P(*(U_VEC + V_VEC))             # نهاية u + v  = [9, 6]
        mid = (O + TIP) / 2

        # ---------------- الخلفية والتوهج ----------------
        warm = vignette_bg()
        hot = soft_glow(mid, 3.4, GOLD, layers=22, peak=0.06)
        tip_glow = soft_glow(TIP, 1.9, GOLD_BRIGHT, layers=16, peak=0.20)

        grid = lattice(STONE_AXIS, 1.4, 0.45)

        # المحاور (بتتلاشى عند حد الشخصية)
        axis_x = VGroup()
        add_faded(axis_x, [GRID_BOX[0], O[1]], [O[0] + AXIS_X_LEN, O[1]], GOLD_LIGHT, 3.0, 0.9)
        axis_y = Line([O[0], GRID_BOX[2], 0], [O[0], O[1] + 4.7, 0], color=GOLD_LIGHT, stroke_width=3.0,
                      stroke_opacity=0.9)
        tips = VGroup(
            Triangle(fill_color=GOLD_LIGHT, fill_opacity=0.95, stroke_width=0).scale(0.14).rotate(-PI / 2)
            .move_to([O[0] + AXIS_X_LEN, O[1], 0]),
            Triangle(fill_color=GOLD_LIGHT, fill_opacity=0.95, stroke_width=0).scale(0.14)
            .move_to(axis_y.get_end()),
        )
        self.add(warm, hot, grid, axis_x, axis_y, tips, channel_frame())

        # ---------------- البطل: u ثم v ثم u+v (رأس لذيل) ----------------
        # خطوط إسقاط خفيفة بتوضّح مركبات المجموع [9, 6]
        drops = VGroup(
            DashedLine(TIP, [TIP[0], O[1], 0], dash_length=0.10, color=GOLD_LIGHT, stroke_width=2.0,
                       stroke_opacity=0.45),
            DashedLine(TIP, [O[0], TIP[1], 0], dash_length=0.10, color=GOLD_LIGHT, stroke_width=2.0,
                       stroke_opacity=0.45),
        )
        u_arrow = glow_arrow(O, A, C_U, 9, COPPER_TERRA, tip_ratio=0.16)
        v_arrow = glow_arrow(A, TIP, C_V, 9, GOLD_LIGHT, tip_ratio=0.16)
        sum_arrow = glow_arrow(O, TIP, C_SUM, 12, GOLD, tip_ratio=0.13)
        joint = VGroup(Dot(A, radius=0.15, color=GOLD_LIGHT).set_opacity(0.25),
                       Dot(A, radius=0.07, color=IVORY_WHITE))
        burst = starburst(TIP)
        tip_dot = VGroup(Dot(TIP, radius=0.20, color=GOLD_BRIGHT).set_opacity(0.30),
                         Dot(TIP, radius=0.09, color=IVORY_WHITE))

        def tx(s, size, col, w=8):
            return stroked(MathTex(s, tex_template=mach_math_template, font_size=size, color=col), width=w)

        u_dir = (A - O) / np.linalg.norm(A - O)
        v_dir = (TIP - A) / np.linalg.norm(TIP - A)
        s_dir = (TIP - O) / np.linalg.norm(TIP - O)
        lu = tx(r"\mathbf{u}", 72, C_U).move_to((O + A) / 2 + np.array([u_dir[1], -u_dir[0], 0]) * 0.50)
        lv = tx(r"\mathbf{v}", 72, C_V).move_to((A + TIP) / 2 + np.array([v_dir[1], -v_dir[0], 0]) * 0.55)
        lsum = tx(r"\mathbf{u}+\mathbf{v}", 72, C_SUM)
        lsum[0][0:1].set_color(C_U)
        lsum[0][2:3].set_color(C_V)
        lsum.move_to(mid + np.array([-s_dir[1], s_dir[0], 0]) * 0.70)

        hero = layer([tip_glow, drops, u_arrow, v_arrow, sum_arrow, joint, burst, tip_dot, glow_dot(O),
                      lu, lv, lsum], 35)
        self.add(hero)

        # ---------------- الشخصية ----------------
        self.add(*mathematician_with_glow())

        # ---------------- العنوان ----------------
        # نبعت "قواعد" مؤقتاً لـ title_block عشان glowing_text ما تقعش على "كيف"، وبعدين نستبدلها بـ TITLE_LINE1
        title = title_block("قواعد", TITLE_LINE2, BADGE_TEXT, line1_width=2.3, line2_width=5.6)
        for mob in title.get_family():
            if isinstance(mob, (Polygon, Ellipse, Rectangle, RoundedRectangle)):
                if mob.get_fill_color().to_hex().lower() in [THUMB_BG.lower(), "#000000", "#0e0905"]:
                    mob.set_fill(opacity=0)
                    mob.set_stroke(opacity=0)

        def _pick_text_mob(m):
            if isinstance(m, VGroup) and len(m) > 1 and len(m[1].family_members_with_points()) > 0:
                return m[1]
            return m

        old_l2 = _pick_text_mob(title[2])
        new_l2 = solid_text(TITLE_LINE2, old_l2.width, GOLD_BRIGHT, GOLD, glow=GOLD, outline_w=9, halo_w=(20, 10))
        new_l2.move_to(old_l2.get_center())
        title.submobjects[2] = new_l2

        old_l1 = _pick_text_mob(title[1])
        new_l1 = solid_text(TITLE_LINE1, old_l1.width)
        new_l1.next_to(new_l2, UP, buff=0.30).align_to(new_l2, RIGHT)
        title.submobjects[1] = new_l1

        title.shift(RIGHT * TEXT_SHIFT_X)
        title.set_z_index(30)
        self.add(title, brand_mark().set_z_index(30))
        underline = title[3]

        # ---------------- عمود تحت العنوان: المعادلة بالمصفوفات + الشروط الخمسة ----------------
        def mat(a, b, col):
            return MathTex(rf"\begin{{bmatrix}}{a}\\[3pt]{b}\end{{bmatrix}}", tex_template=mach_math_template,
                           font_size=62, color=col)

        def op(s):
            return MathTex(s, tex_template=mach_math_template, font_size=62, color=IVORY_WHITE)

        mrow = VGroup(mat(6, 2, C_U), op("+"), mat(3, 4, C_V), op("="), mat(9, 6, C_SUM)).arrange(RIGHT, buff=0.28)
        mrow = stroked(mrow, width=6)
        if mrow.width > 5.3:
            mrow.scale(5.3 / mrow.width)

        pills = [rule_pill(i + 1, c) for i, c in enumerate(RULE_COLS)]
        rules = VGroup(*reversed(pills)).arrange(RIGHT, buff=0.12)      # الشرط 1 على اليمين (اتجاه القراءة)

        col = VGroup(mrow, rules).arrange(DOWN, buff=0.42)
        top_y = underline.get_bottom()[1] - 0.35
        avail = top_y - (-3.30)
        if col.height > avail:
            col.scale(avail / col.height)
        if col.width > 5.4:
            col.scale(5.4 / col.width)
        col.move_to([underline.get_center()[0], 0, 0])
        col.shift(UP * (top_y - col.get_top()[1]))
        col.set_z_index(30)
        self.add(col)