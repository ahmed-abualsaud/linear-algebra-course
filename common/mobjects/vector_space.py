from manim import *
import numpy as np

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_MUTED,
    GOLD_DARK,
    STONE_AXIS,
    STONE_DASH,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.latex import mach_math_template
from common.mobjects.vectors import MachVector


def _clip_segment(p, q, box):
    """قص القطعة p→q داخل المستطيل box=(x0,x1,y0,y1) (Liang–Barsky). يرجع None لو خارج."""
    x0, x1, y0, y1 = box
    p, q = np.asarray(p, float), np.asarray(q, float)
    d = q - p
    t0, t1 = 0.0, 1.0
    for pk, qk in ((-d[0], p[0] - x0), (d[0], x1 - p[0]), (-d[1], p[1] - y0), (d[1], y1 - p[1])):
        if abs(pk) < 1e-9:
            if qk < 0:
                return None
            continue
        r = qk / pk
        if pk < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return None
    return p + t0 * d, p + t1 * d


class MachVectorSpace(VGroup):
    """
    فضاء المتجهات (MACH-MATH) بطابع سينمائي مميز عن "فضاء الإحداثيات":

    - فضاء الإحداثيات  = شبكة متعامدة متصلة وواضحة.
    - فضاء المتجهات   = شبكات متداخلة كلها بخطوط متقطعة:
        1) شبكة دقيقة خافتة
        2) شبكة رئيسية أوضح كل N خطوط
        3) شبكة مائلة (مدارة) بلون نحاسي خافت متداخلة معها
        3b) شبكة ثانية بلون تركوازي معمول لها shear (e2 = (shear, 1))
        4) توهج ناعم عند الأصل + أقواس إطار في الأركان
      ملاحظة رياضية: كل الخطوط مستقيمة ومتوازية (شبكات خطية بمتجهات أساس ثابتة في كل مكان).
      لا توجد إحداثيات قطبية/حلقات عمدًا، لأن متجهات أساسها تتغير من نقطة لأخرى
      وده يخالف بنية فضاء المتجهات (الجبر الخطي).
      وكل الخطوط تخفت تدريجيًا كل ما ابتعدت عن الأصل.

    الواجهة القديمة (المعاملات + grid / axes / origin / vectors / title_group) لم تتغير.
    """

    DEFAULT_VECTORS = [
        ((2.5, 2.0, 0), GOLD_BRIGHT, r"\mathbf{v}_1"),
        ((-1.8, 1.9, 0), COPPER_TERRA, r"\mathbf{v}_2"),
        ((-1.4, -0.7, 0), STONE_AXIS, r"\mathbf{v}_3"),
        ((1.5, -2.1, 0), GOLD_LIGHT, r"\mathbf{v}_4"),
        ((2.8, -0.5, 0), IVORY_WHITE, r"\mathbf{v}_5"),
        ((-0.9, -2.4, 0), GOLD_MUTED, r"\mathbf{v}_6"),
    ]

    def __init__(
        self,
        center=(-3.55, 0, 0),
        width=7.2,
        height=7.8,
        grid_step=0.55,
        vectors=None,
        title="فضاء المتجهات (Vector Space)",
        show_title=True,
        show_origin=True,
        grid_color=STONE_AXIS,
        axis_color=GOLD_LIGHT,
        grid_width=0.85,
        grid_opacity=0.42,
        axis_width=2.4,
        axis_opacity=0.95,
        dash_length=0.08,
        dashed_ratio=0.55,
        vector_width=3.0,
        vector_opacity=1.0,
        origin_opacity=1.0,
        tip_length=0.22,
        label_font_size=19,
        title_font_size=21,
        title_color=GOLD_LIGHT,
        title_background=True,
        title_top_buff=0.45,
        show_vector_labels=True,
        # ---- الجديد (كله قابل للإيقاف) ----
        cinematic=True,          # يفعّل الطبقات السينمائية (إيقافه = الشبكة البسيطة القديمة)
        major_every=4,           # كل كام خط شبكة رئيسي أوضح
        show_rotated_grid=True,  # شبكة مائلة متداخلة
        rotated_angle=30,        # درجات
        rotated_color=COPPER_TERRA,
        show_sheared_grid=True,  # شبكة ثانية بلون مختلف معمول لها shear
        shear=0.75,              # معامل القص: e2 = (shear, 1)
        sheared_color="#4FA7A0", # تركواز هادئ يتميز عن الذهبي والنحاسي
        show_glow=True,
        show_frame=False,        # أقواس الأركان: متوقفة افتراضيًا (بتتداخل مع الخط الفاصل)
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.center = np.array(center, dtype=float)
        self.space_width = float(width)
        self.space_height = float(height)
        self.grid_step = float(grid_step)

        if self.space_width <= 0 or self.space_height <= 0:
            raise ValueError("width and height must be greater than zero.")
        if self.grid_step <= 0:
            raise ValueError("grid_step must be greater than zero.")
        if len(self.center) != 3:
            raise ValueError("center must contain exactly three coordinates.")

        cx, cy, cz = self.center
        self.x_min = cx - self.space_width / 2
        self.x_max = cx + self.space_width / 2
        self.y_min = cy - self.space_height / 2
        self.y_max = cy + self.space_height / 2
        box = (self.x_min, self.x_max, self.y_min, self.y_max)
        half_diag = 0.5 * float(np.hypot(self.space_width, self.space_height))
        fade_r = 0.5 * max(self.space_width, self.space_height)

        self.glow = VGroup()
        self.grid = VGroup()          # الشبكة الأساسية (دقيقة + رئيسية)
        self.rotated_grid = VGroup()  # الشبكة المائلة المتداخلة
        self.sheared_grid = VGroup()  # شبكة الـ shear
        self.axes = VGroup()
        self.origin = VGroup()
        self.vectors = VGroup()
        self.title_group = VGroup()
        self.frame_marks = VGroup()

        C2 = np.array([cx, cy])

        def fade(dist, base, floor=0.10, k=1.0):
            """تخفّي تدريجي مع البعد عن الأصل."""
            t = min(1.0, dist / fade_r)
            return base * max(floor, 1.0 - k * t)

        def add_dashed(group, a, b, color, width_, opacity, dl=dash_length, ratio=dashed_ratio):
            seg = _clip_segment(a, b, box)
            if seg is None:
                return
            p, q = seg
            if np.linalg.norm(q - p) < 0.05:
                return
            line = DashedLine(
                [p[0], p[1], cz], [q[0], q[1], cz],
                dash_length=dl, dashed_ratio=ratio, color=color, stroke_width=width_,
            )
            line.set_stroke(opacity=opacity)
            group.add(line)

        eps = 1e-7
        x_pos = np.arange(cx + self.grid_step, self.x_max + eps, self.grid_step)
        x_neg = np.arange(cx - self.grid_step, self.x_min - eps, -self.grid_step)
        y_pos = np.arange(cy + self.grid_step, self.y_max + eps, self.grid_step)
        y_neg = np.arange(cy - self.grid_step, self.y_min - eps, -self.grid_step)

        # ----------------------------------------------------------
        # 0. توهج سينمائي ناعم خلف كل شيء
        # ----------------------------------------------------------
        if cinematic and show_glow:
            for i in range(14):
                t = i / 13
                r = fade_r * 0.95 * (1 - 0.9 * t)
                self.glow.add(
                    Circle(radius=r, stroke_width=0, fill_color=GOLD_DARK,
                           fill_opacity=0.045 * (0.25 + 0.75 * t ** 1.8)).move_to(self.center)
                )

        # ----------------------------------------------------------
        # 1. الشبكة الأساسية: دقيقة خافتة + رئيسية أوضح (بخطوط متقطعة)
        # ----------------------------------------------------------
        def build_axis_aligned(vals, vertical):
            for idx, v in enumerate(vals):
                k = int(round(abs(v - (cx if vertical else cy)) / self.grid_step))
                major = cinematic and major_every > 0 and k % major_every == 0
                dist = abs(v - (cx if vertical else cy))
                if vertical:
                    a, b = (v, self.y_min), (v, self.y_max)
                else:
                    a, b = (self.x_min, v), (self.x_max, v)
                if cinematic:
                    op = fade(dist, grid_opacity * (1.45 if major else 0.70), floor=0.18)
                    w = grid_width * (1.5 if major else 0.8)
                    dl = dash_length * (1.25 if major else 0.85)
                    col = grid_color
                else:
                    op, w, dl, col = grid_opacity, grid_width, dash_length, grid_color
                add_dashed(self.grid, a, b, col, w, op, dl=dl)

        build_axis_aligned(np.sort(np.concatenate([x_neg, x_pos])), vertical=True)
        build_axis_aligned(np.sort(np.concatenate([y_neg, y_pos])), vertical=False)

        # ----------------------------------------------------------
        # 2. شبكة مائلة متداخلة (نحاسية خافتة)
        # ----------------------------------------------------------
        if cinematic and show_rotated_grid:
            th = np.radians(rotated_angle)
            ux = np.array([np.cos(th), np.sin(th)])
            uy = np.array([-np.sin(th), np.cos(th)])
            step2 = self.grid_step * 1.85
            n = int(half_diag / step2) + 2
            for k in range(-n, n + 1):
                if k == 0:
                    continue
                off = k * step2
                dist = abs(off)
                op = fade(dist, 0.50, floor=0.08, k=1.0)
                if op < 0.03:
                    continue
                for base, d in ((C2 + off * uy, ux), (C2 + off * ux, uy)):
                    add_dashed(self.rotated_grid, base - d * half_diag * 1.2, base + d * half_diag * 1.2,
                               rotated_color, grid_width * 1.15, op,
                               dl=dash_length * 0.9, ratio=0.45)

        # ----------------------------------------------------------
        # 2b. شبكة ثانية بلون مختلف معمول لها shear
        #     (صورة الشبكة المتعامدة تحت المصفوفة [[1, shear], [0, 1]]):
        #     الخطوط مستقيمة ومتوازية ومتباعدة بانتظام = أساس ثابت في كل مكان.
        # ----------------------------------------------------------
        if cinematic and show_sheared_grid:
            e1 = np.array([1.0, 0.0])
            e2 = np.array([float(shear), 1.0])
            step3 = self.grid_step * 1.45
            n = int(half_diag / step3) + 3
            for k in range(-n, n + 1):
                if k == 0:
                    continue
                dist = abs(k) * step3
                op = fade(dist, 0.85, floor=0.14, k=0.95)
                if op < 0.03:
                    continue
                for base, d in ((C2 + k * step3 * e1, e2), (C2 + k * step3 * e2, e1)):
                    add_dashed(self.sheared_grid, base - d * half_diag * 2.0, base + d * half_diag * 2.0,
                               sheared_color, grid_width * 1.5, op,
                               dl=dash_length * 0.95, ratio=0.5)

        # ----------------------------------------------------------
        # 4. المحاور الرئيسية: متقطعة + هالة + رؤوس أسهم صغيرة
        # ----------------------------------------------------------
        def axis_line(a, b, w, op, dl=dash_length):
            ln = DashedLine(a, b, dash_length=dl, dashed_ratio=dashed_ratio, color=axis_color, stroke_width=w)
            ln.set_stroke(opacity=op)
            return ln

        a_h0, a_h1 = np.array([self.x_min, cy, cz]), np.array([self.x_max, cy, cz])
        a_v0, a_v1 = np.array([cx, self.y_min, cz]), np.array([cx, self.y_max, cz])
        if cinematic:
            self.axes.add(
                axis_line(a_h0, a_h1, axis_width * 3.2, 0.10, dl=dash_length * 1.2),
                axis_line(a_v0, a_v1, axis_width * 3.2, 0.10, dl=dash_length * 1.2),
            )
        self.axes.add(axis_line(a_h0, a_h1, axis_width, axis_opacity),
                      axis_line(a_v0, a_v1, axis_width, axis_opacity))

        if cinematic:
            tip = lambda p, ang: Triangle(fill_color=axis_color, fill_opacity=axis_opacity,
                                          stroke_width=0).scale(0.095).rotate(ang).move_to(p)
            self.axes.add(
                tip(a_h1 + LEFT * 0.06, -PI / 2), tip(a_h0 + RIGHT * 0.06, PI / 2),
                tip(a_v1 + DOWN * 0.06, 0), tip(a_v0 + UP * 0.06, PI),
            )

        # ----------------------------------------------------------
        # 5. نقطة الأصل (مع هالة)
        # ----------------------------------------------------------
        if show_origin:
            if cinematic:
                self.origin.add(
                    Dot(self.center, radius=0.22, color=GOLD_LIGHT).set_opacity(0.10),
                    Dot(self.center, radius=0.12, color=GOLD_LIGHT).set_opacity(0.28),
                )
            origin_dot = Dot(point=self.center, radius=0.05, color=GOLD_BRIGHT)
            origin_dot.set_opacity(origin_opacity)
            self.origin.add(origin_dot)

        # ----------------------------------------------------------
        # 6. أقواس إطار في الأركان (طابع سينمائي)
        # ----------------------------------------------------------
        if cinematic and show_frame:
            arm = 0.34
            for sx, sy in ((-1, 1), (1, 1), (1, -1), (-1, -1)):
                c = np.array([cx + sx * self.space_width / 2, cy + sy * self.space_height / 2, cz])
                for d in (np.array([-sx * arm, 0, 0]), np.array([0, -sy * arm, 0])):
                    self.frame_marks.add(Line(c, c + d, color=GOLD_LIGHT, stroke_width=2.0, stroke_opacity=0.7))

        # ----------------------------------------------------------
        # 7. المتجهات والتسميات
        # ----------------------------------------------------------
        vector_data = self.DEFAULT_VECTORS if vectors is None else vectors

        for item in vector_data:
            if len(item) != 3:
                raise ValueError("Each vector must be (endpoint_offset, color, label).")

            endpoint_offset, vector_color, vector_label = item
            offset = np.array(endpoint_offset, dtype=float)
            endpoint = self.center + offset

            vector = MachVector(
                start=self.center,
                end=endpoint,
                color=vector_color,
                stroke_width=vector_width,
                tip_length=tip_length,
                show_pivot=False,
            )
            vector.set_opacity(vector_opacity)

            vector_group = VGroup(vector)

            if show_vector_labels and vector_label:
                label = MathTex(
                    vector_label,
                    tex_template=mach_math_template,
                    font_size=label_font_size,
                    color=vector_color,
                )
                label.set_opacity(vector_opacity)
                if cinematic:
                    label.set_stroke("#070503", width=5, background=True)

                direction = offset / max(np.linalg.norm(offset), 1e-8)
                label_direction = direction + 0.35 * UP
                label_direction /= max(np.linalg.norm(label_direction), 1e-8)

                label.next_to(endpoint, label_direction, buff=0.10)
                vector_group.add(label)

            self.vectors.add(vector_group)

        # ----------------------------------------------------------
        # 8. الترويسة والعنوان
        # ----------------------------------------------------------
        if show_title and title:
            title_text = MarkupText(
                title, font="Cairo", font_size=title_font_size, color=title_color
            )
            title_text.move_to(np.array([cx, self.y_max - title_top_buff, cz]))

            if title_background:
                title_bg = SurroundingRectangle(
                    title_text, buff=0.12, color=GOLD_MUTED, stroke_width=0.8,
                    stroke_opacity=0.55, fill_color="#100D07", fill_opacity=0.92,
                    corner_radius=0.08,
                )
                self.title_group.add(title_bg, title_text)
            else:
                self.title_group.add(title_text)

        # الطبقات السينمائية الإضافية: لازم تتعرض بالمشهد مع grid و axes (FadeIn(vs.extra_layers))
        self.extra_layers = VGroup(self.glow, self.rotated_grid, self.sheared_grid, self.frame_marks)

        # الترتيب = ترتيب الرسم من الخلف للأمام
        self.add(
            self.glow, self.grid, self.rotated_grid, self.sheared_grid, self.axes,
            self.frame_marks, self.origin, self.vectors, self.title_group,
        )