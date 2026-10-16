from manim import *
import numpy as np
from common.palette import COPPER_TERRA  # <--- استيراد اللون المعتمد


class MachVector(VGroup):
    """المتجه الرسمي المخصص لقناة MACH-MATH."""
    def __init__(
        self,
        start=ORIGIN,
        end=RIGHT,
        color=COPPER_TERRA,
        stroke_width=3.0,
        tip_length=0.22,
        tip_angle=PI / 5.5,
        show_pivot=True,
        pivot_radius=0.045,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.start = np.array(start)
        self.end = np.array(end)
        self.color = color

        direction = self.end - self.start
        length = np.linalg.norm(direction)
        unit_dir = RIGHT if length == 0 else direction / length

        actual_end = self.end - unit_dir * (tip_length * 0.8)
        self.line = Line(self.start, actual_end, color=color, stroke_width=stroke_width, buff=0)

        left_angle = np.arctan2(unit_dir[1], unit_dir[0]) + PI - tip_angle
        right_angle = np.arctan2(unit_dir[1], unit_dir[0]) + PI + tip_angle

        wing_left = self.end + tip_length * np.array([np.cos(left_angle), np.sin(left_angle), 0])
        wing_right = self.end + tip_length * np.array([np.cos(right_angle), np.sin(right_angle), 0])

        self.tip = Polygon(
            self.end,
            wing_left,
            self.end - unit_dir * (tip_length * 0.35),
            wing_right,
            color=color,
            fill_color=color,
            fill_opacity=1.0,
            stroke_width=0
        )
        self.add(self.line, self.tip)

        if show_pivot:
            self.pivot = Dot(self.start, radius=pivot_radius, color=color)
            self.add(self.pivot)






class MachVector3D(VGroup):
    """
    المتجه ثلاثي الأبعاد الرسمي لقناة MACH-MATH:
    - يحتفظ بنفس التصميم الهندسي المشطوف لـ MachVector (وليس مخروطاً عادياً).
    - رأس سهم مجسم بتقنية الأوجه المتقاطعة يظهر متناسقاً بدقة من أي زاوية كاميرا 3D.
    - نقطة ارتكاز ثلاثية الأبعاد (Dot3D Pivot) عند نقطة البداية.
    - محاذاة دقيقة 100% في الفضاء ثلاثي الأبعاد بدون أي انحراف في الأجنحة.
    """
    def __init__(
        self,
        start=ORIGIN,
        end=RIGHT + UP + OUT,
        color=COPPER_TERRA,
        stroke_width=3.5,
        tip_length=0.28,
        tip_angle=PI / 5.5,
        show_pivot=True,
        pivot_radius=0.05,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.start = np.array(start, dtype=float)
        self.end = np.array(end, dtype=float)
        self.color = color

        direction = self.end - self.start
        length = np.linalg.norm(direction)
        unit_dir = np.array([1.0, 0.0, 0.0]) if length < 1e-6 else direction / length

        # ----------------------------------------------------------
        # 1. إيجاد متجهين متعامدين تماماً على اتجاه السهم في الفضاء 3D
        # ----------------------------------------------------------
        if np.allclose(np.abs(unit_dir), [0, 0, 1]):
            ref = RIGHT
        else:
            ref = UP

        p1 = np.cross(unit_dir, ref)
        if np.linalg.norm(p1) < 1e-4:
            p1 = np.cross(unit_dir, RIGHT)
        p1 /= np.linalg.norm(p1)
        p2 = np.cross(unit_dir, p1)
        p2 /= np.linalg.norm(p2)

        # ----------------------------------------------------------
        # 2. بناء رأس السهم المشطوف ثلاثي الأبعاد
        # ----------------------------------------------------------
        base_dist = tip_length * 0.85
        notch_dist = tip_length * 0.38
        wing_w = tip_length * np.tan(tip_angle)

        actual_end = self.end - unit_dir * notch_dist
        notch_pt = self.end - unit_dir * notch_dist

        # الوجه الأول (في المستوى الأول)
        w1_a = self.end - unit_dir * base_dist + p1 * wing_w
        w1_b = self.end - unit_dir * base_dist - p1 * wing_w
        poly1 = Polygon(
            self.end, w1_a, notch_pt, w1_b,
            color=color, fill_color=color, fill_opacity=1.0, stroke_width=0
        )

        # الوجه الثاني (في المستوى العمودي عليه ليعطي عمقاً ثلاثي الأبعاد)
        w2_a = self.end - unit_dir * base_dist + p2 * wing_w
        w2_b = self.end - unit_dir * base_dist - p2 * wing_w
        poly2 = Polygon(
            self.end, w2_a, notch_pt, w2_b,
            color=color, fill_color=color, fill_opacity=1.0, stroke_width=0
        )

        self.tip = VGroup(poly1, poly2)

        # ----------------------------------------------------------
        # 3. خط المتجه ونقطة الارتكاز (Pivot)
        # ----------------------------------------------------------
        self.line = Line(
            self.start, actual_end,
            color=color, stroke_width=stroke_width, buff=0
        )

        self.add(self.line, self.tip)

        if show_pivot:
            self.pivot = Dot3D(self.start, radius=pivot_radius, color=color)
            self.add(self.pivot)