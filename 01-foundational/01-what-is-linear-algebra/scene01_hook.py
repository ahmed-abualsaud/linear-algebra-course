from manim import *
from common.portal import MachPortal
from common.identity import turn_on_neon
from common.palette import GOLD_LIGHT, GOLD_BRIGHT, IVORY_WHITE


def play_scene01(scene):
    portal = MachPortal(scene)

    # 1. علامة الاستفهام
    q_mark = Text(
        "?", font="Cairo", weight=BOLD, font_size=150, color=GOLD_LIGHT
    ).shift(UP * 0.6)

    # 2. نص السؤال (بخط Cairo Bold المصمت النقي بدون تفريغ)
    question_text = Text(
        "إيه هو الجبر الخطي؟",
        font="Cairo",
        weight=BOLD,
        font_size=42,
        color=IVORY_WHITE,
    ).next_to(q_mark, DOWN, buff=0.6)

    # ==============================================================
    # 3. بناء ريشة النور المتوهجة
    # ==============================================================
    spark = VGroup(
        Circle(
            radius=0.18,
            stroke_width=0,
            fill_color=GOLD_LIGHT,
            fill_opacity=0.25,
        ),
        Circle(
            radius=0.08,
            stroke_width=0,
            fill_color=GOLD_BRIGHT,
            fill_opacity=0.60,
        ),
        Dot(radius=0.030, color="#FFFFFF", fill_opacity=1.0),
    ).set_z_index(40)

    # حساب نقطتي البداية والنهاية المضبوطتين بالمليمتر
    p_start = question_text.get_right() + RIGHT * 0.08
    # تم سحب نقطة النهاية لتتمركز بدقة فوق علامة الاستفهام "؟" دون تجاوز في الفراغ
    p_end = question_text.get_left() + RIGHT * 0.12
    spark.move_to(p_start)

    # إخفاء النص في البداية استعداداً لكشفه بالليزر
    question_text.set_opacity(0)
    scene.add(question_text)

    # ==============================================================
    # 1. إشعال النيون ودخول علامة الاستفهام (2.2 ثانية)
    # ==============================================================
    turn_on_neon(scene, run_time=1.0)
    portal.enter(q_mark, direction=RIGHT, run_time=1.2)

    # ==============================================================
    # 2. تأثير الليزر السينمائي: الشرارة تكشف النص وتتوقف عند نهاية الجملة
    # ==============================================================
    # أ) اشتعال الشرارة في بداية الجملة من اليمين (0.2s)
    scene.play(
        FadeIn(spark, scale=0.4),
        run_time=0.2,
    )

    # ب) محرك الكشف الليزري
    tracker = ValueTracker(0.0)

    def laser_reveal_update(mob):
        progress = tracker.get_value()
        curr_x = interpolate(p_start[0], p_end[0], progress)
        spark.move_to([curr_x, question_text.get_y(), 0])

        for sub in mob.submobjects:
            sub_x = sub.get_center()[0]
            if sub_x >= curr_x:
                sub.set_opacity(1.0)
            elif sub_x > curr_x - 0.35:
                fade = (curr_x - (sub_x - 0.35)) / 0.35
                sub.set_opacity(np.clip(1.0 - fade, 0.0, 1.0))
            else:
                sub.set_opacity(0.0)

    question_text.add_updater(laser_reveal_update)

    # تحريك الشرارة وكشف النص كاملاً في 1.8 ثانية
    scene.play(
        tracker.animate(rate_func=linear).set_value(1.0),
        run_time=1.8,
    )

    # إيقاف الـ updater وتثبيت النص مكتملاً ونقياً
    question_text.remove_updater(laser_reveal_update)
    question_text.set_opacity(1.0)

    # ج) انطفاء الشرارة فوق علامة الاستفهام مباشرة (0.3s)
    scene.play(
        FadeOut(spark, scale=1.4),
        run_time=0.3,
    )

    # وقفة استيعاب بعد اكتمال السؤال (0.5 ثانية)
    scene.wait(0.5)

    # ==============================================================
    # 3. عرض السؤال وثباته أثناء الشرح والتمهيد (14.2 ثانية)
    # ==============================================================
    scene.wait(14.2)

    # ==============================================================
    # 4. خروج السؤال وتفريغ الشاشة لعلم الحساب (2.8 ثانية)
    # ==============================================================
    portal.exit(q_mark, direction=LEFT, run_time=0.9)
    portal.exit(question_text, direction=DOWN, run_time=0.9)

    scene.wait(1.0)

    # إجمالي زمن المشهد الأول: 22.0 ثانية مضبوطة بالمليمتر!