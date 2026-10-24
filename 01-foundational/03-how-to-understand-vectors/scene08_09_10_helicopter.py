from manim import *
import numpy as np
import weakref

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_MUTED,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.mobjects.coordinate_systems import MachAxes3D
from common.mobjects.helicopter import make_helicopter, fly_along_3d
from common.mobjects.time_slider import MachTimeSlider


# ======================================================================
# الإعدادات الموحدة للمشاهد (تطابق تام لمنع أي اهتزاز)
# ======================================================================
MOVE = (3, 4, 5)          # الإزاحة: شرق، شمال، أرتفاع (بالمتر)
DURATION = 10             # الزمن (بالثواني)
FLIGHT_TIME = 7.5         # مدة الطيران المتزامنة مع الصوت
UNIT = 0.46               # طول الوحدة في الرسم
SCALE = 100               # متر → سنتيمتر

# إعدادات المشهد العاشر (وحدة الخشبة)
PLANK = 3.9
PLANK_VALUES = ("0.769", "1.025", "1.282")
UNIT_NAME = "الخشبة"

AXES_CENTER = np.array([-3.8, -2.5, -0.90])

SPACE_COLOR = GOLD_BRIGHT
TIME_COLOR = COPPER_TERRA
NEW_COLOR = "#7FD6C2"     # لون وحدة الخشبة


# ======================================================================
# أدوات مساعدة
# ======================================================================
def _clear(scene, *mobs):
    fam = []
    for m in mobs:
        if m is not None:
            fam += m.get_family()
    scene.remove(*fam)


def _hud(scene, *mobs):
    if isinstance(scene, ThreeDScene):
        scene.renderer.camera.add_fixed_in_frame_mobjects(*mobs)
    return mobs[0] if len(mobs) == 1 else mobs


class _LiveNumber(VGroup):
    """عداد رقمي حي بدون ترك كائنات متراكمة في الذاكرة."""
    def __init__(self, scene, getter, center_fn, decimals=0, font_size=64, color=IVORY_WHITE):
        super().__init__()
        self._scene_ref = weakref.ref(scene)
        self._getter, self._center_fn = getter, center_fn
        self._dec, self._fs, self._col = decimals, font_size, color
        self._last = None
        self._cur = None
        self._old = []
        self._rebuild(force=True)
        self.add_updater(lambda m: m._rebuild())

    def _rebuild(self, force=False):
        v = round(max(0.0, float(self._getter())), self._dec)
        if not force and v == self._last:
            return
        self._last = v
        sc = self._scene_ref()
        cam = sc.renderer.camera if isinstance(sc, ThreeDScene) else None
        
        if self._cur is not None:
            self._cur.set_opacity(0)
            self._old.append(self._cur)
        txt = f"{v:.{self._dec}f}"
        new = MathTex(txt, font_size=self._fs, color=self._col)
        new.move_to(self._center_fn())
        if cam is not None:
            cam.add_fixed_in_frame_mobjects(new)
        self.add(new)
        self._cur = new

    def dispose(self, scene):
        """حذف نهائي لكل الأرقام (الحالية والمخفية) من المشهد ومن قائمة الـ HUD."""
        self.clear_updaters()
        items = list(self._old) + ([self._cur] if self._cur is not None else [])
        if isinstance(scene, ThreeDScene):
            scene.renderer.camera.remove_fixed_in_frame_mobjects(*items)
        scene.remove(*items, self)
        self._old, self._cur = [], None


def _ar(txt, size=22, color=IVORY_WHITE, bold=False):
    body = f"<b>{txt}</b>" if bold else txt
    return MarkupText(body, font="Cairo", font_size=size, color=color)


