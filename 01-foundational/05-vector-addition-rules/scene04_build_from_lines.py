from manim import *
import numpy as np

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_MUTED,
    GOLD_DARK,
    COPPER_TERRA,
    IVORY_WHITE,
    TEAL,
)
from episode_05_common import *
from common.mobjects import speech_bubble
from common.mobjects.characters import mach_mathematician


# ==============================================================
# الحلقة 05 — الفصل 4: كيف نبني المتجهات من كذا خط؟
# مدة الفصل الفعلية: 03:47.7  (بطاقة الفصل 4.2s + السرد من 08:05.0 حتى 11:48.5؛ ثم _exit داخل فاصل الـ 5.5s قبل الفصل 5)
# ==============================================================


def play_scene04(scene):
    _chapter(scene, 4, 'كيف نبني المتجهات من كذا خط؟')
    cap = _Cap(scene, y=-2.85)
    S = 0.6                                            # ضلع المربع الواحد = طول متجه الأساس (صغير عشان u+v=(9,6) تنزل في الشبكة)
    gr = MachAxes2D(
        center=np.array([-5.4, -1.2, 0.0]),
        x_range=(-1, 10),
        y_range=(-1, 7),
        grid_step=S,
        number_font_size=16,
        number_buff=0.40,
        show_minor_ticks=False,
        show_origin=True,
    )
    for _l in [l for l in gr.labels if l.text == "-1"]:   # رقم -1 بيزحم الصفر على الشبكة الصغيرة
        gr.labels.remove(_l)
        gr.remove(_l)
    grid = gr.grid                                      # الشبكة بتتفصل: بتظهر آخر الفصل مكان السقالات
    gr.remove(grid)
    grid.set_z_index(-1)
    gr.grid = VGroup()
    P = lambda x, y: gr.c2p(x, y)
    O3 = P(0, 0)

    def num_label(axis, val):
        """رقم التدريج على المحور (عشان نلوّنه مع المركّبة)."""
        target = gr.c2p(val, 0) + DOWN * 0.40 if axis == "x" else gr.c2p(0, val) + LEFT * 0.40
        return min(gr.labels, key=lambda l: np.linalg.norm(l.get_center() - target))

    # ---------- 1) من خط أعداد واحد لشبكة أبعاد (مع الشخصية + بالونة السؤال + حركة حرة استعراضية) ----------
    # 08:05.0 - 08:43.0 | «طيب دلوقتي بعد ما شوفنا… ماذا لو كان عندنا أكتر من خط… حركة حرة في الفراغ… لخطين بس» (38.0s)
    with beat(scene, 38.0):
        gr.animate_creation(scene, run_time=2.4)          # محاور وأرقام بس، من غير شبكة

        avatar = mach_mathematician(
            color=COPPER_TERRA,
            accent_color=GOLD_LIGHT,
            pose="thinking",
            scale=1.05,
            blink=True,
            breathing=True,
            glasses=True,
            tie_type="bowtie",
        ).move_to([4.1, -0.6, 0])

        box_q, dots_q, text_q = speech_bubble(
            lines_text=["ماذا لو: أكتر من خط", "بمتجهات أساس مختلفة؟"],
            anchor_head=avatar[0],
            color=GOLD_LIGHT,
            font_size=20,
            shift=LEFT * 0.4 + UP * 0.15,
        )

        scene.play(FadeIn(avatar, shift=UP * 0.2), run_time=0.9)
        scene.wait(4.7 * SPD)

        # 08:13.0: «عاوزين نعرف ماذا لو كان عندنا أكتر من خط...»
        scene.play(
            FadeIn(dots_q, scale=0.5),
            FadeIn(box_q, scale=0.9),
            FadeIn(text_q, shift=LEFT * 0.2),
            run_time=0.8,
        )
        scene.wait(10.7 * SPD)

        # 08:24.5: «ساعتها خط الأعداد هيتمدد ويتحول لشبكة أبعاد»
        cap.set("خط الأعداد هيتمدد ويتحول لشبكة أبعاد")

        # حركة حرة في الفراغ وقت جملة 08:29.5
        explorer = _dot(O3, GOLD_BRIGHT, 0.09)
        trail = TracedPath(
            explorer.get_center, stroke_color=GOLD_LIGHT, stroke_width=2.5,
            stroke_opacity=0.65, dissipating_time=1.4,
        )
        free_vec = always_redraw(
            lambda: _arrow(O3, explorer.get_center(), COPPER_TERRA, 4, 0.2)
            if np.linalg.norm(explorer.get_center() - O3) > 0.25 else VGroup()
        )
        scene.add(trail, free_vec, explorer)
        for pt, dt in [(P(4, 2), 1.6), (P(2, 5), 1.6), (P(7, 4), 1.6), (P(5, 1.5), 1.4)]:
            scene.play(explorer.animate.move_to(pt), run_time=dt * SPD)
        scene.wait(3.0 * SPD)

        # تنظيف سلس قبل بداية Beat 2 (نوقف الرمش والتنفس قبل FadeOut عشان الشفافية ما ترجعش 1.0)
        avatar._blink_enabled = False
        avatar._breathing_enabled = False
        avatar.clear_updaters()
        free_vec.clear_updaters()
        trail.clear_updaters()
        scene.play(
            FadeOut(box_q),
            FadeOut(dots_q),
            FadeOut(text_q),
            FadeOut(avatar, shift=RIGHT * 0.3),
            FadeOut(VGroup(explorer, trail, free_vec)),
            run_time=0.9,
        )
        # 08:38.5: «لخطين بس عشان أقدر أوضح الفكرة ببساطة»
        scene.play(
            ShowPassingFlash(Line(P(-1, 0), P(10, 0), color=GOLD_BRIGHT, stroke_width=6), time_width=0.5),
            ShowPassingFlash(Line(P(0, -1), P(0, 7), color=COPPER_TERRA, stroke_width=6), time_width=0.5),
            run_time=1.3,
        )

    # ---------- 2) خطان x و y متعامدان عند نقطة الصفر ----------
    # 08:43.0 - 09:08.5 | «تخيل ان انا عندي خطين متعامدين علي بعض… والخطين متقاطعين عند الصفر…» (25.5s)
    with beat(scene, 25.5):
        # 08:45.0: «خطين متعامدين على بعض» -> علامة الزاوية القائمة
        scene.wait(2.0 * SPD)
        perp = VMobject().set_points_as_corners([
            P(0.45, 0), P(0.45, 0.45), P(0, 0.45),
        ]).set_stroke(GOLD_LIGHT, 2.6)
        scene.play(Create(perp), run_time=1.0)

        # 08:52.0: «في خط منهم اسمه X وخط تاني اسمه Y»
        scene.wait(5.5 * SPD)
        scene.play(
            ShowPassingFlash(Line(P(-1, 0), P(10, 0), color=GOLD_BRIGHT, stroke_width=5), time_width=0.4),
            ShowPassingFlash(Line(P(0, -1), P(0, 7), color=COPPER_TERRA, stroke_width=5), time_width=0.4),
            run_time=1.2,
        )

        # 09:05.5: «متقاطعين عند نقطة التعامد... النقطة صفر لفضاء المتجهات»
        scene.wait(7.0 * SPD)
        o_ring = Circle(radius=0.12, color=GOLD_BRIGHT, stroke_width=4).move_to(O3)
        scene.add(o_ring)
        scene.play(o_ring.animate.scale(4.5).set_stroke(opacity=0), run_time=1.0)
        scene.remove(o_ring)
        cap.set("نقطة التعامد = النقطة 0 لفضاء المتجهات", GOLD_LIGHT)
        scene.wait(2.0 * SPD)
        scene.play(FadeOut(perp), run_time=0.6)

    # ---------- 3) متجها الأساس e1 و e2 ومربع الوحدة ----------
    # 09:08.5 - 09:26.5 | «وكل خط فيهم ليه متجه أساس مختلف عن التاني…» (18.0s)
    with beat(scene, 18.0):
        scene.wait(1.5 * SPD)
        e1 = _arrow(P(0, 0), P(1, 0), GOLD_BRIGHT, 6, 0.35)
        e2 = _arrow(P(0, 0), P(0, 1), COPPER_TERRA, 6, 0.35)
        unit_sq = Polygon(P(0, 0), P(1, 0), P(1, 1), P(0, 1), stroke_width=0, fill_color=GOLD_BRIGHT, fill_opacity=0.10)
        scene.play(GrowArrow(e1), GrowArrow(e2), run_time=1.2)
        scene.play(FadeIn(unit_sq), run_time=0.6)
        scene.wait(4.5 * SPD)
        scene.play(Indicate(e1, color=GOLD_BRIGHT), Indicate(e2, color=COPPER_TERRA), run_time=1.0)

    # ---------- 4) أمثلة على ما يعبّر عنه متجه الأساس ----------
    # 09:26.5 - 09:40.5 | «يعني ممكن متجهات الاساس دي تكون بتعبر عن مسافة بالمتر او الخشبة او مصفوفة…» (14.0s)
    with beat(scene, 14.0):
        what = VGroup(*[
            _chip(t, TEAL, w=3.4, h=0.55, size=16)
            for t in ["متر", "خشبة", "مصفوفة أو أي كائن رياضي"]
        ]).arrange(DOWN, buff=0.18).move_to([4.9, 1.2, 0])
        what_t = _ar("متجه الأساس ممكن يعبّر عن:", 18, GOLD_LIGHT, True).next_to(what, UP, buff=0.25)

        scene.wait(3.2 * SPD)
        scene.play(FadeIn(what_t), run_time=0.6)
        scene.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in what], lag_ratio=0.55), run_time=3.6)

    # ---------- 5) تسمية e1 و e2 ----------
    # 09:40.5 - 09:58.0 | «بعدين كل متجه أساس هنديله رمز… على الخط x رمز e1… على الخط y رمز e2» (17.5s)
    with beat(scene, 17.5):
        le1 = _tex(r"\mathbf{e}_1", 28, GOLD_BRIGHT).move_to(gr.c2p(0.5, 0) + DOWN * 0.22)
        le2 = _tex(r"\mathbf{e}_2", 28, COPPER_TERRA).move_to(gr.c2p(0, 0.5) + LEFT * 0.26)
        scene.wait(7.0 * SPD)
        scene.play(FadeIn(le1), Indicate(e1, color=GOLD_BRIGHT), run_time=0.9)
        scene.wait(4.5 * SPD)
        scene.play(FadeIn(le2), Indicate(e2, color=COPPER_TERRA), run_time=0.9)

    # ---------- 6) رص مربع الوحدة = سقالات = نظام الإحداثيات الكارتيزية ----------
    # 09:58.0 - 10:18.0 | «ولو فهمت الحلقة اللي فاتت كويس هتلاحظ اننا لو رصينا متجهات الاساس…» (20.0s)
    with beat(scene, 20.0):
        scene.play(FadeOut(VGroup(what, what_t)), run_time=0.5)
        base = VGroup(unit_sq, e1, e2)
        C0 = unit_sq.get_center()
        tiles = []
        for i in range(10):
            for j in range(7):
                if i == 0 and j == 0:
                    continue
                t = base.copy().shift(RIGHT * i * S + UP * j * S)
                t[0].set_stroke(GOLD_MUTED, 1.0, opacity=0.5)
                t[1].set_stroke(width=3)
                t[2].set_stroke(width=3)
                tiles.append(t)
        tiles.sort(key=lambda t: np.linalg.norm(t.get_center() - C0))

        # 10:02.0: «لو رصينا متجهات الأساس دي جنب بعض... تغطي الفضاء بالكامل»
        scene.wait(3.5 * SPD)
        scene.play(LaggedStart(*[FadeIn(t, scale=0.7) for t in tiles], lag_ratio=0.025), run_time=3.8)
        scene.wait(2.2 * SPD)

        # 10:08.5: «شكل شبه السقالات... نظام الإحداثيات الكارتيزية»
        far = list(reversed(tiles))
        collapse = LaggedStart(*[t.animate.move_to(C0).scale(0.25).set_opacity(0) for t in far], lag_ratio=0.02)

        def _key(l):
            c = l.get_center() - O3
            return c[0] if l.width < l.height else c[1]

        lines = sorted(grid, key=_key, reverse=True)
        grow = LaggedStart(*[Create(l) for l in lines], lag_ratio=0.05)
        scene.play(collapse, grow, run_time=3.6)
        scene.remove(*tiles)
        gr.add(grid)
        gr.grid = grid
        cap.set("نظام الإحداثيات الكارتيزية", GOLD_LIGHT)

    # ---------- 7) المتجهان u=[6,2] و v=[3,4] ومركباتهما وصيغتاهما ----------
    # 10:18.0 - 10:40.5 | «تخيل بقي ان انا عندي متجهين واحد هنسميه u والتاني هنسميه v…» (22.5s)
    with beat(scene, 22.5):
        scene.play(FadeOut(VGroup(le1, le2, unit_sq, e1, e2)), run_time=0.6)
        u = _arrow(P(0, 0), P(6, 2), C_U, 7, 0.14)
        lu = _tex(r"\mathbf{u}", 38, C_U).next_to(u.get_end(), UP, buff=0.12)
        v = _arrow(P(0, 0), P(3, 4), C_V, 7, 0.14)
        lv = _tex(r"\mathbf{v}", 38, C_V).next_to(v.get_end(), RIGHT, buff=0.12)

        scene.wait(2.0 * SPD)
        scene.play(GrowArrow(u), FadeIn(lu), run_time=1.0)
        scene.wait(2.0 * SPD)
        scene.play(GrowArrow(v), FadeIn(lv), run_time=1.0)
        scene.wait(6.0 * SPD)
        cap.set("كل متجه هياخد قايمة من رقمين داخل نظام الإحداثيات", GOLD_LIGHT)

    # 10:40.5 - 10:52.5 | «القايمة الخاصة بـ u هتكون [6, 2] والقايمة الخاصة بـ v هتكون [3, 4]» (12.0s)
    with beat(scene, 12.0):
        card_u = _tex(r"\mathbf{u}=\begin{bmatrix}6\\2\end{bmatrix}", 36, C_U).move_to([4.9, 1.9, 0])
        card_v = _tex(r"\mathbf{v}=\begin{bmatrix}3\\4\end{bmatrix}", 36, C_V).move_to([4.9, -0.5, 0])
        scene.wait(2.5 * SPD)
        scene.play(FadeIn(card_u, shift=LEFT * 0.2), run_time=0.8)
        scene.wait(3.0 * SPD)
        scene.play(FadeIn(card_v, shift=LEFT * 0.2), run_time=0.8)

    # 10:52.5 - 11:10.5 | «اول رقم في قايمة u (6) علي x وتاني رقم (2) علي y» (18.0s)
    with beat(scene, 18.0):
        dx_u = DashedLine(P(6, 2), P(6, 0), color=C_U, stroke_width=2.2, stroke_opacity=0.9, dash_length=0.09)
        dy_u = DashedLine(P(6, 2), P(0, 2), color=C_U, stroke_width=2.2, stroke_opacity=0.9, dash_length=0.09)
        bx_u = _stack(np.array([O3[0], O3[1] - 0.16, 0.0]), (S, 0), 6, C_U, 3.5)
        by_u = _stack(np.array([P(6.35, 0)[0], O3[1], 0.0]), (0, S), 2, C_U, 3.5)
        nx_u, ny_u = num_label("x", 6), num_label("y", 2)

        scene.wait(1.5 * SPD)
        scene.play(Create(dx_u), Create(dy_u), run_time=0.9)
        scene.play(
            LaggedStart(*[GrowArrow(a) for a in bx_u], lag_ratio=0.12),
            nx_u.animate.set_color(C_U).scale(1.25),
            run_time=1.2,
        )
        scene.wait(5.5 * SPD)
        scene.play(
            LaggedStart(*[GrowArrow(a) for a in by_u], lag_ratio=0.12),
            ny_u.animate.set_color(C_U).scale(1.25),
            run_time=1.0,
        )

    # 11:10.5 - 11:27.5 | «ونفس الكلام لـ v: اول رقم (3) علي x وتاني رقم (4) علي y» (17.0s)
    with beat(scene, 17.0):
        dx_v = DashedLine(P(3, 4), P(3, 0), color=C_V, stroke_width=2.2, stroke_opacity=0.9, dash_length=0.09)
        dy_v = DashedLine(P(3, 4), P(0, 4), color=C_V, stroke_width=2.2, stroke_opacity=0.9, dash_length=0.09)
        bx_v = _stack(np.array([O3[0], P(0, 4.35)[1], 0.0]), (S, 0), 3, C_V, 3.5)
        by_v = _stack(np.array([O3[0] - 0.16, O3[1], 0.0]), (0, S), 4, C_V, 3.5)
        nx_v, ny_v = num_label("x", 3), num_label("y", 4)

        scene.wait(2.5 * SPD)
        scene.play(Create(dx_v), Create(dy_v), run_time=0.9)
        scene.play(
            LaggedStart(*[GrowArrow(a) for a in bx_v], lag_ratio=0.12),
            nx_v.animate.set_color(C_V).scale(1.25),
            run_time=1.1,
        )
        scene.wait(4.0 * SPD)
        scene.play(
            LaggedStart(*[GrowArrow(a) for a in by_v], lag_ratio=0.12),
            ny_v.animate.set_color(C_V).scale(1.25),
            run_time=1.1,
        )

    # 11:27.5 - 11:41.5 | «بعد كدة الصيغة الرياضية: v = 3e1 + 4e2 و u = 6e1 + 2e2» (14.0s)
    with beat(scene, 14.0):
        comp_v = _tex(r"\mathbf{v}=3\mathbf{e}_1+4\mathbf{e}_2", 30, C_V).move_to([4.7, -1.5, 0])
        comp_u = _tex(r"\mathbf{u}=6\mathbf{e}_1+2\mathbf{e}_2", 30, C_U).move_to([4.7, 0.9, 0])
        scene.wait(5.5 * SPD)
        scene.play(FadeIn(comp_v, shift=LEFT * 0.2), run_time=0.9)
        scene.wait(3.5 * SPD)
        scene.play(FadeIn(comp_u, shift=LEFT * 0.2), run_time=0.9)

    # ---------- 8) نرسمهم ونشوف شكلهم هندسيًا ----------
    # 11:41.5 - 11:48.5 | «خلينا بقي نرسم المتجهات دي ونشوف شكلها عامل ازاي هندسيا داخل فضاء…» (7.0s)
    with beat(scene, 7.0):
        scene.wait(1.5 * SPD)
        scene.play(Indicate(u, color=C_U), Indicate(v, color=C_V), run_time=1.2)

    _exit(scene)


class Dev(Scene):
    def construct(self):
        play_scene04(self)