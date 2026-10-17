from manim import *
from common.latex import mach_math_template
from common.mobjects import mach_stick_figure, thought_bubble
from common.palette import COPPER_TERRA, GOLD_LIGHT, STONE_AXIS


def play_scene01(scene):

    # ==============================================================
    # 1. شخصية التفكير
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
    # يتزامن مع جملة: "السلام عليكم" [00:00 - 00:01]
    # ==============================================================
    scene.play(
        FadeIn(
            thinker,
            shift=UP * 0.2,
        ),
        run_time=0.8,
    )

    # ==============================================================
    # 4. فترة التفكير والاستماع (6.5 ثانية)
    # الشخصية تتنفس وترمش أثناء قولك:
    # "في الحلقة اللي فاتت عرفنا إن الجبر الخطي هو علم بيتعامل مع حاجة اسمها متجه"
    # [00:01 - 00:07.3]
    # ==============================================================
    scene.wait(6.5)

    # ==============================================================
    # 5. ظهور بالونة التفكير (0.6 ثانية)
    # تبدأ بالظهور فوراً مع جملة: "وفي الحلقة دي عاوزين نعرف..."
    # [00:07.3 - 00:08.5]
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
        run_time=0.6,
    )

    # ==============================================================
    # 6. تأثير رسم السؤال بالليزر (1.6 ثانية)
    # يتزامن تماماً مع نطقك لسؤال: "...إيه هو المتجه أصلاً؟"
    # [00:08.5 - 00:10.5]
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
    mark.set_opacity(0)
    scene.add(mark)
    scene.add(spark)

    tracker = ValueTracker(0.0)

    def draw_reveal_update(mob):
        progress = tracker.get_value()
        curr_x = interpolate(draw_start[0], draw_end[0], progress)
        spark.move_to([curr_x, mark.get_y(), 0])

        for sub in mob.submobjects:
            sub_x = sub.get_center()[0]
            if sub_x >= curr_x:
                sub.set_opacity(1.0)
            elif sub_x > curr_x - 0.35:
                fade = (curr_x - (sub_x - 0.35)) / 0.35
                sub.set_opacity(np.clip(1.0 - fade, 0.0, 1.0))
            else:
                sub.set_opacity(0.0)

    mark.add_updater(draw_reveal_update)

    scene.play(
        tracker.animate(rate_func=linear).set_value(1.0),
        run_time=1.6,
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

    # ==============================================================
    # 7. استقرار المشهد والسؤال ظاهر (تمت زيادة 0.5 ثانية هنا لتصبح 1.95 ثانية)
    # لإعطاء المشاهد وقتاً كافياً لقراءة السؤال واستيعابه
    # ==============================================================
    scene.wait(1.95)

    # ==============================================================
    # 8. تفريغ المشهد والانتقال للمشهد الثاني (0.8 ثانية)
    # ==============================================================
    scene.play(
        FadeOut(scene_group),
        run_time=0.8,
    )

    # فاصل سكون طبيعي قبل بدء رسم الجدول في المشهد الثاني
    scene.wait(0.1)