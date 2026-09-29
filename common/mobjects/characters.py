"""
MACH-MATH Avatar v2
الشخصية الرسمية للقناة: هندسية، مضاءة بالذهب، وتحمل "النقطة" (POINT) في صدرها.

الاستخدام:

    person = mach_stick_figure(
        color=STONE_AXIS,
        pose="thinking",
        scale=0.9,
        blink=True,
    )

    person[0]          # الرأس (نفس الفهرس القديم، للبالونات)
    person.blink()     # بربشة يدوية عند الحاجة
    person.breathe()   # تنفس يدوي عند الحاجة

البربشة التلقائية:

    blink=True         # البربشة تعمل تلقائيًا
    blink=False        # بدون بربشة

البربشة التلقائية تعمل عن طريق updater داخلي،
وبالتالي تستمر بالتوازي مع باقي الـanimations.

التنفس:

    التنفس يتم عن طريق updater مستقل.
    الشخصية تطول وتقصر رأسيًا فقط،
    مع تثبيت القدمين وعدم تغيير العرض.
"""

from manim import *
import numpy as np

from common.palette import GOLD_LIGHT, GOLD_BRIGHT, STONE_AXIS


# ---------------------------------------------------------------
# Global style
# ---------------------------------------------------------------

DARK = "#15120D"

MAIN_W = 2.4
FINE_W = 1.1

POSES = (
    "neutral",
    "thinking",
    "explaining",
)


# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------

def _seg(a, b, color, width=MAIN_W, opacity=1.0):
    return Line(
        a,
        b,
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
        buff=0,
    )


def _joint(p, accent, r=0.028):
    """مفصل: نقطة ذهبية صغيرة + هالة خافتة."""

    halo = Circle(
        radius=r * 2.2,
        stroke_width=0,
        fill_color=accent,
        fill_opacity=0.16,
    ).move_to(p)

    return VGroup(
        halo,
        Dot(
            p,
            radius=r,
            color=accent,
        ),
    )


def _hand(p, outline, r=0.05):
    return Circle(
        radius=r,
        color=outline,
        stroke_width=2.0,
        fill_color=DARK,
        fill_opacity=1.0,
    ).move_to(p)


def _limb(shoulder, elbow, hand, outline, accent):
    return VGroup(
        _seg(
            shoulder,
            elbow,
            outline,
        ),
        _seg(
            elbow,
            hand,
            outline,
        ),
        _joint(
            elbow,
            accent,
        ),
        _hand(
            hand,
            outline,
        ),
    )


def _rim(
    shape,
    accent,
    offset=LEFT * 0.08 + DOWN * 0.02,
    opacity=0.22,
):
    """هلال إضاءة على الحافة."""

    return Difference(
        shape.copy().set_stroke(width=0),
        shape.copy().shift(offset),
        stroke_width=0,
        fill_color=accent,
        fill_opacity=opacity,
    )


# ---------------------------------------------------------------
# Avatar
# ---------------------------------------------------------------

