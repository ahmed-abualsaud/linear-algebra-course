"""الـ"هوية البصرية" المشتركة لقناة MACH-MATH.

نسخة نهائية شاملة ومضبوطة سينمائياً وزمنياً:
- النقطة الضوئية: تشتت سطحي فائق النعومة بـ 60 طبقة متدرجة بالمليمتر (60-Layer Optical Flare).
- متوافق 100% مع Manim v0.21.0 وبايثون 3.13.
- الإنترو: 7.0 ثوانٍ بالمليمتر.
- الأوترو: 5.0 ثوانٍ متناسقة مع جملة الختام.
- فريم موحد بتطابق تام في درجة ظهور الخطوط الداخلية والقطرية (0.18).
- فريم نيون ذهبي بتشتت سطحي هادئ وفخم.
- دوال turn_on_neon و turn_off_neon للتحكم في الإضاءة.
"""

from manim import *
import numpy as np

from .palette import (
    GOLD_BRIGHT,
    GOLD_LIGHT,
    GOLD,
    GOLD_DARK,
    GOLD_MUTED,
    IVORY_WHITE,
)

config.background_color = BLACK

OFF_SCREEN_TOP = UP * 4.5
FRAME_HALF_W, FRAME_HALF_H = 3.0, 1.7


def _get_luminous_point(location=ORIGIN):
    """بناء نقطة ضوئية سينمائية فائقة النعومة والتشتت بـ 60 طبقة متدرجة صريحة

    (60-Layer Optical Flare).

    تلاشٍ مستمر يذوب في السواد بدون أي حلقات أو حواف حادة، ومتوافق 100% مع أحدث
    إصدار مانيم.
    """
    glow_group = VGroup()

    # 60 طبقة ضبابية متدرجة بدقة فائقة من الأوسع والأخفت إلى الأقرب والأنصع
    halo_layers = [
        # ======================================================
        # 1. التشتت الجوي الأبعد (ATMOSPHERIC SCATTERING - 15 طبقة)
        # ======================================================
        {"radius": 1.40, "color": GOLD_MUTED, "opacity": 0.0010},
        {"radius": 1.35, "color": GOLD_MUTED, "opacity": 0.0014},
        {"radius": 1.30, "color": GOLD_MUTED, "opacity": 0.0019},
        {"radius": 1.25, "color": GOLD_MUTED, "opacity": 0.0025},
        {"radius": 1.20, "color": GOLD_MUTED, "opacity": 0.0032},
        {"radius": 1.15, "color": GOLD_MUTED, "opacity": 0.0040},
        {"radius": 1.10, "color": GOLD_MUTED, "opacity": 0.0049},
        {"radius": 1.05, "color": GOLD_MUTED, "opacity": 0.0059},
        {"radius": 1.00, "color": GOLD_MUTED, "opacity": 0.0070},
        {"radius": 0.95, "color": GOLD_MUTED, "opacity": 0.0082},
        {"radius": 0.90, "color": GOLD_MUTED, "opacity": 0.0096},
        {"radius": 0.86, "color": GOLD_MUTED, "opacity": 0.0112},
        {"radius": 0.82, "color": GOLD_MUTED, "opacity": 0.0130},
        {"radius": 0.78, "color": GOLD_MUTED, "opacity": 0.0150},
        {"radius": 0.75, "color": GOLD_MUTED, "opacity": 0.0172},
        # ======================================================
        # 2. الهالة الدافئة العميقة (MID WARM GLOW - 10 طبقات)
        # ======================================================
        {"radius": 0.72, "color": GOLD_DARK, "opacity": 0.0198},
        {"radius": 0.69, "color": GOLD_DARK, "opacity": 0.0226},
        {"radius": 0.66, "color": GOLD_DARK, "opacity": 0.0258},
        {"radius": 0.63, "color": GOLD_DARK, "opacity": 0.0294},
        {"radius": 0.60, "color": GOLD_DARK, "opacity": 0.0334},
        {"radius": 0.57, "color": GOLD_DARK, "opacity": 0.0378},
        {"radius": 0.54, "color": GOLD_DARK, "opacity": 0.0428},
        {"radius": 0.51, "color": GOLD_DARK, "opacity": 0.0484},
        {"radius": 0.48, "color": GOLD_DARK, "opacity": 0.0546},
        {"radius": 0.45, "color": GOLD_DARK, "opacity": 0.0615},
        # ======================================================
        # 3. الهالة الذهبية المتوهجة (GOLDEN RADIANCE - 8 طبقات)
        # ======================================================
        {"radius": 0.43, "color": GOLD, "opacity": 0.0680},
        {"radius": 0.41, "color": GOLD, "opacity": 0.0760},
        {"radius": 0.39, "color": GOLD, "opacity": 0.0850},
        {"radius": 0.37, "color": GOLD, "opacity": 0.0950},
        {"radius": 0.35, "color": GOLD, "opacity": 0.1060},
        {"radius": 0.33, "color": GOLD, "opacity": 0.1180},
        {"radius": 0.31, "color": GOLD, "opacity": 0.1310},
        {"radius": 0.29, "color": GOLD, "opacity": 0.1450},
        # ======================================================
        # 4. الهالة المنيرة القريبة (INNER BRIGHT CORONA - 12 طبقة)
        # ======================================================
        {"radius": 0.275, "color": GOLD_LIGHT, "opacity": 0.1600},
        {"radius": 0.260, "color": GOLD_LIGHT, "opacity": 0.1770},
        {"radius": 0.245, "color": GOLD_LIGHT, "opacity": 0.1950},
        {"radius": 0.230, "color": GOLD_LIGHT, "opacity": 0.2150},
        {"radius": 0.215, "color": GOLD_LIGHT, "opacity": 0.2370},
        {"radius": 0.200, "color": GOLD_LIGHT, "opacity": 0.2610},
        {"radius": 0.185, "color": GOLD_LIGHT, "opacity": 0.2870},
        {"radius": 0.170, "color": GOLD_LIGHT, "opacity": 0.3150},
        {"radius": 0.158, "color": GOLD_LIGHT, "opacity": 0.3450},
        {"radius": 0.146, "color": GOLD_LIGHT, "opacity": 0.3780},
        {"radius": 0.135, "color": GOLD_LIGHT, "opacity": 0.4130},
        {"radius": 0.125, "color": GOLD_LIGHT, "opacity": 0.4500},
        # ======================================================
        # 5. التوهج الشديد حول المركز (HOT SURROUND - 9 طبقات)
        # ======================================================
        {"radius": 0.115, "color": GOLD_BRIGHT, "opacity": 0.4900},
        {"radius": 0.105, "color": GOLD_BRIGHT, "opacity": 0.5350},
        {"radius": 0.096, "color": GOLD_BRIGHT, "opacity": 0.5850},
        {"radius": 0.088, "color": GOLD_BRIGHT, "opacity": 0.6400},
        {"radius": 0.080, "color": GOLD_BRIGHT, "opacity": 0.7000},
        {"radius": 0.073, "color": GOLD_BRIGHT, "opacity": 0.7600},
        {"radius": 0.066, "color": GOLD_BRIGHT, "opacity": 0.8200},
        {"radius": 0.060, "color": GOLD_BRIGHT, "opacity": 0.8750},
        {"radius": 0.054, "color": GOLD_BRIGHT, "opacity": 0.9200},
        # ======================================================
        # 6. البؤرة الحارقة النقية (WHITE HOT EMISSION - 6 طبقات)
        # ======================================================
        {"radius": 0.048, "color": "#FFFFFF", "opacity": 0.9400},
        {"radius": 0.043, "color": "#FFFFFF", "opacity": 0.9550},
        {"radius": 0.038, "color": "#FFFFFF", "opacity": 0.9700},
        {"radius": 0.033, "color": "#FFFFFF", "opacity": 0.9800},
        {"radius": 0.028, "color": "#FFFFFF", "opacity": 0.9900},
        {"radius": 0.024, "color": "#FFFFFF", "opacity": 0.9950},
    ]

    for layer in halo_layers:
        glow_group.add(
            Circle(
                radius=layer["radius"],
                stroke_width=0,
                fill_color=layer["color"],
                fill_opacity=layer["opacity"],
            ).move_to(location)
        )

    # النواة المركزية البيضاء الساطعة (Hot Point Core)
    core = Dot(location, radius=0.020, color="#FFFFFF")
    glow_group.add(core)

    return glow_group


