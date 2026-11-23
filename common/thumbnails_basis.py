"""
مشهد "تمهيد لقواعد المتجهات" (الحلقة 04): المتجه نفسه v بطريقتين = أساس e (3,5) وأساس f (4,1)، + العنوان والمعادلات.
الاستخدام (داخل Scene عادي):
    from common.thumbnails_basis import *
    build_basis_change(self, ltr=False, line1=..., line2=..., badge_text=..., line1_width=..., line2_width=...)

المنطق:
  - الرسمة بتتحجّم وتتمركز تلقائياً في المساحة الفاضية (REGION_RTL / REGION_LTR): الارتفاع هو اللي بيحدد وحدة الأساس U.
    كل إزاحات التسميات متصممة على U0=0.60 وبتتضرب في U/U0 فالتخطيط الأصلي بيتحافظ عليه.
  - الشبكتان (المعتدلة بالرمادي، والمائلة بالـ TEAL على الأساس f) بيملوا الإطار كله وبيخفتوا مع البعد عن الأصل،
    فالعنوان بيتقرأ فوقهم من غير هالة سودة (زي الحلقات 01 و02).
  - المحاوران الذهبيان محدودان وبسهم في الطرفين (مش خط كامل) عشان ما يلمسوش اسم القناة أو العنوان.
  - RTL: الرسمة على الشمال والعنوان والمعادلات على اليمين. LTR: العكس.
"""
from manim import *
import numpy as np

from common.palette import (
    GOLD_BRIGHT, GOLD_LIGHT, GOLD, TEAL, STONE_AXIS, COPPER_TERRA, IVORY_WHITE,
)
from common.latex import mach_math_template
from common.thumbnails import *
from common.thumbnails import _axis_arrow

F2_COL = "#A8EDE3"                       # تركواز فاتح لـ f2 (يتفرق عن ذهبي v وعن تركواز f1)

E1, E2 = np.array([1.0, 0.0]), np.array([0.0, 1.0])
F1, F2 = np.array([1.0, 1.0]), np.array([-1.0, 1.0])
V_STD = (3, 5)                           # v = 3 e1 + 5 e2
V_NEW = (4, 1)                           # v = 4 f1 + 1 f2  →  4(1,1) + (-1,1) = (3,5)

FORMULA_W = 6.2                          # أقصى عرض للصيغة العامة v = v1 e1 + ... + vn en
BASIS_TAG_SIZE = 64                      # حجم رمز الأساس e / f جنب المصفوفتين
AXIS_FADE_LEN = 6.0                      # طول تلاشي المحاور القطرية التركواز
U0 = 0.60                                # الوحدة اللي اتصممت عليها إزاحات التسميات الأصلية

# المساحة الفاضية للرسمة (x0, x1, y0, y1). القمة 2.75 عشان محور y يفضل بعيد عن اسم القناة (UL/UR).
REGION_RTL = (-6.30, 0.80, -3.35, 2.75)
REGION_LTR = (-0.50, 6.50, -3.35, 2.75)
# امتداد المحاورين خارج الرسمة (بوحدات الشاشة): يسار، يمين (بعد نهاية مسار f)، تحت، فوق (بعد رأس v)
EXT = dict(left=1.30, right=1.20, bottom=1.00, top=0.70)


def basis_geometry(ltr):
    """يرجّع (U, O, s): وحدة الأساس، نقطة الأصل، ومعامل تكبير الإزاحات s=U/U0."""
    x0, x1, y0, y1 = REGION_LTR if ltr else REGION_RTL
    u_h = ((y1 - y0) - EXT["bottom"] - EXT["top"]) / V_STD[1]
    u_w = ((x1 - x0) - EXT["left"] - EXT["right"]) / 4.0
    U = min(u_h, u_w)
    ox = (x0 + x1) / 2 - (-EXT["left"] + 4 * U + EXT["right"]) / 2
    oy = (y0 + y1) / 2 - (5 * U + EXT["top"] - EXT["bottom"]) / 2
    return U, np.array([ox, oy, 0.0]), U / U0


def lattice(O, U, a, b, color, width, base, fade_rate=0.032, min_op=0.08, k0=-22, k1=26):
    """شبكة واضحة تملأ الإطار وتخف تدريجياً مع البعد عن الأصل لتعطي عمقاً دون تشويش."""
    g = VGroup()
    for fam, step in ((a, b), (b, a)):
        for k in range(k0, k1 + 1):
            c0 = O[:2] + U * k * step
            c = clip_line(c0 - 45 * U * fam, c0 + 45 * U * fam, GRID_BOX)
            if c is None:
                continue
            mid = (c[0] + c[1]) / 2
            opacity = max(min_op, base - fade_rate * np.linalg.norm(mid - O[:2]))
            g.add(Line([*c[0], 0], [*c[1], 0], color=color, stroke_width=width, stroke_opacity=opacity))
    return g


