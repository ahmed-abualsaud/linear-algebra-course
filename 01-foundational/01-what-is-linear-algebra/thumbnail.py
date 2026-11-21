from manim import *
import numpy as np

from common.palette import (
    GOLD_BRIGHT, GOLD_LIGHT, GOLD, STONE_AXIS, STONE_DASH, COPPER_TERRA, IVORY_WHITE,
)
from common.latex import mach_math_template
from common.thumbnails import *

# ---------------- إعدادات سريعة ----------------
TITLE_LINE1 = "ما هو"
TITLE_LINE2 = "الجبر الخطي؟"
BADGE_TEXT = "الجبر الخطي • الحلقة 01"

# إنزال نقطة الأصل مربعين كاملين (1.6 وحدة لأسفل) لتفريغ مساحة تحت العنوان
O = np.array([-1.45, -2.60, 0.0])
BOX = (-3.3, 6.45, -3.7, 1.9)          # منطقة الشبكة
E1 = np.array([1.05, 0.30])            # صورة î بعد التحويل
E2 = np.array([-0.38, 0.92])           # صورة ĵ بعد التحويل


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


class Episode01Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = THUMB_BG

        warm = vignette_bg()
        hot = soft_glow(O + np.array([2.2, 1.0, 0]), 2.8, GOLD, layers=18, peak=0.040)

        P = lambda i, j: O[:2] + i * E1 + j * E2

        # الشبكة الأصلية (خافتة) والشبكة بعد التحويل (مضيئة)
        orig = VGroup()
        for k in range(-4, 9):
            for a, b in (((k * 0.8, -9), (k * 0.8, 9)), ((-9, k * 0.8), (9, k * 0.8))):
                c = clip_line(O[:2] + a, O[:2] + b, BOX)
                if c:
                    orig.add(DashedLine([*c[0], 0], [*c[1], 0], dash_length=0.08, color=STONE_DASH,
                                        stroke_width=0.9, stroke_opacity=0.16))
        warped = VGroup()
        for k in range(-9, 10):
            for a, b in ((P(k, -12), P(k, 12)), (P(-12, k), P(12, k))):
                c = clip_line(a, b, BOX)
                if c:
                    d = np.linalg.norm((c[0] + c[1]) / 2 - O[:2])
                    main = (k == 0)
                    warped.add(Line([*c[0], 0], [*c[1], 0], color=GOLD_LIGHT if main else STONE_AXIS,
                                    stroke_width=2.6 if main else 1.5,
                                    stroke_opacity=0.85 if main else max(0.10, 0.50 - 0.045 * d)))

        # ==============================================================
        # تجسيد الـ Determinant: مساحة متوازي الأضلاع الناتج عن تحويل î و ĵ
        # ==============================================================
        cell_coords = [[*P(i, j), 0] for i, j in ((0, 0), (1.5, 0), (1.5, 1.5), (0, 1.5))]

        cell_bg = Polygon(
            *cell_coords,
            stroke_width=0,
            fill_color=GOLD,
            fill_opacity=0.28,
        )
        cell_border = Polygon(
            *cell_coords,
            stroke_color=GOLD_LIGHT,
            stroke_width=2.0,
            stroke_opacity=0.85,
        )
        # وسم المحدد داخل المساحة الهندسية
        det_pos = (np.array(cell_coords[0]) + np.array(cell_coords[2])) / 2
        det_tag = MathTex(r"\det(A)", tex_template=mach_math_template, font_size=32, color=GOLD_BRIGHT)
        det_tag.move_to(det_pos)
        stroked(det_tag, width=6)

        det_visual = VGroup(cell_bg, cell_border, det_tag)

        # ==============================================================
        # متجها الأساس بعد التحويل (î و ĵ)
        # ==============================================================
        t1, t2 = P(2.6, 0), P(0, 2.6)
        l1 = MathTex(r"\hat{\imath}", tex_template=mach_math_template, font_size=82, color=GOLD_BRIGHT)
        l2 = MathTex(r"\hat{\jmath}", tex_template=mach_math_template, font_size=82, color=COPPER_TERRA)

        # مواضع الرموز بأمان ووضوح
        l1.next_to([*t1, 0], DOWN + RIGHT * 0.15, buff=0.10)
        l2.next_to([*t2, 0], UP + LEFT * 0.25, buff=0.08)
        stroked(l1); stroked(l2)

        # ==============================================================
        # كتلة الجبر: المصفوفة + قانون حساب المحدد
        # ==============================================================
        mat = MathTex(
            r"A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}",
            tex_template=mach_math_template,
            font_size=64,
            color=IVORY_WHITE,
        )
        mat[0][:2].set_color(GOLD_LIGHT)
        stroked(mat)

        det_formula = MathTex(
            r"\det(A) = ad - bc",
            tex_template=mach_math_template,
            font_size=36,
            color=GOLD_BRIGHT,
        )
        stroked(det_formula)

        math_block = VGroup(mat, det_formula).arrange(DOWN, buff=0.22).move_to([TITLE_CX + 0.6, -2.40, 0])

        # تجميع عناصر المشهد
        self.add(warm, hot, orig, warped, det_visual, channel_frame())
        self.add(layer([
            glow_arrow(O, [*t1, 0], GOLD_BRIGHT, 9),
            glow_arrow(O, [*t2, 0], COPPER_TERRA, 9),
            glow_dot(O),
            l1, l2,
            math_block,
        ], 10))

        # الشخصية + العنوان (بتنسيق solid_text النظيف)
        self.add(*mathematician_with_glow())
        title = title_block("قواعد", TITLE_LINE2, BADGE_TEXT, line1_width=2.7, line2_width=5.5)

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
        self.add(title, brand_mark().set_z_index(30))