from manim import *
import numpy as np

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_DARK,
    COPPER_TERRA,
    IVORY_WHITE,
    LABEL_MUTED,
    STONE_AXIS,
    TEAL,
)
from common.latex import mach_math_template
from episode_05_common import *
from common.vector_space_gate import play_vector_space_gate


# ==============================================================
# الحلقة 05 — الفصل 6: البقاء في نفس الفضاء
# (الشرط 1 من 5 — شريط الشروط بيظهر أعلى الشاشة)
# مدة الفصل الفعلية: 02:24.7  (بطاقة الفصل 4.2s + السرد من 15:17.0 حتى 17:37.5؛ ثم _exit داخل فاصل الـ 4.5s قبل الفصل 7)
# ==============================================================


# ---------- أدوات خاصة بلقطة "الإغلاق" (3 متر + 3 متر ≠ 30 درجة / مصفوفة) ----------

def _check(center, s=0.35, color=GOLD_BRIGHT):
    """علامة صح مرسومة (من غير ما نعتمد على خط يدعم ✓)."""
    c = np.asarray(center, float)
    m = VMobject()
    m.set_points_as_corners([
        c + np.array([-0.5 * s, 0.0, 0]),
        c + np.array([-0.15 * s, -0.4 * s, 0]),
        c + np.array([0.6 * s, 0.55 * s, 0]),
    ])
    m.set_stroke(color, 8)
    return m


def _hit_point(start, u, center, radius):
    """نقطة تصادم شعاع (من start باتجاه u) مع محيط دايرة."""
    start, u, center = np.asarray(start, float), np.asarray(u, float), np.asarray(center, float)
    b = float(u @ (start - center))
    c = float((start - center) @ (start - center) - radius ** 2)
    t = -b + np.sqrt(max(b * b - c, 0.0))
    return start + t * u


def _make_frags(start, end, color, n=9):
    """سهم متكسّر لقطع صغيرة (بيتبدّل بالسهم لحظة الاصطدام)."""
    start, end = np.asarray(start, float), np.asarray(end, float)
    d = end - start
    L = float(np.linalg.norm(d))
    u = d / L
    seg = L / n
    return VGroup(*[
        Line(start + u * seg * k, start + u * seg * (k + 0.7), color=color, stroke_width=6)
        for k in range(n)
    ])


def _shatter(frags, u, seed=3):
    """أنيميشن: القطع بترتد لورا وبتلف وتختفي."""
    rs = np.random.RandomState(seed)
    perp = np.array([-u[1], u[0], 0.0])
    anims = []
    for f in frags:
        move = -u * rs.uniform(0.25, 0.9) + perp * rs.uniform(-0.6, 0.6)
        anims.append(f.animate.shift(move).rotate(rs.uniform(-2.2, 2.2)).set_opacity(0))
    return LaggedStart(*anims, lag_ratio=0.05)


CAP_Y = -2.85                             # ارتفاع التعليق السفلي


def _space_circle(center, radius, color=GOLD_LIGHT, fill=0.05):
    """دايرة فضاء: هالة خارجية خافتة + جدار ذهبي + تعبئة خفيفة."""
    c = np.asarray(center, float)
    glow = Circle(radius=radius + 0.1, color=color, stroke_width=12).move_to(c)
    glow.set_stroke(opacity=0.12)
    ring = Circle(radius=radius, color=color, stroke_width=3.2).move_to(c)
    ring.set_fill(color, fill)
    return VGroup(glow, ring)


PLANET_R = 1.2                           # نصف قطر الدواير الصغيرة
PLANET_LABEL_DY = 0.60                    # ارتفاع العنوان جوه الدايرة


