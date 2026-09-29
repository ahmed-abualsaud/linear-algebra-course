from manim import *

from common.mobjects import mach_stick_figure, thought_bubble

from common.palette import GOLD_LIGHT, STONE_AXIS, COPPER_TERRA

from common.latex import mach_math_template


def play_scene05(scene):

    # ==============================================================
    # 1. شخصية التفكير متمركزة في المنتصف
    # ==============================================================

    thinker = mach_stick_figure(
        color=STONE_AXIS,
        pose="thinking",
        scale=1.0,
        blink=True,
        breathing=True,
    ).shift(
        LEFT * 0.9 + DOWN * 0.9
    )

    # ==============================================================
    # 2. بالونة التفكير
    # ==============================================================

    box, dots, mark = thought_bubble(
        text=r"! \ ?",
        anchor_head=thinker[0],
        color=GOLD_LIGHT,
        text_color=COPPER_TERRA,
        tex_template=mach_math_template,
    )

    scene_group = VGroup(
        thinker,
        box,
        dots,
        mark,
    )

    # ==============================================================
    # 3. ظهور الشخصية
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
        Write(mark),
        run_time=1.0,
    )

    # ==============================================================
    # 5. انتظار
    # ==============================================================

    # أثناء الانتظار:
    # - الشخصية تتنفس تلقائيًا
    # - الشخصية تبرمش تلقائيًا
    #
    # وكلاهما يعمل عن طريق updater داخلي.

    scene.wait(2.0)

    # ==============================================================
    # 6. تفريغ المشهد
    # ==============================================================

    scene.play(
        FadeOut(scene_group),
        run_time=0.6,
    )