class _TickLabels:
    """
    يدير أرقام تدريج المحاور (1..6) بحيث تتغير *في مكانها* بين المتر والسنتيمتر والخشبة
    دون أن تتحرك الرسمة أو تختفي.
    """
    def __init__(self, scene, axes, O):
        self.scene = scene
        self.is_3d = isinstance(scene, ThreeDScene)
        self.mode = "m"
        self.items = []
        labs = []
        for m in axes._label_mobjects():
            if isinstance(m, Text):
                raw = m.text.strip()
                if raw.isdigit() and int(raw) > 0:
                    labs.append(m)
        for m in labs:
            c = m.get_center()
            kind = "z" if c[2] > O[2] + 0.1 else ("y" if c[0] < O[0] - 1e-3 else "x")
            self.items.append(dict(mob=m, kind=kind, k=int(m.text.strip()), ref=m.copy()))
        for g in axes.get_family():
            g.remove(*labs)
        scene.add(*labs)

    @staticmethod
    def text_for(mode, k):
        if mode == "cm":
            return str(k * SCALE)
        if mode == "plank":
            return f"{k / PLANK:.2f}"
        return str(k)

    def mobs(self):
        return [it["mob"] for it in self.items if it["mob"] is not None]

    @staticmethod
    def _visible(mode, it):
        return mode == "m" or it["k"] % 2 == 0

    def retarget(self, mode, font_size=13):
        if mode == self.mode:
            return Wait(0.01), (lambda: None)
        cam = self.scene.renderer.camera if self.is_3d else None
        pairs = []
        for it in self.items:
            old = it["mob"]
            new = None
            if self._visible(mode, it):
                ref = it["ref"]
                new = Text(self.text_for(mode, it["k"]), font_size=font_size, color=IVORY_WHITE).set_opacity(0.9)
                new.move_to(ref.get_center())
                if it["kind"] == "x":
                    new.align_to(ref, UP)
                elif it["kind"] == "y":
                    new.align_to(ref, RIGHT)
                else:
                    new.align_to(ref, LEFT)
                if cam is not None:
                    cam.add_fixed_orientation_mobjects(new)
            pairs.append((it, old, new))

        anims = []
        for _, o, n in pairs:
            parts = ([FadeOut(o)] if o is not None else []) + ([FadeIn(n)] if n is not None else [])
            if parts:
                anims.append(AnimationGroup(*parts))
        anim = LaggedStart(*anims, lag_ratio=0.04)

        def commit():
            for it, o, n in pairs:
                if o is not None:
                    self.scene.remove(o)
                    if cam is not None:
                        cam.remove_fixed_orientation_mobjects(o)
                it["mob"] = n
            self.mode = mode

        return anim, commit

    def dispose(self):
        cam = self.scene.renderer.camera if self.is_3d else None
        for m in self.mobs():
            self.scene.remove(m)
            if cam is not None:
                cam.remove_fixed_orientation_mobjects(m)
        self.items = []


def _seg(a, b, **kw):
    if np.linalg.norm(np.asarray(b) - np.asarray(a)) < 1e-3:
        return VGroup()
    return DashedLine(a, b, **kw)


