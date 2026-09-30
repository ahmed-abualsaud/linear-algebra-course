from manim import *

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_DARK,
    GOLD_MUTED,
    STONE_DASH,
)


class MachTableCell:
    """Lightweight layout object representing one table cell."""

    def __init__(
        self,
        center,
        width,
        height,
        padding=0.12,
    ):
        self.center = np.array(center)
        self.width = width
        self.height = height
        self.padding = padding

    def get_center(self):
        return self.center

    @property
    def content_width(self):
        return max(
            0,
            self.width - 2 * self.padding,
        )

    @property
    def content_height(self):
        return max(
            0,
            self.height - 2 * self.padding,
        )


# ==============================================================
# Internal shimmer activation animation
# ==============================================================


class _StartShimmer(Animation):

    def __init__(
        self,
        table,
        run_time=0.01,
    ):
        self.table = table

        super().__init__(
            table.light_group,
            run_time=run_time,
            rate_func=linear,
        )

    def begin(self):
        self.table._shimmer_running = True
        self.table.light_progress.set_value(0)
        self.table.light_group.move_to(self.table._get_shimmer_point(0))
        # إظهار اللمعة بكامل تدرج توهجها الطبيعي دون كسر الشفافية
        self.table._show_shimmer()
        super().begin()

    def interpolate_mobject(self, alpha):
        pass


