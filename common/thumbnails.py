"""
أدوات مشتركة لكل thumbnails قناة MACH-MATH.
الاستخدام:  from common.thumbnails import *
"""
from manim import *
import numpy as np

from common.palette import (
    GOLD_BRIGHT, GOLD_LIGHT, GOLD, GOLD_DARK, GOLD_MUTED,
    STONE_AXIS, STONE_DASH, COPPER_TERRA, IVORY_WHITE,
)
from common.mobjects.characters import mach_mathematician

THUMB_BG = "#070503"
THUMB_FONT = "Cairo"

# موضع/حجم الشخصية الافتراضي
CHAR_SCALE = 1.75
CHAR_POS = np.array([-4.9, -0.85, 0.0])
# عمود العنوان
TITLE_CX = 3.5
FRAME_TOP = 3.78   # ارتفاع إطار القناة (fy في channel_frame)


# ---------------------------------------------------------------- أساسيات
def soft_glow(center, radius, color, layers=22, peak=0.05, power=2.0):
    """هالة ناعمة بلا حواف: طبقات دوائر متراكبة (الأوسع الأخفت)."""
    g = VGroup()
    for i in range(layers):
        t = i / (layers - 1)
        r = radius * (1 - t * 0.92)
        op = peak * (0.25 + 0.75 * t ** power) / layers * 6
        g.add(Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=op).move_to(center))
    return g


def fit_width(mob, width):
    mob.set(width=width)
    return mob


def glowing_text(text, width, color_a=GOLD_BRIGHT, color_b=GOLD, outline=THUMB_BG,
                 weight=BOLD, glow=GOLD, font=THUMB_FONT):
    """نص عريض بتدرج لوني + إطار داكن للتباين + توهج خارجي ناعم."""
    main = Text(text, font=font, weight=weight)
    fit_width(main, width)
    main.set_color_by_gradient(color_a, color_b)
    main.set_stroke(outline, width=12, background=True)
    halo = VGroup(
        main.copy().set_stroke(glow, width=34, opacity=0.07, background=True).set_fill(opacity=0),
        main.copy().set_stroke(glow, width=20, opacity=0.10, background=True).set_fill(opacity=0),
    )
    return VGroup(halo, main)


def glow_dot(point, scale=1.0):
    """نقطة أصل متوهجة."""
    return VGroup(
        Dot(point, radius=0.30 * scale, color=GOLD).set_opacity(0.14),
        Dot(point, radius=0.17 * scale, color=GOLD_LIGHT).set_opacity(0.35),
        Dot(point, radius=0.09 * scale, color=GOLD_BRIGHT),
    )


def glow_arrow(start, end, color=GOLD_BRIGHT, width=10, glow_color=None, tip_ratio=0.21):
    """سهم بطل: طبقتا توهج + الجسم."""
    glow_color = glow_color or color
    g = VGroup()
    for k, op in ((3.4, 0.06), (2.2, 0.10), (1.3, 0.18)):
        g.add(Arrow(start, end, buff=0, stroke_width=width * k, color=glow_color,
                    stroke_opacity=op, max_tip_length_to_length_ratio=tip_ratio + 0.03))
    g.add(Arrow(start, end, buff=0, stroke_width=width, color=color,
                max_tip_length_to_length_ratio=tip_ratio))
    return g


def stroked(mob, width=10, color=THUMB_BG):
    """إطار داكن خلف الرموز الرياضية لرفع التباين."""
    return mob.set_stroke(color, width=width, background=True)


# ---------------------------------------------------------------- مكونات الـ thumbnail
def vignette_bg(center=(0.9, -0.6, 0), radius=6.4, color=GOLD_DARK, peak=0.060):
    return soft_glow(np.array(center, dtype=float), radius, color, layers=26, peak=peak)


def channel_frame(fx=6.85, fy=3.78, arm=0.55):
    """إطار القناة: أقواس ذهبية في الأركان + مستطيل رفيع."""
    frame = VGroup()
    for sx, sy in ((-1, 1), (1, 1), (1, -1), (-1, -1)):
        c = np.array([sx * fx, sy * fy, 0])
        frame.add(
            Line(c, c + np.array([-sx * arm, 0, 0]), color=GOLD_LIGHT, stroke_width=3, stroke_opacity=0.75),
            Line(c, c + np.array([0, -sy * arm, 0]), color=GOLD_LIGHT, stroke_width=3, stroke_opacity=0.75),
        )
    rect = Rectangle(width=2 * fx, height=2 * fy, stroke_width=1,
                     stroke_color=GOLD_MUTED, stroke_opacity=0.55)
    return VGroup(rect, frame)


