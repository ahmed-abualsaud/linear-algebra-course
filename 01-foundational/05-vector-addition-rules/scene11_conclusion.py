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
# الحلقة 05 — الفصل 11: النهاية + تشويقة الحلقة السادسة
# مدة الفصل الفعلية: 00:57.7  (بطاقة الفصل 4.2s + السرد من 29:19.0 حتى 30:12.5 = 53.5s)
# ملحوظة: الأوترو (سلام عليكم) خارج المشاهد — شغّله من ملف الأوترو المشترك
# ==============================================================


def _teaser_grid(O, box=(-6.0, 6.0, -2.4, 2.1), step=0.6):
    """شبكة بنفس أسلوب تشويقة الحلقة الرابعة."""
    x_min, x_max, y_min, y_max = box
    grid = VGroup()

    kx = int(np.floor((x_min - O[0]) / step))
    while O[0] + kx * step <= x_max + 1e-6:
        x = O[0] + kx * step
        is_axis = (kx == 0)
        grid.add(Line(
            [x, y_min, 0], [x, y_max, 0],
            color=GOLD_LIGHT,
            stroke_width=1.8 if is_axis else 1.0,
            stroke_opacity=0.45 if is_axis else 0.22,
        ))
        kx += 1

    ky = int(np.floor((y_min - O[1]) / step))
    while O[1] + ky * step <= y_max + 1e-6:
        y = O[1] + ky * step
        is_axis = (ky == 0)
        grid.add(Line(
            [x_min, y, 0], [x_max, y, 0],
            color=GOLD_LIGHT,
            stroke_width=1.8 if is_axis else 1.0,
            stroke_opacity=0.45 if is_axis else 0.22,
        ))
        ky += 1

    return grid