class MachTable(VGroup):

    def __init__(
        self,
        rows,
        cols,
        width=8.2,
        height=5.8,
        row_heights=None,
        col_widths=None,
        corner_radius=0.28,
        cell_padding=0.12,
        border_color=GOLD_LIGHT,
        border_width=1.4,
        border_opacity=0.45,
        fill_color="#100D07",
        fill_opacity=0.82,
        glass_color=GOLD_LIGHT,
        glass_opacity=0.035,
        glass_border_opacity=0.12,
        separator_color=GOLD_DARK,
        separator_width=0.9,
        separator_opacity=0.38,
        dash_length=0.075,
        dashed_ratio=0.55,
        shimmer=True,
        # سرعة هادئة جداً (50 ثانية للدورة)
        shimmer_speed=50.0,
        shimmer_radius=0.012,
        # الانعكاس الأرضي ثلاثي الأبعاد
        floor_reflection=True,
        reflection_offset=0.22,
        reflection_opacity=0.28,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.rows = rows
        self.cols = cols
        self.table_width = width
        self.table_height = height
        self.cell_padding = cell_padding

        self.shimmer_enabled = shimmer
        self.shimmer_speed = shimmer_speed
        self.shimmer_radius = shimmer_radius
        self.corner_radius = corner_radius

        self.floor_reflection_enabled = floor_reflection
        self.reflection_offset = reflection_offset
        self.reflection_opacity = reflection_opacity

        self._construction_ready = False
        self._shimmer_running = False

        # ======================================================
        # Validate dimensions
        # ======================================================
        if row_heights is None:
            row_heights = [height / rows] * rows

        if col_widths is None:
            col_widths = [width / cols] * cols

        if len(row_heights) != rows:
            raise ValueError(f"row_heights must contain exactly {rows} values.")

        if len(col_widths) != cols:
            raise ValueError(f"col_widths must contain exactly {cols} values.")

        if not np.isclose(sum(row_heights), height):
            raise ValueError("row_heights must sum to table height.")

        if not np.isclose(sum(col_widths), width):
            raise ValueError("col_widths must sum to table width.")

        self.row_heights = row_heights
        self.col_widths = col_widths

        # ======================================================
        # 1. Floor Reflection
        # ======================================================
        self.floor_reflection_group = VGroup()

        if floor_reflection:
            y_base = -height / 2 - reflection_offset

            n_glow_layers = 10
            for i in range(n_glow_layers):
                t = i / (n_glow_layers - 1)
                w_layer = width * interpolate(0.85, 1.25, t)
                h_layer = 0.40 * interpolate(0.35, 1.50, t)
                op_layer = reflection_opacity * interpolate(
                    0.65, 0.005, t**0.6
                )

                glow_ellipse = Ellipse(
                    width=w_layer,
                    height=h_layer,
                    stroke_width=0,
                    fill_color=GOLD_MUTED if t > 0.4 else GOLD_DARK,
                    fill_opacity=op_layer,
                ).move_to([0, y_base - h_layer * 0.25, 0])
                self.floor_reflection_group.add(glow_ellipse)

            reflection_h = 0.55
            p_top_l = np.array([-width / 2 + corner_radius, -height / 2, 0])
            p_top_r = np.array([width / 2 - corner_radius, -height / 2, 0])
            p_bot_r = np.array(
                [
                    (width / 2 - corner_radius) * 1.06,
                    -height / 2 - reflection_h,
                    0,
                ]
            )
            p_bot_l = np.array(
                [
                    (-width / 2 + corner_radius) * 1.06,
                    -height / 2 - reflection_h,
                    0,
                ]
            )

            n_refl_slices = 8
            for j in range(n_refl_slices):
                alpha_a = j / n_refl_slices
                alpha_b = (j + 1) / n_refl_slices

                pt_tl = interpolate(p_top_l, p_bot_l, alpha_a)
                pt_tr = interpolate(p_top_r, p_bot_r, alpha_a)
                pt_br = interpolate(p_top_r, p_bot_r, alpha_b)
                pt_bl = interpolate(p_top_l, p_bot_l, alpha_b)

                slice_op = (
                    reflection_opacity
                    * 0.45
                    * ((1.0 - alpha_a) ** 1.8)
                )

                refl_slice = Polygon(
                    pt_tl,
                    pt_tr,
                    pt_br,
                    pt_bl,
                    stroke_width=0,
                    fill_color=GOLD_LIGHT if alpha_a < 0.3 else GOLD_DARK,
                    fill_opacity=slice_op,
                )
                self.floor_reflection_group.add(refl_slice)

            contact_line = Line(
                p_top_l,
                p_top_r,
                color=GOLD_LIGHT,
                stroke_width=1.0,
                stroke_opacity=reflection_opacity * 0.75,
            )
            self.floor_reflection_group.add(contact_line)

        # ======================================================
        # 2. Main table & Glass
        # ======================================================
        self.table = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=corner_radius,
            stroke_color=border_color,
            stroke_width=border_width,
            stroke_opacity=border_opacity,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
        )

        self.glass = RoundedRectangle(
            width=width - 0.12,
            height=height - 0.12,
            corner_radius=max(0, corner_radius - 0.04),
            stroke_color=glass_color,
            stroke_width=0.5,
            stroke_opacity=glass_border_opacity,
            fill_color=glass_color,
            fill_opacity=glass_opacity,
        )

        # ======================================================
        # 3. Cells
        # ======================================================
        self.cells = []
        y_top = height / 2

        for row in range(rows):
            row_height = row_heights[row]
            row_center_y = y_top - sum(row_heights[:row]) - row_height / 2
            row_cells = []
            x_left = -width / 2

            for col in range(cols):
                col_width = col_widths[col]
                col_center_x = x_left + col_width / 2

                cell = MachTableCell(
                    center=np.array([col_center_x, row_center_y, 0]),
                    width=col_width,
                    height=row_height,
                    padding=cell_padding,
                )
                row_cells.append(cell)
                x_left += col_width

            self.cells.append(row_cells)

        # ======================================================
        # 4. Separators
        # ======================================================
        self.separators = VGroup()
        self.vertical_separators = VGroup()
        self.horizontal_separators = VGroup()

        # Vertical
        x = -width / 2
        for col in range(cols - 1):
            x += col_widths[col]
            separator = DashedLine(
                UP * (height / 2 - 0.12),
                DOWN * (height / 2 - 0.12),
                dash_length=dash_length,
                dashed_ratio=dashed_ratio,
                color=separator_color,
                stroke_width=separator_width,
                stroke_opacity=separator_opacity,
            )
            separator.move_to(RIGHT * x)
            self.vertical_separators.add(separator)
            self.separators.add(separator)

        # Horizontal
        y = height / 2
        for row in range(rows - 1):
            y -= row_heights[row]
            separator = DashedLine(
                LEFT * (width / 2 - 0.12),
                RIGHT * (width / 2 - 0.12),
                dash_length=dash_length,
                dashed_ratio=dashed_ratio,
                color=separator_color,
                stroke_width=separator_width,
                stroke_opacity=separator_opacity,
            )
            separator.move_to(UP * y)
            self.horizontal_separators.add(separator)
            self.separators.add(separator)

        # ======================================================
        # 5. Shimmer (توهج فوتوني ساطع بنواة بيضاء دون زيادة الحجم)
        # ======================================================
        self.light_progress = ValueTracker(0)
        self.light_group = VGroup()
        self._shimmer_path = self.table

        if shimmer:
            # هالة خارجية خافتة تذوب في الزجاج (نصف قطر 0.12)
            glow_outer = Circle(
                radius=0.12,
                stroke_width=0,
                fill_color=GOLD_MUTED,
                fill_opacity=0.12,
            )
            # هالة متوسطة دافئة (نصف قطر 0.065)
            glow_mid = Circle(
                radius=0.065,
                stroke_width=0,
                fill_color=GOLD_LIGHT,
                fill_opacity=0.35,
            )
            # هالة قريبة متوهجة (نصف قطر 0.035)
            glow_inner = Circle(
                radius=0.035,
                stroke_width=0,
                fill_color=GOLD_BRIGHT,
                fill_opacity=0.75,
            )
            # نواة بيضاء ساطعة جداً (Hot Spark Core) دون زيادة الحجم
            spark_core = Dot(
                radius=self.shimmer_radius,
                color="#FFFFFF",
                fill_opacity=1.0,
            )

            # تسجيل درجات الشفافية الأصلية لكل عنصر لحمايتها
            for part in [glow_outer, glow_mid, glow_inner, spark_core]:
                part.base_opacity = part.get_fill_opacity()

            self.light_group.add(
                glow_outer, glow_mid, glow_inner, spark_core
            )
            self.light_group.set_z_index(120)

            self.light_progress.set_value(0)
            self.light_group.move_to(self._get_shimmer_point(0))
            self._hide_shimmer()

            def update_light(mob, dt):
                if not self._shimmer_running:
                    return
                self.light_progress.increment_value(dt / self.shimmer_speed)
                progress = self.light_progress.get_value() % 1
                mob.move_to(self._get_shimmer_point(progress))

            self.light_group.add_updater(update_light)

        # ======================================================
        # Add components
        # ======================================================
        if floor_reflection:
            self.add(self.floor_reflection_group)

        self.add(
            self.table,
            self.glass,
            self.separators,
        )

        if shimmer:
            self.add(self.light_group)

    # دوال ذكية للتحكم في ظهور وإخفاء اللمعة دون كسر تدرج توهجها
    def _hide_shimmer(self):
        for mob in self.light_group:
            mob.set_fill_opacity(0)

    def _show_shimmer(self):
        for mob in self.light_group:
            mob.set_fill_opacity(getattr(mob, "base_opacity", 1.0))

    def _get_shimmer_point(self, progress):
        progress = progress % 1
        return self._shimmer_path.point_from_proportion(progress)

    def construct(
        self,
        run_time=2.5,
        show_shimmer=True,
        center_point=True,
        rate_func=smooth,
    ):
        animations = []

        if self.shimmer_enabled:
            self._shimmer_running = False
            self.light_progress.set_value(0)
            self.light_group.move_to(self._get_shimmer_point(0))
            self._hide_shimmer()

        # 1. رسم الإطار الخارجي أولاً
        animations.append(Create(self.table, run_time=run_time * 0.35))

        # 2. اشتعال الانعكاس والزجاج فور اكتمال الإطار
        if self.floor_reflection_enabled:
            animations.append(
                AnimationGroup(
                    FadeIn(self.floor_reflection_group),
                    FadeIn(self.glass),
                    run_time=run_time * 0.18,
                    rate_func=rate_func,
                )
            )
        else:
            animations.append(
                FadeIn(
                    self.glass,
                    run_time=run_time * 0.18,
                )
            )

        # 3. نمو الفواصل
        for separator in self.vertical_separators:
            animations.append(
                GrowFromCenter(
                    separator,
                    run_time=run_time * 0.18,
                    rate_func=rate_func,
                )
            )

        if len(self.horizontal_separators) > 0:
            animations.append(
                LaggedStart(
                    *[
                        GrowFromCenter(
                            separator,
                            run_time=run_time * 0.14,
                            rate_func=rate_func,
                        )
                        for separator in self.horizontal_separators
                    ],
                    lag_ratio=0.18,
                    run_time=run_time * 0.29,
                )
            )

        self._construction_ready = True
        construction = Succession(*animations)

        if show_shimmer and self.shimmer_enabled:
            shimmer_start = _StartShimmer(self, run_time=0.01)
            return AnimationGroup(construction, shimmer_start, lag_ratio=0)

        return construction

    def start_shimmer(self):
        if not self.shimmer_enabled:
            return
        self.light_progress.set_value(0)
        self.light_group.move_to(self._get_shimmer_point(0))
        self._shimmer_running = True
        self._show_shimmer()

    def stop_shimmer(self):
        self._shimmer_running = False
        if self.shimmer_enabled:
            self._hide_shimmer()

    def cell(self, row, col):
        if not 0 <= row < self.rows:
            raise IndexError(f"row must be between 0 and {self.rows - 1}")
        if not 0 <= col < self.cols:
            raise IndexError(f"col must be between 0 and {self.cols - 1}")
        return self.cells[row][col]

    def place(self, mob, row, col, padding=None, direction=None):
        cell = self.cell(row, col)
        if padding is None:
            padding = cell.padding

        if direction is None:
            mob.move_to(cell.get_center())
        else:
            mob.next_to(cell.get_center(), direction, buff=padding)

        return mob

    def fit(self, mob, row, col, padding=None, allow_upscale=False):
        cell = self.cell(row, col)
        if padding is None:
            padding = cell.padding

        available_width = max(0.01, cell.width - 2 * padding)
        available_height = max(0.01, cell.height - 2 * padding)

        if mob.width <= 0 or mob.height <= 0:
            mob.move_to(cell.get_center())
            return mob

        scale_factor = min(
            available_width / mob.width,
            available_height / mob.height,
        )

        if not allow_upscale:
            scale_factor = min(scale_factor, 1.0)

        mob.scale(scale_factor)
        mob.move_to(cell.get_center())
        return mob