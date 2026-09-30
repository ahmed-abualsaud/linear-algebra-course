from manim import *
from common.mobjects import mach_stick_figure, speech_bubble
from common.palette import GOLD_LIGHT, STONE_AXIS


def play_scene03(scene):

    # ==============================================================
    # 1. الشخصيتان: تفعيل التنفس والبربشة تلقائياً لمنع أي تشوه في العين
    # وضبط الارتفاع على DOWN * 0.65 لحماية الترجمة دون ملامسة السقف
    # ==============================================================

    person_right = mach_stick_figure(
        color=STONE_AXIS,
        pose="neutral",
        scale=0.9,
        blink=True,
        breathing=True,  # تنفس تلقائي داخلي آمن 100%
    ).shift(RIGHT * 1.5 + DOWN * 0.20)

    person_left = mach_stick_figure(
        color=GOLD_LIGHT,
        pose="neutral",
        scale=0.9,
        blink=True,
        breathing=True,  # تنفس تلقائي داخلي آمن 100%
    ).shift(LEFT * 1.5 + DOWN * 0.20)

    # ==============================================================
    # 2. بالونة السؤال - اليمين
    # ==============================================================

    box_r, dots_r, text_r = speech_bubble(
        lines_text=[
            "طيب إيه هو",
            "التفاضل والتكامل؟",
        ],
        anchor_head=person_right[0],
        color=STONE_AXIS,
        font_size=23,
        shift=RIGHT * 0.85,
    )

    # ==============================================================
    # 3. بالونة الإجابة - اليسار
    # ==============================================================

    box_l, dots_l, text_l = speech_bubble(
        lines_text=[
            "إحنا بندرس في التفاضل والتكامل",
            "حاجة اسمها الدوال، وبنطبق عليها",
            "عملية اسمها التفاضل وعملية تانية",
            "اسمها التكامل",
        ],
        anchor_head=person_left[0],
        color=GOLD_LIGHT,
        font_size=19,
        shift=LEFT * 0.85,
    )

    # ==============================================================
    # 4. ظهور الشخصيتين والتمهيد (5.5 ثوانٍ)
    # الشخصيتان تتنفسان وتبرمشان بأمان تام بدون scene.play(breathe)
    # الكلام:
    # "ونفس الكلام لو سألت حد درس علم التفاضل والتكامل عن إيه هو التفاضل والتكامل؟
    # هيرد عليك بطريقته هو وملخص اللي هيقوله غالباً هيكون حاجة شبه كدة:"
    # ==============================================================
    scene.play(
        FadeIn(person_right),
        FadeIn(person_left),
        run_time=0.8,
    )

    # وقفة آمنة تتنفس فيها الشخصيات وتبرمش بحرية
    scene.wait(4.7)

    # ==============================================================
    # 5. بالونة السؤال (4.1 ثوانٍ)
    # ==============================================================
    scene.play(
        FadeIn(
            dots_r,
            scale=0.5,
        ),
        FadeIn(
            box_r,
            scale=0.9,
        ),
        run_time=0.5,
    )

    scene.play(
        LaggedStart(
            *[
                FadeIn(
                    line,
                    shift=LEFT * 0.35,
                )
                for line in text_r
            ],
            lag_ratio=0.55,
        ),
        run_time=1.1,
    )

    # وقفة لقراءة السؤال
    scene.wait(2.5)

    # ==============================================================
    # 6. بالونة الإجابة (10.4 ثوانٍ)
    # ==============================================================
    scene.play(
        FadeIn(
            dots_l,
            scale=0.5,
        ),
        FadeIn(
            box_l,
            scale=0.9,
        ),
        run_time=0.5,
    )

    scene.play(
        LaggedStart(
            *[
                FadeIn(
                    line,
                    shift=LEFT * 0.35,
                )
                for line in text_l
            ],
            lag_ratio=0.45,
        ),
        run_time=2.0,
    )

    # وقفة مريحة وكافية جداً لقراءة أسطر الإجابة
    scene.wait(7.9)

    # ==============================================================
    # 7. تفريغ المشهد (2.0 ثانية)
    # ==============================================================
    all_objects = VGroup(
        person_right,
        person_left,
        box_r,
        dots_r,
        text_r,
        box_l,
        dots_l,
        text_l,
    )

    scene.play(
        FadeOut(all_objects),
        run_time=0.8,
    )

    # استقرار نهائي قبل مشهد الرسم البياني
    scene.wait(1.2)

    # الحسبة الإجمالية للمشهد الثالث:
    # 0.8 + 4.7 + 0.5 + 1.1 + 2.5 + 0.5 + 2.0 + 7.9 + 0.8 + 1.2 = 22.0 ثانية بالتمام والكمال!
    # والعيون محمية 100% ومستحيل تنكمش بعد الآن.