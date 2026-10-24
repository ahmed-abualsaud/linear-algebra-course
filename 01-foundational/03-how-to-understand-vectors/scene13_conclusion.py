"""
المشهد 13: الخلاصة — المتجه ليس سهماً ولا قائمة؛ هما طريقتا تمثيل لعنصر في فضاء المتجهات.
مشهد ثنائي الأبعاد (الكاميرا مسطحة بعد خروج المشهد 12).
المدة المضبوطة: 58.0 ثانية (من 06:45.0 إلى 07:43.0 نهاية الفيديو).
"""
from manim import *
import numpy as np

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    COPPER_TERRA,
    IVORY_WHITE,
    STONE_AXIS,
)

CARD_FILL = "#17100A"


def _ar(txt, size=22, color=IVORY_WHITE, bold=False):
    body = f"<b>{txt}</b>" if bold else txt
    return MarkupText(body, font="Cairo", font_size=size, color=color)


def _card(w=3.8, h=3.0, color=GOLD_LIGHT):
    return RoundedRectangle(corner_radius=0.22, width=w, height=h, stroke_color=color,
                            stroke_width=2.2, fill_color=CARD_FILL, fill_opacity=0.92)


def _cross(card, color=COPPER_TERRA):
    c = card.get_center()
    a, b = card.width * 0.42, card.height * 0.42
    return VGroup(
        Line(c + np.array([-a, b, 0]), c + np.array([a, -b, 0]), color=color, stroke_width=7),
        Line(c + np.array([-a, -b, 0]), c + np.array([a, b, 0]), color=color, stroke_width=7),
    ).set_opacity(0.9)


