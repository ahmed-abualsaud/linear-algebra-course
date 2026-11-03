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
from episode_04_common import _ar, _tex, _column, _ruler


# الحلقة 04 — المشهد 2: الصيغة v = v1 e1 + ... + vn en

def play_scene02(scene):

    # ---------- 1) الصيغة ----------
    formula = MathTex(
        r"\mathbf{v}", "=",
        "v_1", r"\mathbf{e}_1", "+",
        "v_2", r"\mathbf{e}_2", "+",
        "v_3", r"\mathbf{e}_3", "+",
        r"\cdots", "+",
        "v_n", r"\mathbf{e}_n",
        tex_template=mach_math_template, font_size=60, color=IVORY_WHITE,
    )
    formula.set_width(min(formula.width, 11.6))
    formula.move_to([0, 2.1, 0])
    V_IDX = (2, 5, 8, 13)    # المركبات
    E_IDX = (3, 6, 9, 14)    # متجهات الأساس
    formula[0].set_color(GOLD_BRIGHT)
    for i in V_IDX:
        formula[i].set_color(GOLD_LIGHT)
    for i in E_IDX:
        formula[i].set_color(COPPER_TERRA)

    # 01:21.0 - 01:21.5 | فاصل انتقال سريع جداً ونظيف (0.5 ثانية فقط بدلاً من الشاشة السوداء)
    scene.wait(0.5)

    # 01:21.5 - 01:25.5 | كتابة الصيغة بانسيابية أثناء: "خليني أختصر عليك الموضوع وأقولك إن الطريقة الرياضية اللي بيتكتب بيها المتجه..."
    # وتكتمل كتابتها بالضبط عند كلمة: "...بتكون كدة"
    scene.play(Write(formula), run_time=4.0)

    # 01:25.5 - 01:37.5 | استقرار الصيغة كاملة أثناء: "باستخدام الصيغة دي أقدر أكتب بيها أي متجه أنا عاوزه وبتتكون من حاجتين..."
    scene.wait(12.0)

    # ---------- 2) المركبات = القايمة = التمثيل الإحداثي ----------
    # 01:37.5 - 01:40.5 | "أول حاجة: الرموز دي (v1, v2, v3 لحد vn)..."
    scene.play(*[formula[i].animate.set_opacity(0.18) for i in E_IDX],
               *[Indicate(formula[i], color=GOLD_BRIGHT, scale_factor=1.25) for i in V_IDX],
               run_time=1.4)

    comp_lbl = _ar("مركبات المتجه = التمثيل الإحداثي", 24, GOLD_LIGHT, True).move_to([0, 0.75, 0])
    scene.play(FadeIn(comp_lbl, shift=DOWN * 0.1), run_time=0.7)

    col_sym = _column([r"v_1", r"v_2", r"v_3", r"v_n"], 44, GOLD_LIGHT).move_to([-3.6, -1.55, 0])
    scene.play(FadeIn(col_sym, shift=UP * 0.2), run_time=0.9)

    # 01:40.5 - 01:50.0 | "الرموز دي بتمثل الأرقام اللي جوة القايمة اللي كنت بتشوفها في الحلقة اللي فاتت في مثال الطيارة..."
    scene.wait(9.5)

    # 01:50.0 - 01:52.0 | "لما قلتلك إننا ممكن نمثل المتجه بقايمة من الأرقام (3, 4, 5, 10)..."
    col_num = _column(["3", "4", "5", "10"], 44, IVORY_WHITE).move_to(col_sym)
    scene.play(ReplacementTransform(col_sym, col_num), run_time=1.3)
    col_cap = _ar("قايمة الأرقام اللي في الحلقة اللي فاتت", 19, GOLD_MUTED).next_to(col_num, DOWN, buff=0.35)
    scene.play(FadeIn(col_cap), run_time=0.7)

    # 01:52.0 - 02:10.5 | "والأرقام اللي جوة القايمة دي بنسميها التمثيل الإحداثي للمتجه أو مركبات المتجه... وهنفهم مع بعض سبب التسمية ده كمان شوية"
    scene.wait(18.5)

    # ---------- 3) متجهات الأساس = وحدات القياس / المساطر ----------
    # 02:10.5 - 02:20.5 | "وتاني حاجة بتتكون منها الصيغة هي الرموز اللي جنب مركبات المتجه اللي هي دي (e1, e2, e3 لحد en)..."
    scene.play(*[formula[i].animate.set_opacity(1.0) for i in E_IDX],
               *[formula[i].animate.set_opacity(0.18) for i in V_IDX],
               FadeOut(comp_lbl), run_time=1.0)
    scene.play(*[Indicate(formula[i], color=COPPER_TERRA, scale_factor=1.25) for i in E_IDX],
               run_time=1.3)
    scene.wait(7.7)

    # 02:20.5 - 02:35.0 | "الرموز دي بنسميها متجهات الأساس، ودي بتمثل وحدات القياس أو المساطر اللي بقيس بيها المتجه... ومتجهات الأساس دي أنا شرحتلك فكرتها برضو في مثال الطيارة..."
    basis_lbl = _ar("متجهات الأساس = وحدات القياس (المساطر)", 24, COPPER_TERRA, True).move_to([0, 0.75, 0])
    scene.play(FadeIn(basis_lbl, shift=DOWN * 0.1), run_time=0.8)
    scene.wait(13.7)

    # 02:35.0 - 02:37.5 | "لما غيرت وحدات القياس بتاعة المسافة من المتر للسنتيمتر، بعدين استخدمنا وحدة قياس جديدة احنا اخترعناها وسميناها وحدة الخشبة..."
    r_m = _ruler(2.6, 0.26, GOLD_LIGHT, "متر")
    r_cm = _ruler(2.6, 0.13, COPPER_TERRA, "سنتيمتر")
    r_kh = _ruler(2.6, 0.34, IVORY_WHITE, "خشبة")
    rulers = VGroup(r_m, r_cm, r_kh).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([3.3, -1.75, 0])
    scene.play(LaggedStart(*[Create(r) for r in rulers], lag_ratio=0.35), run_time=2.5)

    # 02:37.5 - 03:01.5 | "وقلتلك وقتها إنه ممكن يكون عندي عدد لا نهائي من وحدات القياس... أهي وحدات القياس دي بقى هي نفسها تمثيل هندسي لفكرة متجهات الأساس"
    scene.wait(24.0)

    # ---------- 4) نص الحقيقة + النص التاني ----------
    # 03:01.5 - 03:07.5 | "يعني في الحلقة اللي فاتت لما كنت بقولك إننا ممكن نمثل المتجه بقايمة من الأرقام..."
    scene.play(FadeOut(VGroup(rulers, basis_lbl, col_num, col_cap)),
               *[formula[i].animate.set_opacity(1.0) for i in V_IDX], run_time=1.0)
    scene.wait(5.0)

    # 03:07.5 - 03:15.0 | "أنا وقتها كنت بوريك نص الحقيقة بس من المتجه، والنص التاني ده هي متجهات الأساس..."
    R = 1.5
    CY = -1.0                                   # ارتفاع مركز الدايرة
    left_half = Sector(radius=R, angle=PI, start_angle=PI / 2, color=GOLD_LIGHT, stroke_width=2.2,
                       fill_color="#1A150C", fill_opacity=0.95)
    right_half = Sector(radius=R, angle=PI, start_angle=-PI / 2, color=COPPER_TERRA, stroke_width=2.2,
                        fill_color="#1A150C", fill_opacity=0.95)
    lst_small = _column(["3", "4", "5", "10"], 26, IVORY_WHITE).move_to(left_half.get_center() + LEFT * 0.2)
    e_small = VGroup(*[_tex(s, 28, COPPER_TERRA) for s in
                       (r"\mathbf{e}_1", r"\mathbf{e}_2", r"\mathbf{e}_3", r"\mathbf{e}_4")]).arrange(DOWN, buff=0.17)
    e_small.move_to(right_half.get_center() + RIGHT * 0.2)

    half_l = VGroup(left_half, lst_small).move_to([-3.4, CY, 0])
    half_r = VGroup(right_half, e_small).move_to([3.4, CY, 0])
    cap_l = _ar("نص الحقيقة", 20, GOLD_MUTED).next_to(half_l, DOWN, buff=0.3)
    cap_r = _ar("والنص التاني", 20, GOLD_MUTED).next_to(half_r, DOWN, buff=0.3)

    scene.play(FadeIn(half_l, shift=RIGHT * 0.3), FadeIn(half_r, shift=LEFT * 0.3),
               FadeIn(cap_l), FadeIn(cap_r), run_time=1.2)
    scene.wait(6.3)

    # 03:15.0 - 03:21.5 | "وعلى فكرة، الصيغة الرياضية للمتجه هي نفسها بتستخدم قواعد المتجهات..."
    center = np.array([0.0, CY, 0.0])
    whole_lbl = _tex(r"\mathbf{v}", 52, GOLD_BRIGHT).move_to(center)
    shift_l = np.array([center[0] - half_l[0].get_right()[0], center[1] - half_l[0].get_center()[1], 0])
    shift_r = np.array([center[0] - half_r[0].get_left()[0], center[1] - half_r[0].get_center()[1], 0])
    scene.play(FadeOut(VGroup(cap_l, cap_r)),
               half_l.animate.shift(shift_l), half_r.animate.shift(shift_r),
               run_time=1.4)
    scene.play(FadeIn(whole_lbl, scale=0.6), run_time=0.6)

    # ---------- شعاع نور بعد الاندماج ----------
    glow = Circle(radius=R * 1.1, stroke_width=0, fill_color=GOLD_BRIGHT, fill_opacity=0.0).move_to(center)
    beam = Circle(radius=R, color=IVORY_WHITE, stroke_width=7).move_to(center)
    pulse = Circle(radius=R, color=GOLD_BRIGHT, stroke_width=5, stroke_opacity=0.9).move_to(center)
    rays = VGroup()
    for k, a in enumerate(np.linspace(0, TAU, 24, endpoint=False)):
        d = np.array([np.cos(a), np.sin(a), 0.0])
        out = 1.62 if k % 2 == 0 else 1.40
        rays.add(Line(center + R * 1.10 * d, center + R * out * d, color=GOLD_BRIGHT, stroke_width=3.0))
    scene.add(glow, pulse)
    scene.play(ShowPassingFlash(beam, time_width=0.5),
               pulse.animate.scale(1.55).set_stroke(opacity=0.0),
               LaggedStart(*[Create(r) for r in rays], lag_ratio=0.03),
               glow.animate.set_fill(opacity=0.10),
               run_time=1.8)
    scene.remove(pulse)
    scene.wait(2.7)
    scene.play(FadeOut(VGroup(half_l, half_r, whole_lbl, rays, glow)), run_time=0.7)

    # ---------- 5) الصيغة نفسها: ضرب ثم جمع ----------
    # 03:22.0 - 03:27.5 | "يعني في الصيغة دي احنا بنضرب أرقام مركبات المتجه في متجهات الأساس..."
    pair_idx = ((2, 3), (5, 6), (8, 9), (13, 14))
    mult_marks = VGroup()
    for a, b in pair_idx:
        br = Brace(VGroup(formula[a], formula[b]), direction=DOWN, color=GOLD_LIGHT, buff=0.12)
        times = _tex(r"\times", 30, GOLD_LIGHT).next_to(br, DOWN, buff=0.08)
        mult_marks.add(VGroup(br, times))
    mult_lbl = _ar("بنضرب كل مركبة في متجه الأساس بتاعها", 22, GOLD_LIGHT).move_to([0, -0.15, 0])

    scene.play(LaggedStart(*[GrowFromCenter(m) for m in mult_marks], lag_ratio=0.2), FadeIn(mult_lbl),
               run_time=1.5)
    scene.wait(3.8)

    # 03:27.5 - 03:34.0 | "...وبعدين بنجمعهم على بعض... وهوريك مثال على ده كمان شوية عشان تفهمني أكتر"
    plus_idx = (4, 7, 10, 12)
    scene.play(*[Indicate(formula[i], color=COPPER_TERRA, scale_factor=1.7) for i in plus_idx], run_time=1.0)
    add_lbl = _ar("وبعدين بنجمعهم على بعض", 22, COPPER_TERRA).move_to([0, -1.55, 0])
    scene.play(FadeIn(add_lbl, shift=UP * 0.1), run_time=0.6)
    scene.wait(4.9)

    # 03:34.0 - 03:35.0 | تفريغ الشاشة لنهاية المشهد
    scene.play(FadeOut(VGroup(formula, mult_marks, mult_lbl, add_lbl)), run_time=0.9)
    scene.wait(0.1)

class Dev(ThreeDScene):
    def construct(self):
        play_scene02(self)