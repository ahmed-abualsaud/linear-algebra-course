from manim import *
import numpy as np

from common.palette import (
    GOLD_BRIGHT, GOLD_LIGHT, GOLD, GOLD_MUTED,
    STONE_AXIS, STONE_DASH, COPPER_TERRA, IVORY_WHITE,
)
from common.latex import mach_math_template
from common.thumbnails import *

# ---------------- إعدادات سريعة ----------------
TITLE_LINE1 = "ما هو"
TITLE_LINE2 = "المتجه؟"
BADGE_TEXT = "الجبر الخطي • الحلقة 02"

# إنزال نقطة الأصل للأسفل للاستفادة من المساحة المحررة
O = np.array([-1.55, -2.65, 0.0])
# سهم البطل: طويل ومهيب وفي مساحة حرة ومفتوحة بالكامل
HERO = O + np.array([6 * 0.8, 2 * 0.8, 0.0])  # على تقاطع خطوط الشبكة


def _round_joints(mob):
    for sm in mob.family_members_with_points():
        sm.joint_type = LineJointType.ROUND
    return mob


def solid_text(text, width, color_a=IVORY_WHITE, color_b=GOLD_BRIGHT, glow=GOLD_LIGHT,
               stroke_w=0.7, outline_w=2.4, halo_w=(9, 4)):
    """نص عربي عريض بحدود خفيفة متناسبة مع العرض عشان الحروف ما تلزقش في بعض."""
    main = MarkupText(f"<b>{text}</b>", font=THUMB_FONT, font_size=96)
    if len(main.family_members_with_points()) == 0:
        main = Text(text, font=THUMB_FONT, font_size=96, weight=BOLD)
    main.set(width=width)
    main.set_color_by_gradient(color_a, color_b)
    for sm in main.family_members_with_points():
        sm.set_stroke(sm.get_fill_color(), width=stroke_w, opacity=1)
    _round_joints(main)
    outline = _round_joints(main.copy().set_fill(opacity=0).set_stroke(THUMB_BG, width=outline_w, opacity=0.9))
    halo = VGroup(
        main.copy().set_fill(opacity=0).set_stroke(glow, width=halo_w[0], opacity=0.07),
        main.copy().set_fill(opacity=0).set_stroke(glow, width=halo_w[1], opacity=0.11),
    )
    _round_joints(halo)
    return VGroup(halo, outline, main)


