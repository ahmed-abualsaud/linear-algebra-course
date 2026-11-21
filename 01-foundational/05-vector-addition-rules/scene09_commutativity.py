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
from surface_curved import play_curved_surface


# ==============================================================
# الحلقة 05 — الفصل 9: استقامة الفضاء
# (الشرط 4 من 5 — شريط الشروط بيظهر أعلى الشاشة)
# مدة الفصل الفعلية: 02:46.0  (بطاقة الفصل 4.2s + السرد من 22:18.0 حتى 25:04.0؛ ثم _exit داخل فاصل الـ 5s قبل الفصل 10)
# التخطيط: شبكة MachAxes2D على الشمال — ولوحة الكلام على اليمين بعيد عن الرسمة.
# الألوان: u نحاسي، v أصفر ذهبي، الناتج/المساواة ذهبي ساطع، المركّبات أبيض، متجهات الأساس ذهبي فاتح.
# ==============================================================

PX = 4.25                                   # مركز لوحة الكلام (اليمين)
CU, CV, ZB, CC, EC, OP = C_U, C_V, GOLD_BRIGHT, IVORY_WHITE, GOLD_LIGHT, STONE_AXIS


def _rtl(parts, buff=0.14):
    """سطر عربي فيه رموز لاتينية: الأجزاء بترتيب القراءة (الأول = أقصى اليمين)."""
    return VGroup(*parts[::-1]).arrange(RIGHT, buff=buff)


def _ctex(tokens, size):
    """معادلة ملوّنة: كل جزء (نص، لون) بيتكتب ويتلوّن لوحده."""
    m = MathTex(*[t for t, _ in tokens], tex_template=mach_math_template, font_size=size)
    for sub, (_, col) in zip(m, tokens):
        sub.set_color(col)
    return m


