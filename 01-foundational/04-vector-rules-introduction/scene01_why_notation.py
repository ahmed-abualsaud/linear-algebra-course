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
from episode_04_common import _ar, _tex, _column

# الحلقة 04 — المشهد 1: ليه محتاجين صيغة لكتابة المتجه؟

def play_scene01(scene):

    # ---------- 0) بطاقة عنوان الحلقة (لملء شاشة البداية 00:00 - 00:23.6) ----------
    ep_title = _ar("تمهيد لقواعد المتجهات", 36, COPPER_TERRA, True).move_to([0, 0.85, 0])
    ep_sub = _ar("بناء لغة ومفاهيم الجبر الخطي", 21, GOLD_BRIGHT).next_to(ep_title, DOWN, buff=0.32)
    title_group = VGroup(ep_title, ep_sub)

    # 00:00 - 00:01.2 | "السلام عليكم"
    scene.wait(1.2)

    # 00:01.2 - 00:21.2 | ظهور عنوان الحلقة أثناء مقدمة وتمهيد الحلقة
    scene.play(FadeIn(title_group, shift=UP * 0.2), run_time=1.0)
    scene.wait(19.0)

    # 00:21.2 - 00:23.6 | تلاشي العنوان استعداداً للمقارنة
    scene.play(FadeOut(title_group), run_time=1.0)
    scene.wait(1.4)

    # ---------- أ) السهم ≠ المتجه ≠ القايمة ----------
    arrow = Arrow([-5.3, -0.55, 0], [-2.2, 0.85, 0], buff=0, color=GOLD_LIGHT,
                  stroke_width=7, max_tip_length_to_length_ratio=0.22)
    arrow_lbl = _ar("سهم", 22, GOLD_MUTED).next_to(arrow, DOWN, buff=0.55)

    v_core = _tex(r"\mathbf{v}", 64, GOLD_BRIGHT)
    v_ring = Circle(radius=0.78, color=GOLD_LIGHT, stroke_width=2.4)
    v_glow = Circle(radius=1.05, stroke_width=0, fill_color=GOLD_LIGHT, fill_opacity=0.07)
    v_group = VGroup(v_glow, v_ring, v_core).move_to([0, 0.15, 0])
    v_lbl = _ar("المتجه نفسه", 22, GOLD_LIGHT, True).next_to(v_ring, DOWN, buff=0.45)

    lst = _column(["3", "4", "5", "10"], 40, IVORY_WHITE).move_to([4.2, 0.15, 0])
    lst_lbl = _ar("قايمة أرقام", 22, GOLD_MUTED).next_to(lst, DOWN, buff=0.45)

    neq_l = _tex(r"\neq", 56, COPPER_TERRA).move_to([-1.65, 0.15, 0])
    neq_r = _tex(r"\neq", 56, COPPER_TERRA).move_to([1.65, 0.15, 0])

    # 00:23.6 - 00:28.0 | "لو فاكر في الحلقة اللي فاتت قلنا إن المتجه ممكن أمثله بسهم أو قايمة من الأرقام..."
    scene.play(FadeIn(arrow, shift=RIGHT * 0.2), FadeIn(arrow_lbl),
               FadeIn(lst, shift=LEFT * 0.2), FadeIn(lst_lbl), run_time=1.4)
    scene.wait(3.0)

    # 00:28.0 - 00:33.0 | "...لكن طرق التمثيل دي مش هي المتجه نفسه"
    scene.play(GrowFromCenter(v_group), FadeIn(v_lbl), run_time=1.0)
    scene.play(Write(neq_l), Write(neq_r), run_time=0.8)

    # 00:33.0 - 00:41.0 | "طيب انت هنا ممكن تقول: إذا كان المتجه مش هو القايمة ومش هو السهم..."
    scene.wait(11.2)

    # ---------- ب) السؤال: إزاي نكتبه؟ ----------
    # 00:41.0 - 00:43.0 | خروج السهم والقايمة وانتقال v للأعلى وظهور السؤال
    scene.play(*[FadeOut(m) for m in (arrow, arrow_lbl, lst, lst_lbl, neq_l, neq_r, v_lbl)],
               v_group.animate.move_to([0, 1.55, 0]).scale(0.7), run_time=1.2)

    q = _ar("إزاي نكتب المتجه رياضيًا؟", 34, GOLD_LIGHT, True).move_to([0, -0.15, 0])
    scene.play(FadeIn(q, shift=UP * 0.2), run_time=0.8)

    # 00:43.0 - 00:59.5 | "أومال احنا هنمثل المتجه رياضياً إزاي؟ ... عشان نقدر نطبق عليه القواعد دي"
    scene.wait(16.5)

    # ---------- ج) تشبيه الحساب: 3 ثم 4 بالتتابع ثم 3 + 4 ----------
    scene.play(FadeOut(q), run_time=0.5)
    scene.wait(1.0)

    # 01:01.0 - 01:03.0 | "...بتكتب التلاتة بالشكل ده 3..."
    three = _tex("3", 72, IVORY_WHITE).move_to([-2.2, -0.5, 0])
    scene.play(FadeIn(three, shift=UP * 0.2), run_time=0.7)
    scene.wait(1.5)

    # 01:03.2 - 01:05.5 | "...والأربعة بالشكل ده 4"
    four = _tex("4", 72, IVORY_WHITE).move_to([2.2, -0.5, 0])
    scene.play(FadeIn(four, shift=UP * 0.2), run_time=0.7)
    scene.wait(1.6)

    # 01:05.5 - 01:12.5 | "فلما تيجي تطبق قاعدة الجمع مثلاً على العددين دول بتكتبها بالشكل ده 3 + 4"
    sum_expr = _tex("3 + 4", 72, GOLD_BRIGHT).move_to([0, -0.5, 0])
    scene.play(ReplacementTransform(three, sum_expr[0][0:1]),
               ReplacementTransform(four, sum_expr[0][2:3]),
               FadeIn(sum_expr[0][1:2]), run_time=1.0)
    rule_lbl = _ar("قاعدة الجمع", 22, COPPER_TERRA).next_to(sum_expr, DOWN, buff=0.5)
    scene.play(FadeIn(rule_lbl, shift=UP * 0.1), run_time=0.6)
    scene.wait(5.4)

    # ---------- د) بس المتجه؟ لسه معندناش صيغة ----------
    # 01:12.5 - 01:20.0 | "فاحنا هنا المفروض نعرف إزاي هنكتب المتجه قبل ما نطبق القواعد عليه أصلاً"
    v_eq = _tex(r"\mathbf{v} = \;?", 64, COPPER_TERRA).move_to([0, -2.1, 0])
    scene.play(FadeIn(v_eq, shift=UP * 0.2), run_time=0.8)
    scene.wait(6.7)

    # 01:20.0 - 01:21.0 | تفريغ الشاشة استعداداً للمشهد الثاني
    scene.play(FadeOut(VGroup(sum_expr, rule_lbl, v_eq, v_group)), run_time=1.0)
    scene.wait(0.2)

class Dev(ThreeDScene):
    def construct(self):
        play_scene01(self)