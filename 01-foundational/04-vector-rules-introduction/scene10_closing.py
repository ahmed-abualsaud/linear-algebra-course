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
from episode_04_common import _ar, _tex, _chip, _grid_lines


# الحلقة 04 — المشهد 10: الخلاصة + تشويقة قواعد الجمع

def play_scene10(scene):
    # ---------- 1) الخلاصة (16:08.0 - 16:25.5) ----------
    items = [("مركبات المتجه + متجهات الأساس", GOLD_LIGHT),
             ("نفس المتجه يتكتب بقوائم مختلفة", COPPER_TERRA),
             ("نظام الإحداثيات = سقالات جوه فضاء المتجهات", GOLD_LIGHT),
             ("القياس بنظام الإحداثيات ← أرقام المركبات", COPPER_TERRA)]
    chips = VGroup(*[_chip("✓  " + t, c, w=8.2, h=0.7, size=20) for t, c in items]).arrange(DOWN, buff=0.28)
    chips.move_to([0, 0.5, 0])
    head = _ar("اللي فهمناه في الحلقة دي", 28, GOLD_LIGHT, True).move_to([0, 3.0, 0])

    # 16:08.0 - 16:11.5 | "وبكدة نكون وصلنا لنهاية الحلقة..."
    scene.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.8)
    scene.wait(2.7)

    # 16:11.5 - 16:19.0 | "لكن قبل ما أختم عايز أقول إنك لو قدرت تستوعب كل فكرة أنا قلتها في الحلقة دي..."
    for c in chips:
        scene.play(FadeIn(c, shift=LEFT * 0.3), run_time=0.6)
        scene.wait(1.0)
    scene.wait(1.1)

    # 16:19.0 - 16:24.7 | "...فانت فعلاً بقيت جاهز عشان تدخل في اللعبة الحقيقية وتستوعب قواعد المتجهات كويس إن شاء الله"
    ready = _ar("بقيت جاهز تدخل اللعبة الحقيقية: قواعد المتجهات", 26, GOLD_BRIGHT, True).move_to([0, -2.2, 0])
    scene.play(FadeIn(ready, shift=UP * 0.1), run_time=0.8)
    scene.wait(4.9)

    # 16:24.7 - 16:25.5 | تفريغ الشاشة استعداداً للتشويقة
    scene.play(FadeOut(VGroup(head, chips, ready)), run_time=0.8)

    # ---------- 2) تشويقة: قواعد الجمع (16:25.5 - 16:52.5) ----------
    # 16:25.5 - 16:34.0 | "عشان كدة في الحلقة الجاية بإذن الله هنبدأ في شرح عملية الجمع وقواعد الجمع الخاصة بالمتجهات..."
    nxt = _ar("الحلقة الجاية: قواعد جمع المتجهات", 32, GOLD_LIGHT, True).move_to([0, 3.0, 0])
    O = np.array([-2.0, -1.8, 0.0])
    BOX = (-6.0, 6.0, -2.7, 2.4)
    grid = _grid_lines([0.6, 0, 0], [0, 0.6, 0], BOX, O, n=16, color=GOLD_LIGHT, width=1.0, opacity=0.25)
    a = np.array([2.4, 0.9, 0.0])
    b = np.array([1.2, 1.8, 0.0])
    va = Arrow(O, O + a, buff=0, color=COPPER_TERRA, stroke_width=6, max_tip_length_to_length_ratio=0.12)
    vb = Arrow(O + a, O + a + b, buff=0, color=GOLD_LIGHT, stroke_width=6, max_tip_length_to_length_ratio=0.12)
    vs = Arrow(O, O + a + b, buff=0, color=GOLD_BRIGHT, stroke_width=7, max_tip_length_to_length_ratio=0.1)
    la = _tex(r"\mathbf{a}", 34, COPPER_TERRA).next_to(va, DOWN, buff=0.12)
    lb = _tex(r"\mathbf{b}", 34, GOLD_LIGHT).next_to(vb, RIGHT, buff=0.12)
    ls = _tex(r"\mathbf{a}+\mathbf{b}", 34, GOLD_BRIGHT).move_to(O + (a + b) / 2 + [-0.75, 0.3, 0])

    scene.play(FadeIn(nxt, shift=DOWN * 0.1), FadeIn(grid), run_time=1.0)
    scene.play(GrowArrow(va), FadeIn(la), run_time=0.8)
    scene.play(GrowArrow(vb), FadeIn(lb), run_time=0.8)
    scene.play(GrowArrow(vs), FadeIn(ls), run_time=1.0)
    scene.wait(4.9)

    # 16:34.0 - 16:52.5 | "والحلقة مش هتكون مجرد عرض للقواعد، لكن هنبدأ نفهم طبيعة المتجهات وفضاء المتجهات نفسه بشكل أعمق... وإزاي كل قاعدة من دول بتتحكم في شكل فضاء المتجهات وإزاي بتتحكم في صيغة المتجه نفسه"
    note = _ar("مش مجرد عرض للقواعد — هنفهم طبيعة المتجهات وفضاء المتجهات نفسه بشكل أعمق", 24, GOLD_BRIGHT, True).move_to([0, -3.3, 0])
    scene.play(FadeIn(note, shift=UP * 0.1), run_time=0.9)
    scene.wait(17.6)

    # ---------- 3) الخاتمة والسلام (16:52.5 - 16:58.0) ----------
    # 16:52.5 - 16:56.0 | "وأشوفكم الحلقة الجاية بإذن الله..."
    bye = _ar("أشوفكم الحلقة الجاية بإذن الله", 30, IVORY_WHITE, True).move_to([0, 0.2, 0])
    scene.play(FadeOut(VGroup(nxt, grid, va, vb, vs, la, lb, ls, note)), run_time=0.8)
    scene.play(FadeIn(bye, scale=0.9), run_time=0.8)
    scene.wait(1.9)

    # 16:56.0 - 16:58.0 | "...السلام عليكم"
    scene.play(FadeOut(bye), run_time=1.2)
    scene.wait(0.8)


class Dev(ThreeDScene):
    def construct(self):
        play_scene10(self)