def play_scene11(scene):
    _chapter(scene, 11, 'النهاية')
    cap = _Cap(scene)

    # ---------- 1) كل شرط بيحدد صفة من صفات فضاء المتجهات — واللي بيخالف شرط مش متجه ----------
    # 29:19.0 - 29:50.0 | «لو لاحظت خلال شرحي لل 5 شروط دي… مش بنعتبره متجه» (31 ثانية)
    with beat(scene, 31.0):
        hd = _ar("شروط الجمع الخمسة", 32, GOLD_BRIGHT, True).move_to([0, 3.0, 0])
        scene.play(FadeIn(hd), run_time=0.8)

        rows = VGroup(*[
            _chip(f"✓  {a}", GOLD_LIGHT if i % 2 == 0 else COPPER_TERRA, w=7.6, h=0.68, size=20)
            for i, (a, b) in enumerate(RULES)
        ]).arrange(DOWN, buff=0.2).move_to([0, 0.5, 0])

        # 29:21.0 - 29:27.5: ظهور الـ 5 شروط مع التمهيد
        scene.wait(1.2 * SPD)
        for r in rows:
            scene.play(FadeIn(r, shift=LEFT * 0.3), run_time=0.7)
            scene.wait(0.6 * SPD)

        # 29:38.0: «لكن لازم يكون بيحقق شروط الجمع الخمسة اللي لسه شارحها»
        scene.wait(10.5 * SPD)
        scene.play(
            LaggedStart(
                *[Indicate(r, color=GOLD_BRIGHT, scale_factor=1.05) for r in rows],
                lag_ratio=0.2,
            ),
            run_time=2.2,
        )

        # 29:43.5: «وبالتالي أي كائن رياضي بيخلف قاعدة واحدة من القواعد دي مش بنعتبره متجه»
        scene.wait(3.3 * SPD)
        warn = _chip(
            "أي كائن رياضي بيخالف شرط واحد مش بنعتبره متجه",
            ERR_RED,
            w=8.6,
            h=0.75,
            size=20,
        ).move_to([0, -2.4, 0])
        scene.play(FadeIn(warn, shift=UP * 0.15), run_time=1.0)

    # ---------- 2أ) مش لازم تحفظ — المهم تطبّق ----------
    # 29:50.0 - 30:02.0 | «وخليني اكررها للمرة التالتة… تعرف إزاي تطبق القواعد دي على المتجهات» (12 ثانية)
    with beat(scene, 12.0):
        scene.play(FadeOut(VGroup(hd, rows, warn)), run_time=0.7)

        # 29:54.5: الرسالة الأساسية
        scene.wait(3.8 * SPD)
        keep = _ar("مش لازم تحفظ القواعد — المهم تعرف تطبّقها", 30, GOLD_BRIGHT, True).move_to([0, 0.2, 0])
        scene.play(FadeIn(keep, scale=0.95), run_time=0.9)

        # تفريغ الشاشة استعداداً لتشويقة الحلقة الجاية عند 30:02.0
        scene.wait(5.8 * SPD)
        scene.play(FadeOut(keep), run_time=0.7)

    # ---------- 2ب) تشويقة الحلقة السادسة: ضرب المتجه في رقم قياسي ----------
    # 30:02.0 - 30:12.5 | «والحلقة الجاية إن شاء الله… وأشوفكو الحلقة الجاية بإذن الله» (10.5 ثانية)
    with beat(scene, 10.5):
        nxt = _ar("الحلقة الجاية: ضرب المتجه في رقم قياسي", 32, GOLD_LIGHT, True).move_to([0, 3.0, 0])
        O = np.array([-2.6, -1.4, 0.0])
        v = np.array([1.6, 0.6, 0.0])
        grid = _teaser_grid(O, box=(-6.0, 6.0, -2.4, 2.1), step=0.6)

        dot_o = Dot(O, radius=0.07, color=GOLD_BRIGHT).set_z_index(5)

        c_tracker = ValueTracker(1.0)
        v_stretch = Arrow(
            O, O + v,
            buff=0, color=GOLD_BRIGHT, stroke_width=7,
            max_tip_length_to_length_ratio=0.10,
        )
        lv = _tex(r"\mathbf{v}", 32, GOLD_LIGHT).next_to(O + v * 0.55, DOWN, buff=0.22)

        c_num = DecimalNumber(1.0, num_decimal_places=1, font_size=44, color=GOLD_BRIGHT)
        c_dot_v = _tex(r"\cdot\,\mathbf{v}", 44, GOLD_LIGHT)
        live_eq = VGroup(c_num, c_dot_v).arrange(RIGHT, buff=0.14).move_to([0, 1.45, 0])

        # 30:02.0: ظهور العنوان والشبكة والمتجه
        scene.play(FadeIn(nxt, shift=DOWN * 0.1), FadeIn(grid), run_time=0.9)
        scene.play(
            FadeIn(dot_o),
            GrowArrow(v_stretch),
            FadeIn(lv),
            FadeIn(live_eq),
            run_time=0.9,
        )

        # ربط التمدد والعداد بعد اكتمال الظهور مباشرة
        v_stretch.add_updater(
            lambda m: m.become(
                Arrow(
                    O, O + c_tracker.get_value() * v,
                    buff=0, color=GOLD_BRIGHT, stroke_width=7,
                    max_tip_length_to_length_ratio=0.10,
                )
            )
        )
        c_num.add_updater(
            lambda m: m.set_value(c_tracker.get_value()).next_to(c_dot_v, LEFT, buff=0.14)
        )

        # 30:04.2: مدّ المتجه مع الضرب في الرقم القياسي (1.0 -> 3.0)
        scene.wait(0.4 * SPD)
        scene.play(c_tracker.animate.set_value(3.0), run_time=2.8, rate_func=smooth)
        v_stretch.clear_updaters()
        c_num.clear_updaters()

        # 30:07.5: «وإيه هي شروط العملية دي...»
        scene.wait(0.5 * SPD)
        note = _ar(
            "وإيه هي الشروط اللي بتحكم عملية التمديد والضرب دي؟",
            24, GOLD_BRIGHT, True,
        ).move_to([0, -3.15, 0])
        scene.play(FadeIn(note, shift=UP * 0.1), run_time=0.8)

    _exit(scene)


class Dev(Scene):
    def construct(self):
        play_scene11(self)