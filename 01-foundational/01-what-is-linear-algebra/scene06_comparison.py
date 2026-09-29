from manim import *

from common.mobjects.coordinate_systems import (
    MachAxes,
    MachNumberLine,
)

from common.mobjects.tables import MachTable

from common.palette import (
    COPPER_TERRA,
    GOLD_LIGHT,
    IVORY_WHITE,
)

from common.latex import mach_math_template


def play_scene06(scene):

    # ==========================================================
    # TABLE
    # ==========================================================

    table = MachTable(
        rows=4,
        cols=2,
        width=8.2,
        height=5.8,
        cell_padding=0.12,
        shimmer=True,
        shimmer_speed=12.0,
        shimmer_radius=0.018,
    )

    # ==========================================================
    # TITLES
    # ==========================================================

    title_calc = Text(
        "التفاضل والتكامل",
        font="Cairo",
        font_size=30,
        color=COPPER_TERRA,
    )

    title_arith = MarkupText(
        "الحساب",
        font="Cairo",
        font_size=30,
        color=COPPER_TERRA,
    )

    sub_funcs = MarkupText(
        "دوال",
        font="Cairo",
        font_size=25,
        color=IVORY_WHITE,
    )

    sub_numbers = MarkupText(
        "أرقام",
        font="Cairo",
        font_size=25,
        color=IVORY_WHITE,
    )

    table.place(
        title_calc,
        row=0,
        col=0,
    )

    table.place(
        title_arith,
        row=0,
        col=1,
    )

    table.place(
        sub_funcs,
        row=1,
        col=0,
    )

    table.place(
        sub_numbers,
        row=1,
        col=1,
    )

    # ==========================================================
    # NUMBER LINE
    # ==========================================================

    num_line = MachNumberLine(
        length=3.0,
        font_size=14,
    )

    table.fit(
        num_line,
        row=2,
        col=1,
        padding=0.18,
    )

    # ==========================================================
    # GRAPH
    # ==========================================================

    mini_axes = MachAxes(
        x_range=[-3, 3, 1],
        y_range=[-3, 3, 1],
        x_length=2.05,
        y_length=2.05,
        font_size=9,
    )

    mini_curve = mini_axes.plot(
        lambda x: 0.35 * x**2 - 1,
        x_range=[-2.4, 2.4],
        color=GOLD_LIGHT,
        stroke_width=2.2,
    )

    mini_graph = VGroup(
        mini_axes,
        mini_curve,
    )

    table.fit(
        mini_graph,
        row=2,
        col=0,
        padding=0.08,
    )

    # ==========================================================
    # OPERATIONS
    # ==========================================================

    arithmetic_ops = MathTex(
        r"+ \qquad - \qquad \times \qquad \div",
        tex_template=mach_math_template,
        font_size=28,
        color=GOLD_LIGHT,
    )

    calculus_ops = MathTex(
        r"\frac{df(x)}{dx}"
        r"\qquad"
        r"\int f(x)\,dx",
        tex_template=mach_math_template,
        font_size=27,
        color=GOLD_LIGHT,
    )

    table.fit(
        calculus_ops,
        row=3,
        col=0,
        padding=0.16,
    )

    table.fit(
        arithmetic_ops,
        row=3,
        col=1,
        padding=0.16,
    )


    # ==========================================================
    # TABLE CONSTRUCTION
    # ==========================================================

    scene.play(
        table.construct(
            run_time=2.5,
            show_shimmer=True,
            center_point=True,
        )
    )

    # ==========================================================
    # CONTENT
    # ==========================================================

    # ----------------------------------------------------------
    # Titles
    # ----------------------------------------------------------

    scene.play(
        FadeIn(
            title_calc,
            title_arith,
            run_time=0.5,
        )
    )

    # ----------------------------------------------------------
    # Subtitles
    # ----------------------------------------------------------

    scene.play(
        FadeIn(
            sub_funcs,
            sub_numbers,
            run_time=0.45,
        )
    )

    # ----------------------------------------------------------
    # Graph + number line
    # ----------------------------------------------------------

    scene.play(
        FadeIn(
            mini_graph,
            num_line,
            run_time=0.65,
        )
    )

    # ----------------------------------------------------------
    # Operations
    # ----------------------------------------------------------

    scene.play(
        FadeIn(
            calculus_ops,
            arithmetic_ops,
            run_time=0.55,
        )
    )

    # ==========================================================
    # HOLD
    # ==========================================================

    scene.wait(2)

    # ==========================================================
    # CLEANUP
    # ==========================================================

    scene.play(
        FadeOut(
            table,
            title_calc,
            title_arith,
            sub_funcs,
            sub_numbers,
            mini_graph,
            num_line,
            calculus_ops,
            arithmetic_ops,
            run_time=0.8,
        )
    )