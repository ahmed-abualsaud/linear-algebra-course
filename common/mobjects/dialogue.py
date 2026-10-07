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
    text_color=WHITE,
    font_size=35,
    font="Cairo",
    buff=0.45,            # زيادة طفيفة للمسافة لتعطي مساحة للدوائر
    extra_shift=ORIGIN,
    tex_template=None,
    bg_color="#24201A",
    bg_opacity=0.75,
    use_math=False,
):
    """
    بالونة تفكير موحدة.
    ترجع:
        box, dots, mark, draw_start, draw_end
    """

    if isinstance(text, Mobject):
        mark = text
    elif use_math:
        mark = MathTex(
            text,
            tex_template=tex_template,
            font_size=font_size,
            color=text_color or color,
        )
    else:
        mark = Text(
            str(text),
            font=font,
            font_size=font_size,
            color=text_color or color,
        )
        mark.submobjects.sort(
            key=lambda m: -m.get_center()[0]
        )

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
    bubble_core.next_to(
        anchor_head,
        UP + RIGHT,
        buff=buff,
    ).shift(extra_shift)

    # ==============================================================
    # 3. حساب موضع دوائر التفكير (Thought Dots) بشكل قطري متناسق
    # ==============================================================
    # البداية: ملامسة تماماً لأعلى يمين محيط الرأس
    start_point = anchor_head.get_top() + RIGHT * 0.08 + UP * 0.03
    
    # النهاية: موجهة نحو الزاوية السفلية اليسرى للصندوق مباشرة
    end_point = box.get_corner(DL) + RIGHT * 0.22 + UP * 0.02

    # توزيع نسبي متوازن يمتد من الرأس حتى الصندوق
    dot1 = Circle(radius=0.035, stroke_width=0, fill_color=color, fill_opacity=0.9)\
        .move_to(interpolate(start_point, end_point, 0.12))
        
    dot2 = Circle(radius=0.058, stroke_width=0, fill_color=color, fill_opacity=0.9)\
        .move_to(interpolate(start_point, end_point, 0.42))
        
    dot3 = Circle(radius=0.088, stroke_width=0, fill_color=color, fill_opacity=0.9)\
        .move_to(interpolate(start_point, end_point, 0.74))

    dots = VGroup(dot1, dot2, dot3)

    # ==============================================================
    # نقاط بداية ونهاية تأثير الرسم
    # ==============================================================
    draw_start = mark.get_right() + RIGHT * 0.08
    draw_end = mark.get_left() + RIGHT * 0.12

    return box, dots, mark, draw_start, draw_end