def play_scene09(scene):
    _chapter(scene, 9, 'استقامة الفضاء')
    cap = _Cap(scene, y=-2.85)               # الجملة الدهبية مرفوعة عشان الترجمة تلاقي مكان تحتها
    bar = _rules_bar(3)
    S = 0.6                                  # نفس شبكة الفصل 4 و5 و7 و8
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

    def ripple(pos, color=ZB, n=1, dur=0.9):
        for _ in range(n):
            ring = Circle(radius=0.12, color=color, stroke_width=4).move_to(pos)
            scene.add(ring)
            scene.play(ring.animate.scale(5).set_stroke(opacity=0), run_time=dur)
            scene.remove(ring)

    # ---------- 1) u + v = v + u (الإبدال الجمعي = استقامة الفضاء) ----------
    # 22:18.0 - 22:31.5 | «الشرط الرابع هو انه لو عندي متجهين u و v… ترتيب الجمع مش هيفرق» (13.5s)
    with beat(scene, 13.5):
        scene.play(FadeIn(bar), run_time=0.8)
        gr.animate_creation(scene, run_time=1.4)
        title = _chip("الإبدال الجمعي", ZB, w=4.6, h=0.62, size=20, filled=True).move_to([PX, 2.6, 0])

        u = vec((6, 2), CU)
        v = vec((3, 4), CV)
        tipu, tipv = P(6, 2), P(3, 4)
        lab_u = VGroup(_tex(r"\mathbf{u}", 38, CU), _tex(r"(6,\,2)", 26, CU)).arrange(RIGHT, buff=0.14).move_to(tipu + np.array([0.8, -0.3, 0]))
        lab_v = VGroup(_tex(r"\mathbf{v}", 38, CV), _tex(r"(3,\,4)", 26, CV)).arrange(RIGHT, buff=0.14).move_to(tipv + np.array([-0.8, 0.3, 0]))
        scene.play(FadeIn(title, shift=DOWN * 0.1), GrowArrow(u), FadeIn(lab_u), run_time=1.0)
        scene.play(GrowArrow(v), FadeIn(lab_v), run_time=1.0)

        # 22:23.7: مع جملة «وجيت أجمع v على u = u على v»
        scene.wait(1.5 * SPD)
        f1 = _ctex([
            (r"\mathbf{u}", CU), ("+", OP), (r"\mathbf{v}", CV),
            ("=", ZB),
            (r"\mathbf{v}", CV), ("+", OP), (r"\mathbf{u}", CU),
        ], 44).move_to([PX, 1.5, 0])
        scene.play(FadeIn(f1, shift=LEFT * 0.2), run_time=0.9)

        # 22:26.1: النتيجة بالأرقام
        scene.wait(1.5 * SPD)
        f2 = _ctex([
            (r"(6,\,2)", CU), ("+", OP), (r"(3,\,4)", CV),
            ("=", ZB),
            (r"(3,\,4)", CV), ("+", OP), (r"(6,\,2)", CU),
        ], 26).move_to([PX, 0.6, 0])
        f3 = _ctex([("=", ZB), (r"(9,\,6)", ZB)], 32).move_to([PX, -0.15, 0])
        scene.play(FadeIn(f2, shift=UP * 0.1), FadeIn(f3, shift=UP * 0.1), run_time=0.9)

        # 22:28.5: «يعني ترتيب الجمع مش هيفرق»
        scene.wait(1.5 * SPD)
        c1 = _chip("ترتيب الجمع مش بيفرق", ZB, w=4.6, h=0.6, size=18).move_to([PX, -1.1, 0])
        scene.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)

        b1 = VGroup(f1, f2, f3, c1)

    # ---------- 2) الفضاء المسطح: المساران بيوصلوا لنفس النقطة (متوازي أضلاع بيقفل) ----------
    # 22:31.5 - 23:14.0 | «يعني ده الشرط اللي بيضمنلي ان فضاء المتجهات ميكونش منحني… بيكسر فكرة التوازي» (42.5s)
    with beat(scene, 42.5):
        scene.play(FadeOut(b1), run_time=0.6)

        # 22:35.0: «تقدر تسميه شرط استقامة الفضاء»
        scene.wait(2.9 * SPD)
        cap.set("شرط الإبدال الجمعي = شرط استقامة الفضاء", GOLD_LIGHT)

        # 22:40.0: «يضمنلي ان الفضاء مايكونش منحني... لو حصل u+v هيختلف عن v+u»
        scene.wait(4.3 * SPD)
        u2 = vec((6, 2), CU, start=(3, 4))
        v2 = vec((3, 4), CV, start=(6, 2))
        par = Polygon(P(0, 0), P(6, 2), P(9, 6), P(3, 4), stroke_width=0, fill_color=ZB, fill_opacity=0.10)

        r1 = _rtl([_ar("المسار الأول:", 20, CC, True), _tex(r"\mathbf{u}", 34, CU), _ar("ثم", 20, CC, True),
                   _tex(r"\mathbf{v}", 34, CV)]).move_to([PX, 1.7, 0])
        r2 = _rtl([_ar("المسار التاني:", 20, CC, True), _tex(r"\mathbf{v}", 34, CV), _ar("ثم", 20, CC, True),
                   _tex(r"\mathbf{u}", 34, CU)]).move_to([PX, 0.7, 0])

        w1, w2 = _dot(O, CU, 0.11), _dot(O, CV, 0.11)
        scene.play(FadeIn(par), FadeIn(w1), FadeIn(w2), FadeIn(r1, shift=LEFT * 0.15), run_time=0.9)
        scene.play(w1.animate.move_to(P(6, 2)), w2.animate.move_to(P(3, 4)), FadeIn(r2, shift=LEFT * 0.15), run_time=1.6)
        scene.wait(1.2 * SPD)
        scene.play(TransformFromCopy(v, v2), TransformFromCopy(u, u2), run_time=1.0)
        scene.play(w1.animate.move_to(P(9, 6)), w2.animate.move_to(P(9, 6)), run_time=1.6)
        ripple(P(9, 6), n=2)

        same = _chip("وصلوا لنفس النقطة (9,6)", ZB, w=4.6, h=0.62, size=18, filled=True).move_to([PX, -0.5, 0])
        scene.play(FadeIn(same, shift=UP * 0.1), run_time=0.8)

        # 22:53.5: الانتقال لمقارنة السطح المنحني
        scene.wait(2.5 * SPD)
        cap.set("في الفضاء المسطح: المساران بيوصلوا لنفس النقطة", GOLD_LIGHT)

        # 23:05.5: «لأن الفضاء المنحني بيكسر فكرة التوازي والاستقامة...»
        scene.wait(11.0 * SPD)
        cap.set("الفراغ المستقيم يحافظ على التوازي والاستقامة", GOLD_LIGHT)

    # ---------- 3) تشبيه: سطح منحني (كرة ثم سرج) — المسارين u+v و v+u بيتداخلوا أو بيتباعدوا ----------
    # 23:14.0 - 23:52.0 | «يعني لو كان فضاء المتجهات منحني مثل سطح كرة مثلا… لنقطة مختلفة مش لنفس النقطة» (38.0s)
    with beat(scene, 38.0):
        scene.play(*[FadeOut(m) for m in list(scene.mobjects) if m is not bar and m is not cap.cur], run_time=0.7)
        play_curved_surface(scene, cap)
        cap.set("ده تشبيه: الشرط عن عملية الجمع نفسها", GOLD_LIGHT)

    # ---------- 4) تنبيه: الإبدال سابق على التسطح — مش العكس ----------
    # 23:52.0 - 24:28.0 | «معلش خلو بالكو… شرط الابدال الاول بعدين استنتجوا ان الفضاء لازم يكون مسطح» (36.0s)
    with beat(scene, 36.0):
        scene.play(*[FadeOut(m) for m in list(scene.mobjects) if m is not bar and m is not cap.cur], run_time=0.7)
        cap.set("تنبيه: الإبدال هو الأساس — والتسطح نتيجة", GOLD_LIGHT)

        # الصندوقان بارتفاع 1.0 عند y=1.55 بحيث السهمين (1.30 و 1.85) يربطوا بين حوافهما مباشرة
        bx1 = _chip("شرط الإبدال الجمعي", ZB, w=4.4, h=1.0, size=24, filled=True).move_to([3.2, 1.55, 0])
        bx2 = _chip("تسطح واستقامة الفضاء", GOLD_LIGHT, w=4.4, h=1.0, size=24).move_to([-3.2, 1.55, 0])
        scene.play(FadeIn(bx1, shift=LEFT * 0.2), FadeIn(bx2, shift=RIGHT * 0.2), run_time=1.0)

        # 23:57.0: «افترضوا إن فضاء المتجهات مسطح ونتيجة لده ظهر الإبدال»
        scene.wait(2.6 * SPD)
        ar_no = _arrow([-1.0, 1.30], [1.0, 1.30], CU, 5, 0.25)
        scene.play(GrowArrow(ar_no), run_time=1.0)

        # 24:02.5: «وده غلط؛ بل العكس تماماً هو اللي صحيح»
        scene.wait(4.5 * SPD)
        x9 = _cross([0, 1.30], 0.26, CU)
        lab_no = _ar("مش العكس", 20, CU, True).next_to(ar_no, DOWN, buff=0.32)
        scene.play(FadeIn(x9), FadeIn(lab_no), run_time=0.9)

        # 24:07.0: «حطوا شرط الإبدال الأول، بعدين استنتجوا منه إن الفضاء مسطح»
        scene.wait(3.6 * SPD)
        ar_ok = _arrow([1.0, 1.85], [-1.0, 1.85], ZB, 6, 0.25)
        lab_ok = _ar("بينتج عنه", 18, ZB).next_to(ar_ok, UP, buff=0.14)
        scene.play(GrowArrow(ar_ok), FadeIn(lab_ok), run_time=1.0)

        # 24:19.0: «وأنا هنا عكست الآية...»
        scene.wait(11.0 * SPD)
        scr = _chip("شرط الإبدال سابق على تسطح واستقامة الفضاء", ZB, w=9.2, h=0.85, size=22, filled=True).move_to([0, -0.9, 0])
        scene.play(FadeIn(scr, shift=UP * 0.15), run_time=1.0)

    # ---------- 5) الصيغة: v₁e₁ + v₂e₂ = v₂e₂ + v₁e₁ ----------
    # 24:28.0 - 25:04.0 | «طيب دلوقتي احنا عاوزين نعرف شرط الابدال ده معناه ايه… لو الشرط اتكسر» (36.0s)
    with beat(scene, 36.0):
        scene.play(*[FadeOut(m) for m in list(scene.mobjects) if m is not bar and m is not cap.cur], run_time=0.7)
        cap.set("المعنى الرياضي لشرط الإبدال", GOLD_LIGHT)

        T1 = [("v_1", CU), (r"\mathbf{e}_1", CU)]
        T2 = [("v_2", CV), (r"\mathbf{e}_2", CV)]

        # 24:36.7: «لو عندي متجه مكتوب بالشكل ده»
        scene.wait(7.3 * SPD)
        fe = _ctex([(r"\mathbf{v}", CC), ("=", OP)] + T1 + [("+", OP)] + T2, 44).move_to([0, 2.0, 0])
        scene.play(FadeIn(fe), run_time=0.9)

        # 24:42.0: «بيديني الحق إني أبدل v1 e1 مكان v2 e2...»
        scene.wait(4.4 * SPD)
        ok = _ctex(T1 + [("+", OP)] + T2 + [("=", ZB)] + T2 + [("+", OP)] + T1, 38).move_to([-0.6, 0.7, 0])
        ck = _check([4.6, 0.7], 0.3, ZB)
        scene.play(FadeIn(ok, shift=UP * 0.1), FadeIn(ck), run_time=1.2)

        scene.wait(1.0 * SPD)
        scene.play(
            Indicate(ok[0:2], color=CU, scale_factor=1.25),
            Indicate(ok[9:11], color=CU, scale_factor=1.25),
            run_time=1.4,
        )
        scene.play(
            Indicate(ok[3:5], color=CV, scale_factor=1.15),
            Indicate(ok[6:8], color=CV, scale_factor=1.15),
            run_time=1.0,
        )

        # 24:55.5: «ولو الشرط ده اتكسر، ساعتها ماكنتش هقدر أبدل...»
        scene.wait(8.9 * SPD)
        bad = _ctex(T1 + [("+", OP)] + T2 + [(r"\neq", CU)] + T2 + [("+", OP)] + T1, 38).move_to([-0.6, -0.6, 0])
        xx = _cross([4.6, -0.6], 0.3, CU)
        bt = _ar("لو الشرط اتكسر ماكنتش هقدر أبدّل", 22, CU, True).move_to([0, -1.6, 0])
        scene.play(FadeIn(bad, shift=UP * 0.1), FadeIn(xx), FadeIn(bt), run_time=1.4)

    _exit(scene)


class Dev(Scene):
    def construct(self):
        play_scene09(self)