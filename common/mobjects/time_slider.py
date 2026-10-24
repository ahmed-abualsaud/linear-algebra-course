"""
common/mobjects/time_slider.py
شريط زمن (Time Slider) احترافي لقناة MACH-MATH.

- مسار بتدرج لوني (ذهبي → نحاسي) يمتلئ تدريجياً مع تقدم الزمن.
- تدريج من 0 إلى t_max: علامات رئيسية (كل وحدة) وفرعية (كل نصف وحدة) وأرقام تضيء بعد تجاوزها.
- مقبض متوهج يتحرك مع القيمة، وهالة تنبض أثناء الحركة وتهدأ عند التوقف.
- مصمم كـ HUD: يُسجَّل ثابتاً أمام الكاميرا في المشاهد ثلاثية الأبعاد (register_hud).

الاستخدام:
    slider = MachTimeSlider(center=[4.3, 0.7, 0], width=3.9, t_max=10)
    slider.register_hud(scene)                 # مرة واحدة (ThreeDScene)
    scene.play(FadeIn(slider))
    slider.attach(lambda: current_time)        # يتبع أي قيمة حيّة
    ...
    slider.detach()                            # عند الانتهاء
    scene.play(slider.finish_animation())      # وميض عند الوصول للنهاية
"""
from manim import *
import numpy as np

from common.palette import (
    GOLD_BRIGHT,
    GOLD_LIGHT,
    GOLD_MUTED,
    COPPER_TERRA,
    IVORY_WHITE,
    STONE_AXIS,
)


