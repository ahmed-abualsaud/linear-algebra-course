"""
الـ"هوية البصرية" المشتركة لقناة MACH-MATH.
نسخة نهائية شاملة:
- فريم نيون ذهبي بتشتت سطحي حقيقي يفرش في الفضاء (Planar Volumetric Glow).
- تدرج ضوئي ممتد وانسيابي بدون أي فقع ضوئي أو حواف صلبة.
- دوال turn_on_neon و turn_off_neon للتحكم في الإضاءة.
- أوترو منضبط يمحو الشاشة بالكامل دون أي تكرار.
"""
from manim import *
import numpy as np

from .palette import GOLD_BRIGHT, GOLD_LIGHT, GOLD, GOLD_DARK, GOLD_MUTED, IVORY_WHITE

config.background_color = BLACK

OFF_SCREEN_TOP = UP * 4.5
FRAME_HALF_W, FRAME_HALF_H = 3.0, 1.7


def _get_falloff_radial_line(p_start, p_end, n_segments=50):
    """
    خطوط شعاعية ناعمة جداً بتلاشٍ خافت مستمر.
    """
    segments_group = VGroup()
    points = [p_start + (p_end - p_start) * (i / n_segments) for i in range(n_segments + 1)]

    for i in range(n_segments):
        t = i / n_segments

        if t < 0.35:
            falloff = 1.0 - (t * 0.15)
        else:
            falloff = 0.95 * ((1.0 - t) / 0.65) ** 1.35
        falloff = max(0.01, falloff)

        pt_a, pt_b = points[i], points[i + 1]

        # طبقة الهالة الرقيقة
        bloom_w = interpolate(12.0, 1.0, t) * falloff
        bloom_op = interpolate(0.15, 0.01, t) * falloff
        if bloom_op > 0.001:
            segments_group.add(Line(pt_a, pt_b, color=GOLD_LIGHT, stroke_width=bloom_w, stroke_opacity=bloom_op, buff=0))

        # سلك القلب
        core_w = interpolate(1.2, 0.4, t) * (falloff ** 0.4)
        core_op = interpolate(0.85, 0.10, t) * (falloff ** 0.3)
        if core_op > 0.003:
            segments_group.add(Line(
                pt_a, pt_b,
                color="#FFFFFF" if t < 0.25 else GOLD_BRIGHT,
                stroke_width=core_w,
                stroke_opacity=core_op,
                buff=0
            ))

    return segments_group


