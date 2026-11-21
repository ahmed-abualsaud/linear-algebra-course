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
    TEAL,
)
from common.latex import mach_math_template
from episode_05_common import *


# ==============================================================
# الحلقة 05 — الفصل 7: وجود نقطة الأصل والقدرة على الثبات
# (الشرط 2 من 5 — شريط الشروط بيظهر أعلى الشاشة)
# مدة الفصل الفعلية: 02:24.0  (بطاقة الفصل 4.2s + السرد من 17:42.0 حتى 20:06.0؛ ثم _exit داخل فاصل الـ 6s قبل الفصل 8)
# التخطيط: شبكة MachAxes2D على الشمال — ولوحة الكلام على اليمين بعيد عن الرسمة.
# ==============================================================

PX = 4.25                                   # مركز لوحة الكلام (اليمين)


def _rtl(parts, buff=0.14):
    """سطر عربي فيه رموز لاتينية: الأجزاء بترتيب القراءة (الأول = أقصى اليمين)."""
    return VGroup(*parts[::-1]).arrange(RIGHT, buff=buff)


def play_scene07(scene):
    _chapter(scene, 7, 'وجود نقطة الأصل والقدرة على الثبات')
    cap = _Cap(scene, y=-2.85)               # الجملة الدهبية مرفوعة عشان الترجمة تلاقي مكان تحتها
    bar = _rules_bar(1)
    S = 0.6                                  # نفس شبكة الفصل 4 و5
    gr = MachAxes2D(
        center=np.array([-5.4, -1.55, 0.0]),
        x_range=(-1, 10),
        y_range=(-1, 7),
        grid_step=S,
        number_font_size=16,
        number_buff=0.34,
        show_minor_ticks=False,
        show_origin=True,
    )
    for _l in [l for l in gr.labels if l.text == "-1"]:
        gr.labels.remove(_l)
        gr.remove(_l)
    P = lambda x, y: gr.c2p(x, y)
    O = P(0, 0)

    def vec(comps, color, start=(0, 0), width=7, tip=0.14):
        a_ = P(*start)
        return _arrow(a_, a_ + S * np.array([comps[0], comps[1], 0.0]), color, width, tip=tip)

    def ripple(pos, color=GOLD_BRIGHT, n=2, dur=0.9):
        for _ in range(n):
            ring = Circle(radius=0.12, color=color, stroke_width=4).move_to(pos)
            scene.add(ring)
            scene.play(ring.animate.scale(5).set_stroke(opacity=0), run_time=dur)
            scene.remove(ring)

    # ---------- 1) متجه الصفر: لو جمعته على أي متجه ما يتغيرش ----------
    # 17:42.0 - 18:27.0 | «تاني شرط هو انه لازم يكون عندي متجه معين… شرط وجود نقطة الأصل» (45.0s)
    with beat(scene, 45.0):
        scene.play(FadeIn(bar), run_time=0.8)
        gr.animate_creation(scene, run_time=1.4)

        # 17:45.2: المتجه v ونمشي عليه ثم نضيف الصفر عند رأسه: فضلنا في نفس المكان
        scene.wait(1.0 * SPD)
        v = vec((6, 4), C_V)
        lv = _tex(r"\mathbf{v}", 38, C_V)
        tv = _tex(r"(6,\,4)", 26, C_V)
        lab_v = VGroup(lv, tv).arrange(RIGHT, buff=0.14).next_to(v.get_end(), UP, buff=0.12)
        scene.play(GrowArrow(v), FadeIn(lab_v), run_time=1.1)

        walker = _dot(O, C_SUM, 0.1)
        scene.play(FadeIn(walker), walker.animate.move_to(P(6, 4)), run_time=1.5)

        plus0 = MathTex(
            r"+", r"\mathbf{0}",
            tex_template=mach_math_template, font_size=32, color=IVORY_WHITE,
        ).move_to(P(6, 4) + np.array([0.75, -0.3, 0]))
        plus0[0].set_color(IVORY_WHITE)
        plus0[1].set_color(GOLD_BRIGHT)

        scene.play(FadeIn(plus0, shift=UP * 0.1), run_time=0.7)
        ripple(P(6, 4), color=C_SUM, n=1, dur=0.9)

        f1 = MathTex(
            r"\mathbf{v}", r"+", r"\mathbf{0}", r"=", r"\mathbf{v}",
            tex_template=mach_math_template, font_size=44, color=IVORY_WHITE,
        ).move_to([PX, 0.65, 0])
        f1[0].set_color(C_V)
        f1[1].set_color(IVORY_WHITE)
        f1[2].set_color(GOLD_BRIGHT)
        f1[3].set_color(IVORY_WHITE)
        f1[4].set_color(C_V)
        scene.play(FadeIn(f1, shift=LEFT * 0.2), run_time=0.9)

        f2 = MathTex(
            r"(6,\,4)", r"+", r"(0,\,0)", r"=", r"(6,\,4)",
            tex_template=mach_math_template, font_size=30, color=IVORY_WHITE,
        ).move_to([PX, -0.15, 0])
        f2[0].set_color(C_V)
        f2[1].set_color(IVORY_WHITE)
        f2[2].set_color(GOLD_BRIGHT)
        f2[3].set_color(IVORY_WHITE)
        f2[4].set_color(C_V)
        scene.play(FadeIn(f2, shift=UP * 0.1), run_time=0.8)

        # 17:56.0: «ولو جمعته على أي متجه تاني مابيعملش حاجة أصلاً...»
        scene.wait(4.9 * SPD)
        u = vec((7, 2), C_U)
        lu = _tex(r"\mathbf{u}", 38, C_U)
        tu = _tex(r"(7,\,2)", 26, C_U)
        lab_u = VGroup(lu, tu).arrange(RIGHT, buff=0.14).next_to(u.get_end(), RIGHT, buff=0.15)
        scene.play(GrowArrow(u), FadeIn(lab_u), run_time=1.0)

        f3 = MathTex(
            r"(7,\,2)", r"+", r"(0,\,0)", r"=", r"(7,\,2)",
            tex_template=mach_math_template, font_size=30, color=IVORY_WHITE,
        ).move_to([PX, -0.8, 0])
        f3[0].set_color(C_U)
        f3[1].set_color(IVORY_WHITE)
        f3[2].set_color(GOLD_BRIGHT)
        f3[3].set_color(IVORY_WHITE)
        f3[4].set_color(C_U)
        scene.play(FadeIn(f3, shift=UP * 0.1), run_time=0.8)

        every = _chip("ولأي متجه تاني بالظبط", GOLD_LIGHT, w=4.6, h=0.6, size=18).move_to([PX, -1.65, 0])
        scene.play(FadeIn(every, shift=UP * 0.1), run_time=0.7)

        # 18:06.0: «بيسموه المتجه المحايد الجمعي أو متجه الصفر»
        scene.wait(7.5 * SPD)
        title = _chip("المحايد الجمعي", GOLD_BRIGHT, w=4.6, h=0.62, size=20, filled=True).move_to([PX, 2.6, 0])
        zero = _dot(O, GOLD_BRIGHT, 0.12)
        zero.set_z_index(3)
        scene.play(FadeIn(title, shift=DOWN * 0.1), FadeIn(zero), run_time=0.8)
        ripple(O, n=2)

        # 18:14.5: «ومتجه الصفر ده هو نقطة أصل المتجهات»
        scene.wait(5.9 * SPD)
        leg_box = RoundedRectangle(
            corner_radius=0.16, width=4.8, height=0.66, stroke_color=GOLD_LIGHT,
            stroke_width=1.8, fill_color="#14100A", fill_opacity=0.9,
        ).move_to([PX, 1.75, 0])
        leg_txt = _rtl([
            _ar("متجه الصفر", 19, GOLD_LIGHT, True), _tex(r"\mathbf{0}", 32, GOLD_BRIGHT),
            _ar("هو نقطة الأصل", 19, GOLD_LIGHT, True),
        ]).move_to(leg_box)
        legend = VGroup(leg_box, leg_txt)
        scene.play(FadeIn(legend, shift=LEFT * 0.15), run_time=0.9)

        # 18:19.0: «عشان كده الشرط ده اسمه شرط المحايد الجمعي أو شرط وجود نقطة الأصل»
        scene.wait(3.6 * SPD)
        cap.set("متجه الصفر = المحايد الجمعي = شرط وجود نقطة الأصل", GOLD_LIGHT)

        b1 = VGroup(title, legend, v, lab_v, walker, plus0, f1, f2, u, lab_u, f3, every)

    # ---------- 2) من غير نقطة أصل: 3e₁ بيبعد عن إيه؟ ----------
    # 18:27.0 - 19:36.5 | «طبعا انت لو لاحظت… كنا بنلزق متجهات الاساس… من غير نقطة أصل مفيش مرجع» (69.5s)
    with beat(scene, 69.5):
        scene.play(FadeOut(b1), run_time=0.8)

        # 18:36.5: «أهي النقطة دي اسمها نقطة الأصل...»
        scene.wait(8.7 * SPD)
        ripple(O, n=1)
        scene.play(Indicate(zero, color=GOLD_BRIGHT, scale_factor=1.5), run_time=0.8)

        # 18:44.5: «يعني مثلاً لو عندي المتجه v بتساوي 3e1...»
        scene.wait(6.3 * SPD)
        st = _stack(O, (S, 0), 3, GOLD_BRIGHT, 5)
        l3 = MathTex(
            r"\mathbf{v}", r"=", r"3\mathbf{e}_1",
            tex_template=mach_math_template, font_size=34, color=IVORY_WHITE,
        ).move_to(P(2.1, 0) + np.array([0, 0.55, 0]))
        l3[0].set_color(C_V)
        l3[1].set_color(IVORY_WHITE)
        l3[2].set_color(GOLD_BRIGHT)

        for m in (*st, l3):
            m.set_z_index(3)
        scene.play(LaggedStart(*[GrowArrow(a) for a in st], lag_ratio=0.25), FadeIn(l3), run_time=1.4)

        # 18:57.0: «طيب لو نقطة الأصل مش موجودة... هو v بيبعد 3e1 عن أنهي نقطة بالظبط؟»
        scene.wait(11.1 * SPD)
        q = _rtl([
            _ar("بيبعد", 22, ERR_RED, True),
            _tex(r"3\mathbf{e}_1", 34, GOLD_BRIGHT),
            _ar("عن إيه بالظبط؟", 22, ERR_RED, True),
        ]).move_to([PX, 2.45, 0])
        scene.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.8)

        veil = Rectangle(width=6.9, height=5.1, stroke_width=0).set_fill("#000000", 0.0)
        veil.move_to([-2.65, 0.3, 0]).set_z_index(2)
        qm1 = _ar("؟", 34, ERR_RED, True).move_to(P(0.45, 0) + np.array([0, 0.4, 0])).set_z_index(3)
        qm2 = _ar("؟", 34, ERR_RED, True).move_to(P(3, 0) + np.array([0.4, 0.35, 0])).set_z_index(3)
        scene.add(veil)
        scene.play(veil.animate.set_fill("#000000", 0.78), FadeOut(zero), run_time=1.2)
        scene.play(FadeIn(qm1), FadeIn(qm2), run_time=0.7)
        cap.set("من غير نقطة أصل مفيش متجهات أصلًا", ERR_RED)

        # 19:08.5: «زي الفرق بين النقطة 4e1 و 1e1...»
        scene.wait(8.1 * SPD)
        alt = MathTex(
            r"4\mathbf{e}_1", r"-", r"1\mathbf{e}_1", r"=", r"3\mathbf{e}_1",
            tex_template=mach_math_template, font_size=34, color=IVORY_WHITE,
        ).move_to([PX, 1.2, 0])
        alt[0].set_color(C_U)
        alt[1].set_color(IVORY_WHITE)
        alt[2].set_color(C_V)
        alt[3].set_color(IVORY_WHITE)
        alt[4].set_color(GOLD_BRIGHT)
        scene.play(FadeIn(alt, shift=LEFT * 0.15), run_time=0.9)

        # 19:19.5: «لكن اسأل نفسك: الفرق بين النقطتين ده اتحسب إزاي؟»
        scene.wait(10.1 * SPD)
        alt_q1 = _ar("الاتنين اتحسبوا مقارنةً بإيه؟", 20, GOLD_LIGHT, True).move_to([PX, 0.3, 0])
        alt_q2 = _ar("لازم أصل!", 28, GOLD_BRIGHT, True).move_to([PX, -0.45, 0])
        scene.play(FadeIn(alt_q1), run_time=0.8)
        scene.wait(1.5 * SPD)
        scene.play(FadeIn(alt_q2, scale=1.1), run_time=0.7)

        # 19:24.0: «وقيم 4e1 و 1e1 اتحسبوا إزاي من غير ما يكون في نقطة أصل؟»
        scene.wait(1.5 * SPD)
        scene.play(veil.animate.set_fill("#000000", 0.0), FadeOut(VGroup(qm1, qm2, l3)), FadeIn(zero), run_time=1.1)
        ripple(O, n=1)
        dA, dB = _dot(P(4, 0), C_U, 0.09), _dot(P(1, 0), C_V, 0.09)
        guides = VGroup(
            DashedLine(P(0, 0), P(0, 2.8), color=GOLD_BRIGHT, stroke_width=2, dash_length=0.09),
            DashedLine(P(4, 0), P(4, 4.2), color=C_U, stroke_width=2, dash_length=0.09),
            DashedLine(P(1, 0), P(1, 4.2), color=C_V, stroke_width=2, dash_length=0.09),
        )
        A = vec((4, 0), C_U, start=(0, 1.4), width=6)
        B = vec((1, 0), C_V, start=(0, 2.8), width=6)
        D = vec((3, 0), GOLD_BRIGHT, start=(1, 4.2), width=6)
        lA = _tex(r"4\mathbf{e}_1", 30, C_U).next_to(A, UP, buff=0.1)
        lB = _tex(r"1\mathbf{e}_1", 30, C_V).next_to(B, UP, buff=0.1)
        lD = _tex(r"3\mathbf{e}_1", 30, GOLD_BRIGHT).next_to(D, UP, buff=0.1)
        scene.play(FadeIn(VGroup(dA, dB)), Create(guides), run_time=1.0)
        scene.play(GrowArrow(A), FadeIn(lA), run_time=0.9)
        scene.play(GrowArrow(B), FadeIn(lB), run_time=0.9)
        scene.play(GrowArrow(D), FadeIn(lD), run_time=1.1)
        cap.set("كل المسافات بتتقاس من نقطة الأصل — من غيرها مفيش مرجع", GOLD_LIGHT)

    # ---------- 3) صيغة متجه الصفر وجمعه على v ----------
    # 19:36.5 - 20:06.0 | «طيب خليني اقولك هنا بالمرة ان الصيغة الرياضية لمتجه الصفر… فالنتيجة مش هتتغير» (29.5s)
    with beat(scene, 29.5):
        scene.play(*[FadeOut(m) for m in list(scene.mobjects) if m is not bar and m is not cap.cur], run_time=0.7)
        scene.remove(veil)

        def tag(txt, y):
            return _chip(txt, COPPER_TERRA, w=2.4, h=0.46, size=14, filled=True).move_to([5.45, y, 0])

        EC, CC, ZC, OP = GOLD_LIGHT, IVORY_WHITE, COPPER_TERRA, STONE_AXIS

        def ctex(tokens, size):
            m = MathTex(*[t for t, _ in tokens], tex_template=mach_math_template, font_size=size)
            for sub, (_, col) in zip(m, tokens):
                sub.set_color(col)
            return m

        E = lambda k: (r"\mathbf{e}_" + str(k), EC)
        PL, EQ = ("+", OP), ("=", OP)
        ZERO = ("0", ZC)

        z1 = ctex([
            (r"\mathbf{0}", ZC), EQ, ZERO, E(1), PL, ZERO, E(2), PL, ZERO, E(3), PL,
            (r"\cdots", OP), PL, ZERO, (r"\mathbf{e}_n", EC),
        ], 35).move_to([-1.25, 1.9, 0])

        z2_tok = [
            (r"\mathbf{v}", CC), PL, (r"\mathbf{0}", ZC), EQ,
            ("(", OP), ("v_1", CC), PL, ZERO, (")", OP), E(1), PL,
            ("(", OP), ("v_2", CC), PL, ZERO, (")", OP), E(2), PL,
            (r"\cdots", OP), PL,
            ("(", OP), ("v_n", CC), PL, ZERO, (")", OP), (r"\mathbf{e}_n", EC),
        ]
        z2 = ctex(z2_tok, 28).move_to([-1.25, 0.45, 0])
        zi = [i for i, (t, c) in enumerate(z2_tok) if t == "0"]

        z3 = ctex([
            EQ, ("v_1", CC), E(1), PL, ("v_2", CC), E(2), PL,
            (r"\cdots", OP), PL, ("v_n", CC), (r"\mathbf{e}_n", EC), EQ, (r"\mathbf{v}", CC),
        ], 35).move_to([-1.25, -0.95, 0])

        t1, t2, t3 = tag("تعريف متجه الصفر", 1.9), tag("بنجمعه على المتجه", 0.45), tag("الناتج المتجه نفسه", -0.95)

        # 19:38.5: تعريف متجه الصفر
        scene.wait(1.3 * SPD)
        scene.play(FadeIn(z1, shift=UP * 0.15), FadeIn(t1, shift=LEFT * 0.1), run_time=1.1)

        # 19:46.0: بنجمعه على المتجه v
        scene.wait(6.4 * SPD)
        scene.play(FadeIn(z2, shift=UP * 0.15), FadeIn(t2, shift=LEFT * 0.1), run_time=1.1)

        # 19:52.0: «طبعاً ونتيجة الجمع هتكون هي المتجه v نفسه»
        scene.wait(4.9 * SPD)
        scene.play(FadeIn(z3, shift=UP * 0.15), FadeIn(t3, shift=LEFT * 0.1), run_time=1.1)

        # 19:55.5: «لأن مركباته كلها مجموع عليها صفر»
        scene.wait(2.4 * SPD)
        scene.play(*[Indicate(z2[k], color=ZC, scale_factor=1.5) for k in zi], run_time=1.2)

        # 20:01.0: «فالنتيجة مش هتتغير...»
        scene.wait(4.3 * SPD)
        scene.play(Indicate(z3[-1], color=CC, scale_factor=1.4), run_time=0.9)
        cap.y = -2.05
        cap.set("المركبات كلها اتجمع عليها صفر — فالنتيجة ما اتغيرتش", GOLD_LIGHT)

    _exit(scene)


class Dev(Scene):
    def construct(self):
        play_scene07(self)