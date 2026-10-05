from manim import *
from common.identity import _get_luminous_point

# 1. الدقة الفائقة 2048x2048
config.pixel_width = 2048
config.pixel_height = 2048

# 2. تقريب الكاميرا (Zoom In) لإلغاء المساحة السوداء الشاسعة
config.frame_width = 1.5
config.frame_height = 1.5
config.background_color = BLACK


class ExportLogo(Scene):

    def construct(self):
        # النقطة متمركزة في المركز الهندسي بالضبط (0, 0)
        logo_point = _get_luminous_point(ORIGIN)
        self.add(logo_point)