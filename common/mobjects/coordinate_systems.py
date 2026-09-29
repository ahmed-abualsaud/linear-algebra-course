from manim import *

from common.palette import (
    STONE_AXIS,
    GOLD_SHADOW,
    GOLD_MUTED,
    GOLD_LIGHT,
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