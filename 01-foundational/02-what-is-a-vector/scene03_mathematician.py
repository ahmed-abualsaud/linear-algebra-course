from manim import *
from common.mobjects import mach_stick_figure, speech_bubble
from common.mobjects.characters import mach_mathematician
from common.palette import GOLD_LIGHT, STONE_AXIS, COPPER_TERRA


def play_scene03(scene):

    # ==============================================================
    # 1. الشخصيتان: السائل وعالم الرياضيات
    # ==============================================================

    # السائل (على اليمين في وضعية محايدة متطلعة)
    asker = mach_stick_figure(
        color=STONE_AXIS,
        pose="neutral",
        scale=0.9,
        blink=True,
        breathing=True,
    ).shift(RIGHT * 1.8 + DOWN * 0.4)

    # عالم الرياضيات (على اليسار بالنظارة ووضعية التفكير الرصين)
    mathematician = mach_mathematician(
        color=COPPER_TERRA,
        accent_color=GOLD_LIGHT,
        pose="thinking",
        scale=0.9,
        blink=True,
        breathing=True,
        glasses=True,
    ).shift(LEFT * 1.8 + DOWN * 0.4)

    # ==============================================================
    # 2. بالونة السؤال (صادرة من السائل)
    # ==============================================================

    box_ask, dots_ask, text_ask = speech_bubble(
        lines_text=[
            "إيه هو العدد؟",
        ],
        anchor_head=asker[0],
        color=GOLD_LIGHT,
        font_size=24,
        shift=RIGHT * 0.6 + UP * 0.1,
    )

    # ==============================================================
    # 3. بالونة رد فعل / تفكير عالم الرياضيات (علامة تأمل صامتة)
    # ==============================================================

    box_math, dots_math, text_math = speech_bubble(
        lines_text=[
            "...",
        ],
        anchor_head=mathematician[0],
        color=COPPER_TERRA,
        font_size=26,
        shift=LEFT * 0.6 + UP * 0.1,
    )

    # ==============================================================
    # 4. الظهور الأولي (بداية الكلام)
    # الصوت: "ولو حاولت تسأل سؤال واحد من الـ 3 أسئلة دي لعالم من علماء الرياضيات..."
    # ==============================================================

    scene.play(
        FadeIn(asker, shift=UP * 0.2),
        FadeIn(mathematician, shift=UP * 0.2),
        run_time=0.8,
    )

    # "فغالباً إجابته هتفاجئك..."
    scene.wait(2.2)

    # ==============================================================
    # 5. طرح السؤال: "جرب تسأله وتقوله: إيه هو العدد؟"
    # ==============================================================

    scene.play(
        FadeIn(dots_ask, scale=0.5),
        FadeIn(box_ask, scale=0.9),
        run_time=0.5,
    )

    scene.play(
        FadeIn(text_ask, shift=LEFT * 0.25),
        run_time=0.7,
    )

    # وقفة استيعاب ونظرة عالم الرياضيات
    scene.wait(1.5)

    # ظهور تفكير عالم الرياضيات الرصين "..."
    scene.play(
        FadeIn(dots_math, scale=0.5),
        FadeIn(box_math, scale=0.9),
        FadeIn(text_math),
        run_time=0.6,
    )

    # "طبعاً الصورة اللي أنت متخيلها في ذهنك عن الأعداد قبل ما تسأله السؤال ده..."
    scene.wait(4.0)

    # ==============================================================
    # 6. تفريغ المشهد للانتقال للمشهد الرابع (الأمثلة الحسية)
    # ==============================================================

    all_scene = VGroup(
        asker,
        mathematician,
        box_ask,
        dots_ask,
        text_ask,
        box_math,
        dots_math,
        text_math,
    )

    scene.play(
        FadeOut(all_scene),
        run_time=0.8,
    )

    scene.wait(0.5)