def fade_ray(O, U, direction, color, width, op0, length, neg_scale=0.3):
    """محور قطري طالع من الأصل في الاتجاهين، بيخفت مع البعد. الاتجاه السالب (ناحية تحت) أقصر بنسبة neg_scale."""
    g = VGroup()
    for sign in (1.0, -1.0):
        c = clip_line(O[:2], O[:2] + sign * 45 * U * direction, GRID_BOX)
        if c is None:
            continue
        p, q = c
        L = length if sign > 0 else length * neg_scale
        n = max(4, int(np.ceil(np.linalg.norm(q - p) / 0.35)))
        for i in range(n):
            a = p + (q - p) * i / n
            b = p + (q - p) * (i + 1) / n
            d = np.linalg.norm((a + b) / 2 - O[:2])
            op = op0 * max(0.0, 1 - d / L) ** 1.4
            if op < 0.01:
                continue
            g.add(Line([*a, 0], [*b, 0], color=color, stroke_width=width, stroke_opacity=op))
    return g


def stack(start, d, n, color, width=5.5):
    """رصّة n متجه أساس ورا بعض بتحديد واضح."""
    g = VGroup()
    for i in range(n):
        g.add(Arrow(start + i * d, start + (i + 1) * d, buff=0, stroke_width=width, color=color,
                    max_tip_length_to_length_ratio=0.38, max_stroke_width_to_length_ratio=12))
    return g