def _get_falloff_radial_line(p_start, p_end, n_segments=50):
    """خطوط شعاعية ناعمة جداً بتلاشٍ خافت مستمر يخدم إضاءة النيون بهدوء."""
    segments_group = VGroup()
    points = [
        p_start + (p_end - p_start) * (i / n_segments)
        for i in range(n_segments + 1)
    ]

    for i in range(n_segments):
        t = i / n_segments

        if t < 0.35:
            falloff = 1.0 - (t * 0.15)
        else:
            falloff = 0.95 * ((1.0 - t) / 0.65) ** 1.35
        falloff = max(0.01, falloff)

        pt_a, pt_b = points[i], points[i + 1]

        bloom_w = interpolate(10.0, 1.0, t) * falloff
        bloom_op = interpolate(0.10, 0.008, t) * falloff
        if bloom_op > 0.001:
            segments_group.add(
                Line(
                    pt_a,
                    pt_b,
                    color=GOLD_LIGHT,
                    stroke_width=bloom_w,
                    stroke_opacity=bloom_op,
                    buff=0,
                )
            )

        core_w = interpolate(1.0, 0.35, t) * (falloff**0.4)
        core_op = interpolate(0.70, 0.08, t) * (falloff**0.3)
        if core_op > 0.003:
            segments_group.add(
                Line(
                    pt_a,
                    pt_b,
                    color="#FFFFFF" if t < 0.20 else GOLD_BRIGHT,
                    stroke_width=core_w,
                    stroke_opacity=core_op,
                    buff=0,
                )
            )

    return segments_group


