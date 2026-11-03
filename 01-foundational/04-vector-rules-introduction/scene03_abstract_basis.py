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
from episode_04_common import _ar, _tex, _mini_ruler, _unit_matrix


# الحلقة 04 — المشهد 3: متجهات الأساس رموز مجردة

def play_scene03(scene):

    size = 56
    Y_F = 0.95        # ارتفاع سطر الصيغة
    Y_CAP = -0.55     # ارتفاع التعليق

    # ---------- قطع الصيغة (كل قطعة لوحدها عشان نقدر نوسّع مكان e عند التبديل) ----------
    v_sym = _tex(r"\mathbf{v}", size, GOLD_BRIGHT)
    eq = _tex("=", size, IVORY_WHITE)
    comps = [_tex(f"v_{i}", size, GOLD_LIGHT) for i in (1, 2, 3)]
    plus = [_tex("+", size, IVORY_WHITE) for _ in range(2)]

    def e_sym(i):
        return _tex(rf"\mathbf{{e}}_{i}", size, COPPER_TERRA)

    def build(es_list):
        return [v_sym, eq, comps[0], es_list[0], plus[0], comps[1], es_list[1], plus[1], comps[2], es_list[2]]

    def targets(es_list):
        tmp = VGroup(*[m.copy() for m in build(es_list)]).arrange(RIGHT, buff=0.28).move_to([0, Y_F, 0])
        return [m.get_center() for m in tmp]

    cur = [e_sym(i) for i in (1, 2, 3)]
    for m, pos in zip(build(cur), targets(cur)):
        m.move_to(pos)

    def swap_to(new_es, run_time=1.0, extra=()):
        nonlocal cur
        tg = targets(new_es)
        anims = []
        for old, new, pos in zip(build(cur), build(new_es), tg):
            if old is new:
                anims.append(old.animate.move_to(pos))
            else:
                new.move_to(pos)
                anims.append(ReplacementTransform(old, new))
        scene.play(*anims, *extra, run_time=run_time)
        cur = new_es

    # ---------- 1) الصيغة + "e مش أرقام" ----------
    # 03:35.0 - 03:39.2 | "المهم، خلينا نرجع لمتجهات الأساس عشان عايز أقولك تخلي بالك إن متجهات الأساس دي مش أرقام..."
    scene.play(LaggedStart(*[Write(m) for m in build(cur)], lag_ratio=0.12), run_time=2.2)
    scene.wait(2.0)

    # 03:39.2 - 03:41.2 | وميض متجهات الأساس e
    scene.play(*[Indicate(m, color=COPPER_TERRA, scale_factor=1.3) for m in cur], run_time=1.2)
    note = _ar("متجهات الأساس مش أرقام — دي رموز بتعبر عن شيء معيّن", 24, COPPER_TERRA, True).move_to([0, Y_CAP, 0])
    scene.play(FadeIn(note, shift=UP * 0.1), run_time=0.8)

    # 03:41.2 - 03:55.5 | "دي عبارة عن رموز بتعبر عن شيء معين، لأننا في الجبر الخطي مش بنشغل بالنا هي متجهات الأساس دي بتعبر عن إيه واحنا شغالين..."
    scene.wait(14.3)

    # ---------- 2) الرموز بتتبدل: مسطرة ← مسطرة ← مسطرة ← مصفوفات ← كثيرة حدود ----------
    stages = [
        ("مسطرة بالمتر", [_mini_ruler(GOLD_LIGHT, 0.2, 1.3) for _ in range(3)]),
        ("مسطرة بالسنتيمتر", [_mini_ruler(COPPER_TERRA, 0.1, 1.3) for _ in range(3)]),
        ("مسطرة بالخشبة", [_mini_ruler(IVORY_WHITE, 0.325, 1.3) for _ in range(3)]),
        ("مصفوفات", [_unit_matrix(0, 0), _unit_matrix(0, 1), _unit_matrix(1, 0)]),
        ("كثيرة حدود", [_tex("1", 48, COPPER_TERRA), _tex("x", 48, COPPER_TERRA), _tex("x^{2}", 48, COPPER_TERRA)]),
    ]

    # فترات الانتظار مضبوطة بالكلمة لكل مرحلة: متر (03:55.5) ← سم (03:58.5) ← خشبة (04:01.5) ← مصفوفة (04:04.5) ← كثيرة حدود (04:08.0 إلى 04:14.5)
    stage_waits = [2.1, 2.1, 2.1, 2.6, 5.6]

    prev_cap = note
    for (name, reps), w in zip(stages, stage_waits):
        cap = _ar(name, 24, GOLD_LIGHT, True).move_to([0, Y_CAP, 0])
        swap_to(reps, run_time=0.9, extra=(ReplacementTransform(prev_cap, cap),))
        prev_cap = cap
        scene.wait(w)

    # ---------- 3) كله ميفرقش: نرجع للرموز المجردة ----------
    # 04:14.5 - 04:30.5 | "كل ده ما يفرقش معايا في الحسابات، عشان كدة بدل ما نشغل بالنا بالمفاهيم دي كلها واحنا شغالين، بنستخدم رموز مجردة..."
    abstract = _ar("كل ده ميفرقش في الحسابات — بنستخدم رموز مجردة", 24, COPPER_TERRA, True).move_to([0, Y_CAP, 0])
    swap_to([e_sym(i) for i in (1, 2, 3)], run_time=1.1, extra=(ReplacementTransform(prev_cap, abstract),))
    scene.wait(14.9)
    formula = VGroup(*build(cur))

    # ---------- 4) عدد المركبات = عدد متجهات الأساس (مثال الطيارة) ----------
    # 04:30.5 - 04:37.6 | "برضو لو خدت بالك هنا هتلاحظ إن عدد أرقام مركبات المتجه لازم يساوي عدد متجهات الأساس..."
    scene.play(FadeOut(abstract), FadeOut(formula), run_time=0.7)
    scene.wait(4.8)

    plane = MathTex(
        r"\mathbf{v}", "=",
        "3", r"\mathbf{e}_1", "+",
        "4", r"\mathbf{e}_2", "+",
        "5", r"\mathbf{e}_3", "+",
        "10", r"\mathbf{e}_4",
        tex_template=mach_math_template, font_size=62, color=IVORY_WHITE,
    ).move_to([0, 0.5, 0])
    N_IDX, B_IDX = (2, 5, 8, 11), (3, 6, 9, 12)
    plane[0].set_color(GOLD_BRIGHT)
    for i in N_IDX:
        plane[i].set_color(GOLD_LIGHT)
    for i in B_IDX:
        plane[i].set_color(COPPER_TERRA)

    # 04:37.6 - 04:56.5 | "يعني لو عندي متجه بيصف شيء معين زي المتجه اللي بيصف حركة الطيارة... 3 متر شرق، 4 متر شمال، ارتفاع 5 متر في 10 ثواني"
    scene.play(Write(plane), run_time=1.6)
    scene.wait(18.9)

    # 04:56.5 - 05:01.5 | "فالمتجه في المثال ده هتلاحظ إنه بيتكون من 4 مركبات أو أربع أرقام اللي هما (3, 4, 5, 10)..."
    br_top = BraceBetweenPoints(plane[N_IDX[0]].get_top() + UP * 0.1 + LEFT * 0.1,
                                plane[N_IDX[-1]].get_top() + UP * 0.1 + RIGHT * 0.25,
                                direction=UP, color=GOLD_LIGHT)
    top_lbl = _ar("4 مركبات (أرقام)", 24, GOLD_LIGHT, True).next_to(br_top, UP, buff=0.18)
    scene.play(GrowFromCenter(br_top), FadeIn(top_lbl), run_time=1.0)
    scene.wait(4.0)

    # 05:01.5 - 05:06.5 | "...وكل مركبة أو رقم من دول..."
    br_bot = BraceBetweenPoints(plane[B_IDX[0]].get_bottom() + DOWN * 0.1 + LEFT * 0.1,
                                plane[B_IDX[-1]].get_bottom() + DOWN * 0.1 + RIGHT * 0.15,
                                direction=DOWN, color=COPPER_TERRA)
    bot_lbl = _ar("4 متجهات أساس", 24, COPPER_TERRA, True).next_to(br_bot, DOWN, buff=0.18)
    scene.play(GrowFromCenter(br_bot), FadeIn(bot_lbl), run_time=1.0)
    scene.wait(4.0)

    # 05:06.5 - 05:12.0 | "...ليه متجه أساس خاص بيه"
    pairs = VGroup(*[
        SurroundingRectangle(VGroup(plane[n], plane[b]), color=GOLD_BRIGHT, buff=0.12, corner_radius=0.1,
                             stroke_width=2.2)
        for n, b in zip(N_IDX, B_IDX)
    ])
    pair_lbl = _ar("وكل مركبة ليها متجه أساس خاص بيها", 24, GOLD_BRIGHT, True).move_to([0, -2.3, 0])
    scene.play(FadeOut(VGroup(top_lbl, bot_lbl, br_top, br_bot)),
               LaggedStart(*[Create(p) for p in pairs], lag_ratio=0.3), FadeIn(pair_lbl), run_time=1.8)
    scene.wait(3.7)

    # 05:12.0 - 05:13.0 | تفريغ الشاشة استعداداً للمشهد الرابع
    scene.play(FadeOut(VGroup(plane, pairs, pair_lbl)), run_time=0.9)
    scene.wait(0.1)

class Dev(ThreeDScene):
    def construct(self):
        play_scene03(self)