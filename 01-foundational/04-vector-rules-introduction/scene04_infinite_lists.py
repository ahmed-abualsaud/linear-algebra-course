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
from episode_04_common import _ar, _tex, _list_card


# الحلقة 04 — المشهد 4: نفس المتجه بعدد لا نهائي من القوائم

def play_scene04(scene):

    # ---------- 1) المتجه v في القمة ----------
    # 05:13.0 - 05:14.0 | "بعد ما شرحتلك مكونات المتجه اللي هما مركبات المتجه ومتجهات الأساس..."
    v_core = _tex(r"\mathbf{v}", 52, GOLD_BRIGHT)
    v_ring = Circle(radius=0.62, color=GOLD_LIGHT, stroke_width=2.4)
    v_glow = Circle(radius=0.85, stroke_width=0, fill_color=GOLD_LIGHT, fill_opacity=0.07)
    v_group = VGroup(v_glow, v_ring, v_core).move_to([0, 2.95, 0])
    scene.play(GrowFromCenter(v_group), run_time=1.0)

    # 05:14.0 - 05:25.0 | "عايز ألفت انتباهك لحاجة أنا قلتها الحلقة اللي فاتت، وهي إن مركبات المتجه اللي هي الأرقام اللي بتكون جوة القايمة اللي بتمثل المتجه..."
    scene.wait(11.0)

    # ---------- 2) نفس المتجه بقوائم مختلفة (كل قايمة بمتجهات أساسها) ----------
    c1 = _list_card(["3", "4", "5", "10"],
                    [r"\mathbf{e}_1", r"\mathbf{e}_2", r"\mathbf{e}_3", r"\mathbf{e}_4"], GOLD_LIGHT)
    c2 = _list_card(["3", "400", "1.282", "10"],
                    [r"\mathbf{e}_1", r"\mathbf{e}_{\text{cm}}", r"\mathbf{e}_{\text{khashaba}}", r"\mathbf{e}_4"],
                    GOLD_LIGHT)
    c3 = _list_card(["4.7", "5", "10"],
                    [r"\mathbf{e}_{\text{path}}", r"\mathbf{e}_{\text{pisa}}", r"\mathbf{e}_4"], GOLD_LIGHT)
    cards = [c1, c2, c3]
    xs = [-4.6, 0.0, 4.6]
    links = []
    for card, x in zip(cards, xs):
        card.move_to([x, 0.8, 0])
        links.append(DashedLine(v_ring.get_bottom(), card.get_top(), dash_length=0.1,
                                color=GOLD_MUTED, stroke_width=1.6, stroke_opacity=0.8))

    # 05:25.0 - 05:38.5 | ظهور البطاقات الثلاث بالتتابع أثناء شرح "...دي أرقام مش ثابتة وإنك ممكن تكتب نفس المتجه بعدد لا نهائي من القوائم..."
    card_waits = [3.5, 3.5, 13.5]
    for card, link, w in zip(cards, links, card_waits):
        scene.play(Create(link), FadeIn(card, shift=UP * 0.25), run_time=1.0)
        scene.wait(w)

    # 05:48.5 - 05:56.5 | "طيب، انت ممكن تسأل نفسك: إيه هو السبب اللي يخليني أقدر أكتب نفس المتجه بعدد لا نهائي من القوائم؟"
    inf_lbl = _ar("نفس المتجه… بعدد لا نهائي من القوائم", 26, GOLD_LIGHT, True).move_to([0, -1.1, 0])
    inf_sign = _tex(r"\infty", 56, COPPER_TERRA).next_to(v_ring, RIGHT, buff=0.8)
    scene.play(FadeIn(inf_lbl, shift=UP * 0.1), Write(inf_sign), run_time=1.2)
    scene.wait(6.8)

    # ---------- 3) السبب: حاجتين ----------
    # 05:56.5 - 06:00.5 | "والحقيقة إن السبب الرئيسي لده هما حاجتين:"
    scene.play(FadeOut(inf_lbl), run_time=0.6)
    scene.wait(3.4)

    def _reason_box(txt, color):
        t = _ar(txt, 22, IVORY_WHITE, True)
        box = RoundedRectangle(corner_radius=0.18, width=5.4, height=1.3,
                               stroke_color=color, stroke_width=2.0,
                               fill_color="#14100A", fill_opacity=0.92)
        t.move_to(box)
        return VGroup(box, t)

    r1 = _reason_box("1- طريقة اختيارنا للخصائص\nاللي بتصف المتجه", GOLD_LIGHT).move_to([3.4, -1.5, 0])
    r2 = _reason_box("2- طريقة تعريفنا\nلمتجهات الأساس", COPPER_TERRA).move_to([-3.4, -1.5, 0])
    plus = _tex("+", 52, GOLD_BRIGHT).move_to([0, -1.5, 0])

    # 06:00.5 - 06:06.5 | "أول حاجة: هي طريقة اختيارنا للخصائص اللي بتصف المتجه..."
    scene.play(FadeIn(r1, shift=UP * 0.2), run_time=0.9)
    scene.wait(5.1)

    # 06:06.5 - 06:11.5 | "والحاجة التانية: هي طريقة تعريفنا لمتجهات الأساس..."
    scene.play(FadeIn(r2, shift=UP * 0.2), FadeIn(plus), run_time=0.9)
    scene.wait(4.1)

    # 06:11.5 - 06:24.5 | "يعني بعبارة تانية: الخصائص اللي بنختارها عشان نصف بيها المتجه، ومتجهات الأساس... هما اللي بيأثروا على طريقة كتابة المتجه وعلى أرقام مركباته"
    scene.wait(5.0)
    arrow_down = Arrow([0, -2.1, 0], [0, -2.5, 0], buff=0, color=GOLD_BRIGHT, stroke_width=5,
                       max_tip_length_to_length_ratio=0.5)
    result = _ar("بيأثروا على طريقة كتابة المتجه وعلى أرقام مركباته", 24, GOLD_BRIGHT, True).move_to([0, -3.0, 0])
    scene.play(GrowArrow(arrow_down), FadeIn(result, shift=UP * 0.1), run_time=1.0)
    scene.wait(7.0)

    # 06:24.5 - 06:33.0 | "وخليني أشرحلك التأثير ده بيتم إزاي في مثال الطيارة عشان تقدر تستوعب الفكرة"
    scene.wait(7.3)
    scene.play(FadeOut(VGroup(v_group, inf_sign, r1, r2, plus, arrow_down, result, *cards, *links)), run_time=1.0)
    scene.wait(0.2)


class Dev(ThreeDScene):
    def construct(self):
        play_scene04(self)