# ======================================================================
# المشهد الثامن (Scene 08) - المدة: 45.0 ثانية (03:35.0 إلى 04:20.0)
# ======================================================================
def play_scene08(scene: Scene):
    is_3d = isinstance(scene, ThreeDScene)
    if is_3d:
        scene.set_camera_orientation(phi=0, theta=-90 * DEGREES)

    mx, my, mz = MOVE

    frame_mobs = [m for m in (getattr(scene, "frame", None), getattr(scene, "neon_overlay", None)) if m is not None]
    if is_3d and frame_mobs:
        _hud(scene, *frame_mobs)

    # 1. التأسيس (2.0s إجمالي)
    title = _ar("الطيارة اتحركت: 3 متر شرق • 4 متر شمال • 5 متر أرتفاع — في 10 ثواني", 22, GOLD_LIGHT).to_edge(UP, buff=0.5).shift(RIGHT * 1.6)
    _hud(scene, title)

    axes = MachAxes3D(
        center=AXES_CENTER, grid_step=UNIT,
        x_range=(0, 6), y_range=(0, 6), z_range=(0, 6), show_negative_arrows=False,
        show_minor_ticks=False, number_font_size=13,
    )
    O = axes.get_origin()

    def P(x, y, z):
        return O + np.array([x, y, z]) * UNIT

    SCREEN_RIGHT = np.array([np.cos(np.radians(35)), np.sin(np.radians(35)), 0.0])

    def ar_label(txt, letter_mob, gap=0.42, color=GOLD_LIGHT):
        t = _ar(txt, 18, color, True)
        t.set_opacity(0.92)
        t.move_to(letter_mob.get_center() + SCREEN_RIGHT * gap)
        return t

    ar_labels = VGroup(
        ar_label("شرق", axes.x_label),
        ar_label("شمال", axes.y_label, gap=0.66),
        ar_label("أرتفاع", axes.z_label, gap=0.40),
    )

    heli = make_helicopter(scale=0.55)
    heli.set_pose(P(0, 0, 0.0), heading=float(np.arctan2(my, mx)))
    heli.start_rotors(scene)

    def rel():
        return (heli._pos - O) / UNIT

    def frac():
        return float(np.clip(rel()[0] / mx, 0, 1))

    # العداد الموحد
    t_label = _ar("الزمن", 22, TIME_COLOR, True)
    t_unit = _ar("ثانية", 22, TIME_COLOR)
    timer_ring = RoundedRectangle(
        corner_radius=0.18, width=2.9, height=1.5,
        stroke_color=TIME_COLOR, stroke_width=2.2, fill_color="#17100A", fill_opacity=0.9,
    ).move_to([4.3, 1.95, 0])
    t_label.move_to(timer_ring.get_top() + DOWN * 0.32)
    t_unit.move_to(timer_ring.get_center() + np.array([0.85, -0.2, 0]))
    timer_static = VGroup(timer_ring, t_label, t_unit)

    slider = MachTimeSlider(center=[4.3, 0.50, 0], width=3.9, t_max=DURATION, number_font_size=18, track_width=7)
    slider.register_hud(scene)
    timer_center = timer_ring.get_center() + np.array([-0.45, -0.17, 0])
    t_live = _LiveNumber(scene, lambda: DURATION * frac(), lambda: timer_center,
                         decimals=1, font_size=56, color=IVORY_WHITE)

    # قائمة الأرقام
    finals = ["3", "4", "5", "10"]
    final_tex = [MathTex(f, font_size=64) for f in finals]
    parts = VGroup(
        MathTex(r"(", font_size=80),
        final_tex[0], MathTex(r",", font_size=64),
        final_tex[1], MathTex(r",", font_size=64),
        final_tex[2], MathTex(r",", font_size=64),
        final_tex[3],
        MathTex(r")", font_size=80),
    ).arrange(RIGHT, buff=0.42, aligned_edge=DOWN).move_to([3.45, -0.85, 0])
    slot_centers = [ft.get_center() for ft in final_tex]
    slot_colors = (SPACE_COLOR, SPACE_COLOR, SPACE_COLOR, TIME_COLOR)

    paren_and_commas = VGroup(*[p for p in parts if p not in final_tex])
    for p in paren_and_commas:
        p.set_color(IVORY_WHITE)

    getters = [lambda: rel()[0], lambda: rel()[1], lambda: rel()[2], lambda: DURATION * frac()]
    slots = [
        _LiveNumber(scene, g, (lambda c=c: c), decimals=0, font_size=64, color=col)
        for g, c, col in zip(getters, slot_centers, slot_colors)
    ]
    slots_group = VGroup(*slots)

    _hud(scene, timer_static, paren_and_commas, slots_group, t_live)

    # [03:35.0 - 03:37.0]: "نرجع لمثال حركة الطيارة..."
    if is_3d:
        scene.add(axes)
        axes.face_camera(scene)
        scene.renderer.camera.add_fixed_orientation_mobjects(*ar_labels)
        scene.move_camera(
            phi=68 * DEGREES, theta=-55 * DEGREES, gamma=-4 * DEGREES, run_time=1.5,
            added_anims=[
                FadeIn(title, shift=DOWN * 0.2),
                FadeIn(heli),
                FadeIn(ar_labels),
                FadeIn(timer_static, shift=LEFT * 0.2),
                FadeIn(t_live),
                FadeIn(slider),
                FadeIn(paren_and_commas),
                FadeIn(slots_group),
            ],
        )
    else:
        scene.add(axes)
        scene.play(FadeIn(title), FadeIn(heli), FadeIn(ar_labels), FadeIn(timer_static), FadeIn(t_live), FadeIn(slider),
                   FadeIn(paren_and_commas), FadeIn(slots_group), run_time=1.5)
    scene.wait(0.5)

    # 2. الطيران وتحليق الهليكوبتر (13.5s إجمالي)
    def drop_lines():
        p = heli._pos
        foot = np.array([p[0], p[1], O[2]])
        fx = np.array([p[0], O[1], O[2]])
        fy = np.array([O[0], p[1], O[2]])
        kw = dict(dash_length=0.08, stroke_width=1.8, stroke_opacity=0.85)
        g = VGroup(
            _seg(p, foot, color=GOLD_LIGHT, **kw),
            _seg(foot, fx, color=GOLD_LIGHT, **kw),
            _seg(foot, fy, color=GOLD_LIGHT, **kw),
        )
        g.set_shade_in_3d(True)
        return g

    def rulers():
        p = heli._pos
        g = VGroup()
        for a, b, col in (
            (O, np.array([p[0], O[1], O[2]]), GOLD_BRIGHT),
            (O, np.array([O[0], p[1], O[2]]), GOLD_BRIGHT),
            (O, np.array([O[0], O[1], p[2]]), GOLD_BRIGHT),
        ):
            if np.linalg.norm(b - a) > 1e-3:
                g.add(Line(a, b, color=col, stroke_width=6, stroke_opacity=0.9))
                g.add(Line(a, b, color=GOLD_LIGHT, stroke_width=14, stroke_opacity=0.15))
        g.set_shade_in_3d(True)
        return g

    def trail():
        p = heli._pos
        if np.linalg.norm(p - O) < 1e-3:
            return VGroup()
        g = VGroup(
            Line(O, p, color=COPPER_TERRA, stroke_width=3.2, stroke_opacity=0.9),
            Line(O, p, color=COPPER_TERRA, stroke_width=9, stroke_opacity=0.14),
        )
        g.set_shade_in_3d(True)
        return g

    drops = always_redraw(drop_lines)
    ruler_mob = always_redraw(rulers)
    trail_mob = always_redraw(trail)
    scene.add(ruler_mob, trail_mob, drops)

    slider.attach(lambda: DURATION * frac())
    goal = P(mx, my, mz)
    path = Line(P(0, 0, 0), goal)

    # [03:37.0 - 03:44.5]: طيران الهليكوبتر بالتزامن مع "اتحركت 3 متر شرق و4 متر شمال ووصلت لـ 5 متر ارتفاع في 10 ثواني"
    scene.play(
        fly_along_3d(heli, path, run_time=FLIGHT_TIME, rate_func=smooth, nose_down=0.12),
    )
    
    for sl in slots:
        sl.clear_updaters()
    t_live.clear_updaters()
    slider.detach()
    slider.set_time(DURATION)
    scene.play(slider.finish_animation(), run_time=0.8)
    scene.wait(1.2)

    m_nums = VGroup(*[
        MathTex(str(v), font_size=64, color=col).move_to(sc)
        for v, sc, col in zip(list(MOVE) + [DURATION], slot_centers, slot_colors)
    ])
    _hud(scene, m_nums)
    
    scene.remove(slots_group, t_live)
    for sl in slots:
        sl.dispose(scene)
    t_live.dispose(scene)

    scene.add(m_nums)
    
    t_num_static = MathTex("10.0", font_size=56, color=IVORY_WHITE).move_to(timer_center)
    _hud(scene, t_num_static)
    timer_static.add(t_num_static)
    scene.add(t_num_static)

    # [03:46.5 - 03:50.5]: "انا هنا محتاج قائمة من اربع ارقام تعبر عن حركة الطيارة..."
    scene.play(*[Indicate(m, scale_factor=1.25, color=col) for m, col in zip(m_nums, slot_colors)], run_time=1.0)
    scene.wait(3.0)

    # 3. معنى كل خانة (18.5s إجمالي)
    heli.stop_rotors(scene)

    names = ["شرق", "شمال", "أرتفاع", "زمن"]
    name_cols = [SPACE_COLOR, SPACE_COLOR, SPACE_COLOR, TIME_COLOR]
    name_txt = VGroup(*[
        _ar(n, 22, c, True).next_to(ft, DOWN, buff=0.35)
        for n, c, ft in zip(names, name_cols, final_tex)
    ])
    _hud(scene, name_txt)

    # [03:50.5 - 04:01.0]: "والقايمة دي هي (3, 4, 5, 10)... وكل رقم من دول بيعبر عن قيمة لخاصية او لصفة معينة للحركة"
    scene.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in name_txt], lag_ratio=0.35), run_time=2.0)
    scene.wait(8.5)

    left_x = final_tex[0].get_left()[0] - 0.05
    mid_x = final_tex[2].get_right()[0] + 0.05
    y_b = name_txt.get_bottom()[1] - 0.12
    br_space = Brace(Line([left_x, y_b, 0], [mid_x, y_b, 0]), direction=DOWN, color=SPACE_COLOR, buff=0.05)
    br_time = Brace(Line([final_tex[3].get_left()[0] - 0.05, y_b, 0], [final_tex[3].get_right()[0] + 0.05, y_b, 0]),
                    direction=DOWN, color=TIME_COLOR, buff=0.05)
    cap_space = _ar("3 أرقام للمكان", 19, SPACE_COLOR).next_to(br_space, DOWN, buff=0.12)
    cap_time = _ar("رقم للزمن", 19, TIME_COLOR).next_to(br_time, DOWN, buff=0.12)
    brs = VGroup(br_space, br_time, cap_space, cap_time)
    _hud(scene, brs)

    # [04:01.0 - 04:09.0]: "وفي مثالنا ده عندنا تلات ارقام بنصف بيهم الحركة في المكان ورقم واحد بنصف بيه تطور الحركة عبر الزمن"
    scene.play(Create(br_space), Create(br_time), FadeIn(cap_space), FadeIn(cap_time), run_time=1.5)
    scene.wait(6.5)

    # 4. الرقم الرابع (9.0s إجمالي)
    # [04:09.0 - 04:18.0]: "وفي الطريقة دي عبرنا عن المتجه بليست من اربع ارقام وقدرنا نتغلب على عدد الابعاد المحدود في طريقة السهم"
    box4 = SurroundingRectangle(m_nums[3], buff=0.18, color=TIME_COLOR, stroke_width=3, corner_radius=0.12)
    q = _ar("مفيش محور رابع أرسمه!", 21, TIME_COLOR, True)
    q.move_to([4.3, 0.40, 0])
    pointer = Arrow(q.get_bottom() + DOWN * 0.05, box4.get_top() + UP * 0.05, buff=0.05,
                    color=TIME_COLOR, stroke_width=3, max_tip_length_to_length_ratio=0.25)
    _hud(scene, box4, q, pointer)
    
    scene.play(FadeOut(slider), Create(box4), FadeIn(q, shift=DOWN * 0.1), GrowArrow(pointer), run_time=1.2)
    _clear(scene, slider)
    if is_3d:
        scene.renderer.camera.remove_fixed_in_frame_mobjects(slider)
        for sub in slider.get_family():
            scene.renderer.camera.remove_fixed_in_frame_mobjects(sub)

    scene.wait(7.8)

    # 5. تسليم المشهد: تثبيت الرسمة الثلاثية الأبعاد وتسليمها للمشهد التاسع (2.0s إجمالي)
    # [04:18.0 - 04:20.0]: سكتة تسليم للمشهد التاسع
    ruler_mob.clear_updaters()
    trail_mob.clear_updaters()
    drops.clear_updaters()

    leaving_mobs = [title, brs, box4, q, pointer]
    scene.play(*[FadeOut(m) for m in leaving_mobs], run_time=1.0)
    _clear(scene, *leaving_mobs)
    scene.wait(1.0)

    # حفظ الكائنات لتكمل في المشهدين 9 و 10
    scene.mach_drawing = {
        "axes": axes,
        "O": O,
        "P_func": P,
        "goal": goal,
        "heli": heli,
        "ar_labels": ar_labels,
        "rulers": ruler_mob,
        "trail": trail_mob,
        "drops": drops,
        "timer_static": timer_static,
        "paren_and_commas": paren_and_commas,
        "slot_centers": slot_centers,
        "slot_colors": slot_colors,
        "name_txt": name_txt,
        "m_nums": m_nums,
    }
    # المجموع: 2.0 + 13.5 + 18.5 + 9.0 + 2.0 = 45.0 ثانية بالتمام والكمال!