def _planet_thermo(center, color):
    """عالم ثاني: فضاء درجات الحرارة (ترمومتر)."""
    c = np.asarray(center, float)
    ring = _space_circle(c, PLANET_R, color, fill=0.06)
    lab = _ar("فضاء درجات الحرارة", 13, color, True).move_to(c + np.array([0, PLANET_LABEL_DY, 0]))
    tube = RoundedRectangle(
        corner_radius=0.07, width=0.15, height=0.8, color=IVORY_WHITE,
        stroke_width=2.2,
    ).move_to(c + np.array([-0.4, -0.2, 0]))
    bulb = Circle(radius=0.15, color=IVORY_WHITE, stroke_width=2.2).move_to(tube.get_bottom() + DOWN * 0.08)
    bulb.set_fill(ERR_RED, 0.9)
    liquid = Rectangle(width=0.07, height=0.5, stroke_width=0).set_fill(ERR_RED, 0.9)
    liquid.move_to(tube.get_bottom() + UP * 0.28)
    val = _tex(r"30^\circ\mathrm{C}", 26, IVORY_WHITE).move_to(c + np.array([0.4, -0.2, 0]))
    return VGroup(ring, lab, tube, bulb, liquid, val)


def _planet_matrix(center, color):
    """عالم ثاني: فضاء المصفوفات (شبكة 4×4 بلون منير وواضح)."""
    c = np.asarray(center, float)
    ring = _space_circle(c, PLANET_R, color, fill=0.06)
    lab = _ar("فضاء المصفوفات", 13, color, True).move_to(c + np.array([0, PLANET_LABEL_DY, 0]))
    cells = VGroup(*[Square(side_length=0.2, color=IVORY_WHITE, stroke_width=1.6) for _ in range(16)])
    cells.arrange_in_grid(4, 4, buff=0.04).move_to(c + np.array([0, -0.2, 0]))
    for k in (0, 5, 10, 15):
        cells[k].set_fill(color, 0.55)
    return VGroup(ring, lab, cells)


