from manim import *
import numpy as np

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_MUTED,
    STONE_AXIS,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.latex import mach_math_template
from common.mobjects.vectors import MachVector


class MachVectorSpace(VGroup):
    """
    Reusable vector-space visualization for MACH-MATH.
    """

    DEFAULT_VECTORS = [
        ((2.5, 2.0, 0), GOLD_BRIGHT, r"\mathbf{v}_1"),
        ((-1.8, 1.9, 0), COPPER_TERRA, r"\mathbf{v}_2"),
        ((-1.4, -0.7, 0), STONE_AXIS, r"\mathbf{v}_3"),
        ((1.5, -2.1, 0), GOLD_LIGHT, r"\mathbf{v}_4"),
        ((2.8, -0.5, 0), IVORY_WHITE, r"\mathbf{v}_5"),
        ((-0.9, -2.4, 0), GOLD_MUTED, r"\mathbf{v}_6"),
    ]

    def __init__(
        self,
        center=(-3.55, 0, 0),
        width=7.2,
        height=7.8,
        grid_step=0.55,
        vectors=None,
        title="فضاء المتجهات (Vector Space)",
        show_title=True,
        show_origin=True,
        grid_color=STONE_AXIS,
        axis_color=GOLD_LIGHT,
        grid_width=0.85,
        grid_opacity=0.42,
        axis_width=2.2,
        axis_opacity=0.90,
        dash_length=0.08,
        dashed_ratio=0.55,
        vector_width=3.0,
        vector_opacity=1.0,
        origin_opacity=1.0,
        tip_length=0.22,
        label_font_size=19,
        title_font_size=21,
        title_color=GOLD_LIGHT,
        title_background=True,
        title_top_buff=0.45,
        show_vector_labels=True,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.center = np.array(center, dtype=float)
        self.space_width = float(width)
        self.space_height = float(height)
        self.grid_step = float(grid_step)

        if self.space_width <= 0 or self.space_height <= 0:
            raise ValueError("width and height must be greater than zero.")

        if self.grid_step <= 0:
            raise ValueError("grid_step must be greater than zero.")

        if len(self.center) != 3:
            raise ValueError("center must contain exactly three coordinates.")

        cx, cy, cz = self.center

        self.x_min = cx - self.space_width / 2
        self.x_max = cx + self.space_width / 2
        self.y_min = cy - self.space_height / 2
        self.y_max = cy + self.space_height / 2

        self.grid = VGroup()
        self.axes = VGroup()
        self.origin = VGroup()
        self.vectors = VGroup()
        self.title_group = VGroup()

        # ----------------------------------------------------------
        # 3. خطوط الشبكة المنطلقة من المركز بالتناظر التام
        # ----------------------------------------------------------
        epsilon = 1e-7

        # توليد خطوط رأسية متناظرة حول cx بدقة
        x_positive = np.arange(cx + self.grid_step, self.x_max + epsilon, self.grid_step)
        x_negative = np.arange(cx - self.grid_step, self.x_min - epsilon, -self.grid_step)
        x_values = np.sort(np.concatenate([x_negative, x_positive]))

        # توليد خطوط أفقية متناظرة حول cy بدقة
        y_positive = np.arange(cy + self.grid_step, self.y_max + epsilon, self.grid_step)
        y_negative = np.arange(cy - self.grid_step, self.y_min - epsilon, -self.grid_step)
        y_values = np.sort(np.concatenate([y_negative, y_positive]))

        # رسم الخطوط الرأسية للشبكة
        for x in x_values:
            line = DashedLine(
                start=np.array([x, self.y_min, cz]),
                end=np.array([x, self.y_max, cz]),
                dash_length=dash_length,
                dashed_ratio=dashed_ratio,
                color=grid_color,
                stroke_width=grid_width,
            )
            line.set_opacity(grid_opacity)
            self.grid.add(line)

        # رسم الخطوط الأفقية للشبكة
        for y in y_values:
            line = DashedLine(
                start=np.array([self.x_min, y, cz]),
                end=np.array([self.x_max, y, cz]),
                dash_length=dash_length,
                dashed_ratio=dashed_ratio,
                color=grid_color,
                stroke_width=grid_width,
            )
            line.set_opacity(grid_opacity)
            self.grid.add(line)

        # ----------------------------------------------------------
        # 4. المحاور الرئيسية (تتوسط الشبكة تماماً كخط الأصل)
        # ----------------------------------------------------------
        horizontal_axis = DashedLine(
            start=np.array([self.x_min, cy, cz]),
            end=np.array([self.x_max, cy, cz]),
            dash_length=dash_length,
            dashed_ratio=dashed_ratio,
            color=axis_color,
            stroke_width=axis_width,
        )
        horizontal_axis.set_opacity(axis_opacity)

        vertical_axis = DashedLine(
            start=np.array([cx, self.y_min, cz]),
            end=np.array([cx, self.y_max, cz]),
            dash_length=dash_length,
            dashed_ratio=dashed_ratio,
            color=axis_color,
            stroke_width=axis_width,
        )
        vertical_axis.set_opacity(axis_opacity)

        self.axes.add(horizontal_axis, vertical_axis)

        # ----------------------------------------------------------
        # 5. نقطة الأصل
        # ----------------------------------------------------------
        if show_origin:
            origin_dot = Dot(
                point=self.center,
                radius=0.045,
                color=GOLD_BRIGHT,
            )
            origin_dot.set_opacity(origin_opacity)
            self.origin.add(origin_dot)

        # ----------------------------------------------------------
        # 6. المتجهات والتسميات
        # ----------------------------------------------------------
        vector_data = (
            self.DEFAULT_VECTORS if vectors is None else vectors
        )

        for item in vector_data:
            if len(item) != 3:
                raise ValueError("Each vector must be (endpoint_offset, color, label).")

            endpoint_offset, vector_color, vector_label = item
            offset = np.array(endpoint_offset, dtype=float)
            endpoint = self.center + offset

            vector = MachVector(
                start=self.center,
                end=endpoint,
                color=vector_color,
                stroke_width=vector_width,
                tip_length=tip_length,
                show_pivot=False,
            )
            vector.set_opacity(vector_opacity)

            vector_group = VGroup(vector)

            if show_vector_labels and vector_label:
                label = MathTex(
                    vector_label,
                    tex_template=mach_math_template,
                    font_size=label_font_size,
                    color=vector_color,
                )
                label.set_opacity(vector_opacity)

                direction = offset / max(np.linalg.norm(offset), 1e-8)
                label_direction = direction + 0.35 * UP
                label_direction /= max(np.linalg.norm(label_direction), 1e-8)

                label.next_to(endpoint, label_direction, buff=0.10)
                vector_group.add(label)

            self.vectors.add(vector_group)

        # ----------------------------------------------------------
        # 7. الترويسة والعنوان
        # ----------------------------------------------------------
        if show_title and title:
            title_text = MarkupText(
                title, font="Cairo", font_size=title_font_size, color=title_color
            )
            title_text.move_to(np.array([cx, self.y_max - title_top_buff, cz]))

            if title_background:
                title_bg = SurroundingRectangle(
                    title_text, buff=0.12, color=GOLD_MUTED, stroke_width=0.8,
                    stroke_opacity=0.55, fill_color="#100D07", fill_opacity=0.92,
                    corner_radius=0.08,
                )
                self.title_group.add(title_bg, title_text)
            else:
                self.title_group.add(title_text)

        self.add(self.grid, self.axes, self.origin, self.vectors, self.title_group)