# ======================================================================
# المشهد التاسع (Scene 09) - المدة: 37.0 ثانية (04:20.0 إلى 04:57.0)
# ======================================================================
def play_scene09(scene: Scene, keep_drawing: bool = True):
    is_3d = isinstance(scene, ThreeDScene)
    mx, my, mz = MOVE
    frame_mobs = [m for m in (getattr(scene, "frame", None), getattr(scene, "neon_overlay", None)) if m is not None]

    if not hasattr(scene, "mach_drawing"):
        play_scene08(scene)

    st = scene.mach_drawing
    axes, O, P, goal = st["axes"], st["O"], st["P_func"], st["goal"]
    heli, ar_labels = st["heli"], st["ar_labels"]
    rulers, trail, drops = st["rulers"], st["trail"], st["drops"]
    timer_static = st["timer_static"]
    paren_and_commas = st["paren_and_commas"]
    slot_centers = st["slot_centers"]
    slot_colors = st["slot_colors"]
    name_txt = st["name_txt"]
    m_nums = st["m_nums"]

    # 1. العنوان + شريحة وحدة المسافة (13.0s إجمالي)
    # [04:20.0 - 04:33.0]: "لكن ماذا لو قولتلك ان هي هي نفس الطيارة اتحركت 300 سنتيمتر شرق و400 شمال و500 ارتفاع في 10 ثواني"
    title = _ar("نفس الطيارة • نفس الحركة بالظبط — بس غيّرنا وحدة قياس المسافة", 22, GOLD_LIGHT).to_edge(UP, buff=0.5).shift(RIGHT * 1.6)
    _hud(scene, title)

    chip_ring = RoundedRectangle(
        corner_radius=0.2, width=3.9, height=0.72,
        stroke_color=GOLD_LIGHT, stroke_width=2.2, fill_color="#17100A", fill_opacity=0.9,
    ).move_to([4.3, 0.50, 0])
    chip_title = _ar("وحدة المسافة:", 19, GOLD_LIGHT).move_to(chip_ring.get_center() + np.array([0.95, 0, 0]))
    chip_value = _ar("متر", 24, SPACE_COLOR, True).move_to(chip_ring.get_center() + np.array([-0.85, 0, 0]))
    chip_static = VGroup(chip_ring, chip_title)
    _hud(scene, chip_static, chip_value)

    CF = 64
    cm_vals = [str(v * SCALE) for v in MOVE] + [str(DURATION)]
    cm_tex = [MathTex(v, font_size=CF, color=c) for v, c in zip(cm_vals, slot_colors)]
    cm_parts = VGroup(
        MathTex(r"(", font_size=CF + 16),
        cm_tex[0], MathTex(r",", font_size=CF),
        cm_tex[1], MathTex(r",", font_size=CF),
        cm_tex[2], MathTex(r",", font_size=CF),
        cm_tex[3],
        MathTex(r")", font_size=CF + 16),
    ).arrange(RIGHT, buff=0.34, aligned_edge=DOWN).move_to([3.45, -0.85, 0])
    cm_centers = [t.get_center() for t in cm_tex]
    cm_pc = VGroup(*[p for p in cm_parts if p not in cm_tex])
    for p in cm_pc:
        p.set_color(IVORY_WHITE)
    cm_names = VGroup(*[
        _ar(n, 22, c, True).next_to(MathTex("0").move_to(sc), DOWN, buff=0.35)
        for n, c, sc in zip(["شرق", "شمال", "أرتفاع", "زمن"], slot_colors, cm_centers)
    ])
    _hud(scene, *cm_tex)

    ticks = st.get("ticks")
    if ticks is None:
        ticks = _TickLabels(scene, axes, O)
        st["ticks"] = ticks

    scene.play(
        FadeIn(title, shift=DOWN * 0.15),
        FadeIn(chip_static, shift=UP * 0.1),
        FadeIn(chip_value, shift=UP * 0.1),
        run_time=1.2,
    )
    scene.wait(2.8)

    flash_path = Line(O, goal, color=GOLD_BRIGHT, stroke_width=9).set_shade_in_3d(True)
    scene.play(ShowPassingFlash(flash_path, time_width=0.7), run_time=1.5)
    scene.wait(7.5)

    # 3. التحويل إلى سنتيمتر (7.0s إجمالي)
    # [04:33.0 - 04:40.0]: "هنا المتجه اللي بيعبر عن نفس الحركة هيكون ليست او قائمة مكونة من الاربع ارقام دول (300, 400, 500, 10)"
    chip_value_new = _ar("سنتيمتر", 24, COPPER_TERRA, True).move_to(chip_value)
    _hud(scene, chip_value_new)

    tags = VGroup(*[
        MathTex(r"\times 100", font_size=30, color=COPPER_TERRA).move_to(sc + np.array([0, 0.78, 0]))
        for sc in slot_centers[:3]
    ])
    _hud(scene, tags)

    scene.play(
        FadeOut(chip_value, shift=UP * 0.2),
        FadeIn(chip_value_new, shift=UP * 0.2),
        chip_ring.animate.set_stroke(COPPER_TERRA),
        run_time=1.0,
    )
    scene.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tags], lag_ratio=0.25), run_time=1.0)

    tick_anim, tick_commit = ticks.retarget("cm")
    scene.play(
        *[FadeOut(m_nums[i], shift=UP * 0.18) for i in range(3)],
        *[FadeIn(cm_tex[i], shift=UP * 0.18) for i in range(3)],
        Transform(paren_and_commas, cm_pc),
        Transform(name_txt, cm_names),
        m_nums[3].animate.move_to(cm_centers[3]),
        tick_anim,
        run_time=2.0,
    )
    tick_commit()
    scene.play(FadeOut(tags), run_time=0.4)
    scene.play(FadeOut(m_nums[3]), FadeIn(cm_tex[3]), run_time=0.4)

    flash_path2 = Line(O, goal, color=GOLD_BRIGHT, stroke_width=9).set_shade_in_3d(True)
    scene.play(ShowPassingFlash(flash_path2, time_width=0.7), run_time=1.2)
    scene.wait(1.0)

    # 4. تثبيت الزمن (14.0s إجمالي)
    # [04:40.0 - 04:54.0]: "انا هنا غيرت وحدات القياس الخاصة بالمسافة بس.. انت ممكن تغير وحدة قياس الزمن عادي... وده كفاية لتوضيح الفكرة"
    box_t = SurroundingRectangle(cm_tex[3], buff=0.18, color=TIME_COLOR, stroke_width=3, corner_radius=0.12)
    note = _ar("الزمن زي ما هو — غيّرنا وحدة المسافة بس", 20, TIME_COLOR, True).move_to([3.45, -2.55, 0])
    _hud(scene, box_t, note)
    scene.play(Create(box_t), FadeIn(note, shift=UP * 0.1), run_time=1.2)
    scene.wait(12.8)

    # 5. الخروج (3.0s إجمالي)
    # [04:54.0 - 04:57.0]: سكتة تسليم للمشهد العاشر
    hud_outs = [title, chip_static, chip_value_new, paren_and_commas, VGroup(*cm_tex), name_txt, box_t, note]

    if keep_drawing:
        tick_anim, tick_commit = ticks.retarget("m")
        scene.play(*[FadeOut(m) for m in hud_outs], tick_anim, run_time=1.8)
        tick_commit()
        _clear(scene, *hud_outs, chip_value, tags, *m_nums)
        scene.wait(1.2)
        return

    outs = [title, axes, heli, ar_labels, rulers, trail, drops, timer_static, chip_static, chip_value_new,
            paren_and_commas, VGroup(*cm_tex), name_txt, box_t, note] + ticks.mobs()
    if is_3d:
        scene.move_camera(phi=0, theta=-90 * DEGREES, gamma=0, run_time=1.8,
                          added_anims=[FadeOut(m) for m in outs])
    else:
        scene.play(*[FadeOut(m) for m in outs], run_time=1.8)
    heli.stop_rotors(scene)
    ticks.dispose()
    _clear(scene, *outs, chip_value, tags, *m_nums)
    del scene.mach_drawing
    if is_3d and frame_mobs:
        scene.renderer.camera.remove_fixed_in_frame_mobjects(*frame_mobs)
    scene.wait(1.2)
    # المجموع: 13.0 + 7.0 + 14.0 + 3.0 = 37.0 ثانية بالتمام والكمال!


