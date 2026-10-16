from manim import *
import numpy as np

from common.palette import (
    GOLD_LIGHT,
    GOLD_DARK,
    GOLD_MUTED,
    STONE_AXIS,
)


# ==============================================================
# Glass illumination animation
# ==============================================================

class _GlassIllumination(Animation):
    """Gradually illuminate the glass from a known opacity state."""

    def __init__(
        self,
        glass,
        target_fill_opacity,
        target_border_opacity,
        start_fill_opacity=0.0,
        start_border_opacity=0.0,
        run_time=0.6,
        rate_func=smooth,
    ):
        self.glass = glass
        self.target_fill_opacity = target_fill_opacity
        self.target_border_opacity = target_border_opacity
        self.start_fill_opacity = start_fill_opacity
        self.start_border_opacity = start_border_opacity

        super().__init__(
            glass,
            run_time=run_time,
            rate_func=rate_func,
        )

    def begin(self):
        self.glass.set_fill(opacity=self.start_fill_opacity)
        self.glass.set_stroke(opacity=self.start_border_opacity)
        super().begin()

    def interpolate_mobject(self, alpha):
        fill_opacity = interpolate(
            self.start_fill_opacity,
            self.target_fill_opacity,
            alpha,
        )
        border_opacity = interpolate(
            self.start_border_opacity,
            self.target_border_opacity,
            alpha,
        )
        self.glass.set_fill(opacity=fill_opacity)
        self.glass.set_stroke(opacity=border_opacity)


# ==============================================================
# MACH-MATH Universal Card
# ==============================================================