def build_basis_change(scene, ltr, line1, line2, badge_text, line1_width, line2_width, badge_width=3.5):
    scene.camera.background_color = THUMB_BG
    U, O, s = basis_geometry(ltr)
    fs = min(s, 1.2)  # تكبير الخطوط أقل من تكبير الرسمة عشان ما تبقاش ضخمة
    P = lambda vec: np.array([O[0] + U * vec[0], O[1] + U * vec[1], 0.0])
    Q = lambda dx, dy: O + s * np.array([dx, dy, 0.0])  # إزاحة بالوحدة الأصلية ×s

    # ---------------- 1. الخلفية والتوهج
    tip = P(V_STD)
    warm = vignette_bg(center=(2.5 if ltr else -2.5, -0.5, 0))
    hot = soft_glow(tip * 0.55 + O * 0.45, 4.0, GOLD, layers=22, peak=0.060)

    # ---------------- 2. الشبكتان (بالعرض الكامل) + المحاور القطرية للأساس الجديد
    std_lat = lattice(O, U, E1, E2, STONE_AXIS, width=1.4, base=0.45, fade_rate=0.035, min_op=0.08)
    new_lat = lattice(O, U, F1, F2, TEAL, width=1.4, base=0.38, fade_rate=0.030, min_op=0.06)
    new_axes = VGroup(*[fade_ray(O, U, f, TEAL, 2.4, 0.65, AXIS_FADE_LEN) for f in (F1, F2)])

    # ---------------- 3. المحاور الأصلية المضيئة (سهم في الطرفين)
    axes = VGroup(
        _axis_arrow(O + np.array([-EXT["left"], 0, 0]), O + np.array([4 * U + EXT["right"], 0, 0])),
        _axis_arrow(O + np.array([0, -EXT["bottom"], 0]), O + np.array([0, 5 * U + EXT["top"], 0])),
    )

    # ---------------- 4. رصّ متجهات الأساس
    sw = 5.5 * fs
    e_stack = VGroup(
        stack(O, U * np.array([E1[0], E1[1], 0.0]), V_STD[0], GOLD, width=sw),
        stack(P((V_STD[0], 0)), U * np.array([E2[0], E2[1], 0.0]), V_STD[1], COPPER_TERRA, width=sw),
    )
    f_stack = VGroup(
        stack(O, U * np.array([F1[0], F1[1], 0.0]), V_NEW[0], TEAL, width=sw),
        stack(P(V_NEW[0] * F1), U * np.array([F2[0], F2[1], 0.0]), V_NEW[1], F2_COL, width=sw + 0.5),
    )

    # ---------------- 5. المتجه البطل v والتسميات
    v_glow = soft_glow(tip, 2.4, GOLD_BRIGHT, layers=16, peak=0.08)
    hero_arrow = glow_arrow(O, tip, GOLD_BRIGHT, 12 * fs, GOLD)
    v_label = MathTex(r"\vec{v}", tex_template=mach_math_template, font_size=100 * fs, color=GOLD_BRIGHT)
    v_label.next_to(tip, LEFT + UP * 0.15, buff=0.12)
    stroked(v_label)

    def tag(tex, color, pos, size=48):
        m = MathTex(tex, tex_template=mach_math_template, font_size=size * fs, color=color)
        m.move_to(pos)
        return stroked(m, width=8)

    t_e1 = tag(r"3\,\mathbf{e}_1", GOLD, Q(0.90, -0.47))
    t_e2 = tag(r"5\,\mathbf{e}_2", COPPER_TERRA, Q(2.45, 1.00))
    t_f1 = tag(r"4\,\mathbf{f}_1", TEAL, Q(1.15, 0.60))
    t_f2 = tag(r"1\,\mathbf{f}_2", F2_COL, P(V_NEW[0] * F1) + s * np.array([0.25, 0.55, 0]), size=52)

    hero = layer([v_glow, e_stack, f_stack, hero_arrow, glow_dot(O), v_label, t_e1, t_e2, t_f1, t_f2], 12)

    # ---------------- 6. العنوان والبادج
    title = title_block(
        line1, line2, badge_text,
        ltr=ltr, margin=MARGIN,
        line1_width=line1_width, line2_width=line2_width, badge_width=badge_width,
        line2_y=0.82 if ltr else 0.55, badge_gap=0.24,
        ltr_offsets=(1.05, -0.75),
    )
    # title_block بينزّل الكتلة بس لو الـ badge عدّى الحد؛ لو فيه فراغ زيادة فوق ما بيرفعهاش.
    # هنا نثبّت حافة الـ badge العليا بالظبط على MARGIN من الإطار (الكتلة كلها تتحرك كوحدة).
    title.shift(UP * ((FRAME_TOP - MARGIN) - title[3].get_top()[1]))
    brand = brand_mark_at(UR if ltr else UL)

    # ---------------- 7. كتلة المعادلات تحت العنوان
    # 1) الصيغة العامة للمتجه (3 حدود بدل 4: بتبان أكبر في نفس العرض)
    formula = MathTex(
        r"\mathbf{v}", r"=", r"v_1 \, \mathbf{e}_1", r"+", r"\cdots", r"+", r"v_n \, \mathbf{e}_n",
        tex_template=mach_math_template, font_size=70, color=IVORY_WHITE,
    )
    # أكبر قدر ممكن من العرض من غير ما يلمس تسميات الرسمة: RTL حد الشمال = يمين تسمية 5e2 + 0.45، LTR حد اليمين ثابت
    if ltr:
        formula_w = min(FORMULA_W, 1.3 - (-FRAME_FX + MARGIN))
    else:
        formula_w = min(FORMULA_W, (FRAME_FX - MARGIN) - (t_e2.get_right()[0] + 0.45))
    formula.set_width(formula_w)
    formula[0].set_color(GOLD_BRIGHT)
    for term_idx in (2, 6):
        formula[term_idx][0:2].set_color(GOLD_LIGHT)
        formula[term_idx][2:].set_color(COPPER_TERRA)
    stroked(formula, width=4.0)

    # 2) التعبير عن المتجه في الأساسين e و f (القائمتين)
    r_v = MathTex(r"\mathbf{v}=", tex_template=mach_math_template, font_size=74, color=GOLD_BRIGHT)

    def basis_matrix(top, bottom, label, color):
        """مصفوفة عمودية + رمز الأساس (e أو f) كبير وبولد جنب أسفلها بدل أس سفلي صغير."""
        m = MathTex(rf"\begin{{bmatrix}}{top}\\[3pt]{bottom}\end{{bmatrix}}",
                    tex_template=mach_math_template, font_size=74, color=color)
        t = MathTex(rf"\mathbf{{{label}}}", tex_template=mach_math_template, font_size=BASIS_TAG_SIZE, color=color)
        t.move_to(m.get_corner(DR) + np.array([t.width / 2 + 0.06, t.height / 2 - 0.04, 0]))
        return VGroup(m, t)

    r_a = basis_matrix(3, 5, "e", GOLD_LIGHT)
    r_eq = MathTex(r"=", tex_template=mach_math_template, font_size=74, color=IVORY_WHITE)
    r_b = basis_matrix(4, 1, "f", TEAL)
    row = VGroup(r_v, r_a, r_eq, r_b).arrange(RIGHT, buff=0.24)
    if row.width > 5.6:                       # عشان ما يطلعش برا إطار القناة
        row.scale(5.6 / row.width)
    stroked(row, width=6)

    col = VGroup(formula, row).arrange(DOWN, buff=0.42)
    row.align_to(formula, LEFT if ltr else RIGHT)     # نفس الحافة بتاعة الصيغة والعنوان
    top_y = title[2].get_bottom()[1] - 0.32
    bottom_limit = -(FRAME_TOP - MARGIN)
    avail = top_y - bottom_limit
    if col.height > avail:
        col.scale(avail / col.height)
    edge = -FRAME_FX + MARGIN if ltr else FRAME_FX - MARGIN   # الكتلة على بعد MARGIN من الإطار من ناحية العنوان
    col.align_to(np.array([edge, 0.0, 0.0]), LEFT if ltr else RIGHT)
    col.shift(UP * ((top_y + bottom_limit) / 2 - col.get_center()[1]))
    col.set_z_index(30)

    scene.add(warm, hot, std_lat, new_lat, new_axes, axes, channel_frame().set_z_index(25),
              hero, title, brand, col)