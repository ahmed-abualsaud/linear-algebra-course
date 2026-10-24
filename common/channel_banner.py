from manim import *

import numpy as np

from common.latex import mach_math_template

from common.palette import (
    GOLD,
    GOLD_BRIGHT,
    GOLD_DARK,
    GOLD_LIGHT,
    GOLD_MUTED,
    IVORY_WHITE,
)

# ==============================================================
# Banner Render Configuration
# ==============================================================

config.background_color = BLACK

# YouTube Channel Banner — 16:9
config.pixel_width = 2560
config.pixel_height = 1440
config.frame_rate = 30


# ==============================================================
# 1. النقطة الضوئية
# ==============================================================

def get_luminous_point(location=ORIGIN, scale_factor=1.35):

    glow_group = VGroup()

    halo_layers = [

        # 1. التشتت الضوئي الأبعد
        {"radius": 1.15, "color": GOLD_MUTED, "opacity": 0.003},
        {"radius": 1.08, "color": GOLD_MUTED, "opacity": 0.005},
        {"radius": 1.02, "color": GOLD_MUTED, "opacity": 0.008},
        {"radius": 0.96, "color": GOLD_MUTED, "opacity": 0.012},
        {"radius": 0.90, "color": GOLD_MUTED, "opacity": 0.017},
        {"radius": 0.84, "color": GOLD_MUTED, "opacity": 0.023},
        {"radius": 0.78, "color": GOLD_MUTED, "opacity": 0.030},
        {"radius": 0.72, "color": GOLD_MUTED, "opacity": 0.039},
        {"radius": 0.67, "color": GOLD_MUTED, "opacity": 0.049},
        {"radius": 0.62, "color": GOLD_MUTED, "opacity": 0.060},
        {"radius": 0.57, "color": GOLD_MUTED, "opacity": 0.073},
        {"radius": 0.52, "color": GOLD_MUTED, "opacity": 0.088},
        {"radius": 0.47, "color": GOLD_MUTED, "opacity": 0.105},
        {"radius": 0.43, "color": GOLD_MUTED, "opacity": 0.125},
        {"radius": 0.39, "color": GOLD_MUTED, "opacity": 0.148},

        # 2. الهالة الدافئة العميقة
        {"radius": 0.360, "color": GOLD_DARK, "opacity": 0.175},
        {"radius": 0.332, "color": GOLD_DARK, "opacity": 0.205},
        {"radius": 0.306, "color": GOLD_DARK, "opacity": 0.240},
        {"radius": 0.282, "color": GOLD_DARK, "opacity": 0.280},
        {"radius": 0.260, "color": GOLD_DARK, "opacity": 0.325},
        {"radius": 0.240, "color": GOLD_DARK, "opacity": 0.375},
        {"radius": 0.222, "color": GOLD_DARK, "opacity": 0.430},
        {"radius": 0.205, "color": GOLD_DARK, "opacity": 0.490},
        {"radius": 0.190, "color": GOLD_DARK, "opacity": 0.555},
        {"radius": 0.175, "color": GOLD_DARK, "opacity": 0.625},

        # 3. الهالة الذهبية المتوهجة
        {"radius": 0.162, "color": GOLD, "opacity": 0.695},
        {"radius": 0.149, "color": GOLD, "opacity": 0.765},
        {"radius": 0.137, "color": GOLD, "opacity": 0.830},
        {"radius": 0.125, "color": GOLD, "opacity": 0.885},
        {"radius": 0.114, "color": GOLD, "opacity": 0.930},
        {"radius": 0.104, "color": GOLD, "opacity": 0.960},
        {"radius": 0.095, "color": GOLD, "opacity": 0.980},
        {"radius": 0.087, "color": GOLD, "opacity": 0.995},

        # 4. التوهج المشع القريب
        {"radius": 0.080, "color": GOLD_LIGHT, "opacity": 1.000},
        {"radius": 0.074, "color": GOLD_LIGHT, "opacity": 1.000},
        {"radius": 0.068, "color": GOLD_LIGHT, "opacity": 1.000},
        {"radius": 0.062, "color": GOLD_LIGHT, "opacity": 1.000},
        {"radius": 0.057, "color": GOLD_LIGHT, "opacity": 1.000},
        {"radius": 0.052, "color": GOLD_LIGHT, "opacity": 1.000},
        {"radius": 0.047, "color": GOLD_LIGHT, "opacity": 1.000},
        {"radius": 0.043, "color": GOLD_LIGHT, "opacity": 1.000},
        {"radius": 0.039, "color": GOLD_LIGHT, "opacity": 1.000},
        {"radius": 0.035, "color": GOLD_LIGHT, "opacity": 1.000},
        {"radius": 0.032, "color": GOLD_LIGHT, "opacity": 1.000},
        {"radius": 0.029, "color": GOLD_LIGHT, "opacity": 1.000},

        # 5. التوهج الذهبي الساطع
        {"radius": 0.026, "color": GOLD_BRIGHT, "opacity": 1.000},
        {"radius": 0.023, "color": GOLD_BRIGHT, "opacity": 1.000},
        {"radius": 0.021, "color": GOLD_BRIGHT, "opacity": 1.000},
        {"radius": 0.019, "color": GOLD_BRIGHT, "opacity": 1.000},
        {"radius": 0.017, "color": GOLD_BRIGHT, "opacity": 1.000},
        {"radius": 0.015, "color": GOLD_BRIGHT, "opacity": 1.000},
        {"radius": 0.013, "color": GOLD_BRIGHT, "opacity": 1.000},
        {"radius": 0.012, "color": GOLD_BRIGHT, "opacity": 1.000},
        {"radius": 0.010, "color": GOLD_BRIGHT, "opacity": 1.000},

        # 6. البؤرة البيضاء الساطعة
        {"radius": 0.0095, "color": "#FFFFFF", "opacity": 1.000},
        {"radius": 0.0085, "color": "#FFFFFF", "opacity": 1.000},
        {"radius": 0.0075, "color": "#FFFFFF", "opacity": 1.000},
        {"radius": 0.0065, "color": "#FFFFFF", "opacity": 1.000},
        {"radius": 0.0055, "color": "#FFFFFF", "opacity": 1.000},
        {"radius": 0.0045, "color": "#FFFFFF", "opacity": 1.000},
    ]

    for layer in halo_layers:

        r = layer["radius"] * scale_factor
        op = layer["opacity"]
        col = layer["color"]

        if r > 0.08 * scale_factor:

            width = r * 2.7
            height = r * 2.7
            shift_up_amount = r * 0.2

            ellipse = Ellipse(
                width=width,
                height=height,
                stroke_width=0,
                fill_color=col,
                fill_opacity=op * 0.45,
            )

            ellipse.move_to(
                location + UP * shift_up_amount
            )

            glow_group.add(ellipse)

        else:

            circle = Circle(
                radius=r,
                stroke_width=0,
                fill_color=col,
                fill_opacity=op,
            ).move_to(location)

            glow_group.add(circle)

    glow_group.add(
        Dot(
            location,
            radius=0.036 * scale_factor,
            color="#FFFFFF",
        )
    )

    glow_group.add(
        Dot(
            location,
            radius=0.020 * scale_factor,
            color="#FFFFFF",
        )
    )

    return glow_group