# ======================================================================
# المشهد العاشر (Scene 10) - المدة: 39.0 ثانية (04:57.0 إلى 05:36.0)
# ======================================================================
def play_scene10(scene: Scene, keep_drawing: bool = True):
    is_3d = isinstance(scene, ThreeDScene)
    frame_mobs = [m for m in (getattr(scene, "frame", None), getattr(scene, "neon_overlay", None)) if m is not None]

    if not hasattr(scene, "mach_drawing"):
        play_scene09(scene, keep_drawing=True)

    st = scene.mach_drawing
    axes, heli, ar_labels = st["axes"], st["heli"], st["ar_labels"]
    rulers, trail, drops, O = st["rulers"], st["trail"], st["drops"], st["O"]
    goal = st["goal"]
    timer_static = st["timer_static"]
    ticks = st.get("ticks")
    if ticks is None:
        ticks = _TickLabels(scene, axes, O)
        st["ticks"] = ticks

    # 1. عناصر الشاشة بتنسيق متسع للأرقام العشرية (7.0s إجمالي)
    # [04:57.0 - 05:04.0]: "بل ممكن اخترع اي وحدة قياس على مزاجي عشان اوصف بيها المسافة ووحدة القياس دي احددلها اي قيمة انا عاوزها"
    title = _ar("بل أقدر أخترع وحدة قياس على مزاجي!", 22, GOLD_LIGHT).to_edge(UP, buff=0.5).shift(RIGHT * 1.6)
    _hud(scene, title)

    chip_ring = RoundedRectangle(
        corner_radius=0.2, width=3.9, height=0.72,
        stroke_color=GOLD_LIGHT, stroke_width=2.2, fill_color="#17100A", fill_opacity=0.9,
    ).move_to([4.3, 0.50, 0])
    chip_title = _ar("وحدة المسافة:", 19, GOLD_LIGHT).move_to(chip_ring.get_center() + np.array([0.95, 0, 0]))
    chip_value = _ar("متر", 24, SPACE_COLOR, True).move_to(chip_ring.get_center() + np.array([-0.85, 0, 0]))
    chip_static = VGroup(chip_ring, chip_title)
    _hud(scene, chip_static, chip_value)

    FS = 40
    new_tex = [MathTex(v, font_size=FS) for v in PLANK_VALUES] + [MathTex(str(DURATION), font_size=FS)]
    parts = VGroup(
        MathTex(r"(", font_size=FS + 14),
        new_tex[0], MathTex(r",", font_size=FS),
        new_tex[1], MathTex(r",", font_size=FS),
        new_tex[2], MathTex(r",", font_size=FS),
        new_tex[3],
        MathTex(r")", font_size=FS + 14),
    ).arrange(RIGHT, buff=0.2, aligned_edge=DOWN).move_to([3.7, -1.0, 0])
    slot_centers = [t.get_center() for t in new_tex]
    slot_colors = (SPACE_COLOR, SPACE_COLOR, SPACE_COLOR, TIME_COLOR)
    paren_and_commas = VGroup(*[p for p in parts if p not in new_tex])
    for p in paren_and_commas:
        p.set_color(IVORY_WHITE)

    m_nums = [MathTex(str(v), font_size=FS, color=c).move_to(sc)
              for v, sc, c in zip(list(MOVE) + [DURATION], slot_centers, slot_colors)]
    n_nums = [t.set_color(NEW_COLOR if i < 3 else TIME_COLOR) for i, t in enumerate(new_tex)]

    names = ["شرق", "شمال", "أرتفاع", "زمن"]
    name_txt = VGroup(*[
        _ar(n, 20, c, True).next_to(MathTex("0").move_to(sc), DOWN, buff=0.35)
        for n, c, sc in zip(names, slot_colors, slot_centers)
    ])

    plank_bar = Rectangle(width=1.5, height=0.2, stroke_color=NEW_COLOR, stroke_width=2.5,
                          fill_color=NEW_COLOR, fill_opacity=0.28)
    plank_ticks = VGroup(*[Line(plank_bar.get_left() + RIGHT * 1.5 * k / 3.9 * 1.0 + UP * 0.1,
                                plank_bar.get_left() + RIGHT * 1.5 * k / 3.9 * 1.0 + DOWN * 0.1,
                                color=NEW_COLOR, stroke_width=1.5, stroke_opacity=0.7)
                           for k in (1, 2, 3)])
    plank_lbl = _ar("1 " + UNIT_NAME, 22, NEW_COLOR, True)
    eq_lbl = VGroup(
        _ar("3.9 متر", 22, IVORY_WHITE, True),
        MathTex("=", font_size=34, color=IVORY_WHITE),
    ).arrange(RIGHT, buff=0.15)
    plank_card = VGroup(plank_bar, plank_ticks)
    plank_row = VGroup(eq_lbl, plank_lbl).arrange(RIGHT, buff=0.15)
    plank_all = VGroup(plank_card, plank_row).arrange(DOWN, buff=0.22).move_to([4.3, -2.85, 0])

    _hud(scene, title, chip_static, chip_value, paren_and_commas, name_txt,
         *m_nums, *n_nums, plank_all)

    scene.play(
        FadeIn(title, shift=DOWN * 0.15),
        FadeIn(chip_static, shift=UP * 0.1),
        FadeIn(chip_value, shift=UP * 0.1),
        FadeIn(paren_and_commas),
        *[FadeIn(n) for n in m_nums],
        FadeIn(name_txt),
        run_time=1.2,
    )
    scene.wait(5.8)

    # 3. تعريف الوحدة الجديدة ("الخشبة") (10.0s إجمالي)
    # [05:04.0 - 05:14.0]: "زي اني اخترع وحدة قياس طولها مثلا 3.9 متر واسميها وحدة الخشبة مثلا او اي اسم على مزاجي برضو مش هتفرق"
    scene.play(FadeIn(plank_all, shift=UP * 0.15), run_time=1.5)
    scene.wait(8.5)

    # 4. التحويل: متر → الخشبة (8.0s إجمالي)
    # [05:14.0 - 05:22.0]: "واكتبلك التلات ارقام اللي بصف بيهم المسافة اللي اتحركتها الطيارة بدلالة وحدة القياس الجديدة دي"
    chip_value_new = _ar(UNIT_NAME, 24, NEW_COLOR, True).move_to(chip_value)
    _hud(scene, chip_value_new)

    tags = VGroup(*[
        MathTex(r"\div 3.9", font_size=26, color=NEW_COLOR).move_to(sc + np.array([0, 0.72, 0]))
        for sc in slot_centers[:3]
    ])
    _hud(scene, tags)

    scene.play(
        FadeOut(chip_value, shift=UP * 0.2), FadeIn(chip_value_new, shift=UP * 0.2),
        chip_ring.animate.set_stroke(NEW_COLOR),
        run_time=0.8,
    )
    scene.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tags], lag_ratio=0.25), run_time=0.8)
    
    tick_anim, tick_commit = ticks.retarget("plank")
    scene.play(
        *[FadeOut(m_nums[i], shift=UP * 0.18) for i in range(3)],
        *[FadeIn(n_nums[i], shift=UP * 0.18) for i in range(3)],
        tick_anim,
        run_time=1.8,
    )
    tick_commit()
    scene.play(FadeOut(tags), run_time=0.4)
    scene.play(FadeOut(m_nums[3]), FadeIn(n_nums[3]), run_time=0.4)

    flash = Line(O, goal, color=GOLD_BRIGHT, stroke_width=9).set_shade_in_3d(True)
    scene.play(ShowPassingFlash(flash, time_width=0.7), run_time=1.0)

    box_t = SurroundingRectangle(n_nums[3], buff=0.16, color=TIME_COLOR, stroke_width=3, corner_radius=0.12)
    _hud(scene, box_t)
    scene.play(Create(box_t), run_time=0.8)
    scene.wait(2.0)

    # [05:22.0 - 05:33.0]: (11.0s) "وعايز اقول ملحوظة هنا: ان الحركة اللي عملتها دي من تغيير وحدات القياس والمساطر بيسموها في الجبر الخطي تغيير الاساس بس مش وقتها هنا دلوقتي"
    scene.wait(11.0)

    # 5. الخروج النهائي للمشهد العاشر (3.0s إجمالي)
    # [05:33.0 - 05:36.0]: سكتة تسليم للمشهد الحادي عشر عند 05:36.0
    hud_outs = [title, timer_static, chip_static, chip_value_new, paren_and_commas,
                VGroup(*n_nums), name_txt, plank_all, box_t]

    if keep_drawing and is_3d:
        scene.play(*[FadeOut(m) for m in hud_outs], run_time=1.8)
        _clear(scene, *hud_outs, chip_value, tags, *m_nums)
        scene.wait(1.2)
        return

    outs = [axes, heli, ar_labels, rulers, trail, drops] + hud_outs + ticks.mobs()
    if is_3d:
        scene.move_camera(phi=0, theta=-90 * DEGREES, gamma=0, run_time=1.8,
                          added_anims=[FadeOut(m) for m in outs])
    else:
        scene.play(*[FadeOut(m) for m in outs], run_time=1.8)

    heli.stop_rotors(scene)
    ticks.dispose()
    _clear(scene, *outs, chip_value, tags, *m_nums)
    if hasattr(scene, "mach_drawing"):
        del scene.mach_drawing
    if is_3d and frame_mobs:
        scene.renderer.camera.remove_fixed_in_frame_mobjects(*frame_mobs)
    scene.wait(1.2)
    # المجموع: 7.0 + 10.0 + 8.0 + 11.0 + 3.0 = 39.0 ثانية بالتمام والكمال!