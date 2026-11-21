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
from episode_05_common import *


# ==============================================================
# الحلقة 05 — الفصل 1: ماذا سنفعل في هذه الحلقة؟
# مدة الفصل الفعلية: 02:01.0  (بطاقة الفصل 4.2s + السرد من 00:04.2 حتى 02:01.0؛ ثم _exit داخل فاصل الـ 5s قبل الفصل 2)
# ==============================================================


def play_scene01(scene):
    _chapter(scene, 1, 'ماذا سنفعل في هذه الحلقة؟')
    cap = _Cap(scene, y=-2.75)      # أعلى من الافتراضي (-3.4) عشان نسيب مساحة لترجمة يوتيوب

    # ---------- 1) عنوان الحلقة + مراجعة سريعة ----------
    # 00:04.2 - 00:16.8 | «دلوقتي بعد ما عرفنا في الحلقة اللي فاتت ازاي نكتب المتجه وعرفنا…» (12.6s)
    with beat(scene, 12.6):
        title = _ar("قواعد جمع المتجهات", 46, GOLD_BRIGHT, True).move_to([0, 2.9, 0])
        sub = _ar("الجبر الخطي • الحلقة 05", 20, COPPER_TERRA, True).move_to([0, 2.2, 0])
        scene.play(FadeIn(title, shift=DOWN * 0.15), FadeIn(sub), run_time=1.2)
        scene.wait(1.5 * SPD)

        recap = VGroup(*[
            _chip("✓  " + t, c, w=3.5, h=0.62, size=18)
            for t, c in [
                ("الصيغة الرياضية للمتجه", GOLD_LIGHT),
                ("مركبات المتجه", COPPER_TERRA),
                ("متجهات الأساس", GOLD_LIGHT),
            ]
        ]).arrange(LEFT, buff=0.3).move_to([0, 0.5, 0])
        scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in recap], lag_ratio=0.55), run_time=4.5)

        # 00:13.0: «إحنا كده بقينا قادرين نفهم قواعد المتجهات»
        scene.wait(1.5 * SPD)
        scene.play(Indicate(title, color=GOLD_BRIGHT, scale_factor=1.06), run_time=0.9)

    # ---------- 2) مش لازم تحفظ — المهم تفهم وتطبّق ----------
    # 00:16.8 - 00:47.2 | «وزي ما قولتلك في الحلقة التانية… المهم يلا نبدأ دلوقتي في شرح قواعد المتجهات» (30.4s)
    with beat(scene, 30.4):
        scene.wait(2.5 * SPD)
        keep = _chip(
            "مش لازم تحفظ القواعد — المهم تفهمها وتعرف تطبّقها",
            GOLD_BRIGHT, w=8.6, h=0.8, size=22, filled=True,
        ).move_to([0, -1.2, 0])
        scene.play(FadeIn(keep, shift=UP * 0.15), run_time=1.0)

        # 00:25.0: «لكن الشيء الأهم هو إنك تفهمها كويس وتعرف تطبقها...»
        scene.wait(4.5 * SPD)
        scene.play(Indicate(keep, color=GOLD_BRIGHT, scale_factor=1.04), run_time=1.0)

        # 00:33.0: «وإن شاء الله هيكون في أمثلة توضحلك... بعد ما نخلص شرح العشر قواعد»
        scene.wait(7.2 * SPD)
        ex_note = _ar("أمثلة تطبيقية بعد شرح العشر قواعد", 20, GOLD_LIGHT, True).move_to([0, -2.2, 0])
        scene.play(FadeIn(ex_note, shift=UP * 0.1), run_time=0.8)

    # ---------- 3) الجدول: فيه نوعين من القواعد (الاتنين معتّمين) ----------
    # 00:47.2 - 00:52.8 | «في الجدول اللي قدامك في نوعين من القواعد» (5.6s)
    with beat(scene, 5.6):
        scene.play(FadeOut(VGroup(title, sub, recap, keep, ex_note)), run_time=0.8)
        rx, lx = 3.5, -3.5
        hdr_r = _ar("قواعد جمع المتجهات", 24, GOLD_LIGHT, True).move_to([rx, 2.55, 0])
        hdr_l = _ar("قواعد الضرب في عدد قياسي", 24, COPPER_TERRA, True).move_to([lx, 2.55, 0])
        add_rows = VGroup(*[_chip(f"{i + 1}-  {a}", GOLD_LIGHT, w=5.7, h=0.62, size=17) for i, (a, b) in enumerate(RULES)])
        add_rows.arrange(DOWN, buff=0.17).move_to([rx, -0.05, 0])
        # TODO: أسماء قواعد الضرب مؤقتة لحد ما تكتب الحلقة 06
        SCALAR = ["إغلاق الضرب", "التوزيع على جمع المتجهات", "التوزيع على جمع الأعداد", "تجميع الضرب", "المحايد الضربي"]
        sc_rows = VGroup(*[_chip(f"{i + 1}-  {t}", COPPER_TERRA, w=5.7, h=0.62, size=17) for i, t in enumerate(SCALAR)])
        sc_rows.arrange(DOWN, buff=0.17).move_to([lx, -0.05, 0])

        def _cover(cx):
            return Rectangle(width=6.3, height=5.2, stroke_width=0, fill_color="#000000", fill_opacity=0.72).move_to([cx, 0.4, 0])

        cov_r, cov_l = _cover(rx), _cover(lx)
        cov_r.set_z_index(5)
        cov_l.set_z_index(5)
        scene.play(FadeIn(VGroup(hdr_r, hdr_l, add_rows, sc_rows)), FadeIn(cov_r), FadeIn(cov_l), run_time=1.0)

    # ---------- 4) يمين: قواعد جمع المتجهات (بتنوّر طول الشرح) ----------
    # 00:52.8 - 01:19.5 | «الجزء اللي علي يمين الجدول بيوضح شروط او قواعد جمع المتجهات…» (26.7s)
    with beat(scene, 26.7):
        scene.play(FadeOut(cov_r), run_time=1.0)
        scene.play(Indicate(hdr_r, color=GOLD_BRIGHT, scale_factor=1.1), run_time=0.9)

        # 01:00.5: «بتحددلك طريقة تركيب وتجميع متجهات الأساس مع بعضها...»
        scene.wait(5.8 * SPD)
        scene.play(
            LaggedStart(*[Indicate(r, color=GOLD_BRIGHT, scale_factor=1.03) for r in add_rows], lag_ratio=0.15),
            run_time=1.8,
        )
        cap.set("بتحدد طريقة تركيب متجهات الأساس مع بعضها", GOLD_LIGHT)

        # 01:10.5: «وبتحددلك طبيعة وخصائص فضاء المتجهات نفسه»
        scene.wait(7.0 * SPD)
        cap.set("وبتحدد طبيعة وخصائص فضاء المتجهات نفسه", GOLD_LIGHT)

    # ---------- 5) شمال: قواعد الضرب في عدد قياسي ----------
    # 01:19.5 - 01:38.5 | «والجزء علي الشمال بيشرح شروط او قواعد ضرب المتجه في رقم قياسي…» (19.0s)
    with beat(scene, 19.0):
        scene.play(FadeIn(cov_r), FadeOut(cov_l), run_time=1.0)
        scene.play(Indicate(hdr_l, color=COPPER_TERRA, scale_factor=1.1), run_time=0.9)

        # 01:28.5: «بتحددلك طبيعة وطريقة تصرف متجهات الأساس...»
        scene.wait(7.0 * SPD)
        scene.play(
            LaggedStart(*[Indicate(r, color=COPPER_TERRA, scale_factor=1.03) for r in sc_rows], lag_ratio=0.15),
            run_time=1.8,
        )
        cap.set("بتحدد تصرف متجهات الأساس جوه الفضاء", COPPER_TERRA)

    # ---------- 6) احنا في الحلقة دي: قواعد الجمع بس ----------
    # 01:38.5 - 02:01.0 | «واحنا في الحلقة دي هنتعلم القواعد اللي بتحكم عملية الجمع بس وهنكمل…» (22.5s)
    with beat(scene, 22.5):
        scene.play(FadeOut(cov_r), FadeIn(cov_l), run_time=1.0)
        scene.play(Indicate(hdr_r, color=GOLD_BRIGHT, scale_factor=1.1), run_time=0.9)

        scene.wait(1.5 * SPD)
        cap.set("الحلقة دي: قواعد الجمع — والضرب في الحلقة الجاية", GOLD_LIGHT)

        # 01:49.5: «لكن في الأول لازم تعرف إزاي تطبق عملية الجمع نفسها على المتجهات...»
        scene.wait(6.9 * SPD)
        cap.set("الأول: إزاي نطبق عملية الجمع نفسها على المتجهات؟", GOLD_BRIGHT)
        scene.play(Indicate(add_rows, color=GOLD_BRIGHT, scale_factor=1.02), run_time=1.0)

    _exit(scene)


class Dev(Scene):
    def construct(self):
        play_scene01(self)