def brand_mark(pos=(-5.6, 3.3, 0), width=2.1):
    brand = Text("MACH-MATH", font="Serif", weight=BOLD)
    fit_width(brand, width)
    brand.set_color_by_gradient(GOLD_BRIGHT, GOLD_LIGHT, GOLD_DARK)
    return brand.move_to(np.array(pos, dtype=float))


def series_badge(text, width=3.5, align_right_to=None, y=3.2, cx=TITLE_CX):
    txt = Text(text, font=THUMB_FONT, weight=BOLD, color=COPPER_TERRA)
    fit_width(txt, width)
    bg = RoundedRectangle(corner_radius=0.2, width=txt.width + 0.55, height=txt.height + 0.38,
                          stroke_width=2.2, stroke_color=COPPER_TERRA,
                          fill_color="#17100A", fill_opacity=0.95)
    txt.move_to(bg)
    badge = VGroup(bg, txt).move_to([cx, y, 0])
    if align_right_to is not None:
        badge.align_to(align_right_to, RIGHT)
    return badge


def title_block(line1, line2, badge_text, cx=TITLE_CX, line1_width=2.4, line2_width=5.4,
                line2_y=0.80, badge_gap=0.36, badge_margin=0.40):
    """
    كتلة العنوان الكاملة (يمين الشاشة):
    شارة + سطر صغير + سطر ذهبي عملاق + خط تحتي + خلفية داكنة ناعمة.
    ترجع VGroup بالترتيب: backing, line1, line2, underline, badge
    """
    backing = VGroup(*[
        Ellipse(width=8.6 - 2.6 * (i / 9), height=4.6 - 1.5 * (i / 9), stroke_width=0,
                fill_color=THUMB_BG, fill_opacity=0.12).move_to([cx, 1.8, 0])
        for i in range(10)
    ])
    l1 = glowing_text(line1, line1_width, IVORY_WHITE, GOLD_BRIGHT, glow=GOLD_LIGHT)
    l2 = glowing_text(line2, line2_width, GOLD_BRIGHT, GOLD)
    l2.move_to([cx, line2_y, 0])
    l1.next_to(l2, UP, buff=0.30).align_to(l2, RIGHT)
    half = line2_width / 2
    underline = VGroup(
        Line(LEFT * half, RIGHT * half, color=GOLD, stroke_width=16, stroke_opacity=0.10),
        Line(LEFT * half, RIGHT * half, color=COPPER_TERRA, stroke_width=6),
    ).next_to(l2, DOWN, buff=0.16).align_to(l2, RIGHT)
    for u in underline:
        u.set_cap_style(CapStyleType.ROUND)
    badge = series_badge(badge_text, cx=cx, align_right_to=l2)
    badge.next_to(l1, UP, buff=badge_gap).align_to(l2, RIGHT)  # مسافة ثابتة فوق "إيه هو"
    block = VGroup(backing, l1, l2, underline, badge)
    # لا تسمح للشارة بملامسة إطار القناة: لو علت عن الحد الآمن انزل بالكتلة كلها
    overflow = badge.get_top()[1] - (FRAME_TOP - badge_margin)
    if overflow > 0:
        block.shift(DOWN * overflow)
    return block


def mathematician_with_glow(pos=CHAR_POS, scale=CHAR_SCALE, pose="explaining", **kwargs):
    """شخصية القناة + هالة نحاسية خلفها. ترجع (glow, character)."""
    opts = dict(
        color=COPPER_TERRA,
        accent_color=GOLD_LIGHT,
        pose=pose,
        scale=scale,
        blink=False,
        breathing=False,
        glasses=True,
        tie_type="necktie")
    opts.update(kwargs)
    char = mach_mathematician(**opts).move_to(pos)
    glow = soft_glow(np.array(pos) + np.array([0.2, 0.2, 0]), 3.4, COPPER_TERRA, layers=14, peak=0.045)
    glow.set_z_index(15)
    char.set_z_index(20)
    return glow, char


def clip_line(p, q, box):
    """قص خط p→q داخل مستطيل box=(x0,x1,y0,y1) (Liang–Barsky). يرجع None لو خارج."""
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


def layer(mobs, z):
    """يحط مجموعة عناصر على طبقة z معينة ويرجعها."""
    g = VGroup(*mobs) if not isinstance(mobs, VGroup) else mobs
    g.set_z_index(z)
    return g