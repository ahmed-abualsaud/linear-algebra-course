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