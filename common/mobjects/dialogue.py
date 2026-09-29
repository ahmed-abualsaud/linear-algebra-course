"""
بالونات الحوار والتفكير الموحدة لقناة MACH-MATH:
- أبعاد أوتوماتيكية دقيقة حول النص (Auto-fit).
- دوائر ربط متدرجة ناعمة برأس الشخصية في جميع البالونات.
- زجاج فحمي دافئ معتم يمنع تداخل الخطوط.
"""
from manim import *
import numpy as np


def speech_bubble(
    lines_text,
    anchor_head,
    color=WHITE,
    font_size=20,
    font="Cairo",
    text_color=WHITE,
    buff=0.75,
    shift=ORIGIN,
    bg_color="#24201A",
    bg_opacity=0.75,
):
    """
    بالونة حوار موحدة ومتصلة برأس الشخصية عبر دوائر ناعمة.
    """
    if isinstance(lines_text, str):
        lines_text = lines_text.split("\n")

    # 1. إنشاء الأسطر العربية
    lines_group = VGroup(*[
        Text(line, font=font, font_size=font_size, color=text_color)
        for line in lines_text
    ]).arrange(DOWN, buff=0.18, aligned_edge=RIGHT)

    w = lines_group.width + 0.7
    h = lines_group.height + 0.65

    # 2. الصندوق الزجاجي
    box = RoundedRectangle(
        corner_radius=0.35,
        width=w,
        height=h,
        color=color,
        stroke_width=1.5,
        fill_color=bg_color,
        fill_opacity=bg_opacity
    )
    lines_group.move_to(box)

    bubble_core = VGroup(box, lines_group)
    bubble_core.next_to(anchor_head, UP, buff=buff).shift(shift)

    # 3. حساب موضع دوائر الربط (Bubble Dots)
    is_left = bubble_core.get_center()[0] < anchor_head.get_center()[0]
    head_pos = anchor_head.get_top() + (LEFT * 0.15 if is_left else RIGHT * 0.15)
    box_corner = box.get_bottom() + (RIGHT * 0.4 if is_left else LEFT * 0.4)

    dot1 = Circle(radius=0.06, color=color, fill_color=color, fill_opacity=0.9).move_to(
        head_pos * 0.65 + box_corner * 0.35
    )
    dot2 = Circle(radius=0.10, color=color, fill_color=color, fill_opacity=0.9).move_to(
        head_pos * 0.30 + box_corner * 0.70
    )

    dots = VGroup(dot1, dot2)
    return box, dots, lines_group


def thought_bubble(
    text,
    anchor_head,
    color=WHITE,
    text_color=None,
    font_size=55,
    buff=0.35,              # <--- تم تعديل المسافة الافتراضية
    extra_shift=ORIGIN,
    tex_template=None,
    bg_color="#24201A",
    bg_opacity=0.75,
):
    """
    بالونة تفكير موحدة لمعادلات ورموز التفكير بمسافات دوائر منضبطة.
    """
    mark = MathTex(text, tex_template=tex_template, font_size=font_size, color=text_color or color)

    w = mark.width + 0.85
    h = mark.height + 0.65

    box = RoundedRectangle(
        corner_radius=0.35,
        width=w,
        height=h,
        color=color,
        stroke_width=1.6,
        fill_color=bg_color,
        fill_opacity=bg_opacity,
    )
    mark.move_to(box)

    bubble_core = VGroup(box, mark)
    bubble_core.next_to(anchor_head, UP + RIGHT, buff=buff).shift(extra_shift)

    head_pos = anchor_head.get_top() + RIGHT * 0.15
    box_corner = box.get_bottom() + LEFT * 0.25

    # الدائرة الأولى الصغيرة قرب الرأس
    dot1 = Circle(radius=0.055, color=color, fill_color=color, fill_opacity=0.9).move_to(
        head_pos * 0.68 + box_corner * 0.32
    )
    # الدائرة الثانية أبعدناها عن قاع البالونة (0.58 بدلاً من 0.70) حتى لا تلتصق بها
    dot2 = Circle(radius=0.085, color=color, fill_color=color, fill_opacity=0.9).move_to(
        head_pos * 0.42 + box_corner * 0.58
    )

    dots = VGroup(dot1, dot2)
    return box, dots, mark