def play_scene13(scene: Scene):
    # تأكيد أن الكاميرا مسطحة تماماً (بدون أي ميل أو تدوير)
    if isinstance(scene, ThreeDScene):
        scene.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0)

    CY = 0.35
    LX, RX = -4.35, 4.35

    title = _ar("المتجه مش مجرد سهم.. ومش مجرد قائمة أرقام", 30, GOLD_LIGHT, True).to_edge(UP, buff=0.55)

    # ---------------- بطاقة السهم (يسار) ----------------
    arrow_card = _card().move_to([LX, CY, 0])
    ax = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1], x_length=2.2, y_length=2.2,
              axis_config=dict(color=STONE_AXIS, stroke_width=2, include_ticks=False, include_tip=False))
    ax.move_to(arrow_card.get_center() + np.array([0, 0.05, 0]))
    arr = Arrow(ax.c2p(0, 0), ax.c2p(3, 4), buff=0, color=GOLD_BRIGHT, stroke_width=6,
                max_tip_length_to_length_ratio=0.18)
    arrow_grp = VGroup(arrow_card, ax, arr)
    arrow_cap = _ar("سهم", 24, GOLD_BRIGHT, True).next_to(arrow_card, DOWN, buff=0.25)

    # ---------------- بطاقة القائمة (يمين) ----------------
    list_card = _card().move_to([RX, CY, 0])
    lst = MathTex(r"(\,3\,,\,4\,,\,5\,,\,10\,)", font_size=46, color=IVORY_WHITE).move_to(list_card.get_center())
    list_grp = VGroup(list_card, lst)
    list_cap = _ar("قائمة أرقام", 24, GOLD_BRIGHT, True).next_to(list_card, DOWN, buff=0.25)
    list_cap.match_y(arrow_cap)

    # ---------------- فضاء المتجهات (المنتصف) ----------------
    space = Circle(radius=1.55, stroke_color=COPPER_TERRA, stroke_width=2.4, stroke_opacity=0.9,
                   fill_color=COPPER_TERRA, fill_opacity=0.05).move_to([0, CY, 0])
    space_d = DashedVMobject(space.copy().set_fill(opacity=0), num_dashes=40)
    space_lbl = _ar("فضاء المتجهات", 24, COPPER_TERRA, True).next_to(space, UP, buff=0.2)
    glow = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=GOLD_BRIGHT, fill_opacity=o).move_to(space.get_center())
                    for r, o in ((0.55, 0.06), (0.38, 0.12), (0.24, 0.22))])
    dot = Dot(space.get_center(), radius=0.12, color=GOLD_BRIGHT)
    vec_lbl = _ar("المتجه", 26, IVORY_WHITE, True).next_to(dot, DOWN * 1.7, buff=0.35)
    center_grp = VGroup(space, space_d, glow, dot)

    # ---------------- الروابط ----------------
    def link(a, b):
        return DashedLine(a, b, dash_length=0.1, stroke_width=2.4, color=GOLD_LIGHT, stroke_opacity=0.85)

    l_left = link(arrow_card.get_right(), space.get_left())
    l_right = link(list_card.get_left(), space.get_right())
    t_left = _ar("تمثيل", 18, GOLD_LIGHT).next_to(l_left, UP, buff=0.1)
    t_right = _ar("تمثيل", 18, GOLD_LIGHT).next_to(l_right, UP, buff=0.1)

    # ================= الحركة والتزامن (58.0 ثانية إجمالي) =================

    # 1. العنوان والبطاقتان وعلامات الخطأ (4.0s إجمالي)
    # [06:45.0 - 06:49.0]: "عشان كده المتجه مش مجرد قائمة معينة من الارقام ومش مجرد سهم في الفضاء..."
    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=1.0)
    scene.play(FadeIn(arrow_grp, shift=RIGHT * 0.2), FadeIn(list_grp, shift=LEFT * 0.2), run_time=1.2)
    no_arrow = _ar("مش مجرد سهم", 22, COPPER_TERRA, True).next_to(arrow_card, DOWN, buff=0.25)
    no_list = _ar("مش مجرد قائمة", 22, COPPER_TERRA, True).next_to(list_card, DOWN, buff=0.25)
    cx1, cx2 = _cross(arrow_card), _cross(list_card)
    scene.play(Create(cx1), Create(cx2), FadeIn(no_arrow), FadeIn(no_list), run_time=1.2)
    scene.wait(0.6)

    # 2. المتجه الحقيقي جزء من فضاء المتجهات (3.0s إجمالي)
    # [06:49.0 - 06:52.0]: "...هو زي ما قولتلك من شوية انه جزء من فضاء المتجهات"
    scene.play(FadeOut(cx1), FadeOut(cx2), FadeOut(no_arrow), FadeOut(no_list), run_time=0.8)
    scene.play(Create(space_d), FadeIn(space), FadeIn(space_lbl, shift=DOWN * 0.1), run_time=1.2)
    scene.play(FadeIn(glow), FadeIn(dot, scale=0.4), FadeIn(vec_lbl, shift=UP * 0.1), run_time=1.0)

    # 3. السهم والقائمة = طرق تمثيل (14.0s إجمالي)
    # [06:52.0 - 07:06.0]: "والسهم والقايمة دول هما طرق تمثيل المتجهات لتقريب الصورة الذهنية ليك مش اكتر... عشان صورة المتجه تكون مالوفة ليك وانت بتطبق قواعد المتجهات"
    scene.play(Create(l_left), Create(l_right), FadeIn(t_left), FadeIn(t_right),
               FadeIn(arrow_cap), FadeIn(list_cap), run_time=1.5)
    scene.play(Indicate(arrow_grp, scale_factor=1.05, color=GOLD_BRIGHT),
               Indicate(list_grp, scale_factor=1.05, color=GOLD_BRIGHT), run_time=1.5)
    note = _ar("السهم والقائمة طرق تمثيل لتقريب الصورة الذهنية ليس أكثر", 22, IVORY_WHITE) \
        .move_to([0, -2.6, 0])
    scene.play(FadeIn(note, shift=UP * 0.1), run_time=1.2)
    scene.wait(9.8)

    # 4. تعميم مفهوم العدد (24.0s إجمالي)
    # [07:06.0 - 07:30.0]: "وبالمناسبة.. إنت ممكن تعتبر ان المتجه هو تعميم مباشر لمفهوم 'العدد'... فبدل ما العدد هو نقطة على خط أعداد في بُعد واحد بمسطرة واحدة، المتجه هو نفس الفكرة بس ممتدة لكذا بُعد في فضاء المتجهات وبدل المسطرة الواحدة عندك مساطر أو متجهات أساس بعدد الأبعاد دي"
    scene.wait(10.0)
    # وميض ناعم للنقطة الذهبية بالمنتصف عند قولك: "المتجه هو نفس الفكرة بس ممتدة لكذا بُعد في فضاء المتجهات" (07:16)
    scene.play(Indicate(dot, scale_factor=1.5, color=GOLD_BRIGHT), run_time=2.0)
    scene.wait(12.0)

    # 5. الخاتمة والاستعداد للحلقة الرابعة (9.0s إجمالي)
    # [07:30.0 - 07:39.0]: "واعتقد دلوقتي احنا بقينا جاهزين عشان نبدأ نتعلم قواعد المتجهات.. وده اللي هنعمله الحلقة الجاية.. اشوفكم الحلقة الجاية باذن الله"
    ready = _ar("جاهز تتعلم قواعد فضاء المتجهات — في الحلقة الجاية!", 26, GOLD_BRIGHT, True).move_to([0, -3.3, 0])
    scene.play(FadeIn(ready, shift=UP * 0.1), run_time=1.2)
    scene.play(Indicate(dot, scale_factor=2.0, color=GOLD_BRIGHT), run_time=1.8)
    scene.wait(6.0)

    # 6. التلاشي النهائي الكامل (4.0s إجمالي)
    # [07:39.0 - 07:43.0]: مع قولك "سلام عليكم" حتى نهاية الفيديو بالمللي
    outs = [title, arrow_grp, list_grp, arrow_cap, list_cap, center_grp, space_lbl, vec_lbl,
            l_left, l_right, t_left, t_right, note, ready]
    scene.play(*[FadeOut(m) for m in outs], run_time=2.2)
    scene.wait(1.8)

    # المجموع: 4.0 + 3.0 + 14.0 + 24.0 + 9.0 + 4.0 = 58.0 ثانية بالتمام والكمال!