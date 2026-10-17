from manim import *
import numpy as np

from common.palette import (
    GOLD_BRIGHT, GOLD_LIGHT, GOLD, GOLD_MUTED,
    STONE_AXIS, STONE_DASH, COPPER_TERRA,
)
from common.latex import mach_math_template
from common.thumbnails import *

# ---------------- إعدادات سريعة ----------------
TITLE_LINE1 = "إيه هو"
TITLE_LINE2 = "المتجه؟"
BADGE_TEXT = "الجبر الخطي • الحلقة 02"

O = np.array([-1.55, -2.15, 0.0])
HERO = O + np.array([4.45, 1.6, 0.0])


class Episode02Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = THUMB_BG

        # خلفية
        warm = vignette_bg()
        hot = soft_glow(HERO * 0.55 + O * 0.45, 2.6, GOLD, layers=18, peak=0.040)

        # شبكة + محاور
        step = 0.8
        gx0, gx1, gy0, gy1 = -3.3, 6.5, -3.7, 1.9
        grid = VGroup()
        for k in range(-5, 12):
            x = O[0] + k * step
            if k and gx0 <= x <= gx1:
                grid.add(DashedLine([x, gy0, 0], [x, gy1, 0], dash_length=0.09, dashed_ratio=0.5))
        for k in range(-6, 6):
            y = O[1] + k * step
            if k and gy0 <= y <= gy1:
                grid.add(DashedLine([gx0, y, 0], [gx1, y, 0], dash_length=0.09, dashed_ratio=0.5))
        for ln in grid:
            d = np.linalg.norm((ln.get_center() - O) * np.array([0.8, 1.0, 0]))
            ln.set_stroke(STONE_DASH, width=1.0, opacity=max(0.04, 0.20 - 0.022 * d))

        axis_x = Line([gx0, O[1], 0], [6.45, O[1], 0], color=STONE_AXIS, stroke_width=2.4, stroke_opacity=0.8)
        axis_y = Line([O[0], gy0, 0], [O[0], 1.95, 0], color=STONE_AXIS, stroke_width=2.4, stroke_opacity=0.8)
        tips = VGroup(
            Triangle(fill_color=STONE_AXIS, fill_opacity=0.9, stroke_width=0).scale(0.13).rotate(-PI / 2).move_to([6.5, O[1], 0]),
            Triangle(fill_color=STONE_AXIS, fill_opacity=0.9, stroke_width=0).scale(0.13).move_to([O[0], 2.0, 0]),
        )
        ticks = VGroup()
        for k in range(-2, 8):
            p = np.array([O[0] + k * step, O[1], 0])
            if k and gx0 + 0.1 <= p[0] <= 6.3:
                ticks.add(Line(p + UP * 0.07, p + DOWN * 0.07, color=STONE_AXIS, stroke_width=1.6, stroke_opacity=0.7))
        for k in range(-2, 6):
            p = np.array([O[0], O[1] + k * step, 0])
            if k and gy0 + 0.1 <= p[1] <= 1.9:
                ticks.add(Line(p + LEFT * 0.07, p + RIGHT * 0.07, color=STONE_AXIS, stroke_width=1.6, stroke_opacity=0.7))

        self.add(warm, hot, grid, axis_x, axis_y, tips, ticks, channel_frame())

        # متجهات مرافقة
        ghosts = layer([
            Arrow(O, O + np.array([5.6, -1.15, 0]), buff=0, stroke_width=4, color=STONE_AXIS,
                  stroke_opacity=0.55, max_tip_length_to_length_ratio=0.14),
            Arrow(O, O + np.array([0.9, 3.35, 0]), buff=0, stroke_width=4, color=COPPER_TERRA,
                  stroke_opacity=0.60, max_tip_length_to_length_ratio=0.14),
            Arrow(O, O + np.array([7.0, 0.55, 0]), buff=0, stroke_width=3, color=GOLD_MUTED,
                  stroke_opacity=0.75, max_tip_length_to_length_ratio=0.10),
        ], 3)

        # المتجه البطل + المركّبات + الزاوية
        proj_x = DashedLine(HERO, [HERO[0], O[1], 0], dash_length=0.10, color=GOLD_LIGHT,
                            stroke_width=2.2, stroke_opacity=0.65)
        proj_y = DashedLine(HERO, [O[0], HERO[1], 0], dash_length=0.10, color=GOLD_LIGHT,
                            stroke_width=2.2, stroke_opacity=0.65)
        ang = np.arctan2(HERO[1] - O[1], HERO[0] - O[0])
        arc = Arc(radius=1.05, start_angle=0, angle=ang, arc_center=O, color=COPPER_TERRA, stroke_width=3.4)
        theta = MathTex(r"\theta", tex_template=mach_math_template, font_size=46, color=COPPER_TERRA)
        theta.move_to(O + 1.55 * np.array([np.cos(ang / 2), np.sin(ang / 2), 0]))
        hero_label = MathTex(r"\vec{v}", tex_template=mach_math_template, font_size=104, color=GOLD_BRIGHT)
        hero_label.next_to(HERO, RIGHT + DOWN * 0.15, buff=0.08)
        stroked(hero_label)

        hero = layer([proj_x, proj_y, arc, theta, glow_arrow(O, HERO, GOLD_BRIGHT, 10, GOLD),
                      glow_dot(O), hero_label], 10)
        self.add(ghosts, hero)

        # الشخصية + العنوان
        self.add(*mathematician_with_glow())
        title = title_block(TITLE_LINE1, TITLE_LINE2, BADGE_TEXT, line2_width=5.2)
        title.set_z_index(30)
        brand = brand_mark().set_z_index(30)
        self.add(title, brand)