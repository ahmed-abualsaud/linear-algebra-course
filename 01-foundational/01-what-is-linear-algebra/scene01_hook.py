from manim import *
from common.portal import MachPortal
from common.identity import turn_on_neon
from common.palette import GOLD_LIGHT, IVORY_WHITE


def play_scene01(scene):
    portal = MachPortal(scene)

    # 1. علامة الاستفهام
    q_mark = Text(
        "?",
        font="Cairo",
        weight=BOLD,
        font_size=150,
        color=GOLD_LIGHT
    ).shift(UP * 0.6)

    # 2. نص السؤال
    question_text = Text(
        "إيه هو الجبر الخطي؟",
        font="Cairo",
        weight=BOLD,
        font_size=42,
        color=IVORY_WHITE
    ).next_to(q_mark, DOWN, buff=0.6)

    turn_on_neon(scene, run_time=0.8)

    # ==============================================================
    # الأنيميشن السينمائي: اختراق الجدار بالتزامن مع نبضة النيون
    # ==============================================================
    # علامة الاستفهام تخترق الجدار الأيمن
    portal.enter(q_mark, direction=RIGHT, run_time=1.2)

    # نص السؤال يخترق الأرضية ويصعد لمكانه
    portal.enter(question_text, direction=DOWN, distance=3.0, run_time=0.9)
    scene.wait(1.5)

    # خروج علامة الاستفهام مخترقة الجدار الأيسر واختفاؤها
    portal.exit(q_mark, direction=LEFT, run_time=0.8)
    portal.exit(question_text, direction=DOWN, run_time=0.8)