class MachTimeSlider(VGroup):
    def __init__(
        self,
        center=(0, 0, 0),
        width=4.0,
        t_max=10,
        start_color=GOLD_BRIGHT,
        end_color=COPPER_TERRA,
        segments=64,
        track_width=6.0,
        dim_opacity=0.20,
        show_numbers=True,
        number_every=1,
        number_font_size=15,
        show_minor_ticks=True,
        knob_radius=0.13,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.center_pt = np.array(center, dtype=float)
        self.width_ = float(width)
        self.t_max = float(t_max)
        self.segments = int(segments)
        self.dim_opacity = dim_opacity
        self.start_color, self.end_color = start_color, end_color
        self._value = 0.0
        self._lit = -1
        self._pulse = 0.0
        self._last_value = 0.0
        self._getter = None
        self._clock = 0.0

        self.x0 = self.center_pt[0] - self.width_ / 2
        self.y0 = self.center_pt[1]
        self.z0 = self.center_pt[2]

        # --- المسار الخلفي الخافت ---
        self.base = Line(
            [self.x0, self.y0, self.z0], [self.x0 + self.width_, self.y0, self.z0],
            color=GOLD_MUTED, stroke_width=track_width + 4, stroke_opacity=0.18,
        )
        self.base.set_cap_style(CapStyleType.ROUND)

        # --- مقاطع التدرج اللوني (تضيء تدريجياً) ---
        self.segs = VGroup()
        for i in range(self.segments):
            a = self.x0 + self.width_ * i / self.segments
            b = self.x0 + self.width_ * (i + 1) / self.segments
            col = interpolate_color(ManimColor(start_color), ManimColor(end_color), i / max(1, self.segments - 1))
            seg = Line([a, self.y0, self.z0], [b + 0.004, self.y0, self.z0],
                       color=col, stroke_width=track_width, stroke_opacity=dim_opacity)
            seg.set_cap_style(CapStyleType.BUTT)
            self.segs.add(seg)

        # --- التدريج ---
        self.ticks = VGroup()
        self.numbers = VGroup()
        n_major = int(round(self.t_max))
        for k in range(n_major + 1):
            x = self.x0 + self.width_ * k / n_major
            self.ticks.add(Line([x, self.y0 - 0.10, self.z0], [x, self.y0 - 0.26, self.z0],
                                color=STONE_AXIS, stroke_width=1.8, stroke_opacity=0.85))
            if show_numbers and (k % number_every == 0):
                n = MathTex(str(k), font_size=number_font_size, color=STONE_AXIS)
                n.move_to([x, self.y0 - 0.46, self.z0])
                self.numbers.add(n)
            if show_minor_ticks and k < n_major:
                xm = x + self.width_ / n_major / 2
                self.ticks.add(Line([xm, self.y0 - 0.10, self.z0], [xm, self.y0 - 0.18, self.z0],
                                    color=STONE_AXIS, stroke_width=1.2, stroke_opacity=0.5))

        # --- المقبض ---
        self.halo_outer = Circle(radius=knob_radius * 2.6, stroke_width=0,
                                 fill_color=GOLD_LIGHT, fill_opacity=0.08)
        self.halo_inner = Circle(radius=knob_radius * 1.7, stroke_width=0,
                                 fill_color=GOLD_LIGHT, fill_opacity=0.16)
        self.knob = Circle(radius=knob_radius, stroke_width=2.6, stroke_color=COPPER_TERRA,
                           fill_color=IVORY_WHITE, fill_opacity=1.0)
        self.knob_core = Dot(radius=knob_radius * 0.38, color=COPPER_TERRA)
        self.knob_group = VGroup(self.halo_outer, self.halo_inner, self.knob, self.knob_core)

        self.add(self.base, self.segs, self.ticks, self.numbers, self.knob_group)
        self.set_time(0.0)

    # ------------------------------------------------------------------
    def _x_of(self, t):
        return self.x0 + self.width_ * float(np.clip(t / self.t_max, 0.0, 1.0))

    def set_time(self, t):
        """يضع المقبض والتدرج عند الزمن t (دالة نقية، آمنة للاستدعاء في أي updater)."""
        t = float(np.clip(t, 0.0, self.t_max))
        self._value = t
        x = self._x_of(t)
        self.knob_group.move_to([x, self.y0, self.z0])

        lit = int(np.floor(t / self.t_max * self.segments + 1e-6))
        if lit != self._lit:
            for i, seg in enumerate(self.segs):
                seg.set_stroke(opacity=1.0 if i < lit else self.dim_opacity)
            self._lit = lit

        # الأرقام والعلامات التي تجاوزها المقبض تضيء
        n_major = int(round(self.t_max))
        step = self.t_max / n_major
        for k, num in enumerate(self.numbers):
            passed = (k * step) <= t + 1e-6
            num.set_color(IVORY_WHITE if passed else STONE_AXIS)
        return self

    # ------------------------------------------------------------------
    def attach(self, getter):
        """يتبع getter() (قيمة الزمن الحيّة). يضيف updater واحداً."""
        self._getter = getter
        self._last_value = float(getter())

        def _upd(m, dt):
            v = float(m._getter())
            speed = abs(v - m._last_value) / max(dt, 1e-3)
            m._last_value = v
            m._clock += dt
            m.set_time(v)
            # هالة تنبض أثناء الحركة وتهدأ عند التوقف
            target = float(np.clip(speed / 2.0, 0.0, 1.0))
            m._pulse += (target - m._pulse) * min(1.0, dt * 6)
            flicker = 0.5 + 0.5 * np.sin(m._clock * 9)
            m.halo_outer.set_fill(opacity=0.05 + m._pulse * (0.07 + 0.05 * flicker))
            m.halo_inner.set_fill(opacity=0.10 + m._pulse * (0.10 + 0.05 * flicker))

        self.add_updater(_upd)
        return self

    def detach(self):
        self.clear_updaters()
        self._getter = None
        return self

    def finish_animation(self):
        """وميض خفيف للمقبض عند الوصول لنهاية الشريط."""
        return Indicate(self.knob_group, scale_factor=1.35, color=GOLD_BRIGHT, run_time=0.7)

    def register_hud(self, scene):
        """يثبّت الشريط على الشاشة في المشاهد ثلاثية الأبعاد (HUD)."""
        if isinstance(scene, ThreeDScene):
            scene.renderer.camera.add_fixed_in_frame_mobjects(self)
        return self