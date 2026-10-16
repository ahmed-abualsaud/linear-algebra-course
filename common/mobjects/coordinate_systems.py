import numpy as np
from manim import *

from common.palette import (
    STONE_AXIS,
    GOLD_SHADOW,
    GOLD_MUTED,
    GOLD_LIGHT,
    GOLD_BRIGHT,
    IVORY_WHITE,
)

class MachNumberLine(VGroup):
    """
    خط الأعداد الرسمي لقناة MACH-MATH:
    - متماثل تماماً من -3 إلى +3.
    - أسهم رشيقة متماثلة في الطرفين.
    - تدرج وأرقام واضحة.
    """

    def __init__(
        self,
        length=7.4,
        color=STONE_AXIS,
        stroke_width=1.4,
        font_size=24,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.axis = NumberLine(
            x_range=[-3.8, 3.8, 1],
            length=length,
            color=color,
            stroke_width=stroke_width,
            include_tip=True,
            tip_width=0.10,
            tip_height=0.16,
            include_numbers=False,
            include_ticks=False,
        )

        self.add(self.axis)

        # ==========================================================
        # رأس السهم الأيسر
        # ==========================================================

        tip_w = 0.05
        tip_len = 0.16

        l_end = self.axis.get_left()

        left_tip = Polygon(
            l_end,
            l_end + RIGHT * tip_len + UP * tip_w,
            l_end + RIGHT * tip_len + DOWN * tip_w,
            color=color,
            fill_color=color,
            fill_opacity=1.0,
            stroke_width=0,
        )

        self.add(left_tip)

        # ==========================================================
        # التدرج والأرقام
        # ==========================================================

        self.ticks_group = VGroup()
        self.numbers_group = VGroup()

        for val in range(-3, 4):

            pt = self.axis.n2p(val)

            tick = Line(
                pt + UP * 0.08,
                pt + DOWN * 0.08,
                color=color,
                stroke_width=stroke_width,
            )

            self.ticks_group.add(tick)

            num = MathTex(
                str(val),
                font_size=font_size,
                color=color,
            )

            num.next_to(
                tick,
                DOWN,
                buff=0.15,
            )

            self.numbers_group.add(num)

        self.add(
            self.ticks_group,
            self.numbers_group,
        )


class MachAxes(Axes):
    """
    نظام الإحداثيات الهندسي الرسمي لقناة MACH-MATH.

    يحتوي على:

    - محور X بمحاذاة أفقية.
    - محور Y بمحاذاة رأسية.
    - رأس سهم في كلا طرفي كل محور.
    - Grid داخلي بدون borders خارجية.
    - Ticks وأرقام على المحاور.
    - خلفية زجاجية خفيفة.
    - ألوان متوافقة مع هوية MACH-MATH.
    """

    def __init__(
        self,
        x_range=[-4, 4, 1],
        y_range=[-4, 4, 1],
        x_length=4.6,
        y_length=4.6,
        color=STONE_AXIS,
        stroke_width=1.5,
        font_size=16,
        **kwargs
    ):

        # ==========================================================
        # 1. الـAxes الأساسي
        # ==========================================================

        axis_config = {
            "color": color,
            "stroke_width": stroke_width,
            "include_tip": False,
            "tick_size": 0,
        }

        super().__init__(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            axis_config=axis_config,
            **kwargs
        )

        # ==========================================================
        # 2. الخلفية الزجاجية
        # ==========================================================

        self.glass = Rectangle(
            width=self.x_length,
            height=self.y_length,
            stroke_color=GOLD_MUTED,
            stroke_width=0.8,
            stroke_opacity=0.25,
            fill_color=GOLD_SHADOW,
            fill_opacity=0.72,
        )

        self.glass.move_to(
            self.get_center()
        )

        self.glass_inner = Rectangle(
            width=self.x_length - 0.08,
            height=self.y_length - 0.08,
            stroke_color=GOLD_LIGHT,
            stroke_width=0.4,
            stroke_opacity=0.08,
            fill_color=GOLD_MUTED,
            fill_opacity=0.10,
        )

        self.glass_inner.move_to(
            self.get_center()
        )

        # ==========================================================
        # 3. الشبكة
        # ==========================================================

        self.grid = VGroup()

        # لون الشبكة: ذهبي ترابي هادئ من هوية MACH-MATH
        grid_color = GOLD_LIGHT
        grid_stroke_width = 0.9
        grid_opacity = 0.65
        dash_length = 0.10

        x_min = self.x_range[0]
        x_max = self.x_range[1]
        x_step = self.x_range[2]

        y_min = self.y_range[0]
        y_max = self.y_range[1]
        y_step = self.y_range[2]

        # ----------------------------------------------------------
        # الخطوط الرأسية
        # ----------------------------------------------------------

        x = x_min

        while x <= x_max + 1e-6:

            if abs(x) > 1e-6:

                line = DashedLine(
                    self.c2p(x, y_min),
                    self.c2p(x, y_max),
                    color=grid_color,
                    stroke_width=grid_stroke_width,
                    stroke_opacity=grid_opacity,
                    dash_length=dash_length,
                )

                self.grid.add(line)

            x += x_step

        # ----------------------------------------------------------
        # الخطوط الأفقية
        # ----------------------------------------------------------

        y = y_min

        while y <= y_max + 1e-6:

            if abs(y) > 1e-6:

                line = DashedLine(
                    self.c2p(x_min, y),
                    self.c2p(x_max, y),
                    color=grid_color,
                    stroke_width=grid_stroke_width,
                    stroke_opacity=grid_opacity,
                    dash_length=dash_length,
                )

                self.grid.add(line)

            y += y_step

        # ==========================================================
        # 4. رؤوس الأسهم
        # ==========================================================

        self.arrowheads = VGroup()

        tip_w = 0.05
        tip_len = 0.16

        # ----------------------------------------------------------
        # محور X
        # ----------------------------------------------------------

        x_left = self.c2p(x_min, 0)
        x_right = self.c2p(x_max, 0)

        # السهم الأيسر
        x_left_tip = Polygon(
            x_left,
            x_left + RIGHT * tip_len + UP * tip_w,
            x_left + RIGHT * tip_len + DOWN * tip_w,
            color=color,
            fill_color=color,
            fill_opacity=1.0,
            stroke_width=0,
        )

        # السهم الأيمن
        x_right_tip = Polygon(
            x_right,
            x_right + LEFT * tip_len + UP * tip_w,
            x_right + LEFT * tip_len + DOWN * tip_w,
            color=color,
            fill_color=color,
            fill_opacity=1.0,
            stroke_width=0,
        )

        # ----------------------------------------------------------
        # محور Y
        # ----------------------------------------------------------

        y_bottom = self.c2p(0, y_min)
        y_top = self.c2p(0, y_max)

        # السهم السفلي
        y_bottom_tip = Polygon(
            y_bottom,
            y_bottom + UP * tip_len + LEFT * tip_w,
            y_bottom + UP * tip_len + RIGHT * tip_w,
            color=color,
            fill_color=color,
            fill_opacity=1.0,
            stroke_width=0,
        )

        # السهم العلوي
        y_top_tip = Polygon(
            y_top,
            y_top + DOWN * tip_len + LEFT * tip_w,
            y_top + DOWN * tip_len + RIGHT * tip_w,
            color=color,
            fill_color=color,
            fill_opacity=1.0,
            stroke_width=0,
        )

        self.arrowheads.add(
            x_left_tip,
            x_right_tip,
            y_bottom_tip,
            y_top_tip,
        )

        # ==========================================================
        # 5. التدرج
        # ==========================================================

        self.ticks = VGroup()

        # ----------------------------------------------------------
        # X ticks
        # ----------------------------------------------------------

        x = x_min

        while x <= x_max + 1e-6:

            if abs(x) > 1e-6:

                pt = self.c2p(x, 0)

                tick = Line(
                    pt + UP * 0.07,
                    pt + DOWN * 0.07,
                    color=color,
                    stroke_width=1.15,
                    stroke_opacity=0.9,
                )

                self.ticks.add(tick)

            x += x_step

        # ----------------------------------------------------------
        # Y ticks
        # ----------------------------------------------------------

        y = y_min

        while y <= y_max + 1e-6:

            if abs(y) > 1e-6:

                pt = self.c2p(0, y)

                tick = Line(
                    pt + LEFT * 0.07,
                    pt + RIGHT * 0.07,
                    color=color,
                    stroke_width=1.15,
                    stroke_opacity=0.9,
                )

                self.ticks.add(tick)

            y += y_step

        # ==========================================================
        # 6. الأرقام
        # ==========================================================

        self.numbers = VGroup()

        # ----------------------------------------------------------
        # أرقام X
        # ----------------------------------------------------------

        x = x_min

        while x <= x_max + 1e-6:

            pt = self.c2p(x, 0)

            num = MathTex(
                str(int(x)) if x.is_integer() else str(x),
                font_size=font_size,
                color=color,
            )

            num.next_to(
                pt,
                DOWN,
                buff=0.16,
            )

            self.numbers.add(num)

            x += x_step

        # ----------------------------------------------------------
        # أرقام Y
        # ----------------------------------------------------------

        y = y_min

        while y <= y_max + 1e-6:

            # الصفر مش محتاج يتكرر عند تقاطع المحورين
            if abs(y) > 1e-6:

                pt = self.c2p(0, y)

                num = MathTex(
                    str(int(y)) if y.is_integer() else str(y),
                    font_size=font_size,
                    color=color,
                )

                num.next_to(
                    pt,
                    LEFT,
                    buff=0.16,
                )

                self.numbers.add(num)

            y += y_step

        # ==========================================================
        # 7. ترتيب الطبقات
        # ==========================================================

        # الزجاج في الخلف
        self.add_to_back(
            self.glass
        )

        self.add_to_back(
            self.glass_inner
        )

        # الشبكة فوق الزجاج
        self.add_to_back(
            self.grid
        )

        # الـAxes الأصلية فوق الشبكة
        # ثم نضيف الـticks والأرقام والأسهم
        self.add(
            self.ticks,
            self.arrowheads,
            self.numbers,
        )




    def animate_creation(self, scene):

        # 1. الزجاج
        scene.play(
            FadeIn(
                VGroup(
                    self.glass,
                    self.glass_inner,
                ),
                scale=0.96,
            ),
            run_time=0.4,
        )

        # 2. الشبكة
        scene.play(
            LaggedStart(
                *[
                    Create(line)
                    for line in self.grid
                ],
                lag_ratio=0.04,
            ),
            run_time=1.0,
            rate_func=smooth,
        )

        # 3. المحاور
        origin = self.c2p(0, 0)

        self.x_axis.save_state()
        self.y_axis.save_state()

        self.x_axis.stretch(
            0.01,
            dim=0,
            about_point=origin,
        )

        self.y_axis.stretch(
            0.01,
            dim=1,
            about_point=origin,
        )

        scene.play(
            Restore(self.x_axis),
            Restore(self.y_axis),
            run_time=0.9,
            rate_func=smooth,
        )

        # 4. رؤوس الأسهم
        scene.play(
            LaggedStart(
                *[
                    FadeIn(
                        tip,
                        scale=0.4,
                    )
                    for tip in self.arrowheads
                ],
                lag_ratio=0.10,
            ),
            run_time=0.35,
        )

        # 5. الـ Ticks
        scene.play(
            LaggedStart(
                *[
                    GrowFromCenter(tick)
                    for tick in self.ticks
                ],
                lag_ratio=0.035,
            ),
            run_time=0.55,
        )

        # 6. الأرقام
        scene.play(
            LaggedStart(
                *[
                    FadeIn(
                        number,
                        shift=UP * 0.06,
                    )
                    for number in self.numbers
                ],
                lag_ratio=0.035,
            ),
            run_time=0.55,
        )



#============================================================================================================================


class MachAxes1D(VGroup):
    """
    نظام الإحداثيات في بُعد واحد (1D) الرسمي لقناة MACH-MATH.
    
    مصمم خصيصاً للتحول السينمائي السلس إلى MachAxes2D (2D):
    - محور X متصل ولامع بأسهم متماثلة في الطرفين.
    - تدريج رئيسي وفرعي (Major & Minor Ticks) متطابق مع النسخة ثنائية الأبعاد.
    - أرقام التدريج مع تمييز نقطة الأصل (0) بنقطة ذهبية مشعة.
    - دالة تحويل إحداثيات ديناميكية c2p(x) تتبع الـ shift و move_to بدقة 100%.
    """

    def __init__(
        self,
        center=ORIGIN,
        x_length=7.2,
        grid_step=0.55,

        # Coordinate range
        x_range=None,

        # Main axis
        axis_color=GOLD_LIGHT,
        axis_width=2.2,
        axis_opacity=0.90,

        # Major tick marks
        show_ticks=True,
        tick_length=0.09,
        tick_width=1.5,
        tick_color=GOLD_LIGHT,
        tick_opacity=0.90,

        # Minor tick marks
        show_minor_ticks=True,
        minor_ticks_per_interval=9,
        minor_tick_length=0.045,
        minor_tick_width=1.0,
        minor_tick_color=GOLD_LIGHT,
        minor_tick_opacity=0.70,

        # Numeric labels
        show_numbers=True,
        number_color=IVORY_WHITE,
        number_font_size=17,
        number_opacity=0.92,
        number_buff=0.14,
        show_zero_label=True,
        zero_color=GOLD_BRIGHT,

        # Origin
        show_origin=True,
        origin_radius=0.075,
        origin_color=GOLD_BRIGHT,

        # X axis label
        show_axis_label=True,
        axis_label_color=GOLD_BRIGHT,
        axis_label_font_size=24,
        axis_label_buff=0.20,

        **kwargs,
    ):
        super().__init__(**kwargs)

        self.center = np.array(center, dtype=float)
        self.x_length = float(x_length)
        self.grid_step = float(grid_step)

        if self.x_length <= 0:
            raise ValueError("x_length must be greater than zero.")
        if self.grid_step <= 0:
            raise ValueError("grid_step must be greater than zero.")

        cx, cy, cz = self.center

        # ----------------------------------------------------------
        # 1. حساب النطاق (Range)
        # ----------------------------------------------------------
        if x_range is None:
            half_x_steps = int(np.floor(self.x_length / (2 * self.grid_step) + 1e-8))
            self.x_range = (-half_x_steps, half_x_steps)
        else:
            self.x_range = (x_range[0], x_range[1])

        self.x_min = cx + self.x_range[0] * self.grid_step
        self.x_max = cx + self.x_range[1] * self.grid_step
        self.x_length = self.x_max - self.x_min

        self.axis_line = VGroup()
        self.ticks = VGroup()
        self.minor_ticks = VGroup()
        self.labels = VGroup()
        self.origin = VGroup()
        self.axis_label = VGroup()

        # ----------------------------------------------------------
        # 2. خط المحور X ورؤوس الأسهم المتماثلة
        # ----------------------------------------------------------
        self.x_axis = Line(
            [self.x_min, cy, cz],
            [self.x_max, cy, cz],
            color=axis_color,
            stroke_width=axis_width,
            stroke_opacity=axis_opacity,
            buff=0,
        )

        arrowhead_length = 0.20
        arrowhead_half_width = 0.075

        def make_arrowhead(tip, direction):
            tip = np.array(tip, dtype=float)
            direction = np.array(direction, dtype=float) / np.linalg.norm(direction)
            perpendicular = np.array([-direction[1], direction[0], 0.0])
            base = tip - direction * arrowhead_length
            return Polygon(
                tip,
                base + perpendicular * arrowhead_half_width,
                base - perpendicular * arrowhead_half_width,
                color=axis_color,
                fill_color=axis_color,
                fill_opacity=axis_opacity,
                stroke_width=0,
            )

        self.arrowheads = VGroup(
            make_arrowhead([self.x_min, cy, cz], LEFT),
            make_arrowhead([self.x_max, cy, cz], RIGHT),
        )

        self.axis_line.add(self.x_axis, self.arrowheads)

        # ----------------------------------------------------------
        # 3. اسم المحور X
        # ----------------------------------------------------------
        if show_axis_label:
            self.x_label = MathTex(
                "X",
                color=axis_label_color,
                font_size=axis_label_font_size,
            )
            self.x_label.move_to(
                np.array([self.x_max, cy, cz]) + RIGHT * axis_label_buff
            )
            self.axis_label.add(self.x_label)

        # ----------------------------------------------------------
        # 4. التدريج الرئيسي والأرقام (Major Ticks & Numbers)
        # ----------------------------------------------------------
        x_start = int(np.ceil(self.x_range[0]))
        x_end = int(np.floor(self.x_range[1]))

        for i in range(x_start, x_end + 1):
            point = cx + i * self.grid_step * RIGHT + cy * UP + cz * OUT

            if show_ticks:
                self.ticks.add(
                    Line(
                        point + UP * tick_length / 2,
                        point + DOWN * tick_length / 2,
                        color=tick_color,
                        stroke_width=tick_width,
                        stroke_opacity=tick_opacity,
                    )
                )

            if show_numbers and i != 0:
                label = Text(
                    str(i),
                    font_size=number_font_size,
                    color=number_color,
                ).set_opacity(number_opacity)
                label.next_to(point, DOWN, buff=number_buff)
                self.labels.add(label)

        # رقم الصفر
        if show_numbers and show_zero_label:
            zero = Text("0", font_size=number_font_size, color=zero_color)
            zero.next_to(np.array([cx, cy, cz]), DOWN + LEFT, buff=number_buff)
            self.labels.add(zero)

        # ----------------------------------------------------------
        # 5. التدريج الفرعي (Minor Ticks)
        # ----------------------------------------------------------
        if show_minor_ticks and minor_ticks_per_interval > 0:
            sub = minor_ticks_per_interval + 1
            for i in range(x_start, x_end):
                for j in range(1, sub):
                    x_coord = i + j / sub
                    point = cx + x_coord * self.grid_step * RIGHT + cy * UP + cz * OUT
                    self.minor_ticks.add(
                        Line(
                            point + UP * minor_tick_length / 2,
                            point + DOWN * minor_tick_length / 2,
                            color=minor_tick_color,
                            stroke_width=minor_tick_width,
                            stroke_opacity=minor_tick_opacity,
                        )
                    )

        # ----------------------------------------------------------
        # 6. نقطة الأصل (Origin Dot)
        # ----------------------------------------------------------
        self.origin_dot = Dot(
            self.center,
            radius=origin_radius,
            color=origin_color,
        )
        if not show_origin:
            self.origin_dot.set_opacity(0)
        self.origin.add(self.origin_dot)

        # ----------------------------------------------------------
        # 7. التجميع وترتيب الطبقات
        # ----------------------------------------------------------
        self.add(
            self.axis_line,
            self.minor_ticks,
            self.ticks,
            self.labels,
            self.origin,
            self.axis_label,
        )

    # --------------------------------------------------------------
    # دالة تحويل الإحداثيات الذكية (Dynamic c2p & Origin)
    # --------------------------------------------------------------
    def get_origin(self):
        """إرجاع الموضع الحقيقي الحالي لنقطة الأصل، حتى بعد التحريك أو الإزاحة"""
        if hasattr(self, "origin_dot") and self.origin_dot is not None:
            return self.origin_dot.get_center()
        return self.center.copy()

    def c2p(self, x):
        """تحويل إحداثي البعد الواحد x إلى موضع المشهد الفعلي"""
        origin = self.get_origin()
        return origin + np.array([x * self.grid_step, 0.0, 0.0], dtype=float)

    # --------------------------------------------------------------
    # تحديث self.center عند استخدام shift أو move_to تلقائياً
    # --------------------------------------------------------------
    def shift(self, *vectors):
        super().shift(*vectors)
        if hasattr(self, "origin_dot"):
            self.center = self.origin_dot.get_center()
        return self

    def move_to(self, point_or_mobject, **kwargs):
        super().move_to(point_or_mobject, **kwargs)
        if hasattr(self, "origin_dot"):
            self.center = self.origin_dot.get_center()
        return self

    # --------------------------------------------------------------
    # أنيميشن الظهور
    # --------------------------------------------------------------
    def animate_creation(self, scene, run_time=1.5):
        anims = [
            Create(self.axis_line),
            Create(self.minor_ticks),
            Create(self.ticks),
            FadeIn(self.labels, shift=UP * 0.05),
            FadeIn(self.origin, scale=0.7),
        ]
        if len(self.axis_label) > 0:
            anims.append(FadeIn(self.axis_label, shift=LEFT * 0.08))

        scene.play(
            AnimationGroup(*anims, lag_ratio=0.15),
            run_time=run_time,
        )


#============================================================================================================================


class MachAxes2D(VGroup):
    """
    MACH-MATH coordinate system.

    Features:
    - Backward-compatible x_length and y_length.
    - Optional x_range and y_range for coordinate control.
    - Dashed grid aligned with mathematical coordinates.
    - Continuous gold axes with symmetric arrowheads.
    - Major and minor tick marks.
    - Numeric labels for major ticks only.
    - Highlighted origin.
    - Optional X/Y axis labels.
    - Independent visual layers and creation animation.
    """

    def __init__(
        self,
        center=ORIGIN,
        x_length=7.2,
        y_length=7.8,
        grid_step=0.55,

        # Coordinate ranges
        x_range=None,
        y_range=None,

        # Main axes
        axis_color=GOLD_LIGHT,
        axis_width=2.2,
        axis_opacity=0.90,

        # Grid
        grid_color=STONE_AXIS,
        grid_width=0.85,
        grid_opacity=0.42,
        dash_length=0.08,
        dashed_ratio=0.55,
        show_grid=True,

        # Major tick marks
        show_ticks=True,
        tick_length=0.09,
        tick_width=1.5,
        tick_color=GOLD_LIGHT,
        tick_opacity=0.90,

        # Minor tick marks (NEW)
        show_minor_ticks=True,
        minor_ticks_per_interval=9,
        minor_tick_length=0.045,
        minor_tick_width=1.0,
        minor_tick_color=GOLD_LIGHT,
        minor_tick_opacity=0.70,

        # Numeric labels
        show_numbers=True,
        number_color=IVORY_WHITE,
        number_font_size=17,
        number_opacity=0.92,
        number_buff=0.12,
        show_zero_label=True,
        zero_color=GOLD_BRIGHT,

        # Origin
        show_origin=True,
        origin_radius=0.075,
        origin_color=GOLD_BRIGHT,

        # X/Y axis labels
        show_axis_labels=True,
        axis_label_color=GOLD_BRIGHT,
        axis_label_font_size=24,
        axis_label_buff=0.18,

        **kwargs,
    ):
        super().__init__(**kwargs)

        self.center = np.array(center, dtype=float)
        self.x_length = float(x_length)
        self.y_length = float(y_length)
        self.grid_step = float(grid_step)

        if self.x_length <= 0 or self.y_length <= 0:
            raise ValueError("Axis lengths must be greater than zero.")

        if self.grid_step <= 0:
            raise ValueError("grid_step must be greater than zero.")

        if len(self.center) != 3:
            raise ValueError("center must contain exactly 3 coordinates.")

        if (
            not isinstance(minor_ticks_per_interval, int)
            or isinstance(minor_ticks_per_interval, bool)
            or minor_ticks_per_interval < 0
        ):
            raise ValueError(
                "minor_ticks_per_interval must be a non-negative integer."
            )

        if minor_tick_length < 0:
            raise ValueError("minor_tick_length cannot be negative.")

        # ----------------------------------------------------------
        # 1. Resolve coordinate ranges
        # ----------------------------------------------------------
        def resolve_range(axis_range, axis_length):
            if axis_range is None:
                half_steps = int(
                    np.floor(axis_length / (2 * self.grid_step) + 1e-8)
                )
                return (-half_steps, half_steps)

            if len(axis_range) != 2:
                raise ValueError("Each range must be a (min, max) pair.")

            low, high = axis_range

            if not isinstance(
                low, (int, float, np.integer, np.floating)
            ):
                raise TypeError("Range boundaries must be numeric.")

            if not isinstance(
                high, (int, float, np.integer, np.floating)
            ):
                raise TypeError("Range boundaries must be numeric.")

            if low >= high:
                raise ValueError(
                    "Range minimum must be less than maximum."
                )

            return (low, high)

        self.x_range = resolve_range(x_range, self.x_length)
        self.y_range = resolve_range(y_range, self.y_length)

        cx, cy, cz = self.center

        # ----------------------------------------------------------
        # 2. Calculate visible bounds
        # ----------------------------------------------------------
        if x_range is not None:
            self.x_min = cx + self.x_range[0] * self.grid_step
            self.x_max = cx + self.x_range[1] * self.grid_step
            self.x_length = self.x_max - self.x_min
        else:
            self.x_min = cx - self.x_length / 2
            self.x_max = cx + self.x_length / 2

        if y_range is not None:
            self.y_min = cy + self.y_range[0] * self.grid_step
            self.y_max = cy + self.y_range[1] * self.grid_step
            self.y_length = self.y_max - self.y_min
        else:
            self.y_min = cy - self.y_length / 2
            self.y_max = cy + self.y_length / 2

        self.grid = VGroup()
        self.axes = VGroup()
        self.ticks = VGroup()
        self.minor_ticks = VGroup()
        self.labels = VGroup()
        self.origin = VGroup()
        self.axis_labels = VGroup()

        # ----------------------------------------------------------
        # 3. Dashed grid
        # ----------------------------------------------------------
        if show_grid:
            if x_range is not None:
                x_values = range(
                    int(np.ceil(self.x_range[0])),
                    int(np.floor(self.x_range[1])) + 1,
                )
            else:
                half_x_steps = int(
                    np.floor(
                        self.x_length / (2 * self.grid_step) + 1e-8
                    )
                )
                x_values = range(-half_x_steps, half_x_steps + 1)

            if y_range is not None:
                y_values = range(
                    int(np.ceil(self.y_range[0])),
                    int(np.floor(self.y_range[1])) + 1,
                )
            else:
                half_y_steps = int(
                    np.floor(
                        self.y_length / (2 * self.grid_step) + 1e-8
                    )
                )
                y_values = range(-half_y_steps, half_y_steps + 1)

            for i in x_values:
                if i == 0:
                    continue

                x = cx + i * self.grid_step

                if self.x_min < x < self.x_max:
                    self.grid.add(
                        DashedLine(
                            [x, self.y_min, cz],
                            [x, self.y_max, cz],
                            dash_length=dash_length,
                            dashed_ratio=dashed_ratio,
                            color=grid_color,
                            stroke_width=grid_width,
                            stroke_opacity=grid_opacity,
                        )
                    )

            for i in y_values:
                if i == 0:
                    continue

                y = cy + i * self.grid_step

                if self.y_min < y < self.y_max:
                    self.grid.add(
                        DashedLine(
                            [self.x_min, y, cz],
                            [self.x_max, y, cz],
                            dash_length=dash_length,
                            dashed_ratio=dashed_ratio,
                            color=grid_color,
                            stroke_width=grid_width,
                            stroke_opacity=grid_opacity,
                        )
                    )

        # ----------------------------------------------------------
        # 4. Continuous main axes + symmetric arrowheads
        # ----------------------------------------------------------
        self.x_axis = Line(
            [self.x_min, cy, cz],
            [self.x_max, cy, cz],
            color=axis_color,
            stroke_width=axis_width,
            stroke_opacity=axis_opacity,
            buff=0,
        )

        self.y_axis = Line(
            [cx, self.y_min, cz],
            [cx, self.y_max, cz],
            color=axis_color,
            stroke_width=axis_width,
            stroke_opacity=axis_opacity,
            buff=0,
        )

        arrowhead_length = 0.20
        arrowhead_half_width = 0.075

        def make_arrowhead(tip, direction):
            tip = np.array(tip, dtype=float)
            direction = np.array(direction, dtype=float)
            direction /= np.linalg.norm(direction)

            perpendicular = np.array(
                [-direction[1], direction[0], 0.0]
            )

            base = tip - direction * arrowhead_length

            return Polygon(
                tip,
                base + perpendicular * arrowhead_half_width,
                base - perpendicular * arrowhead_half_width,
                color=axis_color,
                fill_color=axis_color,
                fill_opacity=axis_opacity,
                stroke_width=0,
            )

        self.arrowheads = VGroup(
            make_arrowhead([self.x_min, cy, cz], LEFT),
            make_arrowhead([self.x_max, cy, cz], RIGHT),
            make_arrowhead([cx, self.y_min, cz], DOWN),
            make_arrowhead([cx, self.y_max, cz], UP),
        )

        self.axes.add(
            self.x_axis,
            self.y_axis,
            self.arrowheads,
        )

        # ----------------------------------------------------------
        # 5. X/Y axis labels
        # ----------------------------------------------------------
        if show_axis_labels:
            self.x_label = MathTex(
                "X",
                color=axis_label_color,
                font_size=axis_label_font_size,
            )

            self.x_label.move_to(
                np.array([self.x_max, cy, cz])
                + RIGHT * axis_label_buff
            )

            self.y_label = MathTex(
                "Y",
                color=axis_label_color,
                font_size=axis_label_font_size,
            )

            self.y_label.move_to(
                np.array([cx, self.y_max, cz])
                + UP * axis_label_buff
            )

            self.axis_labels.add(
                self.x_label,
                self.y_label,
            )

        # ----------------------------------------------------------
        # 6. Resolve major tick coordinate ranges
        # ----------------------------------------------------------
        if x_range is not None:
            x_start = int(np.ceil(self.x_range[0]))
            x_end = int(np.floor(self.x_range[1]))
        else:
            half_x_steps = int(
                np.floor(
                    self.x_length / (2 * self.grid_step) + 1e-8
                )
            )
            x_start, x_end = -half_x_steps, half_x_steps

        if y_range is not None:
            y_start = int(np.ceil(self.y_range[0]))
            y_end = int(np.floor(self.y_range[1]))
        else:
            half_y_steps = int(
                np.floor(
                    self.y_length / (2 * self.grid_step) + 1e-8
                )
            )
            y_start, y_end = -half_y_steps, half_y_steps

        # ----------------------------------------------------------
        # 7. Major ticks and numeric labels
        # ----------------------------------------------------------
        if show_ticks or show_numbers:
            # X-axis major ticks
            for i in range(x_start, x_end + 1):
                point = self.c2p(i, 0)

                if not (
                    self.x_min - 1e-8 <= point[0] <= self.x_max + 1e-8
                ):
                    continue

                if show_ticks:
                    self.ticks.add(
                        Line(
                            point + UP * tick_length / 2,
                            point + DOWN * tick_length / 2,
                            color=tick_color,
                            stroke_width=tick_width,
                            stroke_opacity=tick_opacity,
                        )
                    )

                if show_numbers and i != 0:
                    label = Text(
                        str(i),
                        font_size=number_font_size,
                        color=number_color,
                    )
                    label.set_opacity(number_opacity)
                    label.next_to(
                        point,
                        DOWN,
                        buff=number_buff,
                    )
                    self.labels.add(label)

            # Y-axis major ticks
            for i in range(y_start, y_end + 1):
                point = self.c2p(0, i)

                if not (
                    self.y_min - 1e-8 <= point[1] <= self.y_max + 1e-8
                ):
                    continue

                if show_ticks:
                    self.ticks.add(
                        Line(
                            point + LEFT * tick_length / 2,
                            point + RIGHT * tick_length / 2,
                            color=tick_color,
                            stroke_width=tick_width,
                            stroke_opacity=tick_opacity,
                        )
                    )

                if show_numbers and i != 0:
                    label = Text(
                        str(i),
                        font_size=number_font_size,
                        color=number_color,
                    )
                    label.set_opacity(number_opacity)
                    label.next_to(
                        point,
                        LEFT,
                        buff=number_buff,
                    )
                    self.labels.add(label)

            # Distinct zero label
            if show_numbers and show_zero_label:
                zero = Text(
                    "0",
                    font_size=number_font_size,
                    color=zero_color,
                )
                zero.set_opacity(1.0)
                zero.next_to(
                    self.c2p(0, 0),
                    DOWN + LEFT,
                    buff=number_buff,
                )
                self.labels.add(zero)

        # ----------------------------------------------------------
        # 8. Minor ticks between major ticks (NEW)
        # ----------------------------------------------------------
        if show_minor_ticks and minor_ticks_per_interval > 0:
            subdivisions = minor_ticks_per_interval + 1

            # X-axis minor ticks
            for i in range(x_start, x_end):
                for j in range(1, subdivisions):
                    x_coord = i + j / subdivisions
                    point = self.c2p(x_coord, 0)

                    if not (
                        self.x_min + 1e-8
                        < point[0]
                        < self.x_max - 1e-8
                    ):
                        continue

                    self.minor_ticks.add(
                        Line(
                            point + UP * minor_tick_length / 2,
                            point + DOWN * minor_tick_length / 2,
                            color=minor_tick_color,
                            stroke_width=minor_tick_width,
                            stroke_opacity=minor_tick_opacity,
                        )
                    )

            # Y-axis minor ticks
            for i in range(y_start, y_end):
                for j in range(1, subdivisions):
                    y_coord = i + j / subdivisions
                    point = self.c2p(0, y_coord)

                    if not (
                        self.y_min + 1e-8
                        < point[1]
                        < self.y_max - 1e-8
                    ):
                        continue

                    self.minor_ticks.add(
                        Line(
                            point + LEFT * minor_tick_length / 2,
                            point + RIGHT * minor_tick_length / 2,
                            color=minor_tick_color,
                            stroke_width=minor_tick_width,
                            stroke_opacity=minor_tick_opacity,
                        )
                    )

        # ----------------------------------------------------------
        # 9. Origin point
        # ----------------------------------------------------------
        if show_origin:
            self.origin_dot = Dot(
                self.center,
                radius=origin_radius,
                color=origin_color,
            )
            self.origin.add(self.origin_dot)

        # ----------------------------------------------------------
        # 10. Layer order
        # ----------------------------------------------------------
        self.add(
            self.grid,
            self.axes,
            self.minor_ticks,
            self.ticks,
            self.labels,
            self.origin,
            self.axis_labels,
        )

    # --------------------------------------------------------------
    # Coordinate helpers
    # --------------------------------------------------------------
    def c2p(self, x, y, z=0):
        """Convert grid coordinates to scene positions."""
        return self.center + np.array(
            [
                x * self.grid_step,
                y * self.grid_step,
                z,
            ],
            dtype=float,
        )

    def get_origin(self):
        return self.center.copy()

    # --------------------------------------------------------------
    # Creation animation
    # --------------------------------------------------------------
    def animate_creation(self, scene, run_time=1.8):
        """Reveal grid, axes, minor/major ticks, labels, and origin."""
        animations = []

        if len(self.grid) > 0:
            animations.append(Create(self.grid))

        animations.append(Create(self.axes))

        if len(self.axis_labels) > 0:
            animations.append(
                FadeIn(self.axis_labels, shift=UP * 0.08)
            )

        if len(self.minor_ticks) > 0:
            animations.append(Create(self.minor_ticks))

        if len(self.ticks) > 0:
            animations.append(Create(self.ticks))

        if len(self.labels) > 0:
            animations.append(
                FadeIn(self.labels, shift=UP * 0.06)
            )

        if len(self.origin) > 0:
            animations.append(FadeIn(self.origin, scale=0.7))

        scene.play(
            AnimationGroup(*animations, lag_ratio=0.16),
            run_time=run_time,
        )


class _RevealZ(AnimationGroup):
    """تجميع أنيميشن إظهار Z مع تنظيف تلقائي في النهاية."""

    def __init__(self, axes, *anims, **kwargs):
        super().__init__(*anims, **kwargs)
        self._axes3d = axes

    def clean_up_from_scene(self, scene):
        super().clean_up_from_scene(scene)
        self._axes3d._finish_reveal_z(scene)


class MachAxes3D(VGroup):
    """
    نظام الإحداثيات ثلاثي الأبعاد الرسمي لقناة MACH-MATH (نسخة سينمائية).

    الجديد في هذه النسخة:
    - أرضية (XY) بخطوط متدرجة تتلاشى عند الأطراف + لوح زجاجي خفيف جداً بدل الخطوط المقطّعة المزعجة.
    - جدران خلفية اختيارية (show_back_walls) تعطي إحساس "الغرفة" وتوضح العمق.
    - رؤوس أسهم مخروطية حقيقية (Cone) بإضاءة، بدل المثلثات المسطحة.
    - توهج ذهبي ناعم تحت المحاور.
    - كل الأرقام والرموز تواجه الكاميرا دائماً (face_camera) فتبقى مقروءة مهما دارت الكاميرا.
    - hide_z / reveal_z: إخفاء المحور Z عند البداية ثم إظهاره (مناسب لمطابقة 2D ← 3D).
    - دوال مساعدة: get_point, get_drop_lines, get_creation_animation.

    التوافق مع الإصدار القديم: نفس البارامترات والخصائص (grid, axes, ticks, minor_ticks,
    labels, origin, axis_labels, x_axis/y_axis/z_axis, arrowheads, origin_dot)
    ونفس الدوال get_origin / c2p / shift / move_to / animate_creation.
    """

    def __init__(
        self,
        center=ORIGIN,
        x_length=7.2,
        y_length=7.2,
        z_length=5.6,
        grid_step=0.55,

        # Coordinate ranges (min, max)
        x_range=None,
        y_range=None,
        z_range=None,

        # Main axes
        axis_color=GOLD_LIGHT,
        axis_width=2.4,
        axis_opacity=0.92,
        glow=True,
        show_negative_arrows=True,
        arrow_length=0.28,
        arrow_radius=0.065,

        # Grids
        show_xy_grid=True,
        show_xz_grid=False,
        show_yz_grid=False,
        grid_color=STONE_AXIS,
        grid_width=0.9,
        grid_opacity=0.50,
        grid_style="solid",          # "solid" (متدرجة) أو "dashed" (القديمة)
        grid_fade=True,
        dash_length=0.08,
        dashed_ratio=0.55,

        # Floor glass plane
        show_floor_plane=True,
        floor_opacity=0.045,

        # Back walls (room corner)
        show_back_walls=False,
        wall_x_side=-1,              # الجدار YZ عند x = min (-1) أو max (+1)
        wall_y_side=1,               # الجدار XZ عند y = max (+1) أو min (-1)
        wall_opacity=0.28,

        # Major tick marks
        show_ticks=True,
        tick_length=0.09,
        tick_width=1.5,
        tick_color=GOLD_LIGHT,
        tick_opacity=0.90,

        # Minor tick marks
        show_minor_ticks=True,
        minor_ticks_per_interval=4,
        minor_tick_length=0.045,
        minor_tick_width=1.0,
        minor_tick_color=GOLD_LIGHT,
        minor_tick_opacity=0.65,

        # Numeric labels
        show_numbers=True,
        number_color=IVORY_WHITE,
        number_font_size=15,
        number_opacity=0.90,
        number_buff=0.16,
        show_zero_label=True,
        zero_color=GOLD_BRIGHT,

        # Origin
        show_origin=True,
        origin_radius=0.075,
        origin_color=GOLD_BRIGHT,

        # Axis labels (X, Y, Z)
        show_axis_labels=True,
        axis_label_color=GOLD_BRIGHT,
        axis_label_font_size=24,
        axis_label_buff=0.30,

        # Start flat (XY only) and reveal Z later with reveal_z()
        hide_z=False,

        **kwargs,
    ):
        super().__init__(**kwargs)

        self.center = np.array(center, dtype=float)
        self.x_length = float(x_length)
        self.y_length = float(y_length)
        self.z_length = float(z_length)
        self.grid_step = float(grid_step)
        self._faced_scenes = set()
        self._z_hidden = bool(hide_z)
        self._z_built_origin = self.center.copy()

        cx, cy, cz = self.center
        gs = self.grid_step

        # ----------------------------------------------------------
        # 1. Ranges
        # ----------------------------------------------------------
        def resolve_range(axis_range, axis_len):
            if axis_range is None:
                half_steps = int(np.floor(axis_len / (2 * gs) + 1e-8))
                return (-half_steps, half_steps)
            return (axis_range[0], axis_range[1])

        self.x_range = resolve_range(x_range, self.x_length)
        self.y_range = resolve_range(y_range, self.y_length)
        self.z_range = resolve_range(z_range, self.z_length)

        self.x_min = cx + self.x_range[0] * gs
        self.x_max = cx + self.x_range[1] * gs
        self.y_min = cy + self.y_range[0] * gs
        self.y_max = cy + self.y_range[1] * gs
        self.z_min = cz + self.z_range[0] * gs
        self.z_max = cz + self.z_range[1] * gs

        self.floor = VGroup()
        self.walls = VGroup()
        self.grid = VGroup()
        self.glow = VGroup()
        self.axes = VGroup()
        self.ticks = VGroup()
        self.minor_ticks = VGroup()
        self.labels = VGroup()
        self.origin = VGroup()
        self.axis_labels = VGroup()

        x_vals = range(int(np.ceil(self.x_range[0])), int(np.floor(self.x_range[1])) + 1)
        y_vals = range(int(np.ceil(self.y_range[0])), int(np.floor(self.y_range[1])) + 1)
        z_vals = range(int(np.ceil(self.z_range[0])), int(np.floor(self.z_range[1])) + 1)
        mx = max(1, max(abs(self.x_range[0]), abs(self.x_range[1])))
        my = max(1, max(abs(self.y_range[0]), abs(self.y_range[1])))
        mz = max(1, max(abs(self.z_range[0]), abs(self.z_range[1])))

        # ----------------------------------------------------------
        # 2. Grid helpers
        # ----------------------------------------------------------
        def grid_line(a, b, opacity):
            if grid_style == "dashed":
                return DashedLine(
                    a, b, dash_length=dash_length, dashed_ratio=dashed_ratio,
                    color=grid_color, stroke_width=grid_width, stroke_opacity=opacity,
                )
            ln = Line(a, b, color=grid_color, stroke_width=grid_width)
            if grid_fade:
                ln.set_stroke(color=grid_color, width=grid_width,
                              opacity=[opacity * 0.10, opacity, opacity * 0.10])
            else:
                ln.set_stroke(color=grid_color, width=grid_width, opacity=opacity)
            return ln

        def falloff(i, m):
            # الخطوط البعيدة عن المحور أخفت قليلاً
            return grid_opacity * (1.0 - 0.45 * abs(i) / m)

        # ----------------------------------------------------------
        # 3. Floor plane + XY grid
        # ----------------------------------------------------------
        if show_floor_plane and show_xy_grid:
            plane = Polygon(
                [self.x_min, self.y_min, cz], [self.x_max, self.y_min, cz],
                [self.x_max, self.y_max, cz], [self.x_min, self.y_max, cz],
                stroke_width=0, fill_color=grid_color, fill_opacity=floor_opacity,
            )
            self.floor.add(plane)

        if show_xy_grid:
            for i in x_vals:
                if i == 0:
                    continue
                x = cx + i * gs
                self.grid.add(grid_line([x, self.y_min, cz], [x, self.y_max, cz], falloff(i, mx)))
            for j in y_vals:
                if j == 0:
                    continue
                y = cy + j * gs
                self.grid.add(grid_line([self.x_min, y, cz], [self.x_max, y, cz], falloff(j, my)))

        # XZ plane through origin
        if show_xz_grid:
            for i in x_vals:
                if i == 0:
                    continue
                x = cx + i * gs
                self.grid.add(grid_line([x, cy, self.z_min], [x, cy, self.z_max], falloff(i, mx) * 0.7))
            for k in z_vals:
                if k == 0:
                    continue
                z = cz + k * gs
                self.grid.add(grid_line([self.x_min, cy, z], [self.x_max, cy, z], falloff(k, mz) * 0.7))

        # YZ plane through origin
        if show_yz_grid:
            for j in y_vals:
                if j == 0:
                    continue
                y = cy + j * gs
                self.grid.add(grid_line([cx, y, self.z_min], [cx, y, self.z_max], falloff(j, my) * 0.7))
            for k in z_vals:
                if k == 0:
                    continue
                z = cz + k * gs
                self.grid.add(grid_line([cx, self.y_min, z], [cx, self.y_max, z], falloff(k, mz) * 0.7))

        # ----------------------------------------------------------
        # 4. Back walls (room corner)
        # ----------------------------------------------------------
        if show_back_walls:
            wy = self.y_max if wall_y_side >= 0 else self.y_min
            wx = self.x_min if wall_x_side <= 0 else self.x_max
            wo = wall_opacity
            wall_xz = Polygon(
                [self.x_min, wy, self.z_min], [self.x_max, wy, self.z_min],
                [self.x_max, wy, self.z_max], [self.x_min, wy, self.z_max],
                stroke_width=0, fill_color=grid_color, fill_opacity=floor_opacity * 0.6,
            )
            wall_yz = Polygon(
                [wx, self.y_min, self.z_min], [wx, self.y_max, self.z_min],
                [wx, self.y_max, self.z_max], [wx, self.y_min, self.z_max],
                stroke_width=0, fill_color=grid_color, fill_opacity=floor_opacity * 0.6,
            )
            self.walls.add(wall_xz, wall_yz)
            for i in x_vals:
                x = cx + i * gs
                self.walls.add(grid_line([x, wy, self.z_min], [x, wy, self.z_max], wo))
            for k in z_vals:
                z = cz + k * gs
                self.walls.add(grid_line([self.x_min, wy, z], [self.x_max, wy, z], wo))
            for j in y_vals:
                y = cy + j * gs
                self.walls.add(grid_line([wx, y, self.z_min], [wx, y, self.z_max], wo))
            for k in z_vals:
                z = cz + k * gs
                self.walls.add(grid_line([wx, self.y_min, z], [wx, self.y_max, z], wo))

        # ----------------------------------------------------------
        # 5. Axes + glow + cone arrowheads
        # ----------------------------------------------------------
        AL = float(arrow_length)

        def axis_line(a, b):
            return Line(a, b, color=axis_color, stroke_width=axis_width, stroke_opacity=axis_opacity)

        def axis_glow(a, b):
            g = VGroup(
                Line(a, b, color=axis_color, stroke_width=axis_width * 5.0, stroke_opacity=0.06),
                Line(a, b, color=axis_color, stroke_width=axis_width * 2.6, stroke_opacity=0.11),
            )
            return g

        def arrow_cone(tip, direction):
            d = np.array(direction, dtype=float)
            d /= np.linalg.norm(d)
            cone = Cone(
                base_radius=arrow_radius, height=AL, direction=d,
                fill_color=axis_color, fill_opacity=1.0, stroke_width=0,
                resolution=(2, 18), show_base=True,
            )
            cone.shift(np.array(tip, dtype=float))
            return cone

        pX0, pX1 = np.array([self.x_min, cy, cz]), np.array([self.x_max, cy, cz])
        pY0, pY1 = np.array([cx, self.y_min, cz]), np.array([cx, self.y_max, cz])
        pZ0, pZ1 = np.array([cx, cy, self.z_min]), np.array([cx, cy, self.z_max])

        o0 = AL if show_negative_arrows else 0.0
        self.x_axis = axis_line(pX0 + RIGHT * o0, pX1 - RIGHT * AL)
        self.y_axis = axis_line(pY0 + UP * o0, pY1 - UP * AL)
        self.z_axis = axis_line(pZ0 + OUT * o0, pZ1 - OUT * AL)

        self.glow.add(axis_glow(pX0, pX1), axis_glow(pY0, pY1))
        z_glow = axis_glow(pZ0, pZ1)

        x_cones = [arrow_cone(pX1, RIGHT)]
        y_cones = [arrow_cone(pY1, UP)]
        z_cones = [arrow_cone(pZ1, OUT)]
        if show_negative_arrows:
            x_cones.append(arrow_cone(pX0, LEFT))
            y_cones.append(arrow_cone(pY0, DOWN))
            z_cones.append(arrow_cone(pZ0, IN))

        self.arrowheads = VGroup(*x_cones, *y_cones, *z_cones)
        self.axes.add(self.x_axis, self.y_axis, self.z_axis, self.arrowheads)

        # ----------------------------------------------------------
        # 6. Axis labels
        # ----------------------------------------------------------
        z_label = None
        if show_axis_labels:
            self.x_label = MathTex("X", color=axis_label_color, font_size=axis_label_font_size)
            self.x_label.move_to(pX1 + RIGHT * axis_label_buff)
            self.y_label = MathTex("Y", color=axis_label_color, font_size=axis_label_font_size)
            self.y_label.move_to(pY1 + UP * axis_label_buff)
            self.z_label = MathTex("Z", color=axis_label_color, font_size=axis_label_font_size)
            self.z_label.move_to(pZ1 + OUT * axis_label_buff)
            z_label = self.z_label
            self.axis_labels.add(self.x_label, self.y_label, self.z_label)

        # ----------------------------------------------------------
        # 7. Ticks + numbers
        # ----------------------------------------------------------
        z_ticks, z_minor, z_numbers = [], [], []

        def make_num(v, color=number_color):
            s = str(v).replace("-", "−")
            return Text(s, font_size=number_font_size, color=color).set_opacity(number_opacity)

        if show_ticks or show_numbers:
            for i in x_vals:
                pt = self.center + np.array([i * gs, 0, 0])
                if show_ticks:
                    self.ticks.add(Line(pt + UP * tick_length / 2, pt + DOWN * tick_length / 2,
                                        color=tick_color, stroke_width=tick_width, stroke_opacity=tick_opacity))
                if show_numbers and i != 0:
                    lbl = make_num(i)
                    lbl.next_to(pt, DOWN, buff=number_buff)
                    self.labels.add(lbl)

            for j in y_vals:
                pt = self.center + np.array([0, j * gs, 0])
                if show_ticks:
                    self.ticks.add(Line(pt + LEFT * tick_length / 2, pt + RIGHT * tick_length / 2,
                                        color=tick_color, stroke_width=tick_width, stroke_opacity=tick_opacity))
                if show_numbers and j != 0:
                    lbl = make_num(j)
                    lbl.next_to(pt, LEFT, buff=number_buff)
                    self.labels.add(lbl)

            for k in z_vals:
                pt = self.center + np.array([0, 0, k * gs])
                if show_ticks and k != 0:
                    z_ticks.append(Line(pt + RIGHT * tick_length / 2, pt + LEFT * tick_length / 2,
                                        color=tick_color, stroke_width=tick_width, stroke_opacity=tick_opacity))
                if show_numbers and k != 0:
                    lbl = make_num(k)
                    lbl.next_to(pt, RIGHT, buff=number_buff)
                    z_numbers.append(lbl)

            if show_numbers and show_zero_label:
                zero = Text("0", font_size=number_font_size, color=zero_color)
                zero.next_to(self.center, DOWN + LEFT, buff=number_buff)
                self.labels.add(zero)

        if show_minor_ticks and minor_ticks_per_interval > 0:
            sub = minor_ticks_per_interval + 1

            def mt(pt, a, b):
                return Line(pt + a * minor_tick_length / 2, pt + b * minor_tick_length / 2,
                            color=minor_tick_color, stroke_width=minor_tick_width,
                            stroke_opacity=minor_tick_opacity)

            for i in range(x_vals[0], x_vals[-1]):
                for s in range(1, sub):
                    pt = self.center + np.array([(i + s / sub) * gs, 0, 0])
                    self.minor_ticks.add(mt(pt, UP, DOWN))
            for j in range(y_vals[0], y_vals[-1]):
                for s in range(1, sub):
                    pt = self.center + np.array([0, (j + s / sub) * gs, 0])
                    self.minor_ticks.add(mt(pt, LEFT, RIGHT))
            for k in range(z_vals[0], z_vals[-1]):
                for s in range(1, sub):
                    pt = self.center + np.array([0, 0, (k + s / sub) * gs])
                    z_minor.append(mt(pt, RIGHT, LEFT))

        # ----------------------------------------------------------
        # 8. Origin
        # ----------------------------------------------------------
        self.origin_dot = Dot3D(self.center, radius=origin_radius, color=origin_color)
        if not show_origin:
            self.origin_dot.set_opacity(0)
        self.origin.add(self.origin_dot)

        # ----------------------------------------------------------
        # 9. Z parts (قد تكون مخفية في البداية)
        # ----------------------------------------------------------
        self.z_group = VGroup(z_glow, self.z_axis, *z_cones, *z_ticks, *z_minor, *z_numbers)
        if z_label is not None:
            self.z_group.add(z_label)
        self._z_axis_group = VGroup(z_glow, self.z_axis)
        self._z_cones = VGroup(*z_cones)
        self._z_rest = VGroup(*z_ticks, *z_minor, *z_numbers, *([z_label] if z_label is not None else []))

        if self._z_hidden:
            # أزل مكونات Z من المجموعات؛ ستعود عند reveal_z
            self.axes.remove(self.z_axis, *z_cones)
            self.arrowheads.remove(*z_cones)
            if z_label is not None:
                self.axis_labels.remove(z_label)
        else:
            self.glow.add(z_glow)
            self.ticks.add(*z_ticks)
            self.minor_ticks.add(*z_minor)
            self.labels.add(*z_numbers)

        # ----------------------------------------------------------
        # 10. Layers (الترتيب = ترتيب الرسم)
        # ----------------------------------------------------------
        self.add(
            self.floor,
            self.walls,
            self.grid,
            self.glow,
            self.axes,
            self.minor_ticks,
            self.ticks,
            self.labels,
            self.origin,
            self.axis_labels,
        )

    # --------------------------------------------------------------
    # التحويل
    # --------------------------------------------------------------
    def get_origin(self):
        if hasattr(self, "origin_dot") and self.origin_dot is not None:
            return self.origin_dot.get_center()
        return self.center.copy()

    def c2p(self, x, y, z=0):
        origin = self.get_origin()
        return origin + np.array([x * self.grid_step, y * self.grid_step, z * self.grid_step], dtype=float)

    def shift(self, *vectors):
        super().shift(*vectors)
        if hasattr(self, "origin_dot"):
            self.center = self.origin_dot.get_center()
        return self

    def move_to(self, point_or_mobject, **kwargs):
        super().move_to(point_or_mobject, **kwargs)
        if hasattr(self, "origin_dot"):
            self.center = self.origin_dot.get_center()
        return self

    # --------------------------------------------------------------
    # الأرقام تواجه الكاميرا
    # --------------------------------------------------------------
    def _label_mobjects(self):
        labs = list(self.labels) + list(self.axis_labels)
        for m in self._z_rest:
            if isinstance(m, VMobject) and not isinstance(m, Line) and m not in labs:
                labs.append(m)
        return labs

    def face_camera(self, scene):
        """
        يجعل كل الأرقام والرموز تواجه الكاميرا دائماً (لا تُضيف شيئاً للمشهد،
        فقط تسجّلها عند الكاميرا). استدعها مرة واحدة بعد إنشاء المحاور.
        """
        if not isinstance(scene, ThreeDScene):
            return self
        if id(scene) in self._faced_scenes:
            return self
        cam = scene.renderer.camera
        for lab in self._label_mobjects():
            cam.add_fixed_orientation_mobjects(lab)
        self._faced_scenes.add(id(scene))
        return self

    # --------------------------------------------------------------
    # مساعدات للعرض داخل المحاور
    # --------------------------------------------------------------
    def get_point(self, x, y, z=0, color=GOLD_BRIGHT, radius=0.07):
        return Dot3D(self.c2p(x, y, z), radius=radius, color=color)

    def get_drop_lines(self, x, y, z, color=GOLD_MUTED, width=1.4, opacity=0.75, dash_length=0.07, dot_radius=0.035):
        """
        خطوط إسقاط مقطّعة من النقطة إلى الأرضية ثم إلى محوري X و Y،
        تساعد العين على قراءة العمق (موضع النقطة في الفضاء).
        """
        p = self.c2p(x, y, z)
        foot = self.c2p(x, y, 0)
        fx = self.c2p(x, 0, 0)
        fy = self.c2p(0, y, 0)

        def dl(a, b):
            return DashedLine(a, b, dash_length=dash_length, color=color,
                              stroke_width=width, stroke_opacity=opacity)

        g = VGroup()
        if abs(z) > 1e-9:
            g.add(dl(p, foot))
        if abs(y) > 1e-9:
            g.add(dl(foot, fx))
        if abs(x) > 1e-9:
            g.add(dl(foot, fy))
        g.add(Dot3D(foot, radius=dot_radius, color=color))
        return g

    # --------------------------------------------------------------
    # Z: إخفاء / إظهار
    # --------------------------------------------------------------
    def _finish_reveal_z(self, scene):
        """بعد انتهاء الأنيميشن: اجعل أجزاء Z جزءاً من المجموعة (بدون رسم مزدوج)."""
        if not self._z_hidden:
            return
        fam = [m for m in self.z_group.get_family()]
        scene.remove(*fam)
        self.add(self.z_group)
        self._z_hidden = False

    def get_reveal_z_animation(self, run_time=1.4):
        """أنيميشن إظهار المحور Z (ينمو من نقطة الأصل للأعلى وللأسفل)."""
        if not self._z_hidden:
            return AnimationGroup()
        delta = self.get_origin() - self._z_built_origin
        if np.linalg.norm(delta) > 1e-9:
            self.z_group.shift(delta)
        self._z_built_origin = self.get_origin()
        anims = [
            Create(self._z_axis_group, lag_ratio=0.0),
            FadeIn(self._z_cones, scale=0.4),
        ]
        if len(self._z_rest) > 0:
            anims.append(FadeIn(self._z_rest, lag_ratio=0.05))
        return _RevealZ(self, *anims, lag_ratio=0.0, run_time=run_time)

    def reveal_z(self, scene, run_time=1.4):
        self.face_camera(scene)
        scene.play(self.get_reveal_z_animation(run_time), run_time=run_time)

    # --------------------------------------------------------------
    # أنيميشن الإنشاء
    # --------------------------------------------------------------
    def get_creation_animation(self):
        anims = []
        if len(self.floor) > 0:
            anims.append(FadeIn(self.floor))
        if len(self.grid) > 0:
            anims.append(Create(self.grid, lag_ratio=0.02))
        if len(self.walls) > 0:
            anims.append(Create(self.walls, lag_ratio=0.01))
        anims.append(Create(self.glow))
        anims.append(Create(VGroup(*[m for m in self.axes if m is not self.arrowheads])))
        anims.append(FadeIn(self.arrowheads, scale=0.4))
        if len(self.axis_labels) > 0:
            anims.append(FadeIn(self.axis_labels, shift=UP * 0.08))
        if len(self.minor_ticks) > 0:
            anims.append(Create(self.minor_ticks))
        if len(self.ticks) > 0:
            anims.append(Create(self.ticks))
        if len(self.labels) > 0:
            anims.append(FadeIn(self.labels, shift=UP * 0.05))
        if len(self.origin) > 0:
            anims.append(FadeIn(self.origin, scale=0.7))
        return AnimationGroup(*anims, lag_ratio=0.15)

    def animate_creation(self, scene, run_time=2.0):
        self.face_camera(scene)
        scene.play(self.get_creation_animation(), run_time=run_time)