# ==============================================================
# 2. مشهد البنر
# ==============================================================

class BannerScene(Scene):

    def construct(self):

        well_center = DOWN * 0.45

        # ======================================================
        # تحكم موحد في موضع وحجم العناصر الجانبية
        # ======================================================

        SIDE_ELEMENTS_DOWN = DOWN * 0.9

        # مقدار الاقتراب الأفقي من النقطة المضيئة
        SIDE_ELEMENTS_INWARD = 1.2

        # حجم الفضاء المماسي
        TANGENT_SCALE = 0.82

        # حجم الشبكة العصبية
        NEURAL_SCALE = 0.7

        # ضغط الشبكة العصبية رأسيًا
        NEURAL_VERTICAL_COMPRESSION = 0.72

        # ------------------------------------------------------
        # أ) السطح المنحني بزاوية 30 درجة
        # ------------------------------------------------------

        manifold_back = VGroup()
        manifold_front = VGroup()

        tilt_angle = 30 * DEGREES

        sin_t = np.sin(tilt_angle)
        cos_t = np.cos(tilt_angle)

        def warp_pt(x_coord, y_coord):

            r = np.sqrt(
                x_coord**2 + y_coord**2
            )

            z_elevation = (
                1.45
                * (
                    1.0
                    - np.exp(
                        -((r / 2.3) ** 1.6)
                    )
                )
            )

            y_proj = (
                y_coord * sin_t
                + z_elevation * cos_t
            )

            return well_center + np.array(
                [x_coord, y_proj, 0]
            )

        ring_radii = np.linspace(
            0.45,
            5.8,
            15,
        )

        for r in ring_radii:

            dist_factor = np.clip(
                1.0 - (r / 6.0),
                0.15,
                0.85,
            )

            stroke_color = (
                GOLD_LIGHT
                if r < 2.2
                else GOLD_MUTED
            )

            stroke_w = (
                1.3
                if r < 2.5
                else 0.9
            )

            stroke_op = dist_factor * 0.55

            # القوس الخلفي
            pts_back = [
                warp_pt(
                    r * np.cos(th),
                    r * np.sin(th),
                )
                for th in np.linspace(
                    0,
                    PI,
                    60,
                )
            ]

            arc_back = (
                VMobject()
                .set_points_smoothly(
                    pts_back
                )
            )

            arc_back.set_stroke(
                color=stroke_color,
                width=stroke_w,
                opacity=stroke_op,
            )

            manifold_back.add(
                arc_back
            )

            # القوس الأمامي
            pts_front = [
                warp_pt(
                    r * np.cos(th),
                    r * np.sin(th),
                )
                for th in np.linspace(
                    PI,
                    TAU,
                    60,
                )
            ]

            arc_front = (
                VMobject()
                .set_points_smoothly(
                    pts_front
                )
            )

            arc_front.set_stroke(
                color=(
                    GOLD_LIGHT
                    if r < 1.6
                    else stroke_color
                ),
                width=(
                    stroke_w * 1.15
                    if r < 1.6
                    else stroke_w
                ),
                opacity=(
                    min(
                        0.95,
                        stroke_op * 1.3,
                    )
                    if r < 1.6
                    else stroke_op
                ),
            )

            manifold_front.add(
                arc_front
            )

        radial_angles = np.linspace(
            0,
            TAU,
            24,
            endpoint=False,
        )

        for th in radial_angles:

            pts = []

            for r in np.linspace(
                0.35,
                5.8,
                45,
            ):

                x = r * np.cos(th)
                y = r * np.sin(th)

                pts.append(
                    warp_pt(x, y)
                )

            radial_line = VMobject()

            radial_line.set_points_smoothly(
                pts
            )

            radial_line.set_stroke(
                color=GOLD_MUTED,
                width=0.9,
                opacity=0.35,
            )

            if np.sin(th) >= -0.01:
                manifold_back.add(
                    radial_line
                )
            else:
                manifold_front.add(
                    radial_line
                )

        # ------------------------------------------------------
        # ب) النواة المركزية المتوهجة
        # ------------------------------------------------------

        core_pos = (
            well_center
            + UP * 0.12
        )

        core_orb = get_luminous_point(
            core_pos,
            scale_factor=1.35,
        )

        # ------------------------------------------------------
        # ج) الاسم الأساسي: MACH - MATH
        # ------------------------------------------------------

        title_text = Text(
            "MACH - MATH",
            font="Serif",
            weight=BOLD,
            font_size=100,
        )

        r_target = 1.5

        title_text.move_to(
            ORIGIN
        )

        def warp_text_point(point):

            x, y, z = point

            angle = (
                PI / 2
                - x * 0.12
            )

            r = (
                r_target
                + y * 0.55
            )

            x_ring = (
                r * np.cos(angle)
            )

            y_ring = (
                r * np.sin(angle)
            )

            return warp_pt(
                x_ring,
                y_ring,
            )

        title_logo = (
            title_text.apply_function(
                warp_text_point
            )
        )

        title_logo.set_color_by_gradient(
            GOLD_BRIGHT,
            GOLD_LIGHT,
            GOLD_DARK,
        )

        mach_part = VGroup(
            *title_logo[0:4]
        )

        dash_part = title_logo[4]

        math_part = VGroup(
            *title_logo[5:9]
        )

        mach_part.set_color_by_gradient(
            GOLD_BRIGHT,
            GOLD_LIGHT,
            GOLD_DARK,
        )

        dash_part.set_color_by_gradient(
            GOLD_BRIGHT,
            GOLD_LIGHT,
        )

        math_part.set_color_by_gradient(
            GOLD_BRIGHT,
            GOLD_LIGHT,
            GOLD_DARK,
        )

        # ------------------------------------------------------
        # الشريط السفلي
        # ------------------------------------------------------

        sub_ine = Text(
            "ine learning",
            font="Serif",
            font_size=14,
            color=IVORY_WHITE,
        )

        sub_mach = Text(
            "MACH",
            font="Serif",
            weight=BOLD,
            font_size=14,
            color=GOLD_LIGHT,
        )

        sub_mach.next_to(
            sub_ine[0],
            LEFT,
            buff=0.015,
        )

        sub_mach.shift(
            UP
            * (
                sub_ine[0].get_bottom()[1]
                - sub_mach.get_bottom()[1]
            )
        )

        word_machine = VGroup(
            sub_mach,
            sub_ine,
        )

        sub_ematics = Text(
            "ematics",
            font="Serif",
            font_size=14,
            color=IVORY_WHITE,
        )

        sub_math = Text(
            "MATH",
            font="Serif",
            weight=BOLD,
            font_size=14,
            color=GOLD_LIGHT,
        )

        sub_math.next_to(
            sub_ematics[0],
            LEFT,
            buff=0.015,
        )

        sub_math.shift(
            UP
            * (
                sub_ematics[0].get_bottom()[1]
                - sub_math.get_bottom()[1]
            )
        )

        word_mathematics = VGroup(
            sub_math,
            sub_ematics,
        )

        pipe_sep = Text(
            "|",
            font="Serif",
            font_size=16,
            color=GOLD_DARK,
        ).move_to(
            DOWN * 1
        )

        word_machine.next_to(
            pipe_sep,
            LEFT,
            buff=0.23,
        )

        word_mathematics.next_to(
            pipe_sep,
            RIGHT,
            buff=0.23,
        )

        subtitle_bar = VGroup(
            word_machine,
            pipe_sep,
            word_mathematics,
        )

        # ------------------------------------------------------
        # د) الفضاء المماسي
        # ------------------------------------------------------

        tangent_group = VGroup()

        r_tan = ring_radii[8]
        th_tan = radial_angles[1]

        p0 = warp_pt(
            r_tan * np.cos(th_tan),
            r_tan * np.sin(th_tan),
        )

        u_edge = np.array(
            [1.10, 0.12, 0]
        )

        v_edge = np.array(
            [-0.25, -0.46, 0]
        )

        n_dir = np.array(
            [-0.05, 0.60, 0]
        )

        u_scaled = u_edge * 0.80
        v_scaled = v_edge * 0.80

        p1 = p0 + u_scaled
        p2 = p0 + u_scaled + v_scaled
        p3 = p0 + v_scaled

        t_frame = Polygon(
            p0,
            p1,
            p2,
            p3,
            stroke_color=GOLD_LIGHT,
            stroke_width=1.0,
            stroke_opacity=0.75,
            fill_color=GOLD_DARK,
            fill_opacity=0.08,
        )

        arrow_n = Arrow(
            p0,
            p0 + n_dir,
            color=IVORY_WHITE,
            buff=0,
            stroke_width=1.7,
            max_tip_length_to_length_ratio=0.22,
        )

        arrow_l1 = Arrow(
            p0,
            p0 + u_edge * 0.72,
            color=IVORY_WHITE,
            buff=0,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.22,
        )

        arrow_l2 = Arrow(
            p0,
            p0 + v_edge * 0.72,
            color=IVORY_WHITE,
            buff=0,
            stroke_width=1.5,
            max_tip_length_to_length_ratio=0.22,
        )

        lbl_n = MathTex(
            r"\hat{\mathbf{n}}",
            tex_template=mach_math_template,
            font_size=22,
            color=IVORY_WHITE,
        ).next_to(
            arrow_n.get_end(),
            UP,
            buff=0.10,
        )

        lbl_l1 = MathTex(
            "L_1",
            tex_template=mach_math_template,
            font_size=21,
            color=IVORY_WHITE,
        ).next_to(
            arrow_l1.get_center(),
            UP * 0.5 + RIGHT * 1.8,
            buff=0.18,
        )

        lbl_l2 = MathTex(
            "L_2",
            tex_template=mach_math_template,
            font_size=21,
            color=IVORY_WHITE,
        ).next_to(
            arrow_l2.get_center(),
            LEFT * 0.5 + DOWN * 0.8,
            buff=0.22,
        )

        lbl_tp = MathTex(
            r"T_p\mathcal{M}",
            tex_template=mach_math_template,
            font_size=17,
            color=GOLD_LIGHT,
        ).next_to(
            p0,
            LEFT,
            buff=0.10,
        )

        v_target = p0 + np.array(
            [0.44, 0.32, 0]
        )

        v_core = Arrow(
            p0,
            v_target,
            color=GOLD,
            buff=0,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.24,
        )

        shaft_end = (
            p0
            + (v_target - p0) * 0.76
        )

        n_segs = 50

        neon_glow_halo = VGroup()

        seg_points = [
            p0
            + (v_target - p0)
            * (i / n_segs)
            for i in range(
                n_segs + 1
            )
        ]

        for i in range(n_segs):

            t = (
                i + 0.5
            ) / n_segs

            glow_factor = t**1.25

            p_a = seg_points[i]
            p_b = seg_points[i + 1]

            neon_glow_halo.add(
                Line(
                    p_a,
                    p_b,
                    stroke_color=GOLD_DARK,
                    stroke_width=18.0 * glow_factor,
                    stroke_opacity=0.15 * glow_factor,
                    buff=0,
                )
            )

            neon_glow_halo.add(
                Line(
                    p_a,
                    p_b,
                    stroke_color=GOLD,
                    stroke_width=12.0 * glow_factor,
                    stroke_opacity=0.30 * glow_factor,
                    buff=0,
                )
            )

            neon_glow_halo.add(
                Line(
                    p_a,
                    p_b,
                    stroke_color=GOLD_LIGHT,
                    stroke_width=6.5 * glow_factor,
                    stroke_opacity=0.55 * glow_factor,
                    buff=0,
                )
            )

            neon_glow_halo.add(
                Line(
                    p_a,
                    p_b,
                    stroke_color=GOLD_BRIGHT,
                    stroke_width=2.4 * glow_factor,
                    stroke_opacity=0.85 * glow_factor,
                    buff=0,
                )
            )

        tip_pos = (
            shaft_end
            + (v_target - shaft_end)
            * 0.40
        )

        tip_soft_glow = VGroup(

            Dot(
                tip_pos,
                radius=0.08,
                color=GOLD_DARK,
                fill_opacity=0.15,
            ),

            Dot(
                tip_pos,
                radius=0.05,
                color=GOLD,
                fill_opacity=0.30,
            ),

            Dot(
                tip_pos,
                radius=0.02,
                color=GOLD_LIGHT,
                fill_opacity=0.55,
            ),
        )

        neon_vector = VGroup(
            neon_glow_halo,
            tip_soft_glow,
            v_core,
        )

        lbl_v = MathTex(
            r"\mathbf{v}",
            tex_template=mach_math_template,
            font_size=20,
            color=GOLD,
        ).next_to(
            v_target,
            RIGHT * 0.35 + UP * 0.15,
            buff=0.06,
        )

        geo_eq1 = MathTex(
            r"\Gamma^\sigma_{\mu\nu}",
            tex_template=mach_math_template,
            font_size=21,
            color=GOLD_LIGHT,
        ).move_to(
            p1 + RIGHT * 0.45 + UP * 0.15
        )

        geo_eq2 = MathTex(
            r"R^\rho_{\ \sigma\mu\nu}",
            tex_template=mach_math_template,
            font_size=20,
            color=IVORY_WHITE,
        ).next_to(
            geo_eq1,
            DOWN,
            buff=0.18,
        )

        geo_eq3 = MathTex(
            r"\delta^i_j",
            tex_template=mach_math_template,
            font_size=18,
            color=GOLD_MUTED,
        ).next_to(
            geo_eq1,
            RIGHT,
            buff=0.20,
        )

        tangent_group.add(
            t_frame,
            arrow_n,
            arrow_l1,
            arrow_l2,
            lbl_n,
            lbl_l1,
            lbl_l2,
            neon_vector,
            lbl_v,
            geo_eq1,
            geo_eq2,
            geo_eq3,
        )

        # ======================================================
        # تصغير الفضاء المماسي
        # ======================================================

        tangent_group.scale(
            TANGENT_SCALE,
            about_point=tangent_group.get_center(),
        )

        # ======================================================
        # تحريك الفضاء المماسي:
        # 1. لأسفل
        # 2. للداخل ناحية النقطة المضيئة
        # ======================================================

        tangent_group.shift(
            SIDE_ELEMENTS_DOWN
            + LEFT * SIDE_ELEMENTS_INWARD
        )

        # ------------------------------------------------------
        # هـ) الشبكة العصبية
        # ------------------------------------------------------

        neural_group = VGroup()

        grid_specs = [
            [(10, 10), (10, 12)],
            [(8, 9), (8, 11), (8, 13)],
            [(6, 10), (6, 12)],
        ]

        node_layers = []

        for layer in grid_specs:

            layer_pts = []

            for r_idx, th_idx in layer:

                r_val = ring_radii[r_idx]
                th_val = radial_angles[th_idx]

                x = r_val * np.cos(th_val)
                y = r_val * np.sin(th_val)

                layer_pts.append(
                    (
                        r_val,
                        th_val,
                        warp_pt(x, y),
                    )
                )

            node_layers.append(
                layer_pts
            )

        for l in range(
            len(node_layers) - 1
        ):

            curr_layer = node_layers[l]
            next_layer = node_layers[l + 1]

            for r1, th1, p1 in curr_layer:

                for r2, th2, p2 in next_layer:

                    curve_pts = []

                    for t in np.linspace(
                        0,
                        1,
                        15,
                    ):

                        r_t = (
                            (1 - t) * r1
                            + t * r2
                        )

                        th_t = (
                            (1 - t) * th1
                            + t * th2
                        )

                        x_t = (
                            r_t * np.cos(th_t)
                        )

                        y_t = (
                            r_t * np.sin(th_t)
                        )

                        curve_pts.append(
                            warp_pt(
                                x_t,
                                y_t,
                            )
                        )

                    syn_curve = (
                        VMobject()
                        .set_points_smoothly(
                            curve_pts
                        )
                    )

                    syn_curve.set_stroke(
                        color=GOLD_LIGHT,
                        width=1.1,
                        opacity=0.40,
                    )

                    neural_group.add(
                        syn_curve
                    )

        for layer in node_layers:

            for _, _, pt in layer:

                halo = Dot(
                    pt,
                    radius=0.075,
                    color=GOLD_LIGHT,
                    fill_opacity=0.35,
                )

                core = Dot(
                    pt,
                    radius=0.032,
                    color=GOLD_BRIGHT,
                    fill_opacity=0.98,
                )

                neural_group.add(
                    halo,
                    core,
                )

        top_left_node = (
            node_layers[0][0][2]
        )

        ai_eq1 = MathTex(
            r"\nabla_\theta \mathcal{L}",
            tex_template=mach_math_template,
            font_size=23,
            color=GOLD_BRIGHT,
        ).next_to(
            top_left_node,
            UP + LEFT,
            buff=0.15,
        )

        ai_eq2 = MathTex(
            r"\sigma(\mathbf{W}^T\mathbf{x} + \mathbf{b})",
            tex_template=mach_math_template,
            font_size=19,
            color=IVORY_WHITE,
        ).next_to(
            top_left_node,
            LEFT,
            buff=0.25,
        ).shift(
            DOWN * 0.4
        )

        ai_eq3 = MathTex(
            r"\mathcal{L}_{\text{loss}}",
            tex_template=mach_math_template,
            font_size=17,
            color=GOLD_MUTED,
        ).next_to(
            ai_eq2,
            LEFT,
            buff=0.18,
        )

        neural_group.add(
            ai_eq1,
            ai_eq2,
            ai_eq3,
        )

        # ======================================================
        # تصغير الشبكة العصبية
        # ======================================================

        neural_group.scale(
            NEURAL_SCALE,
            about_point=neural_group.get_center(),
        )

        # ======================================================
        # ضغط الشبكة العصبية رأسيًا
        # ======================================================

        neural_group.stretch(
            NEURAL_VERTICAL_COMPRESSION,
            dim=1,
            about_point=neural_group.get_center(),
        )

        # ======================================================
        # تحريك الشبكة العصبية:
        # 1. لأسفل
        # 2. للداخل ناحية النقطة المضيئة
        # ======================================================

        neural_group.shift(
            SIDE_ELEMENTS_DOWN
            + RIGHT * SIDE_ELEMENTS_INWARD
        )

        # ------------------------------------------------------
        # و) خلفية الرموز الرياضية الخافتة
        # ------------------------------------------------------

        cosmic_bg = VGroup()

        faint_symbols = [

            # الجبر الخطي
            (
                r"\mathbf{A}\mathbf{x} = \lambda \mathbf{x}",
                UP * 3.2 + LEFT * 5.8,
            ),

            (
                r"\det(\mathbf{A})",
                DOWN * 2.4 + LEFT * 4.2,
            ),

            (
                r"\mathrm{Im}(T) \quad \mathrm{Ker}(T)",
                UP * 3.4 + LEFT * 2.5,
            ),

            (
                r"\mathbf{A} = [a_{ij}]",
                DOWN * 2.8 + LEFT * 6.2,
            ),

            (
                r"\lambda_i \mathbf{v}_i",
                UP * 1.6 + RIGHT * 5.6,
            ),

            # التفاضل والتكامل
            (
                r"\lim_{x \to 0} \frac{\sin x}{x} = 1",
                UP * 2.8 + LEFT * 3.2,
            ),

            (
                r"\int_a^b f(x)\,dx",
                UP * 2.0 + LEFT * 6.2,
            ),

            (
                r"\frac{\partial f}{\partial x}",
                UP * 3.3 + RIGHT * 2.3,
            ),

            (
                r"\oint_{\partial \Omega}",
                UP * 2.5 + LEFT * 4.6,
            ),

            (
                r"\iint_D f(x,y)\,dx\,dy",
                DOWN * 2.2 + RIGHT * 5.8,
            ),

            # الاحتمالات والإحصاء
            (
                r"P(A|B) = \frac{P(B|A)P(A)}{P(B)}",
                DOWN * 1.8 + LEFT * 5.5,
            ),

            (
                r"f(x) = \frac{1}{\sigma \sqrt{2\pi}} "
                r"e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}",
                DOWN * 3.3 + LEFT * 2.2,
            ),

            (
                r"\mathbb{E}[X] \quad \mathrm{Var}(X)",
                UP * 2.5 + RIGHT * 5.8,
            ),

            # المعادلات التفاضلية
            (
                r"y' + p(x)y = q(x)",
                UP * 3.3 + RIGHT * 0.2,
            ),

            (
                r"\frac{dy}{dx} = f(x,y)",
                UP * 1.8 + RIGHT * 5.9,
            ),

            # الجبر والتفاضل التنسوري
            (
                r"T^{\mu\nu}_{\alpha\beta}",
                DOWN * 3.2 + RIGHT * 2.1,
            ),

            (
                r"g_{\mu\nu} g^{\nu\rho} = \delta_\mu^\rho",
                DOWN * 3.5 + LEFT * 0.8,
            ),

            (
                r"\nabla_\mu A^\mu = "
                r"\partial_\mu A^\mu + "
                r"\Gamma^\mu_{\mu\lambda}A^\lambda",
                DOWN * 3.2 + RIGHT * 5.2,
            ),

            # نظرية المجموعات ونظرية المعلومات
            (
                r"A \cup B \quad A \cap B \quad \emptyset",
                DOWN * 2.2 + LEFT * 2.2,
            ),

            (
                r"\forall x \in M,\ \exists y",
                DOWN * 2.9 + LEFT * 3.8,
            ),

            (
                r"H(X) = -\sum P(x) \log P(x)",
                DOWN * 3.2 + LEFT * 4.2,
            ),

            # التحليل العددي والهندسة
            (
                r"\mathcal{O}(h^p)",
                DOWN * 2.1 + RIGHT * 6.2,
            ),

            (
                r"\mathbb{R}^n",
                UP * 2.3 + RIGHT * 5.2,
            ),

            (
                r"\mathrm{Tr}(\mathbf{T})",
                DOWN * 2.5 + RIGHT * 4.5,
            ),

            (
                r"C^k(M)",
                DOWN * 2.0 + RIGHT * 4.8,
            ),

            (
                r"k[x_1, \dots, x_n]",
                DOWN * 3.5 + RIGHT * 3.5,
            ),
        ]

        for tex, pos in faint_symbols:

            sym = MathTex(
                tex,
                tex_template=mach_math_template,
                font_size=18,
                color=GOLD_MUTED,
            )

            sym.move_to(pos).set_opacity(
                0.5
            )

            cosmic_bg.add(sym)

        # ======================================================
        # الترتيب النهائي
        # ======================================================

        self.add(
            cosmic_bg,
            manifold_back,
            core_orb,
            manifold_front,
            neural_group,
            tangent_group,
            title_logo,
            subtitle_bar,
        )

        self.wait(0.1)