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
from episode_05_common import *


# ==============================================================
# الحلقة 05 — الفصل 8: القدرة على العودة
# (الشرط 3 من 5 — شريط الشروط بيظهر أعلى الشاشة)
# مدة الفصل الفعلية: 02:00.0  (بطاقة الفصل 4.2s + السرد من 20:12.0 حتى 22:12.0؛ ثم _exit داخل فاصل الـ 6s قبل الفصل 9)
# التخطيط: شبكة MachAxes2D على الشمال — ولوحة الكلام على اليمين بعيد عن الرسمة.
# الألوان: v أصفر ذهبي، −v نحاسي، الصفر ذهبي ناصع، المركّبات أبيض، متجهات الأساس ذهبي فاتح.
# ==============================================================

PX = 4.25                                   # مركز لوحة الكلام (اليمين)
CV, CU, ZB, CC, EC, OP = C_V, C_U, GOLD_BRIGHT, IVORY_WHITE, GOLD_LIGHT, STONE_AXIS


def _rtl(parts, buff=0.14):
    """سطر عربي فيه رموز لاتينية: الأجزاء بترتيب القراءة (الأول = أقصى اليمين)."""
    return VGroup(*parts[::-1]).arrange(RIGHT, buff=buff)


def _ctex(tokens, size):
    """معادلة ملوّنة: كل جزء (نص، لون) بيتكتب ويتلوّن لوحده."""
    m = MathTex(*[t for t, _ in tokens], tex_template=mach_math_template, font_size=size)
    for sub, (_, col) in zip(m, tokens):
        sub.set_color(col)
    return m


