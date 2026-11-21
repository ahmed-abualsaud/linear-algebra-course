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
from common.latex import mach_math_template
from episode_05_common import *


# ==============================================================
# الحلقة 05 — الفصل 3: كيف نجمع الأعداد؟
# مدة الفصل الفعلية: 04:26.5  (بطاقة الفصل 4.2s + السرد من 03:37.2 حتى 07:59.5؛ ثم _exit داخل فاصل الـ 5s قبل الفصل 4)
# ==============================================================


def play_scene03(scene):
    _chapter(scene, 3, 'كيف نجمع الأعداد؟')
    cap = _Cap(scene, y=-2.75)
    U0, UN, Y0 = -5.0, 1.0, -0.8                 # x الصفر، طول الوحدة، y خط الأعداد
    X = lambda v: U0 + UN * v

    # ---------- 1) خط الأعداد: النقطتان 2 و 7 ----------
    # 03:37.2 - 03:59.5 | «لو جيت قولتلك اجمعلي رقم 2 علي رقم 7… تتخيل رقم 2 و 7 كانهم نقاط» (22.3s)
    with beat(scene, 22.3):
        ax = MachAxes1D(x_range=(-1, 11), grid_step=UN, number_font_size=22, show_axis_label=False)
        ax.shift(np.array([U0, Y0, 0.0]))
        _z = next(l for l in ax.labels if l.text == "0")
        _r = next(l for l in ax.labels if l.text == "1")
        _z.move_to([ax.c2p(0)[0], _r.get_center()[1], 0])
        ax.animate_creation(scene, run_time=1.6)
        n9 = next(l for l in ax.labels if l.text == "9")

        scene.wait(8.2 * SPD)
        p2, p7 = _dot([X(2), Y0], C_U), _dot([X(7), Y0], C_V)
        t2 = _tex("2", 34, C_U).move_to([X(2), Y0 + 0.45, 0])
        t7 = _tex("7", 34, C_V).move_to([X(7), Y0 + 0.45, 0])
        scene.play(FadeIn(p2), FadeIn(p7), FadeIn(t2), FadeIn(t7), run_time=1.0)

        # 03:56.0: «بتبعد مسافة معينة عن الرقم صفر»
        scene.wait(8.0 * SPD)
        scene.play(Indicate(_z, color=GOLD_BRIGHT, scale_factor=1.35), run_time=0.9)

    # ---------- 2) كل رقم = متجه (متزامنة: الأسهم ← الرمز unit ← التسمية 2 unit و 7 unit) ----------
    # 03:59.5 - 04:24.0 | «والمسافة دي يمكن تمثيلها بمتجه… 2 متجه اساس… 7 متجه اساس» (24.5s)
    with beat(scene, 24.5):
        A_ROW, B_ROW = Y0 + 0.9, Y0 + 1.6
        stack_a = _stack([X(0), A_ROW], [UN, 0], 2, C_U, 6)
        stack_b = _stack([X(0), B_ROW], [UN, 0], 7, C_V, 6)

        scene.wait(2.5 * SPD)
        scene.play(LaggedStart(*[GrowArrow(a) for a in stack_a], lag_ratio=0.25), run_time=1.4)
        scene.wait(2.0 * SPD)
        scene.play(LaggedStart(*[GrowArrow(b) for b in stack_b], lag_ratio=0.12), run_time=1.8)

        # 04:12.5 & 04:18.0: تأكيد المسافة 2 و 7 متجه أساس
        scene.wait(5.0 * SPD)
        scene.play(Indicate(stack_a, color=C_U, scale_factor=1.06), run_time=1.0)
        scene.wait(4.5 * SPD)
        scene.play(Indicate(stack_b, color=C_V, scale_factor=1.04), run_time=1.0)

    # 04:24.0 - 04:36.5 | «وزي ما قولنا متجه الاساس علي خط الاعداد اسمه متجه الوحدة… نرمزله بالرمز unit» (12.5s)
    with beat(scene, 12.5):
        unit_ar = _arrow([X(0), 1.85], [X(1), 1.85], GOLD_BRIGHT, 7, 0.32)
        unit_lb = _tex(r"\mathrm{unit}", 30, GOLD_BRIGHT).next_to(unit_ar, RIGHT, buff=0.2)
        unit_tx = VGroup(
            _ar("متجه الأساس", 18, IVORY_WHITE, True),
            _tex("=", 22, COPPER_TERRA),
            _ar("متجه الوحدة", 18, TEAL, True),
            _tex("=", 22, COPPER_TERRA),
            _ar("الرقم واحد", 18, GOLD_BRIGHT, True),
        ).arrange(LEFT, buff=0.14).next_to(unit_lb, RIGHT, buff=0.35)

        scene.wait(1.0 * SPD)
        scene.play(GrowArrow(unit_ar), FadeIn(unit_tx), run_time=1.1)
        # 04:31.5: «وخلينا بالمرة نرمز لمتجه الأساس ده بالرمز unit»
        scene.wait(5.0 * SPD)
        scene.play(FadeIn(unit_lb, scale=1.15), Indicate(unit_ar, color=GOLD_BRIGHT), run_time=1.1)

    # 04:36.5 - 04:56.0 | «بعد كدة هنضرب الارقام دي… 2 unit… 7 unit» (19.5s)
    with beat(scene, 19.5):
        lab_a = _tex(r"2\,\mathrm{unit}", 28, C_U).next_to(stack_a, LEFT, buff=0.15)
        lab_b = _tex(r"7\,\mathrm{unit}", 28, C_V).next_to(stack_b, LEFT, buff=0.15)
        # 04:47.0: «يعني رقم 2 هيكون ليه متجه بيساوي 2 unit»
        scene.wait(10.5 * SPD)
        scene.play(FadeIn(lab_a), run_time=0.9)
        # 04:52.0: «ورقم 7 هيكون ليه متجه بيساوي 7 unit»
        scene.wait(4.0 * SPD)
        scene.play(FadeIn(lab_b), run_time=0.9)

    # ---------- 3) جمع 2 + 7 خطوة بخطوة مع الكلام ----------
    # 04:56.0 - 05:15.5 | «وعملية جمع 2 + 7 تقدر تتخيلها كانك واقف عند النقطة 0… بتشاور عند النقطة 2» (19.5s)
    with beat(scene, 19.5):
        scene.wait(3.0 * SPD)
        walker = _dot([X(0), Y0], GOLD_BRIGHT, 0.12)
        scene.play(FadeIn(walker, scale=1.4), run_time=0.8)
        # 05:11.0: «فهتلاقي رأس المتجه بتشاور عند النقطة رقم 2»
        scene.wait(11.2 * SPD)
        scene.play(Indicate(p2, color=C_U, scale_factor=1.5), run_time=1.0)

    # 05:15.5 - 05:25.5 | «بعد كدة هتتحرك من النقطة 0 علي طول المتجه 2 unit لحد ما توصل للنقطة 2» (10.0s)
    with beat(scene, 10.0):
        scene.wait(1.5 * SPD)
        scene.play(walker.animate.move_to([X(2), Y0, 0]), run_time=2.5)

    # 05:25.5 - 05:37.5 | «بعدين من عند النقطة 2 دي هنحط ديل المتجه 7 unit ونشوف بيشاور فين» (12.0s)
    with beat(scene, 12.0):
        scene.wait(2.5 * SPD)
        scene.play(stack_b.animate.shift(RIGHT * 2 * UN), lab_b.animate.shift(RIGHT * 2 * UN), run_time=1.8)

    # 05:37.5 - 05:59.5 | «فهنكتشف ان راس المتجه بتشاور علي 9… لحد ما توصل للنقطة 9» (22.0s)
    with beat(scene, 22.0):
        # 05:39.3: أولاً نكتشف إن الرأس بتشاور عند 9
        scene.wait(1.8 * SPD)
        t9 = _tex("9", 40, C_SUM).move_to([X(9), Y0 + 0.5, 0])
        scene.play(FadeIn(t9, scale=1.3), Indicate(n9, color=C_SUM), run_time=1.0)

        # 05:44.3: ثم نتحرك على طول المتجه 7 unit لحد 9
        scene.wait(4.0 * SPD)
        scene.play(walker.animate.move_to([X(9), Y0, 0]), run_time=2.4)

    # ---------- 4) نبدّل الترتيب: نوصل لنفس النقطة 9 = مجموع المسافة 9 unit ----------
    # 05:59.5 - 06:24.0 | «وعلي فكرة انت ممكن تبدل وتحط 7 unit عند 0 الاول… تحط 2 unit عند 7…» (24.5s)
    with beat(scene, 24.5):
        scene.play(
            walker.animate.move_to([X(0), Y0, 0]),
            stack_b.animate.shift(LEFT * 2 * UN),
            lab_b.animate.shift(LEFT * 2 * UN),
            run_time=1.2,
        )
        scene.wait(4.5 * SPD)
        # 06:05.2: «فالمتجه ده هيوصلك للنقطة رقم 7»
        scene.play(walker.animate.move_to([X(7), Y0, 0]), run_time=1.6)
        scene.wait(3.8 * SPD)
        # 06:11.0: «بعدين هتحط المتجه 2 unit عند النقطة رقم 7»
        scene.play(stack_a.animate.shift(RIGHT * 7 * UN), lab_a.animate.shift(RIGHT * 7 * UN), run_time=1.2)
        scene.wait(3.0 * SPD)
        scene.play(walker.animate.move_to([X(9), Y0, 0]), run_time=1.4)

    # 06:24.0 - 06:40.8 | «والمسافة اللي بيبعدها الرقم 9 عن 0 هنمثلها بـ 9 unit = 2 unit + 7 unit» (16.8s)
    with beat(scene, 16.8):
        total = _arrow([X(0), Y0 - 1.1], [X(9), Y0 - 1.1], C_SUM, 7, 0.1)
        total_lb = _tex(r"9\,\mathrm{unit}=2\,\mathrm{unit}+7\,\mathrm{unit}", 30, C_SUM).next_to(total, DOWN, buff=0.15)
        scene.wait(2.5 * SPD)
        scene.play(GrowArrow(total), run_time=1.2)
        # 06:34.0: «مجموع المسافة الكلية اللي هي 7 unit + 2 unit»
        scene.wait(6.3 * SPD)
        scene.play(FadeIn(total_lb), run_time=0.8)

    # ---------- 5) unit = 1 فمش بيأثر في الحساب — بنكتب الرقم من غيره ----------
    # 06:40.8 - 07:27.0 | «وعشان الرمز unit ده بيعبر اصلا عن قيمة "الواحد" نفسه فمش هيكون…» (46.2s)
    with beat(scene, 46.2):
        def _eq_box(mob):
            mob.move_to([0, 3.05, 0])
            w, h = mob.width + 0.7, 0.80
            glow = RoundedRectangle(
                corner_radius=0.14, width=w + 0.08, height=h + 0.08,
                stroke_color=GOLD_BRIGHT, stroke_width=8, stroke_opacity=0.14,
                fill_opacity=0.0,
            ).move_to(mob)
            bg = RoundedRectangle(
                corner_radius=0.12, width=w, height=h,
                stroke_color=GOLD_BRIGHT, stroke_width=2.0, stroke_opacity=0.85,
                fill_color=GOLD_DARK, fill_opacity=0.18,
            ).move_to(mob)
            return VGroup(glow, bg, mob)

        f1_eq = MathTex(
            r"2\,", r"\mathrm{unit}", r"+", r"7\,", r"\mathrm{unit}", r"=", r"9\,", r"\mathrm{unit}",
            tex_template=mach_math_template, font_size=40, color=IVORY_WHITE,
        )
        f1_eq[0].set_color(C_U)
        f1_eq[1].set_color(GOLD_BRIGHT)
        f1_eq[2].set_color(IVORY_WHITE)
        f1_eq[3].set_color(C_V)
        f1_eq[4].set_color(GOLD_BRIGHT)
        f1_eq[5].set_color(TEAL)
        f1_eq[6].set_color(C_SUM)
        f1_eq[7].set_color(GOLD_BRIGHT)
        f1 = _eq_box(f1_eq)

        f2_eq = MathTex(
            r"2", r"+", r"7", r"=", r"9",
            tex_template=mach_math_template, font_size=40, color=IVORY_WHITE,
        )
        f2_eq[0].set_color(C_U)
        f2_eq[1].set_color(IVORY_WHITE)
        f2_eq[2].set_color(C_V)
        f2_eq[3].set_color(TEAL)
        f2_eq[4].set_color(C_SUM)
        f2 = _eq_box(f2_eq)

        scene.wait(1.0 * SPD)
        scene.play(FadeIn(f1), run_time=0.8)

        # 06:55.6: «بنتكلم عن الرقم نفسه من غير ما نذكر متجه الأساس...»
        scene.wait(13.0 * SPD)
        scene.play(ReplacementTransform(f1, f2), FadeOut(VGroup(lab_a, lab_b, total_lb)), run_time=1.4)

        # 07:09.5: «لأن وجود متجه الأساس من عدمه مش هيفرق معايا في الحسابات الرياضية البسيطة»
        scene.wait(12.5 * SPD)
        cap.set("وجود متجه الأساس من عدمه مش بيغيّر الحسابات البسيطة")

    # ---------- 6) لكن متجه الأساس موجود دايمًا على خط الأعداد (وقفة وتأمّل) ----------
    # 07:27.0 - 07:59.5 | «لكن خليني اقولك انت بقي سواء اتعاملت مع الارقام بالطريقة العادية او…» (32.5s)
    with beat(scene, 32.5):
        # 07:43.0: «فكده كده متجه الأساس ده موجود... وعدم تأثيره مش معناه عدم وجوده»
        scene.wait(16.0 * SPD)
        scene.play(Indicate(unit_ar, color=GOLD_BRIGHT, scale_factor=1.25), Indicate(unit_lb), run_time=1.4)
        cap.set("عدم تأثيره في الحساب مش معناه إنه مش موجود", GOLD_BRIGHT)

    _exit(scene)


class Dev(Scene):
    def construct(self):
        play_scene03(self)