def play_scene06(scene):
    _chapter(scene, 6, 'البقاء في نفس الفضاء')
    cap = _Cap(scene)
    cap.y = CAP_Y
    bar = _rules_bar(0)

    # ---------- 1) ناتج جمع متجهين لازم يفضل جوه نفس فضاء المتجهات ----------
    # 15:17.0 - 15:46.5 | «الشرط الاول هو ان حاصل جمع متجه علي متجه تاني… فكرة او concept في عقولنا بس» (29.5s)
    with beat(scene, 29.5):
        scene.play(FadeIn(bar), run_time=0.8)
        circ = _space_circle([0, -0.2, 0], 2.1)
        cl = _ar("فضاء المتجهات", 22, GOLD_LIGHT, True).move_to([0, 1.1, 0])
        O6 = np.array([-1.0, -1.2, 0])
        a6 = _arrow(O6, O6 + np.array([1.3, 0.5, 0]), C_U, 6, 0.2)
        b6 = _arrow(O6 + np.array([1.3, 0.5, 0]), O6 + np.array([1.8, 1.7, 0]), C_V, 6, 0.2)
        s6 = _arrow(O6, O6 + np.array([1.8, 1.7, 0]), C_SUM, 7, 0.14)

        fm = MathTex(
            r"\mathbf{u}", r"+", r"\mathbf{v}", r"\in", r"V",
            tex_template=mach_math_template,
            font_size=40,
            color=IVORY_WHITE,
        ).move_to([3.9, 0.3, 0])
        fm[0].set_color(C_U)
        fm[1].set_color(IVORY_WHITE)
        fm[2].set_color(C_V)
        fm[3].set_color(IVORY_WHITE)
        fm[4].set_color(GOLD_LIGHT)

        scene.play(FadeIn(circ), FadeIn(cl), run_time=1.0)
        scene.play(GrowArrow(a6), GrowArrow(b6), run_time=1.4)
        scene.play(GrowArrow(s6), FadeIn(fm), run_time=1.2)
        scene.wait(5.0 * SPD)  # البقاء لحد انتهاء «بيعيش معاه في نفس فضاء المتجهات» عند 15:27

        grp6 = VGroup(circ, cl, a6, b6, s6, fm)
        scene.play(FadeOut(grp6), run_time=0.6)
        play_vector_space_gate(
            scene, cap=cap, drive_time=6.0, hold=2.5,
            caption="فضاء المتجهات فكرة رياضية — مش مكان فيزيائي",
        )
        scene.play(FadeIn(grp6), run_time=0.8)

    # ---------- 2) مسافات / مصفوفات / كثيرات حدود ----------
    # 15:46.5 - 16:05.0 | «يبقي بناء علي ده… بيعبروا عن مسافات مثلا… خارج فضاء المسافات» (18.5s)
    with beat(scene, 18.5):
        scene.play(FadeOut(VGroup(circ, cl, a6, b6, s6, fm)), run_time=0.6)

        K_S = 0.857
        R_S, Y_S = 1.8, 1.0
        U_S = 0.42 * K_S
        defs = [
            (4.5, "فضاء المسافات", ("ar", "3 متر شرق"), ("ar", "4 متر شمال"), ("ar", "5 متر")),
            (0.0, "فضاء المصفوفات", ("tex", "A"), ("tex", "B"), ("tex", r"A+B")),
            (-4.5, "فضاء كثيرات الحدود", ("tex", "x^2"), ("tex", "x+1"), ("tex", r"x^2+x+1")),
        ]

        def _lab(spec, color, bold=False):
            kind, txt = spec
            return _ar(txt, 14, color, bold) if kind == "ar" else _tex(txt, 24, color)

        spaces, shown, parts = [], [], []
        for x, name, su, sv, sw in defs:
            cen = np.array([x, Y_S, 0.0])
            glow = Circle(radius=R_S + 0.1, color=GOLD_LIGHT, stroke_width=12).move_to(cen)
            glow.set_stroke(opacity=0.12)
            c = Circle(radius=R_S, color=GOLD_LIGHT, stroke_width=3.2).move_to(cen)
            c.set_fill(GOLD_LIGHT, 0.05)
            lab = _ar(name, 17, GOLD_LIGHT, True).move_to(cen + np.array([0, 1.33, 0]))
            Qs = cen + np.array([-0.95 * K_S, -1.1 * K_S, 0])
            e_end = Qs + np.array([3 * U_S, 0, 0])
            n_end = e_end + np.array([0, 4 * U_S, 0])
            u_ = _arrow(Qs, e_end, C_U, 6, 0.2)
            v_ = _arrow(e_end, n_end, C_V, 6, 0.2)
            w_ = _arrow(Qs, n_end, C_SUM, 7, 0.14)
            lu = _lab(su, C_U).next_to(u_, DOWN, buff=0.1)
            lv = _lab(sv, C_V).next_to(v_, RIGHT, buff=0.1)
            lw = _lab(sw, C_SUM, True)
            anchor = Qs + 0.7 * (n_end - Qs) + np.array([-0.8, 0.6, 0.0]) * 0.12
            lw.move_to(anchor + np.array([-lw.width / 2, lw.height / 2, 0.0]))
            shown.append(VGroup(glow, c, lab))
            parts.append((c, u_, v_, w_, lu, lv, lw))
            spaces.append(VGroup(glow, c, lab, u_, v_, w_, lu, lv, lw))

        scene.play(LaggedStart(*[FadeIn(g, scale=0.9) for g in shown], lag_ratio=0.3), run_time=2.0)

        # 15:52.0: «بيعبروا عن مسافات مثلاً... فناتج الجمع لازم يكون متجه في نفس فضاء المسافات»
        scene.wait(2.9 * SPD)
        c, u_, v_, w_, lu, lv, lw = parts[0]
        scene.play(GrowArrow(u_), FadeIn(lu), run_time=0.8)
        scene.play(GrowArrow(v_), FadeIn(lv), run_time=0.8)
        scene.wait(2.0 * SPD)
        scene.play(GrowArrow(w_), FadeIn(lw), run_time=0.9)
        scene.play(Indicate(c, color=GOLD_BRIGHT, scale_factor=1.04), run_time=0.6)

    # 16:05.0 - 16:15.5 | «ولو بجمع متجهين ليهم متجهات اساس بيعبرو عن مصفوفات…» (10.5s)
    with beat(scene, 10.5):
        scene.wait(1.5 * SPD)
        c, u_, v_, w_, lu, lv, lw = parts[1]
        scene.play(GrowArrow(u_), FadeIn(lu), run_time=0.8)
        scene.play(GrowArrow(v_), FadeIn(lv), run_time=0.8)
        scene.wait(1.5 * SPD)
        scene.play(GrowArrow(w_), FadeIn(lw), run_time=0.9)
        scene.play(Indicate(c, color=GOLD_BRIGHT, scale_factor=1.04), run_time=0.6)

    # 16:15.5 - 16:23.0 | «ونفس الكلام لو بجمع متجهات بتتكون من… كثيرة حدود او دوال» (7.5s)
    with beat(scene, 7.5):
        scene.wait(1.2 * SPD)
        c, u_, v_, w_, lu, lv, lw = parts[2]
        scene.play(GrowArrow(u_), FadeIn(lu), run_time=0.8)
        scene.play(GrowArrow(v_), FadeIn(lv), run_time=0.8)
        scene.play(GrowArrow(w_), FadeIn(lw), run_time=0.9)
        scene.play(Indicate(c, color=GOLD_BRIGHT, scale_factor=1.04), run_time=0.6)

    # 16:23.0 - 16:40.5 | «والشرط ده بيسموه شرط الاغلاق الجمعي… عشان ابني منها متجهات الاساس» (17.5s)
    with beat(scene, 17.5):
        nm = _chip(
            "شرط الإغلاق الجمعي = شرط البقاء في نفس الفضاء",
            GOLD_BRIGHT, w=7.6, h=0.7, size=20, filled=True,
        ).move_to([0, -1.65, 0])
        scene.play(FadeIn(nm, shift=UP * 0.15), run_time=1.0)
        # 16:32.0: «والهدف من الشرط ده إنه لازم يكون في نظام واتساق داخلي...»
        scene.wait(8.0 * SPD)
        scene.play(Indicate(nm, color=GOLD_BRIGHT, scale_factor=1.04), run_time=1.0)

    # ---------- 3) مثال المستحيل: شرط الإغلاق يمنع الخروج برا الفضاء ----------
    # 16:40.5 - 17:16.5 | «يعني تخيل نفسك اتحركت 3 متر شرق بعدين 3 متر شمال… نواتج منطقية لعملية الجمع» (36.0s)
    with beat(scene, 36.0):
        scene.play(FadeOut(VGroup(*spaces, nm)), run_time=0.6)

        CEN2, R2 = np.array([-2.6, 0.75, 0.0]), 2.1
        wall_glow = Circle(radius=R2 + 0.12, color=GOLD_LIGHT, stroke_width=12).move_to(CEN2)
        wall_glow.set_stroke(opacity=0.12)
        wall = Circle(radius=R2, color=GOLD_LIGHT, stroke_width=3.5).move_to(CEN2)
        wall.set_fill(GOLD_LIGHT, 0.05)
        cl2 = _ar("فضاء المسافات", 20, GOLD_LIGHT, True).move_to(CEN2 + np.array([0, 1.55, 0]))

        Q = CEN2 + np.array([-0.95, -1.1, 0])
        e_end = Q + np.array([1.26, 0, 0])
        n_end = e_end + np.array([0, 1.26, 0])
        e_ = _arrow(Q, e_end, C_U, 6, 0.2)
        n_ = _arrow(e_end, n_end, C_V, 6, 0.2)
        lab_e = _ar("3 متر شرق", 16, C_U).next_to(e_, DOWN, buff=0.1)
        lab_n = _ar("3 متر شمال", 16, C_V).next_to(n_, RIGHT, buff=0.1)

        scene.play(Create(wall_glow), Create(wall), FadeIn(cl2), run_time=0.9)
        scene.play(GrowArrow(e_), FadeIn(lab_e), run_time=0.9)
        scene.wait(1.0 * SPD)
        scene.play(GrowArrow(n_), FadeIn(lab_n), run_time=0.9)

        scene.wait(1.5 * SPD)
        s_ok = _arrow(Q, n_end, C_SUM, 7, 0.14)
        mid = (Q + n_end) / 2
        nrm = np.array([-0.8, 0.6, 0.0])
        lab_s = _ar("~4.24 متر", 18, C_SUM, True).move_to(mid + nrm * 0.5)
        ok_grp = VGroup(s_ok, lab_s)
        scene.play(GrowArrow(s_ok), FadeIn(lab_s), run_time=1.0)
        cap.set("3 متر + 3 متر ≈ 4.24 متر — والناتج لسه جوه فضاء المسافات", GOLD_BRIGHT)
        scene.wait(1.0 * SPD)

        # 16:48.9: «وبعد ما توصل تلاقي إن المسافة الكلية...»
        P1, P2 = np.array([4.7, 1.75, 0.0]), np.array([4.7, -1.30, 0.0])
        pl1 = _planet_thermo(P1, COPPER_TERRA)
        pl2 = _planet_matrix(P2, TEAL)
        scene.play(LaggedStart(FadeIn(pl1, scale=0.9), FadeIn(pl2, scale=0.9), lag_ratio=0.4), run_time=1.4)

        bad_chip = _chip("3 متر + 3 متر = 30 درجة سيليزية ؟!", ERR_RED, w=5.4, h=0.6, size=17).move_to(
            [CEN2[0], -2.05, 0])
        scene.play(FadeIn(bad_chip, shift=UP * 0.1), ok_grp.animate.set_opacity(0.3), run_time=0.7)

        def attempt(target, seed):
            d = target - Q
            u = d / np.linalg.norm(d)
            H = _hit_point(Q, u, CEN2, R2)
            bad = _arrow(Q, H + u * 0.22, ERR_RED, 6, 0.2)
            scene.play(GrowArrow(bad), run_time=1.0)
            flash = Circle(radius=0.12, color=ERR_RED, stroke_width=5).move_to(H)
            frags = _make_frags(Q + u * 0.4, H + u * 0.22, ERR_RED)
            scene.remove(bad)
            scene.add(frags, flash)
            scene.play(
                flash.animate.scale(5).set_stroke(opacity=0),
                Indicate(wall, color=ERR_RED, scale_factor=1.05),
                run_time=0.6,
            )
            scene.play(_shatter(frags, u, seed), run_time=0.9)
            scene.remove(frags, flash)
            ghost = DashedLine(
                H + u * 0.15, target - u * (PLANET_R + 0.15),
                color=ERR_RED, dash_length=0.12, stroke_width=3,
            )
            ghost.set_opacity(0.6)
            xh = _cross([H[0], H[1]], 0.3)
            scene.play(FadeIn(ghost), Create(xh), run_time=0.6)
            scene.wait(0.7 * SPD)
            return ghost, xh

        # 16:51.0: محاولة 30°C
        g1, x1 = attempt(P1, 3)

        # 16:56.0: محاولة مصفوفة 4×4
        scene.wait(1.2 * SPD)
        bad_chip2 = _chip("3 متر + 3 متر = مصفوفة 4×4 ؟!", ERR_RED, w=5.4, h=0.6, size=17).move_to(
            [CEN2[0], -2.05, 0])
        scene.play(ReplacementTransform(bad_chip, bad_chip2), run_time=0.6)
        g2, x2 = attempt(P2, 7)

        # 17:00.5: «ساعتها إنت من نفسك هتقول ده مستحيل يحصل...»
        cap.set("لو الناتج خرج برا الفضاء — ده مستحيل", ERR_RED)
        scene.wait(5.8 * SPD)

        # 17:07.5: «أهو شرط الإغلاق ده بيضمنلك إن الموقف الغريب ده مايحصلش...»
        scene.play(FadeOut(VGroup(g1, x1, g2, x2, bad_chip2)), run_time=0.7)
        ck = _check(n_end + np.array([0.55, 0.3, 0]), 0.4)
        scene.play(ok_grp.animate.set_opacity(1.0), Create(ck), run_time=1.3)
        cap.set("شرط الإغلاق: الناتج لازم يفضل جوه نفس الفضاء", GOLD_BRIGHT)
        scene.wait(2.5 * SPD)
        scene.play(
            wall_glow.animate.set_stroke(opacity=0.4),
            Indicate(wall, color=GOLD_BRIGHT, scale_factor=1.04),
            run_time=1.4,
        )

    # ---------- 4) الصيغة الرياضية: مجموع الحدود v_i e_i ----------
    # 17:16.5 - 17:37.5 | «وده كله معناه بالنسبة للصيغة الرياضية… يكون متجه في نفس فضاء المتجهات» (21.0s)
    with beat(scene, 21.0):
        scene.play(*[FadeOut(m) for m in list(scene.mobjects) if m is not bar and m is not cap.cur], run_time=0.7)

        fv = MathTex(
            r"\mathbf{v}",
            r"=",
            r"v_1\mathbf{e}_1",
            r"+",
            r"v_2\mathbf{e}_2",
            r"+",
            r"v_3\mathbf{e}_3",
            r"+",
            r"\cdots",
            r"+",
            r"v_n\mathbf{e}_n",
            tex_template=mach_math_template,
            font_size=40,
            color=IVORY_WHITE,
        ).move_to([0, 1.5, 0])

        fv[0].set_color(GOLD_BRIGHT)
        fv[1].set_color(IVORY_WHITE)
        fv[2].set_color(C_U)
        fv[3].set_color(IVORY_WHITE)
        fv[4].set_color(C_V)
        fv[5].set_color(IVORY_WHITE)
        fv[6].set_color(TEAL)
        fv[7].set_color(IVORY_WHITE)
        fv[8].set_color(LABEL_MUTED)
        fv[9].set_color(IVORY_WHITE)
        fv[10].set_color(GOLD_LIGHT)

        # 17:19.7: «معناه بالنسبة للصيغة الرياضية...»
        scene.wait(2.5 * SPD)
        scene.play(FadeIn(fv), run_time=1.2)

        note1 = VGroup(
            _ar("كل حد", 22, GOLD_LIGHT, True),
            _tex(r"(v_i\mathbf{e}_i)", 24, GOLD_BRIGHT),
            _ar("متجه لوحده", 22, GOLD_LIGHT, True),
        ).arrange(LEFT, buff=0.16).move_to([0, 0.3, 0])

        note2 = MathTex(
            r"\Rightarrow",
            r"\mathbf{v}",
            r"\in",
            r"V",
            tex_template=mach_math_template,
            font_size=44,
            color=IVORY_WHITE,
        ).move_to([0, -0.6, 0])

        note2[0].set_color(IVORY_WHITE)
        note2[1].set_color(GOLD_BRIGHT)
        note2[2].set_color(IVORY_WHITE)
        note2[3].set_color(GOLD_LIGHT)

        # 17:25.4: «لما أجمع عناصر المتجه...»
        scene.wait(4.5 * SPD)
        scene.play(FadeIn(note1), run_time=0.8)

        # 17:31.5: «لازم الناتج بتاعهم اللي هو v يكون متجه في نفس فضاء المتجهات»
        scene.wait(5.3 * SPD)
        scene.play(FadeIn(note2, shift=UP * 0.1), Indicate(fv[0], color=GOLD_BRIGHT, scale_factor=1.3), run_time=0.9)

    _exit(scene)


class Dev(Scene):
    def construct(self):
        play_scene06(self)