def get_mach_frame(neon=False):
    """
    بناء الفريم الموحد:
    - neon=False : الفريم الهادئ الكلاسيكي.
    - neon=True  : نيون ذهبي بتشتت سطحي ضبابي حقيقي كالصورة المرجعية تماماً.
    """
    inner = [
        np.array([-FRAME_HALF_W,  FRAME_HALF_H, 0]),
        np.array([ FRAME_HALF_W,  FRAME_HALF_H, 0]),
        np.array([ FRAME_HALF_W, -FRAME_HALF_H, 0]),
        np.array([-FRAME_HALF_W, -FRAME_HALF_H, 0]),
    ]
    outer = [
        (LEFT * config.frame_width / 2 + UP * config.frame_height / 2) * 1.02,
        (RIGHT * config.frame_width / 2 + UP * config.frame_height / 2) * 1.02,
        (RIGHT * config.frame_width / 2 + DOWN * config.frame_height / 2) * 1.02,
        (LEFT * config.frame_width / 2 + DOWN * config.frame_height / 2) * 1.02,
    ]

    if not neon:
        inner_edges = VGroup(*[
            Line(inner[i], inner[(i + 1) % 4], color=GOLD_MUTED, stroke_width=0.8, stroke_opacity=0.25)
            for i in range(4)
        ])
        radial_lines = VGroup(*[
            Line(inner[i], outer[i], color=GOLD_MUTED, stroke_width=0.7, stroke_opacity=0.18)
            for i in range(4)
        ])
        return VGroup(inner_edges, radial_lines)
    else:
        # ==============================================================
        # 2. فريم النيون السطحي فائق النعومة والانتشارية (Planar Glow)
        # ==============================================================
        # أ) أسطح الجدران الأربعة المضيئة بضباب خافت جداً وناعم يفرش في الفراغ
        wall_top = Polygon(inner[0], outer[0], outer[1], inner[1], fill_color=GOLD_MUTED, fill_opacity=0.018, stroke_width=0)
        wall_bottom = Polygon(inner[3], outer[3], outer[2], inner[2], fill_color=GOLD_MUTED, fill_opacity=0.018, stroke_width=0)
        wall_right = Polygon(inner[1], outer[1], outer[2], inner[2], fill_color=GOLD_MUTED, fill_opacity=0.022, stroke_width=0)
        wall_left = Polygon(inner[0], outer[0], outer[3], inner[3], fill_color=GOLD_MUTED, fill_opacity=0.022, stroke_width=0)
        volumetric_walls = VGroup(wall_top, wall_bottom, wall_right, wall_left)

        # ب) طبقات ضبابية ناعمة تحيط بأضلاع المستطيل
        diffusion_layers = [
            # ==========================================================
            # ULTRA-WIDE ATMOSPHERIC SCATTERING
            # ----------------------------------------------------------
            # The important change:
            # We are NOT making one giant bright stroke.
            # Instead, the same small amount of light is distributed over
            # many very faint layers. This creates a broad, soft field.
            #
            # Far field: almost invisible individually.
            # Their job is only to make the glow remain present far away
            # from the actual neon wire.
            # ==========================================================
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
            {"width": 96.0,  "color": GOLD_MUTED, "opacity": 0.00047},
            {"width": 86.0,  "color": GOLD_MUTED, "opacity": 0.00054},
            {"width": 77.0,  "color": GOLD_MUTED, "opacity": 0.00062},
            {"width": 69.0,  "color": GOLD_MUTED, "opacity": 0.00071},

            # ==========================================================
            # VERY WIDE SOFT FIELD
            # ==========================================================
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

            # ==========================================================
            # SOFT ATMOSPHERIC GLOW
            # ==========================================================
            {"width": 19.5, "color": GOLD_MUTED, "opacity": 0.00315},
            {"width": 17.0, "color": GOLD_MUTED, "opacity": 0.00355},
            {"width": 15.0, "color": GOLD_LIGHT, "opacity": 0.00400},
            {"width": 13.2, "color": GOLD_LIGHT, "opacity": 0.00455},
            {"width": 11.5, "color": GOLD_LIGHT, "opacity": 0.00515},
            {"width": 10.0, "color": GOLD_LIGHT, "opacity": 0.00580},
            {"width": 8.7,  "color": GOLD_LIGHT, "opacity": 0.00650},

            # ==========================================================
            # INNER SOFT GLOW
            # ----------------------------------------------------------
            # Kept deliberately below the old medium-glow energy.
            # The core below remains unchanged.
            # ==========================================================
            {"width": 7.5, "color": GOLD_LIGHT, "opacity": 0.0080},
            {"width": 6.5, "color": GOLD_LIGHT, "opacity": 0.0110},
            {"width": 5.5, "color": GOLD_LIGHT, "opacity": 0.0150},

            # ==========================================================
            # ORIGINAL CORE
            # ==========================================================
            {"width": 5.0, "color": GOLD_LIGHT,  "opacity": 0.180},
            {"width": 2.2, "color": GOLD_BRIGHT, "opacity": 0.380},
            {"width": 1.1, "color": "#FFFFFF",   "opacity": 0.650},
            {"width": 0.6, "color": "#FFFFFF",   "opacity": 0.850},
        ]

        frame_rect_layers = VGroup()
        for layer in diffusion_layers:
            layer_edges = VGroup(*[
                Line(
                    inner[i], inner[(i + 1) % 4],
                    color=layer["color"],
                    stroke_width=layer["width"],
                    stroke_opacity=layer["opacity"]
                )
                for i in range(4)
            ])
            frame_rect_layers.add(layer_edges)

        # ج) لحام ضوئي رقيق ومنتشر بنعومة عند الزوايا
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

        # د) الخطوط المائلة المتناسقة
        radial_falloff_group = VGroup(*[
            _get_falloff_radial_line(inner[i], outer[i], n_segments=50)
            for i in range(4)
        ])

        return VGroup(volumetric_walls, frame_rect_layers, radial_falloff_group, corner_halos)


def turn_on_neon(scene, run_time=0.9):
    """إشعال فريم النيون بانسيابية مع منح الهالة مدى للانتشار."""
    neon_glow = get_mach_frame(neon=True).set_z_index(15)
    scene.neon_overlay = neon_glow
    
    # استخدام ease_out_quad يجعل التوهج يظهر بسرعة ثم يستقر بنعومة
    scene.play(
        FadeIn(neon_glow, rate_func=rate_functions.ease_out_quad),
        run_time=run_time
    )

def turn_off_neon(scene, run_time=0.8):
    """
    إطفاء النيون بسلاسة تمنع الإحساس بانطفاء السلك الأبيض فجأة،
    مع التأكد من تنظيف الذاكرة تلقائياً.
    """
    if hasattr(scene, "neon_overlay") and scene.neon_overlay is not None:
        # استخدام ease_in_cubic يجعل التلاشي يبدأ برقة شديدة 
        # حتى تتكيف بؤبؤة عين المشاهد تدريجياً مع زوال السطوع
        scene.play(
            FadeOut(scene.neon_overlay, rate_func=rate_functions.ease_in_sine),
            run_time=run_time,
        )
        scene.remove(scene.neon_overlay)
        scene.neon_overlay = None