class MachCard(VGroup):
    """
    بطاقة MACH-MATH العامة متعددة الاستخدامات:
    - تدعم أي نوع من المحتوى (معادلات، نصوص، رسومات هندسية).
    - توهج أرضي وانعكاس زجاجي ثلاثي الأبعاد.
    - مرونة كاملة في المحاذاة والتحريك التدريجي.
    """

    def __init__(
        self,
        width=5.0,
        height=3.5,
        center=ORIGIN,
        title=None,
        subtitle=None,
        content=None,
        auto_fit_content=True,
        show_divider=True,
        divider_style="horizontal",  # 'horizontal', 'vertical', or None
        background_color="#100D07",
        accent_color=GOLD_LIGHT,
        title_color=GOLD_LIGHT,
        subtitle_color=STONE_AXIS,
        border_opacity=0.45,
        background_opacity=0.88,
        glass_opacity=0.038,
        glass_border_opacity=0.18,
        glass_glow_opacity=0.085,
        glass_glow_border_opacity=0.30,
        reflection_offset=0.22,
        reflection_opacity=0.30,
        corner_radius=0.24,
        title_font="Cairo",
        title_font_size=20,
        subtitle_font_size=13,
        title_buff=0.14,
        content_padding=0.30,
        **kwargs,
    ):
        super().__init__(**kwargs)

        center = np.array(center, dtype=float)
        if center.size == 2:
            center = np.append(center, 0.0)

        self.card_width = width
        self.card_height = height
        self.center_point = center.copy()
        self.content_padding = content_padding

        self.base_glass_opacity = glass_opacity
        self.base_glass_border_opacity = glass_border_opacity
        self.glass_glow_opacity = glass_glow_opacity
        self.glass_glow_border_opacity = glass_glow_border_opacity

        # ======================================================
        # 1. جسم البطاقة الخارجي (Main Body)
        # ======================================================
        self.body = RoundedRectangle(
            corner_radius=corner_radius,
            width=width,
            height=height,
            stroke_width=1.4,
            color=accent_color,
            stroke_opacity=border_opacity,
            fill_color=background_color,
            fill_opacity=background_opacity,
        ).move_to(center)

        # ======================================================
        # 2. طبقة الزجاج الداخلية (Inner Glass)
        # ======================================================
        self.glass = RoundedRectangle(
            corner_radius=max(0, corner_radius - 0.04),
            width=width - 0.12,
            height=height - 0.12,
            stroke_color=accent_color,
            stroke_width=0.5,
            stroke_opacity=glass_border_opacity,
            fill_color=accent_color,
            fill_opacity=glass_opacity,
        ).move_to(self.body.get_center())

        # ======================================================
        # 3. التوهج الأرضي والانعكاس (Reflection & Floor Glow)
        # ======================================================
        self.reflection = self._make_floor_reflection(
            card=self.body,
            accent_color=accent_color,
            reflection_offset=reflection_offset,
            reflection_opacity=reflection_opacity,
        )

        # ======================================================
        # 4. الترويسة والعنوان (Title, Subtitle & Divider)
        # ======================================================
        self.title_group = VGroup()
        self.divider = VGroup()

        content_top_y = self.body.get_top()[1] - content_padding
        content_bottom_y = self.body.get_bottom()[1] + content_padding

        # إنشاء العنوان الرئيسي
        title_mob = None
        if title is not None:
            if isinstance(title, str):
                title_mob = MarkupText(
                    title,
                    font=title_font,
                    font_size=title_font_size,
                    color=title_color,
                )
            elif isinstance(title, Mobject):
                title_mob = title

            max_title_width = width - 2 * content_padding
            if title_mob.width > max_title_width:
                title_mob.scale(max_title_width / title_mob.width)

            title_mob.move_to([
                center[0],
                self.body.get_top()[1] - content_padding - title_mob.height / 2,
                center[2],
            ])
            self.title_group.add(title_mob)

        # إنشاء العنوان الفرعي (اختياري)
        subtitle_mob = None
        if subtitle is not None:
            if isinstance(subtitle, str):
                subtitle_mob = Text(
                    subtitle,
                    font=title_font,
                    font_size=subtitle_font_size,
                    color=subtitle_color,
                )
            elif isinstance(subtitle, Mobject):
                subtitle_mob = subtitle

            if title_mob is not None:
                subtitle_mob.next_to(title_mob, DOWN, buff=0.08)
            else:
                subtitle_mob.move_to([
                    center[0],
                    self.body.get_top()[1] - content_padding - subtitle_mob.height / 2,
                    center[2],
                ])
            self.title_group.add(subtitle_mob)

        # الفاصل (Divider)
        header_anchor = subtitle_mob if subtitle_mob is not None else title_mob
        if header_anchor is not None:
            content_top_y = header_anchor.get_bottom()[1] - title_buff

        if show_divider and divider_style is not None:
            if divider_style == "horizontal" and header_anchor is not None:
                line_y = header_anchor.get_bottom()[1] - title_buff
                div_line = Line(
                    self.body.get_left() + RIGHT * 0.35,
                    self.body.get_right() + LEFT * 0.35,
                    color=GOLD_DARK,
                    stroke_width=1.0,
                    stroke_opacity=0.45,
                ).move_to([center[0], line_y, center[2]])
                self.divider.add(div_line)
                content_top_y = div_line.get_bottom()[1] - content_padding

            elif divider_style == "vertical":
                top_v = (header_anchor.get_bottom()[1] - 0.15) if header_anchor is not None else (self.body.get_top()[1] - 0.28)
                bot_v = self.body.get_bottom()[1] + 0.28
                div_line = Line(
                    [center[0], top_v, center[2]],
                    [center[0], bot_v, center[2]],
                    stroke_width=1.0,
                    color=GOLD_DARK,
                    stroke_opacity=0.45,
                )
                self.divider.add(div_line)

        # حساب مركز ومساحة المحتوى القابلة للاستخدام
        self.usable_content_bounds = {
            "top": content_top_y,
            "bottom": content_bottom_y,
            "left": self.body.get_left()[0] + content_padding,
            "right": self.body.get_right()[0] - content_padding,
        }

        # ======================================================
        # 5. إدارة المحتوى (Content Management)
        # ======================================================
        self.content = VGroup()

        if content is not None:
            if isinstance(content, (list, tuple)):
                content_mobs = VGroup(*content)
            else:
                content_mobs = content

            if auto_fit_content:
                # ملاءمة تلقائية للحجم والتوسيط
                avail_w = max(0.1, self.usable_content_bounds["right"] - self.usable_content_bounds["left"])
                avail_h = max(0.1, self.usable_content_bounds["top"] - self.usable_content_bounds["bottom"])

                if content_mobs.width > 0 and content_mobs.height > 0:
                    scale_factor = min(
                        avail_w / content_mobs.width,
                        avail_h / content_mobs.height,
                        1.0,
                    )
                    content_mobs.scale(scale_factor)

                center_y = (self.usable_content_bounds["top"] + self.usable_content_bounds["bottom"]) / 2
                content_mobs.move_to([center[0], center_y, center[2]])

            self.content.add(content_mobs)

        # ======================================================
        # 6. ترتيب الطبقات (Z-Index)
        # ======================================================
        self.reflection.set_z_index(-2)
        self.body.set_z_index(0)
        self.glass.set_z_index(1)
        self.divider.set_z_index(2)
        self.title_group.set_z_index(3)
        self.content.set_z_index(3)

        self.add(
            self.reflection,
            self.body,
            self.glass,
            self.divider,
            self.title_group,
            self.content,
        )

    # ==========================================================
    # دوال مساعدة لمواقع العناصر
    # ==========================================================

    def get_content_center(self):
        """إرجاع إحداثيات مركز المنطقة المخصصة للمحتوى داخل البطاقة."""
        cx = self.center_point[0]
        cy = (self.usable_content_bounds["top"] + self.usable_content_bounds["bottom"]) / 2
        return np.array([cx, cy, self.center_point[2]])

    # ==========================================================
    # تحريكات البطاقة (Animations)
    # ==========================================================

    def construct(
        self,
        run_time=2.2,
        rate_func=smooth,
        show_reflection=True,
        illuminate_glass=True,
        show_content=True,
    ):
        """تحريك البطاقة بالكامل (الإطار -> التوهج والزجاج -> المحتوى)."""
        self.glass.set_fill(opacity=0.0)
        self.glass.set_stroke(opacity=0.0)

        animations = []

        # 1. رسم الإطار الخارجي
        animations.append(
            Create(self.body, run_time=run_time * 0.35, rate_func=rate_func)
        )

        # 2. إشعال الزجاج والتوهج
        reveal = []
        if show_reflection:
            reveal.append(FadeIn(self.reflection, run_time=run_time * 0.30, rate_func=rate_func))

        target_f_op = self.glass_glow_opacity if illuminate_glass else self.base_glass_opacity
        target_b_op = self.glass_glow_border_opacity if illuminate_glass else self.base_glass_border_opacity

        reveal.append(
            _GlassIllumination(
                self.glass,
                target_fill_opacity=target_f_op,
                target_border_opacity=target_b_op,
                run_time=run_time * 0.30,
                rate_func=rate_func,
            )
        )
        animations.append(AnimationGroup(*reveal, lag_ratio=0))

        # 3. إظهار الترويسة والمحتوى
        foreground = VGroup(self.divider, self.title_group)
        if show_content and len(self.content) > 0:
            foreground.add(self.content)

        if len(foreground) > 0:
            animations.append(
                FadeIn(foreground, run_time=run_time * 0.30, rate_func=rate_func)
            )

        return Succession(*animations)

    def animate_shell(
        self,
        run_time=1.2,
        rate_func=smooth,
        show_reflection=True,
        illuminate_glass=True,
        show_header=True,
    ):
        """
        بناء هيكل البطاقة والزجاج والترويسة فقط، مع ترك المحتوى للمستخدم ليحركه بنفسه
        (مفيدة جداً للمتجهات والرسوم التفاعلية).
        """
        self.glass.set_fill(opacity=0.0)
        self.glass.set_stroke(opacity=0.0)

        reveal_glass = _GlassIllumination(
            self.glass,
            target_fill_opacity=self.glass_glow_opacity if illuminate_glass else self.base_glass_opacity,
            target_border_opacity=self.glass_glow_border_opacity if illuminate_glass else self.base_glass_border_opacity,
            run_time=run_time * 0.45,
            rate_func=rate_func,
        )

        anims_step1 = [Create(self.body, run_time=run_time * 0.55)]
        if show_header and len(self.title_group) > 0:
            anims_step1.append(FadeIn(self.title_group, run_time=run_time * 0.55))
        if show_header and len(self.divider) > 0:
            anims_step1.append(Create(self.divider, run_time=run_time * 0.55))

        anims_step2 = [reveal_glass]
        if show_reflection:
            anims_step2.append(FadeIn(self.reflection, run_time=run_time * 0.45))

        return Succession(
            AnimationGroup(*anims_step1),
            AnimationGroup(*anims_step2),
        )

    def illuminate_glass(self, run_time=0.6, rate_func=smooth):
        """إشعال توهج الزجاج."""
        return _GlassIllumination(
            self.glass,
            target_fill_opacity=self.glass_glow_opacity,
            target_border_opacity=self.glass_glow_border_opacity,
            start_fill_opacity=self.base_glass_opacity,
            start_border_opacity=self.base_glass_border_opacity,
            run_time=run_time,
            rate_func=rate_func,
        )

    def dim_glass(self, run_time=0.5, rate_func=smooth):
        """إعادة الزجاج للشفافية الهادئة الأساسية."""
        return _GlassIllumination(
            self.glass,
            target_fill_opacity=self.base_glass_opacity,
            target_border_opacity=self.base_glass_border_opacity,
            start_fill_opacity=self.glass_glow_opacity,
            start_border_opacity=self.glass_glow_border_opacity,
            run_time=run_time,
            rate_func=rate_func,
        )

    # ==========================================================
    # خوارزمية التوهج والانعكاس المعتمدة لقناة MACH-MATH
    # ==========================================================

    @staticmethod
    def _make_floor_reflection(
        card,
        accent_color=GOLD_LIGHT,
        reflection_offset=0.22,
        reflection_opacity=0.30,
    ):
        glow_group = VGroup()
        w = card.width
        corner_radius = 0.22
        y_base = card.get_bottom()[1] - reflection_offset
        center_x = card.get_center()[0]

        # 1. طبقات التوهج الإهليلجي (10 طبقات)
        n_glow_layers = 10
        for i in range(n_glow_layers):
            t = i / (n_glow_layers - 1)
            w_layer = w * interpolate(0.85, 1.25, t)
            h_layer = 0.38 * interpolate(0.35, 1.45, t)
            op_layer = reflection_opacity * interpolate(0.65, 0.005, t ** 0.6)

            glow_ellipse = Ellipse(
                width=w_layer,
                height=h_layer,
                stroke_width=0,
                fill_color=GOLD_MUTED if t > 0.4 else accent_color,
                fill_opacity=op_layer,
            ).move_to([center_x, y_base - h_layer * 0.25, 0])
            glow_group.add(glow_ellipse)

        # 2. شرائح الانعكاس المنظوري الزجاجي (8 شرائح)
        reflection_h = 0.45
        p_top_l = np.array([center_x - w / 2 + corner_radius, card.get_bottom()[1], 0])
        p_top_r = np.array([center_x + w / 2 - corner_radius, card.get_bottom()[1], 0])
        p_bot_r = np.array([center_x + (w / 2 - corner_radius) * 1.05, card.get_bottom()[1] - reflection_h, 0])
        p_bot_l = np.array([center_x - (w / 2 - corner_radius) * 1.05, card.get_bottom()[1] - reflection_h, 0])

        n_refl_slices = 8
        for j in range(n_refl_slices):
            alpha_a = j / n_refl_slices
            alpha_b = (j + 1) / n_refl_slices
            pt_tl = interpolate(p_top_l, p_bot_l, alpha_a)
            pt_tr = interpolate(p_top_r, p_bot_r, alpha_a)
            pt_br = interpolate(p_top_r, p_bot_r, alpha_b)
            pt_bl = interpolate(p_top_l, p_bot_l, alpha_b)

            slice_op = reflection_opacity * 0.45 * ((1.0 - alpha_a) ** 1.8)
            refl_slice = Polygon(
                pt_tl, pt_tr, pt_br, pt_bl,
                stroke_width=0,
                fill_color=accent_color if alpha_a < 0.3 else GOLD_DARK,
                fill_opacity=slice_op,
            )
            glow_group.add(refl_slice)

        # 3. خط التلامس الأساسي
        contact_line = Line(
            p_top_l, p_top_r,
            color=accent_color,
            stroke_width=1.0,
            stroke_opacity=reflection_opacity * 0.8,
        )
        glow_group.add(contact_line)
        glow_group.set_z_index(-2)

        return glow_group