class Episode02Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = THUMB_BG

        # خلفية
        warm = vignette_bg()
        hot = soft_glow(HERO * 0.55 + O * 0.45, 2.6, GOLD, layers=18, peak=0.040)

        # شبكة + محاور (محور الصادات يبدأ من -1 فقط أسفل نقطة الأصل)
        step = 0.8
        gx0, gx1 = -3.3, 6.5
        gy0, gy1 = -3.55, 1.55  # يبدأ من -1 أسفل الأصل وينتهي بأمان

        # شبكة رئيسية: خطوط متصلة تتلاشى تدريجيًا بعيدًا عن الأصل (زي الحلقة 01)
        grid = VGroup()
        for k in range(-5, 12):
            x = O[0] + k * step
            if k and gx0 <= x <= gx1:
                d = abs(k) * step
                grid.add(Line([x, gy0, 0], [x, gy1, 0], color=STONE_AXIS, stroke_width=1.5,
                              stroke_opacity=max(0.12, 0.52 - 0.045 * d)))
        for k in range(-2, 7):
            y = O[1] + k * step
            if k and gy0 <= y <= gy1:
                d = abs(k) * step
                grid.add(Line([gx0, y, 0], [gx1, y, 0], color=STONE_AXIS, stroke_width=1.5,
                              stroke_opacity=max(0.12, 0.52 - 0.045 * d)))
        # شبكة فرعية خافتة (منتصف الخطوات)
        sub = VGroup()
        for k in range(-5, 12):
            x = O[0] + (k + 0.5) * step
            if gx0 <= x <= gx1:
                sub.add(DashedLine([x, gy0, 0], [x, gy1, 0], dash_length=0.08, color=STONE_DASH,
                                   stroke_width=0.9, stroke_opacity=0.14))
        for k in range(-2, 7):
            y = O[1] + (k + 0.5) * step
            if gy0 <= y <= gy1:
                sub.add(DashedLine([gx0, y, 0], [gx1, y, 0], dash_length=0.08, color=STONE_DASH,
                                   stroke_width=0.9, stroke_opacity=0.14))

        axis_x = Line([gx0, O[1], 0], [6.45, O[1], 0], color=GOLD_LIGHT, stroke_width=3.0, stroke_opacity=0.9)
        axis_y = Line([O[0], gy0, 0], [O[0], gy1 + 0.05, 0], color=GOLD_LIGHT, stroke_width=3.0, stroke_opacity=0.9)
        tips = VGroup(
            Triangle(fill_color=GOLD_LIGHT, fill_opacity=0.95, stroke_width=0).scale(0.13).rotate(-PI / 2).move_to([6.5, O[1], 0]),
            Triangle(fill_color=GOLD_LIGHT, fill_opacity=0.95, stroke_width=0).scale(0.13).move_to([O[0], gy1 + 0.10, 0]),
        )
        ticks = VGroup()
        for k in range(-2, 8):
            p = np.array([O[0] + k * step, O[1], 0])
            if k and gx0 + 0.1 <= p[0] <= 6.3:
                ticks.add(Line(p + UP * 0.07, p + DOWN * 0.07, color=GOLD_LIGHT, stroke_width=1.8, stroke_opacity=0.8))
        # تدريج الصادات يبدأ من -1 فقط أسفل الصفر
        for k in range(-1, 6):
            p = np.array([O[0], O[1] + k * step, 0])
            if k and gy0 + 0.05 <= p[1] <= gy1:
                ticks.add(Line(p + LEFT * 0.07, p + RIGHT * 0.07, color=GOLD_LIGHT, stroke_width=1.8, stroke_opacity=0.8))

        self.add(warm, hot, sub, grid, axis_x, axis_y, tips, ticks, channel_frame())

        # متجهات مرافقة (موزعة بأمان داخل الإطار وبعيداً عن العناوين)
        ghosts = layer([
            Arrow(O, O + np.array([5.6, -0.75, 0]), buff=0, stroke_width=4, color=STONE_AXIS,
                  stroke_opacity=0.55, max_tip_length_to_length_ratio=0.14),
            Arrow(O, O + np.array([0.50, 2.50, 0]), buff=0, stroke_width=4, color=COPPER_TERRA,
                  stroke_opacity=0.60, max_tip_length_to_length_ratio=0.14),
            Arrow(O, O + np.array([6.8, 0.45, 0]), buff=0, stroke_width=3, color=GOLD_MUTED,
                  stroke_opacity=0.75, max_tip_length_to_length_ratio=0.10),
        ], 3)

        # المتجه البطل + المركّبات + الزاوية
        proj_x = DashedLine(HERO, [HERO[0], O[1], 0], dash_length=0.10, color=GOLD_LIGHT,
                            stroke_width=2.2, stroke_opacity=0.65)
        proj_y = DashedLine(HERO, [O[0], HERO[1], 0], dash_length=0.10, color=GOLD_LIGHT,
                            stroke_width=2.2, stroke_opacity=0.65)
        ang = np.arctan2(HERO[1] - O[1], HERO[0] - O[0])
        arc = Arc(radius=1.10, start_angle=0, angle=ang, arc_center=O, color=COPPER_TERRA, stroke_width=3.4)
        theta = MathTex(r"\theta", tex_template=mach_math_template, font_size=46, color=COPPER_TERRA)
        theta.move_to(O + 1.60 * np.array([np.cos(ang / 2), np.sin(ang / 2), 0]))

        # رمز المتجه بجوار رأس السهم بأريحية كاملة
        hero_label = MathTex(r"\vec{v}", tex_template=mach_math_template, font_size=96, color=GOLD_BRIGHT)
        hero_label.next_to(HERO, RIGHT + DOWN * 0.12, buff=0.10)
        stroked(hero_label)

        hero = layer([proj_x, proj_y, arc, theta, glow_arrow(O, HERO, GOLD_BRIGHT, 10, GOLD),
                      glow_dot(O), hero_label], 10)
        self.add(ghosts, hero)

        # الشخصية
        self.add(*mathematician_with_glow())

        # العنوان في مكانه القياسي الطبيعي (بنفس طريقة solid_text النظيفة بدون تلاصق)
        title = title_block("قواعد", TITLE_LINE2, BADGE_TEXT, line1_width=2.7, line2_width=5.2)

        def _pick_text_mob(m):
            if isinstance(m, VGroup) and len(m) > 1 and len(m[1].family_members_with_points()) > 0:
                return m[1]
            return m

        old_l2 = _pick_text_mob(title[2])
        new_l2 = solid_text(TITLE_LINE2, old_l2.width, GOLD_BRIGHT, GOLD, glow=GOLD,
                            stroke_w=1.5, outline_w=7, halo_w=(18, 9))
        new_l2.move_to(old_l2.get_center())
        title.submobjects[2] = new_l2

        old_l1 = _pick_text_mob(title[1])
        new_l1 = solid_text(TITLE_LINE1, old_l1.width, IVORY_WHITE, GOLD_BRIGHT, glow=GOLD_LIGHT,
                            stroke_w=0.7, outline_w=2.4, halo_w=(9, 4))
        new_l1.next_to(new_l2, UP, buff=0.34).align_to(new_l2, RIGHT)
        title.submobjects[1] = new_l1

        if title[0].get_bottom()[1] < new_l1.get_top()[1] + 0.20:
            title[0].next_to(new_l1, UP, buff=0.24).align_to(new_l1, RIGHT)

        title.set_z_index(30)
        brand = brand_mark().set_z_index(30)

        self.add(title, brand)