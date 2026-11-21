from manim import *
import numpy as np

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_DARK,
    COPPER_TERRA,
    IVORY_WHITE,
    LABEL_MUTED,
    TEAL,
)
from common.latex import mach_math_template
from episode_05_common import *


# ==============================================================
# الحلقة 05 — الفصل 5: كيف نجمع المتجهات؟
# مدة الفصل الفعلية: 03:21.7  (بطاقة الفصل 4.2s + السرد من 11:54.0 حتى 15:11.5؛ ثم _exit داخل فاصل الـ 5.5s قبل الفصل 6)
# ==============================================================


def play_scene05(scene):
    _chapter(scene, 5, 'كيف نجمع المتجهات؟')
    cap = _Cap(scene, y=-2.85)
    S = 0.6                                             # نفس شبكة الفصل 4
    gr = MachAxes2D(
        center=np.array([-5.4, -1.2, 0.0]),
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

    def vec(comps, color, start=(0, 0), width=7, tip=0.14):
        a_ = P(*start)
        return _arrow(a_, a_ + S * np.array([comps[0], comps[1], 0.0]), color, width, tip=tip)

    O3 = P(0, 0)

    def pulse(pos, color=GOLD_BRIGHT, dur=0.9):
        ring = Circle(radius=0.12, color=color, stroke_width=4).move_to(pos)
        scene.add(ring)
        scene.play(ring.animate.scale(4.5).set_stroke(opacity=0), run_time=dur)
        scene.remove(ring)

    def comps(x, y, color, row_y, col_x):
        """خطا إسقاط متقطعان لحد المحورين + مركّبتا المتجه كمتجهات أساس مرصوصة."""
        dx = DashedLine(P(x, y), P(x, 0), color=color, stroke_width=2.2, stroke_opacity=0.9, dash_length=0.09)
        dy = DashedLine(P(x, y), P(0, y), color=color, stroke_width=2.2, stroke_opacity=0.9, dash_length=0.09)
        bx = _stack(np.array([O3[0], row_y, 0.0]), (S, 0), x, color, 3.5)
        by = _stack(np.array([col_x, O3[1], 0.0]), (0, S), y, color, 3.5)
        return dx, dy, bx, by

    def show_comps(c):
        dx, dy, bx, by = c
        scene.play(Create(dx), Create(dy), run_time=1.0)
        scene.play(
            LaggedStart(*[GrowArrow(a) for a in bx], lag_ratio=0.12),
            LaggedStart(*[GrowArrow(a) for a in by], lag_ratio=0.12),
            run_time=1.4,
        )

    # ---------- 1) رسم u و v بذيلهما عند 0 ----------
    # 11:54.0 - 12:04.5 | «احنا عموما لما بنيجي نرسم المتجهات هندسيا بنحط بدايتها عند النقطة صفر…» (10.5s)
    with beat(scene, 10.5):
        gr.animate_creation(scene, run_time=1.4)
        scene.wait(3.6 * SPD)
        pulse(O3)

    # 12:04.5 - 12:15.5 | «يعني بالنسبة للمتجه u هتكون بدايته عند النقطة صفر وراسه عند (6, 2)…» (11.0s)
    with beat(scene, 11.0):
        scene.wait(1.0 * SPD)
        u = vec((6, 2), C_U)
        lu = _tex(r"\mathbf{u}", 38, C_U).move_to(P(5.45, 0.9))
        tu = _tex(r"(6,\,2)", 26, C_U).next_to(lu, LEFT, buff=0.14)
        scene.play(GrowArrow(u), FadeIn(lu), FadeIn(tu), run_time=1.0)
        cu = comps(6, 2, C_U, O3[1] - 0.22, P(6.35, 0)[0])
        show_comps(cu)

    # 12:15.5 - 12:25.5 | «والمتجه v هتكون بدايته عند النقطة صفر وراسه عند (3, 4)…» (10.0s)
    with beat(scene, 10.0):
        scene.wait(1.0 * SPD)
        v = vec((3, 4), C_V)
        lv = _tex(r"\mathbf{v}", 38, C_V).next_to(v.get_end(), RIGHT, buff=0.18)
        tv = _tex(r"(3,\,4)", 26, C_V).next_to(lv, RIGHT, buff=0.14)
        scene.play(GrowArrow(v), FadeIn(lv), FadeIn(tv), run_time=1.0)
        cv = comps(3, 4, C_V, P(0, 4.35)[1], O3[0] - 0.22)
        show_comps(cv)

    # 12:25.5 - 12:43.5 | «وعلي فكرة مش شرط انه يكون كل المتجهات بتبدا من النقطة صفر… لتسهيل عملية الجمع» (18.0s)
    with beat(scene, 18.0):
        scene.wait(1.5 * SPD)
        cap.set("مش شرط كل المتجهات تبدأ من الصفر — بنبدأ منه لتسهيل الجمع بس", GOLD_LIGHT)
        scene.wait(8.3 * SPD)
        pulse(O3)

    # ---------- 2) نمشي على u ثم ننقل v لرأس u ----------
    # 12:43.5 - 13:00.5 | «طيب دلوقتي عشان نجمع u و v… واقف عند النقطة صفر… واتحركت علي طول u لحد (6, 2)» (17.0s)
    with beat(scene, 17.0):
        scene.wait(5.0 * SPD)
        walker = _dot(O3, GOLD_BRIGHT, 0.12)
        scene.play(FadeIn(walker, scale=1.4), run_time=0.6)
        scene.wait(2.5 * SPD)
        scene.play(walker.animate.move_to(P(6, 2)), run_time=2.0)

    # 13:00.5 - 13:14.5 | «بعد كدة هتنقل المتجه v بحيث تكون بدايته عند النقطة الجديدة (6, 2)…» (14.0s)
    with beat(scene, 14.0):
        v2 = vec((3, 4), C_V, start=(6, 2))
        scene.play(TransformFromCopy(v, v2), run_time=1.6)
        scene.play(FadeOut(VGroup(v, lv, tv, *cv)), run_time=0.8)
        lv2 = _tex(r"\mathbf{v}", 38, C_V).move_to(P(7.5, 4) + np.array([0.36, -0.2, 0.0]))
        scene.play(FadeOut(tu), lu.animate.move_to(P(3, 1) + np.array([0.12, -0.36, 0.0])), FadeIn(lv2), run_time=0.8)

    # 13:14.5 - 13:26.5 | «بعد كدة هنشوف راس المتجه بتشاور فين… هتتحرك ناحية النقطة الجديدة (9, 6)» (12.0s)
    with beat(scene, 12.0):
        ts = _tex(r"(9,\,6)", 28, C_SUM).next_to(P(9, 6), RIGHT, buff=0.4)
        scene.wait(2.0 * SPD)
        scene.play(walker.animate.move_to(P(9, 6)), run_time=1.8)
        scene.wait(3.5 * SPD)
        scene.play(FadeIn(ts, scale=1.2), run_time=0.7)

    # 13:26.5 - 13:42.5 | «وتقدر ترسم المتجه المحصل طالع من صفر لـ (9, 6) بحيث يقفل شكل مثلث» (16.0s)
    with beat(scene, 16.0):
        scene.wait(1.5 * SPD)
        s = vec((9, 6), C_SUM, width=8)
        tri = Polygon(P(0, 0), P(6, 2), P(9, 6), stroke_width=0, fill_color=C_SUM, fill_opacity=0.12)
        nrm = np.array([-6.0, 9.0, 0.0])
        nrm /= np.linalg.norm(nrm)
        ls = MathTex(
            r"\mathbf{u}", r"+", r"\mathbf{v}",
            tex_template=mach_math_template,
            font_size=36,
            color=IVORY_WHITE,
        ).move_to((P(0, 0) + P(9, 6)) / 2 + nrm * 0.5)
        ls[0].set_color(C_U)
        ls[1].set_color(IVORY_WHITE)
        ls[2].set_color(C_V)
        scene.play(GrowArrow(s), FadeIn(tri), FadeIn(ls), run_time=1.6)
        # 13:38.5: «بحيث يقفل مع السهمين u و v شكل مثلث»
        scene.wait(8.5 * SPD)
        scene.play(Indicate(tri, color=C_SUM, scale_factor=1.02), run_time=1.0)

    # ---------- 3) تفكيك المركبات وتوضيح المنطق ----------
    # 13:42.5 - 14:07.5 | «لكن انت ممكن تسال… فاكر لما كنا بنجمع 2 unit + 7 unit = 9 unit…» (25.0s)
    with beat(scene, 25.0):
        rem = MathTex(
            r"2\,\mathrm{unit}", r"+", r"7\,\mathrm{unit}", r"=", r"9\,\mathrm{unit}",
            tex_template=mach_math_template,
            font_size=28,
            color=IVORY_WHITE,
        ).move_to([3.9, 2.7, 0])
        rem[0].set_color(C_U)
        rem[1].set_color(IVORY_WHITE)
        rem[2].set_color(C_V)
        rem[3].set_color(IVORY_WHITE)
        rem[4].set_color(TEAL)
        scene.wait(11.0 * SPD)
        scene.play(FadeIn(rem), run_time=0.8)

    # 14:07.5 - 14:19.5 | «يعني احنا لما جمعنا u علي v جمعنا ارقام e1 علي بعضها وارقام e2 علي بعضها…» (12.0s)
    with beat(scene, 12.0):
        fa = MathTex(
            r"\mathbf{u}", r"+", r"\mathbf{v}", r"=",
            r"(", r"6", r"+", r"3", r")", r"\mathbf{e}_1",
            r"+",
            r"(", r"2", r"+", r"4", r")", r"\mathbf{e}_2",
            tex_template=mach_math_template,
            font_size=30,
            color=IVORY_WHITE,
        ).move_to([3.7, 0.9, 0])

        fa[0].set_color(C_U)
        fa[1].set_color(IVORY_WHITE)
        fa[2].set_color(C_V)
        fa[3].set_color(IVORY_WHITE)
        fa[4].set_color(IVORY_WHITE)
        fa[5].set_color(C_U)
        fa[6].set_color(IVORY_WHITE)
        fa[7].set_color(C_V)
        fa[8].set_color(IVORY_WHITE)
        fa[9].set_color(TEAL)
        fa[10].set_color(IVORY_WHITE)
        fa[11].set_color(IVORY_WHITE)
        fa[12].set_color(C_U)
        fa[13].set_color(IVORY_WHITE)
        fa[14].set_color(C_V)
        fa[15].set_color(IVORY_WHITE)
        fa[16].set_color(TEAL)

        row_y, col_x = O3[1] - 0.22, P(9.35, 0)[0]
        dsx = DashedLine(P(9, 6), P(9, 0), color=C_SUM, stroke_width=2.2, stroke_opacity=0.9, dash_length=0.09)
        dsy = DashedLine(P(9, 6), P(0, 6), color=C_SUM, stroke_width=2.2, stroke_opacity=0.9, dash_length=0.09)
        ext = DashedLine(P(6, 2), P(9, 2), color=C_V, stroke_width=2.2, stroke_opacity=0.9, dash_length=0.09)

        scene.wait(1.5 * SPD)
        scene.play(FadeOut(cu[3]), Create(dsx), Create(dsy), Create(ext), run_time=1.0)

        row_v = _stack(np.array([P(6, 0)[0], row_y, 0.0]), (S, 0), 3, C_V, 3.5)
        col_u = _stack(np.array([col_x, O3[1], 0.0]), (0, S), 2, C_U, 3.5)
        col_v = _stack(np.array([col_x, P(0, 2)[1], 0.0]), (0, S), 4, C_V, 3.5)

        scene.play(
            LaggedStart(*[GrowArrow(a) for a in row_v], lag_ratio=0.15),
            LaggedStart(*[GrowArrow(a) for a in list(col_u) + list(col_v)], lag_ratio=0.12),
            FadeIn(fa, shift=LEFT * 0.2),
            run_time=1.6,
        )

    # 14:19.5 - 14:38.0 | «وزي ما انت ملاحظ ان مركبات المتجه هي 9 و 6… متكرر علي كذا محور» (18.5s)
    with beat(scene, 18.5):
        fb = MathTex(
            r"=",
            r"9", r"\mathbf{e}_1",
            r"+",
            r"6", r"\mathbf{e}_2",
            tex_template=mach_math_template,
            font_size=30,
            color=IVORY_WHITE,
        ).next_to(fa, DOWN, buff=0.35)
        fb.shift(RIGHT * (fa[3].get_left()[0] - fb[0].get_left()[0]))

        fb[0].set_color(IVORY_WHITE)
        fb[1].set_color(C_SUM)
        fb[2].set_color(TEAL)
        fb[3].set_color(IVORY_WHITE)
        fb[4].set_color(C_SUM)
        fb[5].set_color(TEAL)

        scene.wait(1.0 * SPD)
        scene.play(FadeIn(fb, shift=LEFT * 0.2), run_time=1.2)

    # ---------- 4) الشروط الخمسة لعملية الجمع ----------
    # 14:38.0 - 14:50.0 | «وبرضو لو لاحظت هتلاقي ان عملية جمع المتجهات دي شكلها بديهي جدا… نتايج كارثية» (12.0s)
    with beat(scene, 12.0):
        scene.wait(5.5 * SPD)
        cap.set("لو غيرنا طبيعة الفضاء — النتايج ممكن تبقى كارثية!", ERR_RED)

    # 14:50.0 - 15:11.5 | «وده اللي خلي علماء الرياضيات يعملو 5 قوانين او 5 شروط… والشروط دي هي كالتالي:» (21.5s)
    with beat(scene, 21.5):
        scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=0.8)

        hd = _ar("الشروط الخمسة لعملية الجمع", 30, GOLD_BRIGHT, True).move_to([0, 3.0, 0])
        rows = VGroup()
        for i, (a, b) in enumerate(RULES):
            rows.add(VGroup(
                _chip(f"{i + 1}-  {a}", GOLD_LIGHT, w=6.2, h=0.64, size=18),
                _chip(b, LABEL_MUTED, w=2.9, h=0.64, size=16),
            ).arrange(LEFT, buff=0.15))

        rows.arrange(DOWN, buff=0.2).move_to([0, 0.0, 0])

        scene.wait(2.2 * SPD)
        scene.play(FadeIn(hd), run_time=0.7)
        scene.wait(4.3 * SPD)
        scene.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.25) for r in rows], lag_ratio=0.45), run_time=4.0)

        # 15:07.0: «والشروط دي هي كالتالي:»
        scene.wait(5.0 * SPD)
        scene.play(
            LaggedStart(
                *[Indicate(r, color=GOLD_BRIGHT, scale_factor=1.03) for r in rows],
                lag_ratio=0.18,
            ),
            run_time=2.0,
        )

    _exit(scene)


class Dev(Scene):
    def construct(self):
        play_scene05(self)