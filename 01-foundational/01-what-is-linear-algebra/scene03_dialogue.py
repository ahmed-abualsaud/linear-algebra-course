from manim import *
from common.identity import turn_off_neon
from common.mobjects import mach_stick_figure, speech_bubble
from common.palette import GOLD_LIGHT, STONE_AXIS


def play_scene03(scene):

    # ==============================================================
    # 1. الشخصيتان في مواضعهما المعتمدة
    # ==============================================================

    person_right = mach_stick_figure(
        color=STONE_AXIS,
        pose="neutral",
        scale=0.9,
        blink=True,
    ).shift(
        RIGHT * 1.5 + DOWN * 0.9
    )

    person_left = mach_stick_figure(
        color=GOLD_LIGHT,
        pose="neutral",
        scale=0.9,
        blink=True,
    ).shift(
        LEFT * 1.5 + DOWN * 0.9
    )

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

    turn_off_neon(scene, run_time=0.6)


    # ==============================================================
    # 4. ظهور الشخصيتين
    # ==============================================================

    scene.play(
        FadeIn(person_right),
        FadeIn(person_left),
        run_time=0.8,
    )

    # ==============================================================
    # 5. أول لحظة حياة للشخصيتين
    # ==============================================================
    #
    # البربشة أصبحت تلقائية داخل MachAvatar.
    #
    # لذلك لا نحتاج:
    #
    #     person_right.blink()
    #     person_left.blink()
    #
    # الـupdater الداخلي للشخصية سيستمر في العمل
    # بالتوازي مع بقية الـanimations.
    #
    # هنا نستخدم التنفس فقط كلحركة إضافية أولية.
    #

    scene.play(
        person_right.breathe(
            amount=0.035,
            run_time=1.3,
        ),
        person_left.breathe(
            amount=0.035,
            run_time=1.3,
        ),
    )

    # ==============================================================
    # 6. بالونة السؤال
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

    scene.wait(0.6)

    # ==============================================================
    # 7. بالونة الإجابة
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

    scene.wait(2.2)

    # ==============================================================
    # 8. تفريغ المشهد
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
        run_time=0.6,
    )