def get_mach_frame(neon=False):
    """بناء الفريم الموحد:

    - neon=False : فريم هادئ متطابق في كل خطوطه الداخلية والقطرية.
    - neon=True  : نيون ذهبي بانتشار سطحي فخم ومحسوب.
    """
    inner = [
        np.array([-FRAME_HALF_W, FRAME_HALF_H, 0]),
        np.array([FRAME_HALF_W, FRAME_HALF_H, 0]),
        np.array([FRAME_HALF_W, -FRAME_HALF_H, 0]),
        np.array([-FRAME_HALF_W, -FRAME_HALF_H, 0]),
    ]
    outer = [
        (LEFT * config.frame_width / 2 + UP * config.frame_height / 2) * 1.02,
        (RIGHT * config.frame_width / 2 + UP * config.frame_height / 2) * 1.02,
        (RIGHT * config.frame_width / 2 + DOWN * config.frame_height / 2)
        * 1.02,
        (LEFT * config.frame_width / 2 + DOWN * config.frame_height / 2) * 1.02,
    ]

    if not neon:
        inner_edges = VGroup(
            *[
                Line(
                    inner[i],
                    inner[(i + 1) % 4],
                    color=GOLD_MUTED,
                    stroke_width=0.6,
                    stroke_opacity=0.18,
                )
                for i in range(4)
            ]
        )

        radial_lines = VGroup(
            *[
                Line(
                    inner[i],
                    outer[i],
                    color=GOLD_MUTED,
                    stroke_width=0.6,
                    stroke_opacity=0.18,
                )
                for i in range(4)
            ]
        )
        return VGroup(inner_edges, radial_lines)
    else:
        wall_top = Polygon(
            inner[0],
            outer[0],
            outer[1],
            inner[1],
            fill_color=GOLD_MUTED,
            fill_opacity=0.016,
            stroke_width=0,
        )
        wall_bottom = Polygon(
            inner[3],
            outer[3],
            outer[2],
            inner[2],
            fill_color=GOLD_MUTED,
            fill_opacity=0.016,
            stroke_width=0,
        )
        wall_right = Polygon(
            inner[1],
            outer[1],
            outer[2],
            inner[2],
            fill_color=GOLD_MUTED,
            fill_opacity=0.020,
            stroke_width=0,
        )
        wall_left = Polygon(
            inner[0],
            outer[0],
            outer[3],
            inner[3],
            fill_color=GOLD_MUTED,
            fill_opacity=0.020,
            stroke_width=0,
        )
        volumetric_walls = VGroup(wall_top, wall_bottom, wall_right, wall_left)

        diffusion_layers = [
            {"width": 320.0, "color": GOLD_MUTED, "opacity": 0.00010},
            {"width": 285.0, "color": GOLD_MUTED, "opacity": 0.00012},
            {"width": 255.0, "color": GOLD_MUTED, "opacity": 0.00014},
            {"width": 228.0, "color": GOLD_MUTED, "opacity": 0.00016},
            {"width": 205.0, "color": GOLD_MUTED, "opacity": 0.00018},
            {"width": 184.0, "color": GOLD_MUTED, "opacity": 0.00021},
            {"width": 165.0, "color": GOLD_MUTED, "opacity": 0.00024},
            {"width": 148.0, "color": GOLD_MUTED, "opacity": 0.00028},
            {"width": 133.0, "color": GOLD_MUTED, "opacity": 0.00032},
            {"width": 119.0, "color": GOLD_MUTED, "opacity": 0.00036},
            {"width": 107.0, "color": GOLD_MUTED, "opacity": 0.00041},
            {"width": 96.0, "color": GOLD_MUTED, "opacity": 0.00047},
            {"width": 86.0, "color": GOLD_MUTED, "opacity": 0.00054},
            {"width": 77.0, "color": GOLD_MUTED, "opacity": 0.00062},
            {"width": 69.0, "color": GOLD_MUTED, "opacity": 0.00071},
            {"width": 62.0, "color": GOLD_MUTED, "opacity": 0.00082},
            {"width": 56.0, "color": GOLD_MUTED, "opacity": 0.00094},
            {"width": 50.0, "color": GOLD_MUTED, "opacity": 0.00108},
            {"width": 45.0, "color": GOLD_MUTED, "opacity": 0.00124},
            {"width": 40.0, "color": GOLD_MUTED, "opacity": 0.00142},
            {"width": 36.0, "color": GOLD_MUTED, "opacity": 0.00162},
            {"width": 32.0, "color": GOLD_MUTED, "opacity": 0.00185},
            {"width": 28.0, "color": GOLD_MUTED, "opacity": 0.00212},
            {"width": 25.0, "color": GOLD_MUTED, "opacity": 0.00243},
            {"width": 22.0, "color": GOLD_MUTED, "opacity": 0.00278},
            {"width": 19.5, "color": GOLD_MUTED, "opacity": 0.00315},
            {"width": 17.0, "color": GOLD_MUTED, "opacity": 0.00355},
            {"width": 15.0, "color": GOLD_LIGHT, "opacity": 0.00400},
            {"width": 13.2, "color": GOLD_LIGHT, "opacity": 0.00455},
            {"width": 11.5, "color": GOLD_LIGHT, "opacity": 0.00515},
            {"width": 10.0, "color": GOLD_LIGHT, "opacity": 0.00580},
            {"width": 8.7, "color": GOLD_LIGHT, "opacity": 0.00650},
            {"width": 7.5, "color": GOLD_LIGHT, "opacity": 0.0080},
            {"width": 6.5, "color": GOLD_LIGHT, "opacity": 0.0110},
            {"width": 5.5, "color": GOLD_LIGHT, "opacity": 0.0150},
            {"width": 5.0, "color": GOLD_LIGHT, "opacity": 0.180},
            {"width": 2.2, "color": GOLD_BRIGHT, "opacity": 0.380},
            {"width": 1.1, "color": "#FFFFFF", "opacity": 0.650},
            {"width": 0.6, "color": "#FFFFFF", "opacity": 0.850},
        ]

        frame_rect_layers = VGroup()
        for layer in diffusion_layers:
            layer_edges = VGroup(
                *[
                    Line(
                        inner[i],
                        inner[(i + 1) % 4],
                        color=layer["color"],
                        stroke_width=layer["width"],
                        stroke_opacity=layer["opacity"],
                    )
                    for i in range(4)
                ]
            )
            frame_rect_layers.add(layer_edges)

        corner_halos = VGroup()
        for pt in inner:
            corner_glow = VGroup(
                Dot(pt, radius=0.55, color=GOLD_MUTED, fill_opacity=0.006),
                Dot(pt, radius=0.32, color=GOLD_MUTED, fill_opacity=0.010),
                Dot(pt, radius=0.18, color=GOLD_LIGHT, fill_opacity=0.022),
                Dot(pt, radius=0.08, color=GOLD_BRIGHT, fill_opacity=0.090),
                Dot(pt, radius=0.015, color="#FFFFFF", fill_opacity=0.50),
            )
            corner_halos.add(corner_glow)

        radial_falloff_group = VGroup(
            *[
                _get_falloff_radial_line(inner[i], outer[i], n_segments=50)
                for i in range(4)
            ]
        )

        return VGroup(
            volumetric_walls,
            frame_rect_layers,
            radial_falloff_group,
            corner_halos,
        )


