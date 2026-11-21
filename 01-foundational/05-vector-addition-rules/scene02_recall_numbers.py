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


# ==============================================================
# الحلقة 05 — الفصل 2: استدعاء فكرة من نهاية الحلقة الثالثة
# مدة الفصل الفعلية: 01:30.4  (بطاقة الفصل 4.2s + السرد من 02:06.0 حتى 03:32.2؛ ثم _exit داخل فاصل الـ 5s قبل الفصل 3)
# ==============================================================


def play_scene02(scene):
    _chapter(scene, 2, 'استدعاء فكرة من نهاية الحلقة الثالثة')

    # ---------- 1) اقتباس: المتجه تعميم لمفهوم العدد (خط أعداد ← فضاء) ----------
    # 02:06.0 - 02:29.5 | «لو متابع معايا السلسلة دي من الاول… خط أعداد في بُعد واحد… ممتد لكذا بُعد» (23.5s)
    with beat(scene, 23.5):
        quote = _ar("المتجه هو تعميم مباشر\nلمفهوم العدد", 40, IVORY_WHITE, True).move_to([1.4, 1.35, 0])
        src = _ar("من نهاية الحلقة الثالثة", 18, COPPER_TERRA).next_to(quote, DOWN, buff=0.3, aligned_edge=RIGHT)
        bar = Line(
            UP * (quote.height / 2 + 0.06),
            DOWN * (quote.height / 2 + 0.06),
            color=GOLD_BRIGHT,
            stroke_width=6,
        ).next_to(quote, RIGHT, buff=0.32)

        # 02:08.5: «في نهاية الحلقة التالتة...» ثم 02:11.7: نص الاقتباس
        scene.wait(2.5 * SPD)
        scene.play(Create(bar), FadeIn(src), run_time=0.7)
        scene.wait(2.5 * SPD)
        scene.play(FadeIn(quote, shift=LEFT * 0.2), run_time=1.0)

        IY = -0.95
        nl = MachAxes1D(
            x_range=(-4, 4), grid_step=0.5, number_font_size=18,
            show_minor_ticks=False, show_axis_label=False, show_origin=True,
        )
        nl.shift(np.array([3.5, IY, 0.0]))
        _z = next(l for l in nl.labels if l.text == "0")
        _ref = next(l for l in nl.labels if l.text == "1")
        _z.move_to([nl.c2p(0)[0], _ref.get_center()[1], 0])
        nl.add(_dot(nl.c2p(2)[:2], GOLD_BRIGHT))

        gr = MachAxes2D(
            center=np.array([-3.5, IY, 0.0]), x_range=(-3, 3), y_range=(-3, 3),
            grid_step=0.5, number_font_size=15, show_minor_ticks=False,
            show_axis_labels=False, show_origin=True,
        )
        gr.add(_arrow(gr.c2p(0, 0)[:2], gr.c2p(2.5, 1.5)[:2], COPPER_TERRA, 5, 0.25))
        arr = _arrow([0.85, IY], [-1.2, IY], GOLD_MUTED, 4, 0.2)
        l1 = _ar("خط أعداد — بُعد واحد", 17, TEAL).next_to(nl, DOWN, buff=0.3)
        l2 = _ar("فضاء متجهات — كذا بُعد", 17, GOLD_MUTED).next_to(gr, DOWN, buff=0.3)

        # 02:18.5: «فبدل ما العدد هو نقطة على خط أعداد في بُعد واحد...»
        scene.wait(5.8 * SPD)
        scene.play(FadeIn(nl), FadeIn(l1), run_time=0.8)

        # 02:23.5: «المتجه هو نفس الفكرة بس ممتد لكذا بُعد في فضاء المتجهات»
        scene.wait(4.2 * SPD)
        scene.play(GrowArrow(arr), FadeIn(gr), FadeIn(l2), run_time=1.2)

    # ---------- 2) ليه بفكّرك بالجملة دي؟ ----------
    # 02:29.5 - 02:44.0 | «طيب انت ممكن تقول ليه انا بفكرك بالجملة دي هنا تحديدا؟… عشان نفهم…» (14.5s)
    with beat(scene, 14.5):
        why = _ar("طيب ليه بفكّرك بالجملة دي هنا؟", 28, GOLD_LIGHT, True).move_to([0, 3.15, 0])
        ans = _chip(
            "عشان نفهم جمع المتجهات جت منين وليه شغّالة بالطريقة دي",
            GOLD_BRIGHT, w=9.4, h=0.8, size=20, filled=True,
        ).move_to([0, 3.15, 0])
        scene.play(FadeIn(why, shift=DOWN * 0.1), run_time=0.8)
        scene.wait(5.0 * SPD)
        scene.play(ReplacementTransform(why, ans), run_time=1.0)

    # ---------- 3) مش هنجمع بالأمثلة المدرسية (التفاحات) ----------
    # 02:44.0 - 02:57.5 | «لازم نشوف نفسنا الاول… مش هنجمع باستخدام الامثلة المدرسية…» (13.5s)
    with beat(scene, 13.5):
        scene.play(FadeOut(VGroup(bar, quote, src, nl, gr, arr, l1, l2, ans)), run_time=0.8)

        # 02:44.8: «لازم نشوف نفسنا الأول إحنا إزاي بنجمع الأرقام أصلاً»
        q_num = _ar("الأول: إحنا إزاي بنجمع الأرقام أصلاً؟", 30, GOLD_BRIGHT, True).move_to([0, 1.1, 0])
        scene.play(FadeIn(q_num, shift=DOWN * 0.1), run_time=0.8)

        # 02:49.0: «مش هنجمع باستخدام الأمثلة المدرسية، زي جمع التفاحات...»
        scene.wait(3.4 * SPD)
        school_box = _chip("الأمثلة المدرسية (زي جمع التفاحات)", COPPER_TERRA, w=7.2, h=0.8, size=21).move_to([0, -0.4, 0])
        scene.play(FadeIn(school_box, shift=UP * 0.1), run_time=0.8)
        scene.wait(1.0 * SPD)
        school_x = _cross([0, -0.4], 0.35, ERR_RED)
        scene.play(Create(school_x), run_time=0.6)

        scene.wait(4.2 * SPD)
        scene.play(FadeOut(VGroup(q_num, school_box, school_x)), run_time=0.6)

    # ---------- 4) الخطة: نجمع الأرقام كمتجهات ثم نعمّم ----------
    # 02:57.5 - 03:13.5 | «لكن احنا المرة دي هنجمع الارقام… متجه الوحدة وبيعبر عن الرقم واحد» (16.0s)
    with beat(scene, 16.0):
        scene.wait(1.0 * SPD)
        s1 = _chip(
            "1-  نجمع الأرقام كمتجهات على خط الأعداد (متجه الأساس: unit)",
            GOLD_LIGHT, w=9.6, h=0.85, size=20,
        ).move_to([0, 1.3, 0])
        scene.play(FadeIn(s1, shift=LEFT * 0.3), run_time=1.0)
        # 03:08.0: «والخط ده ليه متجه أساس اسمه متجه الوحدة وبيعبر عن الرقم واحد»
        scene.wait(8.5 * SPD)
        scene.play(Indicate(s1, color=GOLD_BRIGHT, scale_factor=1.03), run_time=1.0)

    # 03:13.5 - 03:21.5 | «بعدين هنعمم الفكرة من خط الاعداد الحقيقية الي اي عدد من الخطوط…» (8.0s)
    with beat(scene, 8.0):
        scene.wait(1.0 * SPD)
        s2 = _chip(
            "2-  نعمّم لأي عدد من الخطوط — وكل خط له متجه أساس مختلف",
            COPPER_TERRA, w=9.6, h=0.85, size=20,
        ).move_to([0, 0.0, 0])
        scene.play(FadeIn(s2, shift=LEFT * 0.3), run_time=1.0)

    # 03:21.5 - 03:27.0 | «…ومش شرط يكون بيعبر عن الرقم واحد اصلا» (5.5s)
    with beat(scene, 5.5):
        scene.wait(0.5 * SPD)
        note = _ar("ومتجه الأساس مش شرط يعبّر عن الرقم واحد", 22, TEAL).move_to([0, -1.3, 0])
        scene.play(FadeIn(note), run_time=0.8)

    # ---------- 5) نبدأ التنفيذ ----------
    # 03:27.0 - 03:32.2 | «وبدون سرديات اكتر من كدة يلا بينا نبدأ في التنفيذ مباشرة» (5.2s)
    with beat(scene, 5.2):
        scene.wait(2.2 * SPD)
        go = _ar("يلا نبدأ في التنفيذ مباشرة!", 24, GOLD_BRIGHT, True).move_to([0, -2.4, 0])
        scene.play(FadeIn(go, scale=1.08), run_time=0.7)

    _exit(scene)


class Dev(Scene):
    def construct(self):
        play_scene02(self)