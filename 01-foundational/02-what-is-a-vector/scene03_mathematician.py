from manim import *
from common.mobjects import mach_stick_figure, speech_bubble
from common.mobjects.characters import mach_mathematician
from common.palette import COPPER_TERRA, GOLD_LIGHT, STONE_AXIS


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
            "إيه هو العدد أصلاً؟",
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

    # ==============================================================
    # 4. الظهور الأولي وتجهيز الحوار (6.3 ث)
    # [00:58.0 -> 01:04.3 في التراك الصوتي]
    # ==============================================================
    # ظهور الشخصيتين مع بداية الجملة:
    # "ولو حاولت تسأل سؤال واحد من الـ 3 أسئلة دي لعالم من علماء الرياضيات..."
    scene.play(
        FadeIn(asker, shift=UP * 0.2),
        FadeIn(mathematician, shift=UP * 0.2),
        run_time=0.8,
    )

    # الشخصيتان تتنفسان وترمشان أثناء تكملة الجملة:
    # "...فغالباً إجابته هتفاجئك..."
    scene.wait(5.5)

    # ==============================================================
    # 5. طرح السؤال من السائل (2.7 ث)
    # "جرب انت تسأله وتقوله: إيه هو العدد أصلاً؟" [01:04.3 -> 01:07.0]
    # ==============================================================
    # ظهور البالونة مع "جرب انت تسأله وتقوله..."
    scene.play(
        FadeIn(dots_ask, scale=0.5),
        FadeIn(box_ask, scale=0.9),
        run_time=0.5,
    )

    # ظهور النص مع نطق "...إيه هو العدد أصلاً؟"
    scene.play(
        FadeIn(text_ask, shift=LEFT * 0.2),
        run_time=0.7,
    )

    # وقفة قصيرة جداً لانتهاء نطق السؤال [01:07.0 -> 01:08.5]
    scene.wait(1.5)

    # ==============================================================
    # 6. رد فعل وحيرة عالم الرياضيات الصامتة (2.6 ث)
    # [01:08.5 -> 01:10.5 في التراك الصوتي]
    # ==============================================================
    # ظهور بالونة التفكير "..." فوق رأس عالم الرياضيات
    scene.play(
        FadeIn(dots_math, scale=0.5),
        FadeIn(box_math, scale=0.9),
        FadeIn(text_math),
        run_time=0.6,
    )

    # وقفة صمت وتأمل لإبراز عمق السؤال وصعوبة الإجابة
    scene.wait(2.0)

    # ==============================================================
    # 7. تفريغ المشهد والانتقال للمشهد الرابع (1.4 ث)
    # [01:10.5 -> 01:12.0 في التراك الصوتي]
    # ==============================================================
    scene.play(
        FadeOut(all_scene),
        run_time=0.8,
    )

    # فاصل شاشة سوداء نظيف قبل انطلاق بطاقات المشهد الرابع عند 01:12.0
    scene.wait(0.6)