def turn_on_neon(scene, run_time=0.9):
    """إشعال فريم النيون بانسيابية مع منح الهالة مدى للانتشار."""
    neon_glow = get_mach_frame(neon=True).set_z_index(15)
    scene.neon_overlay = neon_glow

    scene.play(
        FadeIn(neon_glow, rate_func=rate_functions.ease_out_quad),
        run_time=run_time,
    )


def turn_off_neon(scene, run_time=0.8):
    """إطفاء النيون بسلاسة مع التلاشي التدريجي المريح للعين."""
    if hasattr(scene, "neon_overlay") and scene.neon_overlay is not None:
        scene.play(
            FadeOut(scene.neon_overlay, rate_func=rate_functions.ease_in_sine),
            run_time=run_time,
        )
        scene.remove(scene.neon_overlay)
        scene.neon_overlay = None


# ==============================================================
# 1. INTRO SCENE (المدة المحسوبة بالضبط: 7.0 ثوانٍ)
# ==============================================================
class IntroScene(Scene):

    def construct(self):
        # بناء النقطة الضوئية فائقة النعومة بـ 60 طبقة
        point = _get_luminous_point(OFF_SCREEN_TOP)

        # 1. نزول النقطة الذهبية المتوهجة بنعومة (0.9s)
        self.play(
            point.animate.move_to(ORIGIN),
            run_time=0.9,
            rate_func=rate_functions.ease_out_cubic,
        )

        # 2. تفرع الفريم الهادئ من النقطة (0.8s)
        self.frame = get_mach_frame(neon=False)
        self.play(
            GrowFromPoint(self.frame, ORIGIN),
            run_time=0.8,
            rate_func=rate_functions.ease_out_cubic,
        )

        font_kwargs = {"font": "Serif", "weight": BOLD, "font_size": 46}

        ma_part = Text("MA", **font_kwargs)
        c_letter = Text("C", **font_kwargs)
        h_letter = Text("H", **font_kwargs)
        mach_word = (
            VGroup(ma_part, c_letter, h_letter)
            .arrange(RIGHT, buff=0.04)
            .move_to(ORIGIN)
        )
        mach_word.set_color_by_gradient(GOLD_BRIGHT, GOLD_LIGHT, GOLD_DARK)

        # 3. ظهور كلمة MACH وتلاشي النقطة الضوئية (0.6s)
        self.play(
            FadeIn(mach_word, scale=0.1),
            FadeOut(point, scale=0.1),
            run_time=0.6,
        )
        # 4. وقفة خفيفة للمشاهد (0.5s)
        self.wait(0.5)

        t_letter = Text("T", **font_kwargs).move_to(c_letter.get_center())
        t_letter.set_color_by_gradient(GOLD_BRIGHT, GOLD_LIGHT)
        t_letter.shift(UP * 0.6).set_opacity(0)

        # 5. تحول C إلى T لتكوين MATH (0.8s)
        self.play(
            c_letter.animate.shift(DOWN * 0.6).set_opacity(0),
            t_letter.animate.shift(DOWN * 0.6).set_opacity(1),
            run_time=0.8,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.remove(c_letter)
        math_word = VGroup(ma_part, t_letter, h_letter)

        # 6. وقفة إدراك للمشاهد (0.5s)
        self.wait(0.5)

        left_mach = Text("MACH", **font_kwargs).set_color_by_gradient(
            GOLD_BRIGHT, GOLD_LIGHT, GOLD_DARK
        )
        dash_char = Text("-", **font_kwargs).set_color_by_gradient(
            GOLD_BRIGHT, GOLD_LIGHT
        )

        full_logo_target = (
            VGroup(left_mach, dash_char, math_word.copy())
            .arrange(RIGHT, buff=0.12)
            .move_to(ORIGIN)
        )

        target_math_pos = full_logo_target[2].get_center()
        target_dash_pos = full_logo_target[1].get_center()
        target_mach_pos = full_logo_target[0].get_center()

        dash_char.move_to(target_dash_pos)
        left_mach.move_to(target_mach_pos)

        # 7. اكتمال الشعار MACH-MATH (1.0s)
        self.play(
            math_word.animate.move_to(target_math_pos),
            FadeIn(left_mach, shift=RIGHT * 0.5),
            FadeIn(dash_char, scale=0.5),
            run_time=1.0,
            rate_func=rate_functions.ease_in_out_sine,
        )

        complete_logo = VGroup(left_mach, dash_char, math_word)

        # 8. استعراض الشعار بكامل فخامته (1.2s)
        self.wait(1.2)

        # 9. تلاشي الشعار للانتقال للمشهد الأول (0.7s)
        self.play(FadeOut(complete_logo, scale=1.2), run_time=0.7)


# ==============================================================
# 2. BASE CONTENT SCENE
# ==============================================================
class MachMathScene(Scene):

    def setup(self):
        super().setup()
        self.frame = get_mach_frame(neon=False)
        self.add(self.frame)


# ==============================================================
# 3. OUTRO SCENE (المدة المحسوبة بالضبط: 5.0 ثوانٍ)
# ==============================================================
class OutroScene(Scene):

    def construct(self):
        # بناء النقطة الضوئية فائقة النعومة بـ 60 طبقة في المركز
        point = _get_luminous_point(ORIGIN)

        existing_mobjects = Group(*self.mobjects)

        # 1. ظهور النقطة الضوئية المتوهجة في المركز كبؤرة جذب (0.6s)
        self.play(FadeIn(point, scale=0.2), run_time=0.6)

        # 2. ابتلاع كافة محتويات الشاشة إلى داخل النقطة (1.4s)
        self.play(
            FadeOut(existing_mobjects, scale=0.01, target_position=ORIGIN),
            run_time=1.4,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.clear()
        self.add(point)

        # 3. وقفة صامتة تتناغم مع جملة: "سلام عليكم" (0.8s)
        self.wait(0.8)

        # 4. انطلاق النقطة الضوئية للأعلى واختفائها في الفضاء (1.4s)
        self.play(
            point.animate.move_to(OFF_SCREEN_TOP),
            run_time=1.4,
            rate_func=rate_functions.ease_in_quad,
        )

        # 5. استقرار أخير للشاشة السوداء (0.8s)
        self.wait(0.8)