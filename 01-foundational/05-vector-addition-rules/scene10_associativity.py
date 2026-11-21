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
from common.mobjects.coordinate_systems import MachAxes2D
from episode_05_common import *


# ==============================================================
# الحلقة 05 — الفصل 10: اتساق الفضاء
# (الشرط 5 من 5 — شريط الشروط بيظهر أعلى الشاشة)
# مدة الفصل الفعلية: 04:04.0  (بطاقة الفصل 4.2s + السرد من 25:10.0 حتى 29:14.0؛ ثم _exit داخل فاصل الـ 5s قبل الفصل 11)
# ==============================================================

GRID_STEP = 0.6
AX_ORIGIN = np.array([-5.4, -1.35, 0.0])
AX_X_RANGE = (-1, 11)
AX_Y_RANGE = (-1, 7)

E1_COL = GOLD_BRIGHT
E2_COL = IVORY_WHITE

CAP_Y = -2.70
TEAL_L = "#7FDCCF"


def _halo(m, w=8):
    """هالة داكنة خلف النص لمنع التداخل مع خطوط الشبكة."""
    m.set_stroke("#000000", width=w, background=True)
    return m


def play_scene10(scene):
    _chapter(scene, 10, 'اتساق الفضاء')
    cap = _Cap(scene)
    cap.y = CAP_Y
    bar = _rules_bar(4)

    # الشبكة الرسمية MachAxes2D
    ax = MachAxes2D(
        center=AX_ORIGIN,
        grid_step=GRID_STEP,
        x_range=AX_X_RANGE,
        y_range=AX_Y_RANGE,
        grid_opacity=0.32,
        number_font_size=14,
        show_minor_ticks=False,
    )

    def P(x, y):
        return ax.c2p(x, y)

    def vec(delta, color, start=(0, 0), width=7):
        a = P(*start)
        b = P(start[0] + delta[0], start[1] + delta[1])
        return _arrow(a, b, color, width, 0.16)

    # ---------- 1) (u+v)+w = u+(v+w): ثلاثة متجهات على مسار واحد ----------
    # 25:10.0 - 25:45.0 | «الشرط الخامس والاخير… طالما هجمع التلاتة في الاخر»
    with beat(scene, 35.0):
        scene.play(FadeIn(bar), run_time=0.6)
        ax.animate_creation(scene, run_time=1.4)

        u = vec((3, 1), C_U)
        v = vec((2, 3), C_V, start=(3, 1))
        w = vec((3, -2), C_W, start=(5, 4))

        lu = _halo(_tex(r"\mathbf{u}", 36, C_U).move_to(P(2.35, 1.28)))
        lv = _halo(_tex(r"\mathbf{v}", 36, C_V).move_to(P(4.4, 2.35)))
        lw = _halo(_tex(r"\mathbf{w}", 36, C_W).move_to(P(7.0, 3.7)))

        # 25:14.5: ظهور المتجهات u, v, w بالتزامن مع ذكرها
        scene.wait(2.5 * SPD)
        scene.play(GrowArrow(u), FadeIn(lu), run_time=0.9)
        scene.play(GrowArrow(v), FadeIn(lv), run_time=0.9)
        scene.play(GrowArrow(w), FadeIn(lw), run_time=0.9)

        fa = MathTex(
            r"(", r"\mathbf{u}", r"+", r"\mathbf{v}", r")",
            r"+", r"\mathbf{w}",
            r"=",
            r"\mathbf{u}", r"+",
            r"(", r"\mathbf{v}", r"+", r"\mathbf{w}", r")",
            tex_template=mach_math_template,
            font_size=36,
            color=IVORY_WHITE,
        ).move_to([4.0, 2.65, 0])

        fa[1].set_color(C_U)
        fa[3].set_color(C_V)
        fa[6].set_color(C_W)
        fa[8].set_color(C_U)
        fa[11].set_color(C_V)
        fa[13].set_color(C_W)

        uv = DashedLine(P(0, 0), P(5, 4), color=C_SUM, stroke_width=4)
        vw = DashedLine(P(3, 1), P(8, 2), color=C_SUM, stroke_width=4)

        # 25:19.5: جمع (u+v) ثم w
        scene.wait(2.3 * SPD)
        scene.play(Create(uv), FadeIn(fa[:7], shift=LEFT * 0.2), run_time=1.2)

        # 25:28.0: مقارنة بـ u+(v+w)
        scene.wait(7.3 * SPD)
        scene.play(Create(vw), FadeIn(fa[7:], shift=LEFT * 0.2), run_time=1.2)

    # ---------- 2) الاتساق: كل نقطة بتسلّمك للنقطة اللي جنبها ----------
    # 25:45.0 - 26:19.0 | «والشرط ده بيسموه شرط التجميع… ومش بتسوحك في مكان تاني»
    with beat(scene, 34.0):
        # انتظار التسمية (25:45 -> 25:55.5) ثم التحرك مع شرح المسار
        scene.wait(10.5 * SPD)

        d1 = _dot(P(0, 0), GOLD_BRIGHT, 0.1)
        fend = _dot(P(8, 2), C_SUM, 0.14)
        scene.play(FadeIn(d1), run_time=0.5)
        scene.play(d1.animate.move_to(P(3, 1)), run_time=1.4)
        scene.play(d1.animate.move_to(P(5, 4)), run_time=1.4)
        scene.play(d1.animate.move_to(P(8, 2)), FadeIn(fend), run_time=1.4)

        # 26:02.5: «بدون وجود أي انحرافات أو قفزات غير مبررة»
        cap.set("نقطة نهاية واحدة، من غير انحراف أو قفزات غير مبررة", GOLD_LIGHT)
        scene.wait(7.5 * SPD)
        scene.play(FadeOut(VGroup(d1, fend)), run_time=0.6)

    # ---------- 3) التجربة الذهنية (متزامنة بالثانية مع السرد الصوتي) ----------

    # 26:19.0 - 26:32.0 | «عشان تقدر تستوعب انا قصدي ايه… خليني اوريك تجربة ذهنية» (13 ثانية)
    with beat(scene, 13.0):
        scene.play(FadeOut(VGroup(fa, lu, lv, lw)), run_time=0.6)
        scene.wait(5.4 * SPD)
        cap.set("تجربة ذهنية: جمع بطريقة بتخالف شرط التجميع", GOLD_MUTED)

    # 26:32.0 - 26:49.0 | «تخيل انك واقف عند نقطة الاصل… وعاوز توصل لـ f بس تعدي على m1 و m2» (17 ثانية)
    with beat(scene, 17.0):
        O_, M1, M2, F_ = P(0, 0), P(3, 1), P(5, 4), P(8, 2)
        X_ = P(6, 5)                              # بعد القفزة: m2 + (1, 1)
        Fx = P(9, 3)                              # x + w

        pts = VGroup(
            _dot(O_, GOLD_BRIGHT, 0.1),
            _dot(M1, C_U, 0.1),
            _dot(M2, ERR_RED, 0.12),
            _dot(F_, C_SUM, 0.12),
        )

        # إبعاد التسميات عن الهالة والأسهم، وفصل 1 و 2 عن m
        tags = VGroup(
            _halo(_tex("o", 30, GOLD_BRIGHT).next_to(O_, UL, buff=0.24)),
            _halo(_tex(r"m_{\,1}", 30, C_U).next_to(M1, UL, buff=0.24)),
            _halo(_tex(r"m_{\,2}", 30, ERR_RED).next_to(M2, UL, buff=0.24)),
            _halo(_tex("f", 32, C_SUM).next_to(F_, DR, buff=0.24)),
        )

        # 26:32: o
        scene.play(FadeIn(pts[0]), FadeIn(tags[0]), run_time=0.7)
        # 26:38: f
        scene.wait(5.3 * SPD)
        scene.play(FadeIn(pts[3]), FadeIn(tags[3]), run_time=0.7)
        # 26:43: m1, m2
        scene.wait(4.3 * SPD)
        scene.play(FadeIn(VGroup(pts[1], pts[2], tags[1], tags[2])), run_time=0.9)

    # 26:49.0 - 27:03.0 | «بالنسبة للنقطة m1 عادية… لكن m2 دي خبيثة بتضيف 1 لكل مركبة» (14 ثانية)
    with beat(scene, 14.0):
        # 26:50: m1 عادية
        scene.wait(1.0 * SPD)
        scene.play(Indicate(pts[1], color=C_U, scale_factor=1.4), run_time=0.9)

        # 26:54: لكن m2 خبيثة
        scene.wait(2.1 * SPD)
        note_m2_txt = _ar("بتضيف 1 لكل مركبة", 18, GOLD_LIGHT, True)
        note_m2_lbl = _tex(r":\, m_{\,2}", 26, GOLD_LIGHT)
        note_m2 = VGroup(note_m2_txt, note_m2_lbl).arrange(RIGHT, buff=0.12).move_to([4.1, 2.15, 0])

        scene.play(FadeIn(note_m2, shift=DOWN * 0.1), run_time=0.9)
        scene.play(Indicate(pts[2], color=ERR_RED, scale_factor=1.6), run_time=1.0)

    # 27:03.0 - 27:19.0 | «فلو تخيلت ان فيه نقطتين… واحدة بتتحرك علي u لـ m1 ثم w+v لـ f» (16 ثانية)
    with beat(scene, 16.0):
        dA = _dot(O_, C_U, 0.11)
        dB = _dot(O_, C_V, 0.11)
        scene.play(FadeIn(dA), FadeIn(dB), run_time=0.6)

        # 27:07.5: تتحرك على u لـ m1
        scene.wait(3.9 * SPD)
        vw2 = Line(M1, F_, color=C_SUM, stroke_width=4)
        scene.play(dA.animate.move_to(M1), run_time=1.6)

        # 27:13.0: ثم تنقل على w+v لـ f
        scene.wait(3.9 * SPD)
        scene.play(ReplacementTransform(vw, vw2), dA.animate.move_to(F_), run_time=1.8)

    # 27:19.0 - 27:33.0 | «والتانية بتتحرك علي u+v في اتجاه m2… المفروض تنقل على w لـ f» (14 ثانية)
    with beat(scene, 14.0):
        scene.wait(1.0 * SPD)
        uv2 = Line(O_, M2, color=C_SUM, stroke_width=4)
        scene.play(dB.animate.move_to(M2), ReplacementTransform(uv, uv2), run_time=1.8)

        # 27:26.5: «بعدين المفروض إنها تنقل على المتجه w في اتجاه f»
        scene.wait(4.7 * SPD)
        scene.play(Indicate(w, color=C_W, scale_factor=1.06), run_time=1.2)

    # 27:33.0 - 27:48.0 | «بتحصل حاجة غريبة عند m2… بتنط لنقطة جديدة اسمها x» (15 ثانية)
    with beat(scene, 15.0):
        # 27:33.5: حاجة غريبة عند m2
        ring = Circle(radius=0.12, color=ERR_RED, stroke_width=4).move_to(M2)
        scene.play(ring.animate.scale(4).set_stroke(opacity=0), run_time=1.2)

        # 27:41.0: بتنط لـ x
        scene.wait(6.8 * SPD)
        jump = _arrow(M2, X_, ERR_RED, 4, 0.18)
        tx = _halo(_tex("x", 32, ERR_RED).next_to(X_, UL, buff=0.22))
        scene.play(GrowArrow(jump), dB.animate.move_to(X_), FadeIn(tx), run_time=1.1)

    # 27:48.0 - 28:29.0 | «كأنه ثقب دودي… تغير اتجاهها موازي لـ w… وصلت لنقطة غير f… عدم اتساق» (41 ثانية)
    with beat(scene, 41.0):
        # 27:48.0: القفزة والعدسة المكبرة مع جملة «كأن في ثقب دودي...»
        M2r = M2 + np.array([GRID_STEP, 0.0, 0.0])
        e1s = _arrow(M2, M2r, E1_COL, 4, 0.32)
        e2s = _arrow(M2r, X_, E2_COL, 4, 0.32)
        scene.play(GrowArrow(e1s), GrowArrow(e2s), run_time=1.0)

        LC, LR = np.array([4.0, -0.35, 0.0]), 1.3
        lens_glow = Circle(radius=LR + 0.1, color=GOLD_LIGHT, stroke_width=10).move_to(LC)
        lens_glow.set_stroke(opacity=0.12)
        lens_ring = Circle(radius=LR, color=GOLD_LIGHT, stroke_width=3).move_to(LC)
        lens_ring.set_fill(GOLD_LIGHT, 0.05)

        S_ = LC + np.array([-0.55, -0.5, 0.0])
        L_ = 1.1
        big_e1 = _arrow(S_, S_ + np.array([L_, 0, 0]), E1_COL, 6, 0.2)
        big_e2 = _arrow(S_ + np.array([L_, 0, 0]), S_ + np.array([L_, L_, 0]), E2_COL, 6, 0.2)
        big_j = _arrow(S_, S_ + np.array([L_, L_, 0]), ERR_RED, 5, 0.16)

        big_l1 = _halo(_tex(r"\mathbf{e}_1", 30, E1_COL).move_to(S_ + np.array([L_ / 2, -0.3, 0])))
        big_l2 = _halo(_tex(r"\mathbf{e}_2", 30, E2_COL).move_to(S_ + np.array([L_ + 0.32, L_ / 2, 0])))
        lens_cap = _ar("القفزة = e₁ + e₂", 16, GOLD_LIGHT, True).move_to(LC + np.array([0, -LR - 0.35, 0]))

        mid_j = (M2 + X_) / 2
        d_ = LC - mid_j
        conn = Line(
            mid_j + d_ / np.linalg.norm(d_) * 0.2,
            LC - d_ / np.linalg.norm(d_) * (LR + 0.1),
            color=GOLD_LIGHT,
            stroke_width=1.6,
        )
        conn.set_stroke(opacity=0.6)

        note_x = _ar("كأنه ثقب دودي: بيحدفها لنقطة جديدة x", 18, IVORY_WHITE, True).move_to([4.1, 1.35, 0])

        scene.play(Create(conn), FadeIn(VGroup(lens_glow, lens_ring)), FadeIn(note_x), run_time=1.0)
        scene.play(
            GrowArrow(big_j), GrowArrow(big_e1), GrowArrow(big_e2),
            FadeIn(big_l1), FadeIn(big_l2), FadeIn(lens_cap),
            run_time=1.4,
        )

        # 27:55.5: «فلما تيجي تغير اتجاهها في اتجاه موازي لـ w، هتلاقي نفسها وصلت لنقطة مختلفة عن f»
        scene.wait(4.1 * SPD)
        w_copy = _arrow(X_, Fx, C_W, 6, 0.14)
        scene.play(TransformFromCopy(w, w_copy), run_time=1.4)
        scene.play(dB.animate.move_to(Fx), run_time=1.4)

        miss = _arrow(F_, Fx, ERR_RED, 4, 0.18)
        scene.play(Indicate(pts[3], color=C_SUM, scale_factor=2), GrowArrow(miss), run_time=1.4)

        # 28:07.0: «أهو الموقف الغريب ده اسمه عدم اتساق...»
        scene.wait(7.3 * SPD)
        cap.set("وصلت لنقطة غير f — ده اسمه عدم اتساق", COPPER_TERRA)
        scene.play(Indicate(pts[2], color=ERR_RED, scale_factor=1.5), run_time=1.0)

    # ---------- 4) الصيغة: التعويض بـ v₁₂ جوه v (متزامنة مع السرد) ----------
    # 28:29.0 - 29:14.0 | «طيب كل ده معناه ايه بالنسبة للصيغة الرياضية… عملية التعويض دي بتنهار»
    with beat(scene, 45.0):
        scene.play(
            *[FadeOut(m) for m in list(scene.mobjects) if m is not bar and m is not cap.cur],
            run_time=0.7,
        )

        def eq(*parts, size):
            return MathTex(*parts, tex_template=mach_math_template, font_size=size, color=IVORY_WHITE)

        T1, T2, T3, V12 = r"v_1\mathbf{e}_1", r"v_2\mathbf{e}_2", r"v_3\mathbf{e}_3", r"\mathbf{v}_{12}"

        # 28:32.5: v = v1 e1 + v2 e2 + v3 e3
        scene.wait(2.8 * SPD)
        g1 = eq(r"\mathbf{v}", "=", T1, "+", T2, "+", T3, size=40).move_to([0, 2.1, 0])
        g1[0].set_color(GOLD_BRIGHT)
        g1[2].set_color(C_U)
        g1[4].set_color(C_V)
        g1[6].set_color(TEAL_L)
        scene.play(FadeIn(g1, shift=UP * 0.15), run_time=1.0)

        # 28:43.0: v12 = v1 e1 + v2 e2
        scene.wait(9.5 * SPD)
        g2 = eq(V12, "=", T1, "+", T2, size=40).move_to([0, 0.9, 0])
        g2[0].set_color(GOLD)
        g2[2].set_color(C_U)
        g2[4].set_color(C_V)
        scene.play(FadeIn(g2, shift=UP * 0.15), run_time=1.0)

        # 28:55.0: v = v12 + v3 e3 = v1 e1 + v2 e2 + v3 e3
        scene.wait(11.0 * SPD)
        g3 = eq(r"\mathbf{v}", "=", V12, "+", T3, "=", T1, "+", T2, "+", T3, size=34).move_to([0, -0.4, 0])
        g3[0].set_color(GOLD_BRIGHT)
        g3[2].set_color(GOLD)
        g3[4].set_color(TEAL_L)
        g3[6].set_color(C_U)
        g3[8].set_color(C_V)
        g3[10].set_color(TEAL_L)
        scene.play(FadeIn(g3, shift=UP * 0.15), run_time=1.2)

        # 29:09.0: ختام التعليق («عملية التعويض دي هتنهار بالكامل»)
        scene.wait(12.8 * SPD)
        cap.set("من غير شرط التجميع عملية التعويض دي بتنهار", COPPER_TERRA)

    _exit(scene)


class Dev(Scene):
    def construct(self):
        play_scene10(self)