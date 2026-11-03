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
from episode_04_common import _ar, _tex, _Cap


# الحلقة 04 — المشهد 5: خصائص مثال الطيارة ← متجهات الأساس e1..e4

def play_scene05(scene):
    # 06:33.0 - 06:39.5 | "أنا في مثال الطيارة اخترت إني أصف حركتها باستخدام 4 خصائص اللي هما..."
    title = _ar("مثال الطيارة: 4 خصائص بتصف الحركة", 28, GOLD_LIGHT, True).move_to([0, 3.1, 0])
    scene.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.8)
    scene.wait(5.7)

    ys = [1.7, 0.5, -0.7, -1.9]
    props = ["المسافة في اتجاه الشرق", "المسافة في اتجاه الشمال", "ارتفاع الطيارة", "الوقت أثناء الحركة"]
    units = ["وحدة قياس: المتر", "وحدة قياس: المتر", "وحدة قياس: المتر", "وحدة قياس: الثانية"]
    syms = [r"\mathbf{e}_1", r"\mathbf{e}_2", r"\mathbf{e}_3", r"\mathbf{e}_4"]
    descs = ["متجه الأساس: المتر شرقًا", "متجه الأساس: المتر شمالًا", "متجه الأساس: المتر لفوق", "متجه الأساس: الثانية"]

    # --- أ) الخصائص تظهر تباعاً بالكلمة ---
    rows = []
    for i, (p, y) in enumerate(zip(props, ys)):
        num = _tex(str(i + 1), 34, GOLD_MUTED).move_to([5.9, y, 0])
        box = RoundedRectangle(corner_radius=0.16, width=4.1, height=0.82, stroke_color=GOLD_LIGHT,
                               stroke_width=1.8, fill_color="#14100A", fill_opacity=0.9).move_to([3.5, y, 0])
        txt = _ar(p, 21, IVORY_WHITE, True).move_to(box)
        rows.append(VGroup(num, box, txt))

    # أوقات الانتظار مضبوطة بالكلمة لكل خاصية:
    # 1- مسافة الشرق (06:39.5) | 2- مسافة الشمال (06:43.5) | 3- الارتفاع (06:49.0) | 4- الوقت (06:52.5 إلى 06:56.5)
    row_waits = [3.2, 4.7, 2.7, 3.2]
    for r, w in zip(rows, row_waits):
        scene.play(FadeIn(r, shift=LEFT * 0.3), run_time=0.8)
        scene.wait(w)

    # --- ب) وحدات القياس (متجهات الأساس بشكل غير مباشر) ---
    unit_boxes = []
    arrows = []
    for y, u, d in zip(ys, units, descs):
        ar = Arrow([1.3, y, 0], [0.4, y, 0], buff=0, color=GOLD_MUTED, stroke_width=3,
                   max_tip_length_to_length_ratio=0.45)
        box = RoundedRectangle(corner_radius=0.16, width=3.2, height=0.82, stroke_color=COPPER_TERRA,
                               stroke_width=1.8, fill_color="#14100A", fill_opacity=0.9).move_to([-1.4, y, 0])
        txt = _ar(u, 19, COPPER_TERRA, True).move_to(box)
        unit_boxes.append(VGroup(box, txt))
        arrows.append(ar)

    # 06:56.5 - 06:58.7 | "وبشكل غير مباشر حددت لكل خاصية من الخصائص الأربعة دول متجه أساس منفصل بيعبر عن وحدة قياسها..."
    note = _ar("متجه أساس لكل خاصية — بتعبّر عن وحدة قياسها", 22, COPPER_TERRA, True).move_to([0, -3.15, 0])
    scene.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(u, shift=LEFT * 0.2))
                             for a, u in zip(arrows, unit_boxes)], lag_ratio=0.3), FadeIn(note), run_time=2.2)

    # 06:58.7 - 07:43.5 | شرح تفصيلي لوحدات القياس (المتر شرقاً وشمالاً وللارتفاع، والثانية للزمن، ولماذا لم نصرح بها سابقاً)
    scene.wait(44.8)

    # --- ج) نديلها رموز ---
    sym_objs = []
    for y, s in zip(ys, syms):
        e = _tex(s, 50, COPPER_TERRA).move_to([-5.0, y, 0])
        sym_objs.append(e)
    arrows2 = [Arrow([-3.15, y, 0], [-4.2, y, 0], buff=0, color=GOLD_MUTED, stroke_width=3,
                     max_tip_length_to_length_ratio=0.45) for y in ys]

    # 07:43.5 - 07:46.0 | "وخليني هنا بالمرة أدي رمز لكل متجه أساس فيهم، عشان زي ما قلتلك أنا ما يفرقش معايا في الحسابات هما بيعبروا عن إيه بالظبط..."
    note2 = _ar("ومن غير ما نهتم بيعبّروا عن إيه — بنديهم رموز مجردة", 22, COPPER_TERRA, True).move_to([0, -3.15, 0])
    scene.play(ReplacementTransform(note, note2),
               LaggedStart(*[AnimationGroup(GrowArrow(a), Write(e)) for a, e in zip(arrows2, sym_objs)],
                           lag_ratio=0.35), run_time=2.5)

    # 07:46.0 - 07:52.8 | استقرار الرموز (e1, e2, e3, e4) مع ختام الجملة
    scene.wait(6.8)

    # 07:52.8 - 07:54.0 | تفريغ الشاشة استعداداً للمشهد السادس
    scene.play(FadeOut(VGroup(title, note2, *rows, *unit_boxes, *arrows, *arrows2, *sym_objs)), run_time=1.0)
    scene.wait(0.2)


class Dev(ThreeDScene):
    def construct(self):
        play_scene05(self)