def play_scene08(scene):
    _chapter(scene, 8, 'القدرة على العودة')
    cap = _Cap(scene, y=-2.85)               # الجملة الدهبية مرفوعة عشان الترجمة تلاقي مكان تحتها
    bar = _rules_bar(2)
    S = 0.6                                  # نفس شبكة الفصل 4 و5 و7
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

    def ripple(pos, color=ZB, n=2, dur=0.9):
        for _ in range(n):
            ring = Circle(radius=0.12, color=color, stroke_width=4).move_to(pos)
            scene.add(ring)
            scene.play(ring.animate.scale(5).set_stroke(opacity=0), run_time=dur)
            scene.remove(ring)

    def tag(txt, y):
        return _chip(txt, COPPER_TERRA, w=2.7, h=0.46, size=14, filled=True).move_to([5.35, y, 0])

    # ---------- 1) المتجه المعكوس −v بيلغي تأثير v ويرجّعنا للأصل ----------
    # 20:12.0 - 20:55.5 | «تالت شرط هو انه لكل متجه v… لنفس النقطة اللي اتحركت منها في البداية» (43.5s)
    with beat(scene, 43.5):
        scene.play(FadeIn(bar), run_time=0.8)
        gr.animate_creation(scene, run_time=1.4)
        title = _chip("المعكوس الجمعي", ZB, w=4.6, h=0.62, size=20, filled=True).move_to([PX, 2.6, 0])
        zero = _dot(O, ZB, 0.12)
        scene.play(FadeIn(title, shift=DOWN * 0.1), FadeIn(zero), run_time=0.8)

        # 20:16.0: نمشي لبعيد على v
        scene.wait(1.0 * SPD)
        tip = P(5, 3)
        v = _arrow(O, tip, CV, 7, tip=0.14)
        lv = _tex(r"\mathbf{v}", 38, CV)
        tv = _tex(r"(5,\,3)", 26, CV)
        lab_v = VGroup(lv, tv).arrange(RIGHT, buff=0.14).next_to(tip, UP, buff=0.12)
        scene.play(GrowArrow(v), FadeIn(lab_v), run_time=1.1)
        walker = _dot(O, CC, 0.1)
        scene.play(FadeIn(walker), walker.animate.move_to(tip), run_time=1.5)

        # 20:26.0: «المتجه اللي بيلغي التأثير ده بنسميه المتجه المعكوس»
        scene.wait(7.4 * SPD)
        d = (tip - O) / np.linalg.norm(tip - O)
        nrm = np.array([d[1], -d[0], 0.0])                  # ناحية يمين/تحت
        off = nrm * 0.17
        mv = _arrow(tip + off, O + off, CU, 7, tip=0.14)
        lmv = _tex(r"-\mathbf{v}", 38, CU)
        tmv = _tex(r"(-5,\,-3)", 26, CU)
        lab_mv = VGroup(lmv, tmv).arrange(RIGHT, buff=0.14).move_to((tip + O) / 2 + nrm * 0.75)
        scene.play(GrowArrow(mv), FadeIn(lab_mv), run_time=1.2)
        scene.play(walker.animate.move_to(O), run_time=1.5)
        ripple(O, n=1)

        # 20:32.0: «وبنرمز ليه بالرمز -v... هو المتجه الأصلي بإشارة سالب»
        scene.wait(2.4 * SPD)
        f1 = _ctex([
            (r"\mathbf{v}", CV), ("+", OP), ("(", OP), (r"-\mathbf{v}", CU), (")", OP),
            ("=", OP), (r"\mathbf{0}", ZB),
        ], 44).move_to([PX, 1.45, 0])
        scene.play(FadeIn(f1, shift=LEFT * 0.2), run_time=0.9)

        scene.wait(2.0 * SPD)
        f2 = _ctex([(r"(5,\,3)", CV), ("+", OP), (r"(-5,\,-3)", CU), ("=", OP), (r"(0,\,0)", ZB)], 30).move_to([PX, 0.6, 0])
        scene.play(FadeIn(f2, shift=UP * 0.1), run_time=0.8)

        scene.wait(1.5 * SPD)
        c1 = _chip("نفس الطول — عكس الاتجاه تمامًا", CU, w=4.8, h=0.6, size=17).move_to([PX, -0.4, 0])
        scene.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)

        # 20:42.0: «عشان كده الشرط ده اسمه شرط المعكوس الجمعي، وإنت تقدر تسميه شرط القدرة على العودة»
        scene.wait(4.1 * SPD)
        c2 = _chip("بيرجعنا لنقطة الأصل", ZB, w=4.8, h=0.6, size=17).move_to([PX, -1.2, 0])
        scene.play(FadeIn(c2, shift=UP * 0.1), run_time=0.7)
        cap.set("شرط المعكوس الجمعي = شرط القدرة على العودة", GOLD_LIGHT)

        b1 = VGroup(v, lab_v, mv, lab_mv, walker, f1, f2, c1, c2)

    # ---------- 2) السقالات طرق رايح-جاي: لكل خطوة v خطوة مضادة −v بنفس الطول ----------
    # 20:55.5 - 21:38.5 | «يعني بعبارة تانية: متجهات الأساس والسقالات… وتشيل أثر الحركة تماماً» (43.0s)
    with beat(scene, 43.0):
        scene.play(FadeOut(b1), FadeOut(title), run_time=0.7)
        o = 0.11  # إزاحة أنعم تبعد الأسهم السفلية عن أرقام محور X
        pts_f = [O + np.array([0, o, 0]), P(5, 0) + np.array([-o, o, 0]), P(5, 3) + np.array([-o, 0, 0])]
        pts_b = [P(5, 3) + np.array([o, 0, 0]), P(5, 0) + np.array([o, -o, 0]), O + np.array([0, -o, 0])]

        def steps(pts, color, ns=(5, 3)):
            out = []
            for (a, b), n in zip(zip(pts[:-1], pts[1:]), ns):
                for i in range(n):
                    out.append(_arrow(a + (b - a) * i / n, a + (b - a) * (i + 1) / n, color, 4, tip=0.38))
            return VGroup(*out)

        fwd, bwd = steps(pts_f, CV), steps(pts_b, CU, ns=(3, 5))

        key = VGroup(
            _chip("رايح — خطوات للأمام", CV, w=4.6, h=0.6, size=18),
            _chip("جاي — نفس الخطوات بالعكس", CU, w=4.6, h=0.6, size=18),
        ).arrange(DOWN, buff=0.25).move_to([PX, 2.3, 0])

        scene.wait(1.3 * SPD)
        scene.play(FadeIn(key, shift=DOWN * 0.1), run_time=0.8)

        # 21:01.0: السقالة للأمام («طرق مزدوجة رايح جاي...»)
        scene.wait(2.7 * SPD)
        scene.play(LaggedStart(*[GrowArrow(a) for a in fwd], lag_ratio=0.18), run_time=3.5)

        # 21:13.0: «لكل خطوة v مشيتها للأمام...»
        scene.wait(8.5 * SPD)
        rule = _rtl([
            _ar("لكل خطوة", 21, CC, True), _tex(r"\mathbf{v}", 34, CV),
            _ar("خطوة مضادة", 21, CC, True), _tex(r"-\mathbf{v}", 34, CU),
        ]).move_to([PX, 0.9, 0])
        scene.play(FadeIn(rule, shift=LEFT * 0.15), run_time=0.9)

        # 21:18.0: السقالة بالعكس («وجود خطوة مضادة اسمها -v»)
        scene.wait(4.1 * SPD)
        scene.play(LaggedStart(*[GrowArrow(a) for a in bwd], lag_ratio=0.18), run_time=3.5)

        # 21:24.0: «ليها نفس الطول بالظبط لكن باصة في الاتجاه المعاكس 180 درجة»
        scene.wait(2.5 * SPD)
        c3 = _chip("بنفس الطول — عكس الاتجاه 180°", CU, w=4.8, h=0.6, size=17).move_to([PX, -0.2, 0])
        scene.play(FadeIn(c3, shift=UP * 0.1), run_time=0.8)

        # 21:31.5: «ووظيفتها ترجعك لنقطة الصفر وتشيل أثر الحركة تماماً»
        scene.wait(6.7 * SPD)
        ripple(O, n=1)
        c4 = _chip("مفيش نقطة تتحبس فيها", ZB, w=4.8, h=0.6, size=17).move_to([PX, -1.0, 0])
        scene.play(FadeIn(c4, shift=UP * 0.1), run_time=0.8)
        b2 = VGroup(key, fwd, bwd, rule, c3, c4)

    # ---------- 3) الصيغة: عكس إشارات كل المركبات، ومجموعهم = 0 ----------
    # 21:38.5 - 21:55.5 | «وطبعاً الصيغة الرياضية للمتجه المعكوس… هيكون الناتج هو متجه الصفر» (17.0s)
    with beat(scene, 17.0):
        scene.play(*[FadeOut(m) for m in list(scene.mobjects) if m is not bar and m is not cap.cur], run_time=0.7)
        PL, EQ = ("+", OP), ("=", OP)
        E = lambda k: (r"\mathbf{e}_" + str(k), EC)

        i1 = _ctex([
            (r"-\mathbf{v}", CU), EQ, ("(", OP), ("-v_1", CU), (")", OP), E(1), PL,
            ("(", OP), ("-v_2", CU), (")", OP), E(2), PL, (r"\cdots", OP), PL,
            ("(", OP), ("-v_n", CU), (")", OP), (r"\mathbf{e}_n", EC),
        ], 32).move_to([-1.25, 1.9, 0])

        i2 = _ctex([
            (r"\mathbf{0}", ZB), EQ, (r"\mathbf{v}", CV), PL, ("(", OP), (r"-\mathbf{v}", CU), (")", OP), EQ,
            ("(", OP), ("v_1", CC), ("-", CU), ("v_1", CU), (")", OP), E(1), PL, (r"\cdots", OP), PL,
            ("(", OP), ("v_n", CC), ("-", CU), ("v_n", CU), (")", OP), (r"\mathbf{e}_n", EC),
        ], 27).move_to([-1.25, 0.45, 0])

        i3 = _ctex([
            EQ, ("0", ZB), E(1), PL, ("0", ZB), E(2), PL, (r"\cdots", OP), PL,
            ("0", ZB), (r"\mathbf{e}_n", EC), EQ, (r"\mathbf{0}", ZB),
        ], 33).move_to([-1.25, -0.95, 0])

        t1, t2, t3 = tag("بنغيّر إشارة كل مركّبة", 1.9), tag("بنجمعه على المعكوس", 0.45), tag("كل المركّبات بقت صفر", -0.95)

        # 21:39.2: صيغة المعكوس
        scene.play(FadeIn(i1, shift=UP * 0.15), FadeIn(t1, shift=LEFT * 0.1), run_time=1.0)

        # 21:47.5: جمعه على المعكوس
        scene.wait(7.3 * SPD)
        scene.play(FadeIn(i2, shift=UP * 0.15), FadeIn(t2, shift=LEFT * 0.1), run_time=1.0)

        # 21:51.5: الأصفار والرجوع للأصل
        scene.wait(3.0 * SPD)
        scene.play(FadeIn(i3, shift=UP * 0.15), FadeIn(t3, shift=LEFT * 0.1), run_time=1.0)
        back = _ar("وبكده نرجع لنقطة الأصل!", 26, ZB, True).move_to([0, -2.05, 0])
        scene.play(FadeIn(back, scale=1.1), run_time=0.8)

    # ---------- 4) من غير المعكوس مفيش طرح ولا حل معادلات ----------
    # 21:55.5 - 22:12.0 | «ومن غير شرط المعكوس ده، مستحيل نعمل طرح… أو ننقل متجه من طرف لطرف» (16.5s)
    with beat(scene, 16.5):
        scene.play(*[FadeOut(m) for m in list(scene.mobjects) if m is not bar and m is not cap.cur], run_time=0.6)

        # 21:57.5: «مستحيل نعمل عملية الطرح»
        scene.wait(1.4 * SPD)
        sub = _ctex([
            (r"\mathbf{v}", CV), ("-", CU), (r"\mathbf{v}", CU), ("=", OP),
            (r"\mathbf{v}", CV), ("+", OP), ("(", OP), (r"-\mathbf{v}", CU), (")", OP), ("=", OP),
            (r"\mathbf{0}", ZB),
        ], 44).move_to([0, 1.6, 0])
        scene.play(FadeIn(sub, shift=UP * 0.1), run_time=0.9)

        # 22:01.0: «لأن الطرح أصلاً هو عملية جمع على المعكوس»
        scene.wait(2.6 * SPD)
        nb = _chip("الطرح = جمع على المعكوس", ZB, w=5.8, h=0.7, size=21, filled=True).move_to([0, 0.35, 0])
        scene.play(FadeIn(nb, shift=UP * 0.1), run_time=0.8)

        # 22:05.5: «وبدونه مستحيل نحل معادلة مجهولة...»
        scene.wait(3.7 * SPD)
        rows = VGroup()
        for txt in ("من غير المعكوس مفيش عملية طرح", "ومفيش حل لمعادلة فيها مجهول"):
            r = _ar(txt, 22, CC, True)
            x = _cross([0, 0], 0.13, COPPER_TERRA)
            rows.add(VGroup(x, r).arrange(LEFT, buff=0.3))
        rows.arrange(DOWN, buff=0.4, aligned_edge=RIGHT).move_to([0, -1.1, 0])
        scene.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rows], lag_ratio=0.4), run_time=1.4)

    _exit(scene)


class Dev(Scene):
    def construct(self):
        play_scene08(self)