# ==============================================================
# 1. INTRO SCENE (شعار متوازن بالمليمتر بخط Cairo العريض)
# ==============================================================
class IntroScene(Scene):
    def construct(self):
        core = Dot(OFF_SCREEN_TOP, radius=0.06, color=GOLD_BRIGHT)
        glow_mid = Circle(radius=0.15, stroke_width=0, fill_color=GOLD_LIGHT, fill_opacity=0.35).move_to(OFF_SCREEN_TOP)
        glow_outer = Circle(radius=0.30, stroke_width=0, fill_color=GOLD, fill_opacity=0.15).move_to(OFF_SCREEN_TOP)
        point = VGroup(glow_outer, glow_mid, core)

        self.play(point.animate.move_to(ORIGIN), run_time=1.0, rate_func=rate_functions.ease_out_cubic)

        self.frame = get_mach_frame(neon=False)
        self.play(
            GrowFromPoint(self.frame, ORIGIN),
            run_time=0.9,
            rate_func=rate_functions.ease_out_cubic,
        )

        font_kwargs = {
            "font": "Cairo",
            "weight": BOLD,
            "font_size": 46
        }

        ma_part = Text("MA", **font_kwargs)
        c_letter = Text("C", **font_kwargs)
        h_letter = Text("H", **font_kwargs)
        mach_word = VGroup(ma_part, c_letter, h_letter).arrange(RIGHT, buff=0.04).move_to(ORIGIN)
        mach_word.set_color_by_gradient(GOLD_BRIGHT, GOLD_LIGHT, GOLD_DARK)

        self.play(FadeIn(mach_word, scale=0.1), FadeOut(point, scale=0.1), run_time=0.7)
        self.wait(0.7)

        t_letter = Text("T", **font_kwargs).move_to(c_letter.get_center())
        t_letter.set_color_by_gradient(GOLD_BRIGHT, GOLD_LIGHT)
        t_letter.shift(UP * 0.6).set_opacity(0)

        self.play(
            c_letter.animate.shift(DOWN * 0.6).set_opacity(0),
            t_letter.animate.shift(DOWN * 0.6).set_opacity(1),
            run_time=0.85,
            rate_func=rate_functions.ease_in_out_cubic
        )
        self.remove(c_letter)
        math_word = VGroup(ma_part, t_letter, h_letter)
        self.wait(0.6)

        left_mach = Text("MACH", **font_kwargs).set_color_by_gradient(GOLD_BRIGHT, GOLD_LIGHT, GOLD_DARK)
        dash_char = Text("-", **font_kwargs).set_color_by_gradient(GOLD_BRIGHT, GOLD_LIGHT)

        full_logo_target = VGroup(left_mach, dash_char, math_word.copy()).arrange(RIGHT, buff=0.12).move_to(ORIGIN)

        target_math_pos = full_logo_target[2].get_center()
        target_dash_pos = full_logo_target[1].get_center()
        target_mach_pos = full_logo_target[0].get_center()

        dash_char.move_to(target_dash_pos)
        left_mach.move_to(target_mach_pos)

        self.play(
            math_word.animate.move_to(target_math_pos),
            FadeIn(left_mach, shift=RIGHT * 0.5),
            FadeIn(dash_char, scale=0.5),
            run_time=1.1,
            rate_func=rate_functions.ease_in_out_sine
        )

        complete_logo = VGroup(left_mach, dash_char, math_word)
        self.wait(1.0)
        self.play(FadeOut(complete_logo, scale=1.2), run_time=0.6)


# ==============================================================
# 2. BASE CONTENT SCENE
# ==============================================================
class MachMathScene(Scene):
    def setup(self):
        super().setup()
        self.frame = get_mach_frame(neon=False)
        self.add(self.frame)


# ==============================================================
# 3. OUTRO SCENE
# ==============================================================
class OutroScene(Scene):
    def construct(self):
        core = Dot(ORIGIN, radius=0.06, color=GOLD_BRIGHT)
        glow_mid = Circle(radius=0.15, stroke_width=0, fill_color=GOLD_LIGHT, fill_opacity=0.35).move_to(ORIGIN)
        glow_outer = Circle(radius=0.30, stroke_width=0, fill_color=GOLD, fill_opacity=0.15).move_to(ORIGIN)
        point = VGroup(glow_outer, glow_mid, core)

        existing_mobjects = Group(*self.mobjects)

        self.play(FadeIn(point, scale=0.2), run_time=0.5)

        self.play(
            FadeOut(existing_mobjects, scale=0.01, target_position=ORIGIN),
            run_time=1.2,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.clear()
        self.add(point)
        self.wait(0.2)

        self.play(
            point.animate.move_to(OFF_SCREEN_TOP),
            run_time=1.3,
            rate_func=rate_functions.ease_in_quad,
        )
        self.wait(0.4)