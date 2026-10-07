from manim import *
from common.mobjects import mach_stick_figure, thought_bubble
from common.palette import GOLD_LIGHT, STONE_AXIS, COPPER_TERRA
from common.latex import mach_math_template


def play_scene01(scene):

    # ==============================================================
    # 1. شخصية التفكير (العين والتنفس يعملان تلقائياً بأمان 100%)
    # ==============================================================

    thinker = mach_stick_figure(
        color=STONE_AXIS,
        pose="thinking",
        scale=1.0,
        blink=True,
        breathing=True,
    ).shift(LEFT * 0.9)

    # ==============================================================
    # 2. بالونة التفكير
    # ==============================================================

    box, dots, mark, draw_start, draw_end = thought_bubble(
        text="إيه هو المتجه؟",
        anchor_head=thinker[0],
        color=GOLD_LIGHT,
        tex_template=mach_math_template,
    )

    scene_group = VGroup(
        thinker,
        box,
        dots,
        mark,
    )

    # ==============================================================
    # 3. ظهور الشخصية (0.8 ثانية)
    # يبدأ عند 01:29 في الفيديو مع بداية صوتك
    # ==============================================================

    scene.play(
        FadeIn(
            thinker,
            shift=UP * 0.2,
        ),
        run_time=0.8,
    )

    # ==============================================================
    # 4. ظهور بالونة التفكير
    # ==============================================================

    scene.play(
        FadeIn(
            dots,
            scale=0.5,
        ),
        FadeIn(
            box,
            scale=0.9,
        ),
        run_time=0.5,
    )

    # ==============================================================
    # تأثير الرسم / الليزر
    # النص يظهر من اليمين إلى اليسار
    # ==============================================================

    spark = VGroup(
        Circle(
            radius=0.14,
            stroke_width=0,
            fill_color=GOLD_LIGHT,
            fill_opacity=0.25,
        ),
        Circle(
            radius=0.065,
            stroke_width=0,
            fill_color=GOLD_LIGHT,
            fill_opacity=0.65,
        ),
        Dot(
            radius=0.022,
            color="#FFFFFF",
            fill_opacity=1.0,
        ),
    ).set_z_index(40)

    spark.move_to(draw_start)

    # إخفاء النص بالكامل
    mark.set_opacity(0)

    scene.add(mark)
    scene.add(spark)

    tracker = ValueTracker(0.0)


    def draw_reveal_update(mob):
        progress = tracker.get_value()

        curr_x = interpolate(
            draw_start[0],
            draw_end[0],
            progress,
        )

        spark.move_to(
            [
                curr_x,
                mark.get_y(),
                0,
            ]
        )

        for sub in mob.submobjects:
            sub_x = sub.get_center()[0]

            if sub_x >= curr_x:
                sub.set_opacity(1.0)

            elif sub_x > curr_x - 0.35:
                fade = (
                    curr_x - (sub_x - 0.35)
                ) / 0.35

                sub.set_opacity(
                    np.clip(
                        1.0 - fade,
                        0.0,
                        1.0,
                    )
                )

            else:
                sub.set_opacity(0.0)


    mark.add_updater(draw_reveal_update)

    scene.play(
        tracker.animate(
            rate_func=linear
        ).set_value(1.0),
        run_time=1.3,
    )

    mark.remove_updater(draw_reveal_update)
    mark.set_opacity(1.0)

    scene.play(
        FadeOut(
            spark,
            scale=1.4,
        ),
        run_time=0.25,
    )

    scene.wait(5)

    # ==============================================================
    # 6. تفريغ المشهد (1.8 ثانية)
    # ==============================================================

    scene.play(
        FadeOut(scene_group),
        run_time=0.8,
    )

    # استقرار الغرفة قبل كروت المقارنة في المشهد السادس
    scene.wait(1.0)