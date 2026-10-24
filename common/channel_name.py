"""
توليد العلامة المائية (Watermark) لقناة MACH-MATH بجودة فائقة
متوافق مع معايير يوتيوب (خلفية شفافة + دقة عالية).
"""

from manim import *
import numpy as np

# استيراد لوحة الألوان الخاصة بالمشروع مع توفير قيم افتراضية متطابقة في حال التشغيل المستقل
try:
    from common.palette import (
        GOLD_BRIGHT,
        GOLD_LIGHT,
        GOLD,
        GOLD_DARK,
        GOLD_MUTED,
        IVORY_WHITE,
    )
except ImportError:
    try:
        from .palette import (
            GOLD_BRIGHT,
            GOLD_LIGHT,
            GOLD,
            GOLD_DARK,
            GOLD_MUTED,
            IVORY_WHITE,
        )
    except ImportError:
        GOLD_BRIGHT = "#FFD700"
        GOLD_LIGHT = "#F9E79F"
        GOLD = "#F5B041"
        GOLD_DARK = "#B78727"
        GOLD_MUTED = "#8A7343"
        IVORY_WHITE = "#F8F9FA"


def create_mach_math_logo(font_size=90, add_shadow=True):
    """
    بناء شعار MACH - MATH المتطابق مع لقطة الفيديو:
    - MAC و MAT والشرطة باللون الأبيض العاجي (IVORY_WHITE).
    - حرفي الـ H باللون الذهبي المميز للقناة.
    - ظل خافت وناعم خلف الحروف لضمان وضوح الشعار سواء كان خلفية الفيديو فاتحة أو داكنة.
    """
    font_kwargs = {
        "font": "Serif",
        "weight": BOLD,
        "font_size": font_size,
    }

    # الجزء الأول: MACH
    mac_text = Text("MAC", color=IVORY_WHITE, **font_kwargs)
    h1_text = Text("H", color=GOLD_BRIGHT, **font_kwargs)
    mach_group = VGroup(mac_text, h1_text).arrange(RIGHT, buff=0.04)

    # الفاصل: -
    dash_text = Text("-", color=IVORY_WHITE, **font_kwargs)

    # الجزء الثاني: MATH
    mat_text = Text("MAT", color=IVORY_WHITE, **font_kwargs)
    h2_text = Text("H", color=GOLD_BRIGHT, **font_kwargs)
    math_group = VGroup(mat_text, h2_text).arrange(RIGHT, buff=0.04)

    # تجميع الشعار كاملاً
    full_logo = VGroup(mach_group, dash_text, math_group).arrange(
        RIGHT, buff=0.32
    )

    if not add_shadow:
        return full_logo

    # إضافة هالة ظل خفيفة خلف الحروف لضمان القراءة على أي خلفية فيديو (Light / Dark)
    shadow_layers = VGroup()
    for radius, opacity in [(0.06, 0.4), (0.12, 0.25), (0.20, 0.12)]:
        shadow = full_logo.copy()
        shadow.set_color(BLACK)
        shadow.set_stroke(color=BLACK, width=radius * font_size * 0.18, opacity=opacity)
        shadow_layers.add(shadow)

    return VGroup(shadow_layers, full_logo)


# ======================================================================
# المشهد 1: علامة مائية أفقية شفافة عريضة (Transparent Banner Watermark)
# ======================================================================
class MachMathWatermark(Scene):
    """صورة أفقية شفافة بأعلى دقة."""
    def construct(self):
        logo = create_mach_math_logo(font_size=110, add_shadow=True)
        self.add(logo)


# ======================================================================
# المشهد 2: علامة مائية مربعة 1:1 مخصصة ليوتيوب (Square Transparent Watermark)
# ======================================================================
class MachMathSquareWatermark(Scene):
    """
    توليد مقاس مربع (1:1) وهو المقاس القياسي الموصى به رسمياً في إعدادات يوتيوب.
    """
    def construct(self):
        # ضبط الكاميرا على نسبة أبعاد مربعة 1:1
        self.camera.frame_width = 8.0
        self.camera.frame_height = 8.0

        logo = create_mach_math_logo(font_size=75, add_shadow=True)
        logo.move_to(ORIGIN)
        self.add(logo)


# ======================================================================
# المشهد 3: الشعار داخل الفريم الهندسي السينمائي الكامل (مثل لقطة الفيديو تماماً)
# ======================================================================
class MachMathFramedWatermark(Scene):
    """النسخة الكاملة مع الفريم الأسود والهندسة الفراغية كما في لقطة الفيديو."""
    def construct(self):
        FRAME_HALF_W, FRAME_HALF_H = 3.0, 1.7
        inner = [
            np.array([-FRAME_HALF_W, FRAME_HALF_H, 0]),
            np.array([FRAME_HALF_W, FRAME_HALF_H, 0]),
            np.array([FRAME_HALF_W, -FRAME_HALF_H, 0]),
            np.array([-FRAME_HALF_W, -FRAME_HALF_H, 0]),
        ]
        outer = [
            (LEFT * config.frame_width / 2 + UP * config.frame_height / 2) * 1.02,
            (RIGHT * config.frame_width / 2 + UP * config.frame_height / 2) * 1.02,
            (RIGHT * config.frame_width / 2 + DOWN * config.frame_height / 2) * 1.02,
            (LEFT * config.frame_width / 2 + DOWN * config.frame_height / 2) * 1.02,
        ]

        inner_edges = VGroup(*[
            Line(inner[i], inner[(i + 1) % 4], color=GOLD_MUTED, stroke_width=0.6, stroke_opacity=0.18)
            for i in range(4)
        ])
        radial_lines = VGroup(*[
            Line(inner[i], outer[i], color=GOLD_MUTED, stroke_width=0.6, stroke_opacity=0.18)
            for i in range(4)
        ])
        frame = VGroup(inner_edges, radial_lines)

        logo = create_mach_math_logo(font_size=82, add_shadow=False)
        self.add(frame, logo)