class MachAvatar(VGroup):

    def __init__(
        self,
        color=STONE_AXIS,
        accent_color=GOLD_LIGHT,
        pose="neutral",
        size=1.0,
        eyes=True,
        look=ORIGIN,
        ground_glow=True,

        # -------------------------------------------------------
        # Automatic blinking
        # -------------------------------------------------------

        blink=True,

        # -------------------------------------------------------
        # Automatic breathing
        # -------------------------------------------------------

        breathing=True,

        **kwargs,
    ):

        super().__init__(**kwargs)

        if pose not in POSES:
            raise ValueError(
                f"Unknown pose '{pose}'. "
                f"Expected one of {POSES}."
            )

        outline = color
        accent = accent_color

        # -------------------------------------------------------
        # Head
        # -------------------------------------------------------

        shell = Circle(
            radius=0.365,
            color=outline,
            stroke_width=MAIN_W,
            fill_color=DARK,
            fill_opacity=1.0,
        ).stretch(
            1.08,
            dim=0,
        )

        glow = Circle(
            radius=0.405,
            stroke_width=0,
            fill_color=accent,
            fill_opacity=0.03,
        ).move_to(
            shell.get_center()
        )

        rim = _rim(
            shell,
            accent,
            opacity=0.20,
        )

        glass = Arc(
            radius=0.285,
            start_angle=PI * 0.08,
            angle=PI * 0.55,
            arc_center=shell.get_center(),
            color=accent,
            stroke_width=1.5,
            stroke_opacity=0.55,
        )

        # -------------------------------------------------------
        # Eyes
        # -------------------------------------------------------

        eye_l = self._eye(
            LEFT * 0.115 + UP * 0.03,
            accent,
        )

        eye_r = self._eye(
            RIGHT * 0.115 + UP * 0.03,
            accent,
        )

        self.eyes = VGroup(
            eye_l,
            eye_r,
        )

        self.eyes.shift(
            look * 0.04
        )

        self._eyes_enabled = eyes

        if not eyes:
            self.eyes.set_opacity(0)

        head = VGroup(
            glow,
            shell,
            rim,
            glass,
            self.eyes,
        )

        if pose == "thinking":
            head.rotate(
                8 * DEGREES,
                about_point=shell.get_center(),
            )

        self.head = head

        # -------------------------------------------------------
        # Neck + torso
        # -------------------------------------------------------

        neck_top = shell.get_bottom()

        neck_bottom = (
            neck_top
            + DOWN * 0.13
        )

        neck = _seg(
            neck_top,
            neck_bottom,
            outline,
        )

        top = neck_bottom

        H = 0.92

        sl = (
            top
            + LEFT * 0.38
            + DOWN * 0.05
        )

        sr = (
            top
            + RIGHT * 0.38
            + DOWN * 0.05
        )

        wl = (
            top
            + DOWN * H
            + LEFT * 0.27
        )

        wr = (
            top
            + DOWN * H
            + RIGHT * 0.27
        )

        torso = Polygon(
            sl,
            sr,
            wr,
            wl,
            color=outline,
            stroke_width=MAIN_W,
            fill_color=DARK,
            fill_opacity=1.0,
        )

        torso_rim = _rim(
            torso,
            accent,
            offset=LEFT * 0.10,
            opacity=0.16,
        )

        # -------------------------------------------------------
        # POINT
        # -------------------------------------------------------

        core_p = (
            top
            + DOWN * 0.36
        )

        core = VGroup(
            Circle(
                radius=0.13,
                stroke_width=0,
                fill_color=accent,
                fill_opacity=0.07,
            ).move_to(core_p),

            Circle(
                radius=0.075,
                stroke_width=0.8,
                color=accent,
                stroke_opacity=0.45,
                fill_color=accent,
                fill_opacity=0.10,
            ).move_to(core_p),

            Dot(
                core_p,
                radius=0.03,
                color=GOLD_BRIGHT,
            ),
        )

        axis = _seg(
            top + DOWN * 0.50,
            top + DOWN * (H - 0.10),
            accent,
            FINE_W,
            0.25,
        )

        shoulder_line = ArcBetweenPoints(
            sl + RIGHT * 0.04,
            sr + LEFT * 0.04,
            angle=-PI * 0.10,
            color=outline,
            stroke_width=1.0,
            stroke_opacity=0.45,
        )

        shoulders = VGroup(
            _joint(
                sl,
                accent,
                0.024,
            ),
            _joint(
                sr,
                accent,
                0.024,
            ),
        )

        # -------------------------------------------------------
        # Arms
        # -------------------------------------------------------

        if pose == "neutral":

            el = (
                sl
                + LEFT * 0.15
                + DOWN * 0.42
            )

            er = (
                sr
                + RIGHT * 0.15
                + DOWN * 0.42
            )

            arm_l = _limb(
                sl,
                el,
                el + LEFT * 0.05 + DOWN * 0.42,
                outline,
                accent,
            )

            arm_r = _limb(
                sr,
                er,
                er + RIGHT * 0.05 + DOWN * 0.42,
                outline,
                accent,
            )

        elif pose == "thinking":

            er = (
                sr
                + RIGHT * 0.06
                + DOWN * 0.44
            )

            arm_r = _limb(
                sr,
                er,
                er + LEFT * 0.70 + UP * 0.02,
                outline,
                accent,
            )

            el = (
                sl
                + LEFT * 0.06
                + DOWN * 0.44
            )

            chin = (
                shell.get_bottom()
                + LEFT * 0.10
                + DOWN * 0.03
            )

            arm_l = _limb(
                sl,
                el,
                chin,
                outline,
                accent,
            )

        else:

            el = (
                sl
                + LEFT * 0.15
                + DOWN * 0.42
            )

            arm_l = _limb(
                sl,
                el,
                el + LEFT * 0.05 + DOWN * 0.42,
                outline,
                accent,
            )

            er = (
                sr
                + RIGHT * 0.26
                + DOWN * 0.30
            )

            arm_r = _limb(
                sr,
                er,
                er + RIGHT * 0.14 + UP * 0.36,
                outline,
                accent,
            )

        arms = VGroup(
            arm_l,
            arm_r,
        )

        # -------------------------------------------------------
        # Pelvis + legs
        # -------------------------------------------------------

        pl = (
            wl
            + DOWN * 0.15
            + RIGHT * 0.05
        )

        pr = (
            wr
            + DOWN * 0.15
            + LEFT * 0.05
        )

        pelvis = Polygon(
            wl,
            wr,
            pr,
            pl,
            color=outline,
            stroke_width=MAIN_W,
            fill_color=DARK,
            fill_opacity=1.0,
        )

        hl = (
            pl
            + RIGHT * 0.09
        )

        hr = (
            pr
            + LEFT * 0.09
        )

        kl = (
            hl
            + LEFT * 0.07
            + DOWN * 0.42
        )

        kr = (
            hr
            + RIGHT * 0.07
            + DOWN * 0.42
        )

        fl = (
            kl
            + LEFT * 0.05
            + DOWN * 0.42
        )

        fr = (
            kr
            + RIGHT * 0.05
            + DOWN * 0.42
        )

        legs = VGroup(

            VGroup(
                _seg(
                    hl,
                    kl,
                    outline,
                ),
                _seg(
                    kl,
                    fl,
                    outline,
                ),
                _joint(
                    kl,
                    accent,
                ),
            ),

            VGroup(
                _seg(
                    hr,
                    kr,
                    outline,
                ),
                _seg(
                    kr,
                    fr,
                    outline,
                ),
                _joint(
                    kr,
                    accent,
                ),
            ),

            _joint(
                hl,
                accent,
                0.024,
            ),

            _joint(
                hr,
                accent,
                0.024,
            ),
        )

        feet = VGroup(

            Ellipse(
                width=0.17,
                height=0.06,
                color=outline,
                stroke_width=2.0,
                fill_color=DARK,
                fill_opacity=1,
            ).move_to(
                fl
                + LEFT * 0.05
                + DOWN * 0.01
            ),

            Ellipse(
                width=0.17,
                height=0.06,
                color=outline,
                stroke_width=2.0,
                fill_color=DARK,
                fill_opacity=1,
            ).move_to(
                fr
                + RIGHT * 0.05
                + DOWN * 0.01
            ),
        )

        # -------------------------------------------------------
        # Ground glow
        # -------------------------------------------------------

        floor_y = fl[1] - 0.03

        floor = VGroup(*[
            Ellipse(
                width=w,
                height=h,
                stroke_width=0,
                fill_color=accent,
                fill_opacity=o,
            ).move_to(
                np.array([
                    0,
                    floor_y,
                    0,
                ])
            )
            for w, h, o in (
                (1.15, 0.17, 0.04),
                (0.80, 0.12, 0.06),
                (0.48, 0.07, 0.09),
            )
        ])

        floor.set_z_index(-1)

        if not ground_glow:
            floor.set_opacity(0)

        self.floor = floor

        self.feet_point = np.array([
            0,
            fl[1],
            0,
        ])

        # -------------------------------------------------------
        # Main hierarchy
        # -------------------------------------------------------

        self.add(
            head,
            neck,
            torso,
            torso_rim,
            core,
            axis,
            shoulder_line,
            shoulders,
            pelvis,
            legs,
            arms,
            feet,
            floor,
        )

        self.scale(size)

        self.feet_point = (
            self.feet_point
            * size
        )

        # -------------------------------------------------------
        # Automatic blink state
        # -------------------------------------------------------

        self._blink_enabled = (
            blink
            and eyes
        )

        # 1.0 = مفتوحة
        # 0.08 = شبه مغلقة

        self._blink_factor = 1.0

        self._blink_timer = 0.0

        self._next_blink_delay = np.random.uniform(
            0.8,
            2.2,
        )

        self._blink_close_duration = 0.055
        self._blink_open_duration = 0.105

        # -------------------------------------------------------
        # Automatic breathing state
        # -------------------------------------------------------

        self._breathing_enabled = breathing

        # مقدار التمدد الرأسي الأقصى
        self._breathing_amount = 0.012

        # زمن دورة كاملة:
        # شهيق + زفير

        self._breathing_period = 2.6

        self._breathing_timer = 0.0

        # عامل التمدد الحالي
        self._breathing_factor = 1.0

        # -------------------------------------------------------
        # Install updaters
        # -------------------------------------------------------

        if self._blink_enabled:
            self.add_updater(
                self._blink_updater
            )

        if self._breathing_enabled:
            self.add_updater(
                self._breathing_updater
            )

    # -----------------------------------------------------------
    # Eye
    # -----------------------------------------------------------

    @staticmethod
    def _eye(pos, accent):

        return VGroup(

            Circle(
                radius=0.07,
                stroke_width=0,
                fill_color=accent,
                fill_opacity=0.12,
            ).move_to(pos),

            RoundedRectangle(
                corner_radius=0.02,
                width=0.04,
                height=0.10,
                stroke_width=0,
                fill_color=GOLD_BRIGHT,
                fill_opacity=1,
            ).move_to(pos),
        )

    # -----------------------------------------------------------
    # Automatic blink updater
    # -----------------------------------------------------------

    def _blink_updater(self, mob, dt):

        if not self._blink_enabled:
            return

        if not self._eyes_enabled:
            return

        self._blink_timer += dt

        if self._blink_timer < self._next_blink_delay:
            return

        total_duration = (
            self._blink_close_duration
            + self._blink_open_duration
        )

        t = (
            self._blink_timer
            - self._next_blink_delay
        )

        if t < self._blink_close_duration:

            alpha = (
                t
                / self._blink_close_duration
            )

            alpha = smooth(alpha)

            target_factor = interpolate(
                1.0,
                0.08,
                alpha,
            )

        elif t < total_duration:

            alpha = (
                t
                - self._blink_close_duration
            ) / self._blink_open_duration

            alpha = smooth(alpha)

            target_factor = interpolate(
                0.08,
                1.0,
                alpha,
            )

        else:

            target_factor = 1.0

            self._blink_timer = 0.0

            self._next_blink_delay = np.random.uniform(
                2.0,
                4.2,
            )

        if not np.isclose(
            self._blink_factor,
            target_factor,
        ):

            ratio = (
                target_factor
                / self._blink_factor
            )

            for eye in self.eyes:

                eye.stretch(
                    ratio,
                    dim=1,
                    about_point=eye.get_center(),
                )

            self._blink_factor = target_factor

    # -----------------------------------------------------------
    # Automatic breathing updater
    # -----------------------------------------------------------

    def _breathing_updater(self, mob, dt):

        if not self._breathing_enabled:
            return

        self._breathing_timer += dt

        # -------------------------------------------------------
        # دورة مستمرة:
        #
        # 0.00 -> 0.50 : شهيق
        # 0.50 -> 1.00 : زفير
        # -------------------------------------------------------

        phase = (
            self._breathing_timer
            / self._breathing_period
        ) % 1.0

        # sin يبدأ من 0:
        #
        # 0       = طبيعي
        # 0.25    = أقصى شهيق
        # 0.50    = طبيعي
        # 0.75    = أقصى انكماش
        # 1.00    = طبيعي
        #
        # استخدمنا مقدارًا صغيرًا جدًا حتى يكون
        # التنفس subtle وليس cartoonish.

        target_factor = (
            1.0
            + self._breathing_amount
            * np.sin(
                TAU * phase
            )
        )

        if np.isclose(
            self._breathing_factor,
            target_factor,
        ):
            return

        ratio = (
            target_factor
            / self._breathing_factor
        )

        # -------------------------------------------------------
        # Stretch رأسي فقط.
        #
        # get_bottom() يحافظ على القدمين في مكانهما.
        # -------------------------------------------------------

        self.stretch(
            ratio,
            dim=1,
            about_point=self.get_bottom(),
        )

        self._breathing_factor = target_factor

    # -----------------------------------------------------------
    # Manual blink
    # -----------------------------------------------------------

    def blink(self, run_time=0.24):

        return ApplyMethod(
            self.eyes.stretch,
            0.08,
            1,
            rate_func=there_and_back,
            run_time=run_time,
        )

    # -----------------------------------------------------------
    # Manual breathing
    # -----------------------------------------------------------

    def breathe(
        self,
        amount=0.012,
        run_time=2.6,
    ):

        return (
            self.animate.stretch(
                1 + amount,
                dim=1,
                about_point=self.get_bottom(),
            )
            .set_rate_func(there_and_back)
            .set_run_time(run_time)
        )

    # -----------------------------------------------------------
    # Breathing control
    # -----------------------------------------------------------

    def start_breathing(self):

        self._breathing_enabled = True

    def stop_breathing(self):

        self._breathing_enabled = False

        if not np.isclose(
            self._breathing_factor,
            1.0,
        ):

            ratio = (
                1.0
                / self._breathing_factor
            )

            self.stretch(
                ratio,
                dim=1,
                about_point=self.get_bottom(),
            )

            self._breathing_factor = 1.0

    def set_breathing(self, enabled=True):

        if enabled:
            self.start_breathing()
        else:
            self.stop_breathing()

    # -----------------------------------------------------------
    # Blink control
    # -----------------------------------------------------------

    def start_blinking(self):

        self._blink_enabled = (
            self._eyes_enabled
        )

        if self._blink_enabled:

            if self._blink_updater not in self.updaters:
                self.add_updater(
                    self._blink_updater
                )

    def stop_blinking(self):

        self._blink_enabled = False

        if not np.isclose(
            self._blink_factor,
            1.0,
        ):

            ratio = (
                1.0
                / self._blink_factor
            )

            for eye in self.eyes:

                eye.stretch(
                    ratio,
                    dim=1,
                    about_point=eye.get_center(),
                )

            self._blink_factor = 1.0

    def set_blinking(self, enabled=True):

        if enabled:
            self.start_blinking()
        else:
            self.stop_blinking()


# ---------------------------------------------------------------
# Public factory
# ---------------------------------------------------------------

def mach_stick_figure(
    color=STONE_AXIS,
    accent_color=GOLD_LIGHT,
    pose="neutral",
    scale=1.0,
    **kwargs,
):

    return MachAvatar(
        color=color,
        accent_color=accent_color,
        pose=pose,
        size=scale,
        **kwargs,
    )