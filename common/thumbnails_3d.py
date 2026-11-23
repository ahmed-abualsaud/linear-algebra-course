"""
مشهد "أمثلة لتوضيح المتجهات" (الحلقة 03): رسمة ثلاثية الأبعاد سينمائية + العنوان + القوائم الثلاث.
الاستخدام (داخل ThreeDScene):
    from common.thumbnails_3d import *
    build_vector_examples(self, ltr=False, line1=..., line2=..., badge_text=..., axis_names=(...),
                          line1_width=..., line2_width=..., room=True)

المنطق:
  - الرسمة بتتحجّم وتتمركز تلقائياً جوه منطقة محددة من الشاشة (REGION_RTL / REGION_LTR) بحساب الإسقاط الفعلي للكاميرا.
    الحساب على الرسمة الأساسية فقط (المحاور + الهليكوبتر + اسم Z)؛ الغرفة بتتمدد حواليها من غير ما تصغّرها.
  - RTL: الرسمة على الشمال والعنوان على اليمين. LTR: العكس.
  - الكاميرا شبه متعامدة (focal_distance كبير) وgamma=0 عشان المحور الرأسي يفضل رأسي في أي مكان على الشاشة.
  - room=True: غرفة سينمائية = جداران خلفيان زجاجيان بتدرج وشبكة بتخفت، وحواف ذهبية متوهجة، وعقد في الأركان.
    + ظل الهليكوبتر على الأرض بحلقات teal، + توهجات خلفية دافئة وteal. room=False: الرسمة القديمة النظيفة.
  - كل عناصر الغرفة shade_in_3d عشان تترسم بالعمق (خلف الهليكوبتر والمسار)، لأن manim بيرسم غير كده كل العناصر
    العادية فوق المجسمات.
"""
from manim import *
import numpy as np

from common.palette import (
    GOLD_BRIGHT, GOLD_LIGHT, GOLD, GOLD_MUTED, STONE_AXIS, COPPER_TERRA, IVORY_WHITE, TEAL,
)
from common.latex import mach_math_template
from common.thumbnails import *
from common.mobjects.coordinate_systems import MachAxes3D
from common.mobjects.helicopter import make_helicopter

# نفس الحركة بثلاث قوائم مختلفة (المتر، السنتيمتر، الخشبة مع الزمن)
LISTS = [
    (r"(3,\;4,\;5,\;10)", GOLD_BRIGHT),
    (r"(300,\;400,\;500,\;10)", COPPER_TERRA),
    (r"(0.769,\;1.025,\;1.282,\;10)", TEAL_LIGHT),
]
LIST_WIDTH = 2.45  # العرض الأساسي لضبط تناسق حجم الخط

# الكاميرا: gamma=0 وبُعد بؤري كبير جداً (شبه متعامد) عشان المحور الرأسي يفضل رأسي مهما كان مكان الرسمة على الشاشة.
# (المنظور القديم focal_distance=20 مع gamma=-4 كان بيميّل المحور ~-2° في العربي و+4° في الإنجليزي.)
CAM = dict(phi=68 * DEGREES, theta=-55 * DEGREES, gamma=0, focal_distance=1000)

MOVE = (3, 4, 5)
N = 6  # طول كل محور بوحدات الشبكة
UNIT0 = 0.54
AXES_CENTER_FALLBACK = np.array([-1.9, -2.6, -1.60])

# المنطقة اللي الرسمة بتتحجّم جواها: (x0, x1, y0, y1) بوحدات الشاشة
# (القمة 3.05 عشان اسم Z يفضل بعيد عن اسم القناة؛ الجدران نفسها بتوصل لحوالي 3.3 = نفس padding الإطار)
REGION_RTL = (-6.30, 0.80, -3.35, 3.05)
REGION_LTR = (-0.55, 6.55, -3.35, 3.05)  # مزاحة 0.25 يمين عن المتماثل؛ أقرب مسافة لاسم القناة (UR) ~0.26 للجدار و~0.44 للمروحة

# نقاط الرسمة الأساسية بوحدات المحاور (نهايات المحاور + الأسهم + ركن الأرضية + الهدف + اسم Z + قمة الهليكوبتر)
FIT_POINTS = np.array([
    [0, 0, 0], [6.6, 0, 0], [0, 6.6, 0], [0, 0, 6.6],
    [6, 0, 0], [0, 6, 0], [6, 6, 0], [3, 4, 5],
    [0, 0, 7.4], [3, 4, 6.5],
], dtype=float)


# ---------------------------------------------------------------- حساب الحجم والمكان
def _project(scene, pts):
    """إسقاط نقاط العالم على الشاشة بنفس كاميرا المشهد (x, y فقط)."""
    cam = scene.renderer.camera
    reset = getattr(cam, "reset_rotation_matrix", None)
    if callable(reset):
        reset()
    out = cam.project_points(np.array(pts, dtype=float))
    return np.asarray(out)[:, :2]


def fit_3d_to_region(scene, region, unit0=UNIT0, pad=0.15, max_unit=0.95, iters=4, points=FIT_POINTS):
    """يرجّع (center, unit) بحيث صندوق الرسمة على الشاشة يتمركز في region ويملاه."""
    x0, x1, y0, y1 = region
    target = np.array([(x0 + x1) / 2, (y0 + y1) / 2])
    C = np.zeros(3)

    sp = _project(scene, points * unit0 + C)
    w, h = np.ptp(sp[:, 0]), np.ptp(sp[:, 1])
    unit = min(unit0 * min((x1 - x0 - 2 * pad) / w, (y1 - y0 - 2 * pad) / h), max_unit)

    eps = 0.05
    for _ in range(iters):
        sp = _project(scene, points * unit + C)
        cur = (sp.min(axis=0) + sp.max(axis=0)) / 2
        base = _project(scene, [C])[0]
        J = np.stack([(_project(scene, [C + eps * e])[0] - base) / eps for e in np.eye(3)], axis=1)
        C = C + np.linalg.pinv(J) @ (target - cur)
    return C, unit


def _hud(scene, *mobs):
    scene.renderer.camera.add_fixed_in_frame_mobjects(*mobs)
    scene.add(*mobs)


def _rot(scene):
    return scene.renderer.camera.get_rotation_matrix()


def _screen_vec(scene, dx, dy):
    """متجه في العالم بيتحوّل لإزاحة (dx, dy) بالظبط على الشاشة (الكاميرا شبه متعامدة)."""
    return _rot(scene).T @ np.array([dx, dy, 0.0])


# ---------------------------------------------------------------- عناصر سينمائية
def _behind_glow(scene, world_pt, radius, color, peak, layers=16, depth=9.0):
    """توهج ناعم مسطّح بيواجه الكاميرا ومرسوم خلف كل حاجة (بيتحط بعيد على خط النظر)."""
    toward_cam = _rot(scene)[2]
    pt = np.asarray(world_pt, float) - toward_cam * depth
    g = soft_glow(pt, radius, color, layers=layers, peak=peak)
    g.set_shade_in_3d(True, z_index_as_group=True)
    scene.renderer.camera.add_fixed_orientation_mobjects(g)
    return g


def build_room(O, s, n=N, show_edges=False):
    """
    غرفة سينمائية: جداران خلفيان (x=0 وy=n) بتدرج زجاجي وشبكة بتخفت بعيداً عن الركن، وحواف ذهبية متوهجة وعقد.
    كل جزء له مجموعة بمرجع عمق خاص فيترسم خلف الهليكوبتر والمسار.
    """
    W = lambda x, y, z: O + np.array([x, y, z], float) * s
    parts = []
    bands = 10

    def fade_h(k):
        return 0.22 - 0.12 * (k / n)

    # ---- الجدار الخلفي A: المستوى y = n
    wall_a = VGroup()
    for k in range(bands):
        z0, z1 = n * k / bands, n * (k + 1) / bands
        op = 0.085 * (1 - k / bands) ** 1.2 + 0.012
        wall_a.add(Polygon(W(0, n, z0), W(n, n, z0), W(n, n, z1), W(0, n, z1),
                           stroke_width=0, fill_color=STONE_AXIS, fill_opacity=op))
    for i in range(0, n + 1):
        wall_a.add(Line(W(i, n, 0), W(i, n, n), color=GOLD_LIGHT, stroke_width=1.0,
                        stroke_opacity=0.22 - 0.12 * (i / n)))
    for k in range(1, n + 1):
        wall_a.add(Line(W(0, n, k), W(n, n, k), color=GOLD_LIGHT, stroke_width=1.0, stroke_opacity=fade_h(k)))
    wall_a.set_shade_in_3d(True, z_index_as_group=True)
    parts.append(wall_a)

    # ---- الجدار الخلفي B: المستوى x = 0 (بيحتوي محوري Y وZ فبنتخطى خطوطهم)
    wall_b = VGroup()
    for k in range(bands):
        z0, z1 = n * k / bands, n * (k + 1) / bands
        op = 0.085 * (1 - k / bands) ** 1.2 + 0.012
        wall_b.add(Polygon(W(0, 0, z0), W(0, n, z0), W(0, n, z1), W(0, 0, z1),
                           stroke_width=0, fill_color=STONE_AXIS, fill_opacity=op))
    for j in range(1, n + 1):
        wall_b.add(Line(W(0, j, 0), W(0, j, n), color=GOLD_LIGHT, stroke_width=1.0,
                        stroke_opacity=0.10 + 0.12 * (j / n)))
    for k in range(1, n + 1):
        wall_b.add(Line(W(0, 0, k), W(0, n, k), color=GOLD_LIGHT, stroke_width=1.0, stroke_opacity=fade_h(k)))
    wall_b.set_shade_in_3d(True, z_index_as_group=True)
    parts.append(wall_b)

    if show_edges:
        # ---- الحواف الذهبية المتوهجة (طبقتين: هالة عريضة + خط رفيع)
        edges = [
            ((0, n, 0), (0, n, n)),   # حرف الركن الرأسي
            ((0, n, n), (0, 0, n)),   # أعلى الجدار B
            ((0, n, n), (n, n, n)),   # أعلى الجدار A
            ((n, n, 0), (n, n, n)),   # الحرف الأيمن للجدار A
            ((0, n, 0), (n, n, 0)),   # حرف الأرضية الخلفي
        ]
        for a, b in edges:
            e = VGroup(
                Line(W(*a), W(*b), color=GOLD, stroke_width=9, stroke_opacity=0.07),
                Line(W(*a), W(*b), color=GOLD_LIGHT, stroke_width=2.2, stroke_opacity=0.55),
            )
            e.set_shade_in_3d(True, z_index_as_group=True)
            parts.append(e)

        # ---- العقد الصغيرة في الأركان
        for c in ((0, n, n), (n, n, n), (n, n, 0), (0, n, 0)):
            parts.append(Dot3D(W(*c), radius=0.05, color=GOLD_LIGHT))
    return parts


def build_floor_shadow(foot, s):
    """ظل الهليكوبتر على الأرض + حلقتا هدف teal حوالين نقطة الإسقاط."""
    shadow = VGroup(
        Circle(radius=0.85 * s, stroke_width=0, fill_color="#000000", fill_opacity=0.34),
        Circle(radius=0.55 * s, stroke_width=0, fill_color="#000000", fill_opacity=0.30),
        Circle(radius=1.15 * s, stroke_color=TEAL_LIGHT, stroke_width=2.0, stroke_opacity=0.55, fill_opacity=0),
        Circle(radius=1.65 * s, stroke_color=TEAL, stroke_width=1.2, stroke_opacity=0.28, fill_opacity=0),
    ).move_to(foot)
    shadow.set_shade_in_3d(True, z_index_as_group=True)
    return shadow


# ---------------------------------------------------------------- المشهد
def build_vector_examples(scene, ltr, line1, line2, badge_text, axis_names,
                          line1_width, line2_width, badge_width=3.5, lists=LISTS, room=True, room_edges=False, vec_label=True):
    scene.camera.background_color = THUMB_BG
    scene.set_camera_orientation(**CAM)

    region = REGION_LTR if ltr else REGION_RTL
    try:
        center, unit = fit_3d_to_region(scene, region)
        if not (np.all(np.isfinite(center)) and 0.3 < unit < 1.2):
            raise ValueError("bad fit")
    except Exception:
        center, unit = AXES_CENTER_FALLBACK.copy(), UNIT0

    # ---------------- الرسمة ثلاثية الأبعاد
    axes = MachAxes3D(
        center=center, grid_step=unit,
        x_range=(0, N), y_range=(0, N), z_range=(0, N),
        show_negative_arrows=False, show_minor_ticks=False, number_font_size=14,
        show_back_walls=False, floor_opacity=0.06, grid_opacity=0.55,
    )
    O = axes.get_origin()
    P = lambda x, y, z: O + np.array([x, y, z]) * unit
    goal = P(*MOVE)

    heli = make_helicopter(scale=0.74 * unit / UNIT0)
    climb = np.arctan2(MOVE[2], np.hypot(MOVE[0], MOVE[1]))
    heli.set_pose(goal, heading=float(np.arctan2(MOVE[1], MOVE[0])), bank=0.0, pitch=0.12 - 0.6 * climb)

    trail = VGroup(
        Line(O, goal, color=COPPER_TERRA, stroke_width=5.0, stroke_opacity=0.95),
        Line(O, goal, color=COPPER_TERRA, stroke_width=16, stroke_opacity=0.25),
    )
    trail.set_shade_in_3d(True)

    # أرضية الإسقاط (teal) + خطوط الإسقاط المنقطة + عقد الإسقاط على المحورين
    foot = np.array([goal[0], goal[1], O[2]])
    fx = np.array([goal[0], O[1], O[2]])
    fy = np.array([O[0], goal[1], O[2]])
    floor_fill = Polygon(O, fx, foot, fy, stroke_color=TEAL, stroke_width=2.0, stroke_opacity=0.75,
                         fill_color=TEAL, fill_opacity=0.16)
    floor_fill.set_shade_in_3d(True)
    kw = dict(dash_length=0.09, stroke_width=2.2, stroke_opacity=0.9, color=TEAL_LIGHT)
    drops = VGroup(
        DashedLine(goal, foot, **kw),
        DashedLine(foot, fx, **kw),
        DashedLine(foot, fy, **kw),
        Dot3D(foot, radius=0.06, color=TEAL_LIGHT),
        Dot3D(fx, radius=0.05, color=TEAL_LIGHT),
        Dot3D(fy, radius=0.05, color=TEAL_LIGHT),
    ).set_shade_in_3d(True)
    shadow = build_floor_shadow(foot, unit)

    rulers = VGroup(
        Line(O, fx, color=GOLD_BRIGHT, stroke_width=6.5),
        Line(O, fy, color=GOLD_BRIGHT, stroke_width=6.5),
        Line(O, np.array([O[0], O[1], goal[2]]), color=GOLD_BRIGHT, stroke_width=6.5),
    ).set_shade_in_3d(True)

    # توهجات خلفية: دافئ ورا الهليكوبتر وteal ورا أرضية الإسقاط
    glows = [
        _behind_glow(scene, goal, 2.3, COPPER_TERRA, 0.045),
        _behind_glow(scene, P(1.5, 2.0, 0), 2.4, TEAL, 0.038),
    ]
    room_parts = build_room(O, unit, show_edges=room_edges) if room else []

    # تسميات المحاور (بتواجه الكاميرا). الإزاحات بالشاشة مش بالعالم:
    #  - X وZ على يمين حرفهم. Y فوق حرفه وبين خطين رأسيين (حرف الغرفة والخط المنقط) فمفيش حاجة بتقطعه.
    def axis_label(txt, letter_mob, dx, dy):
        t = MarkupText(f"<b>{txt}</b>", font=THUMB_FONT, font_size=22, color=GOLD_LIGHT)
        t.set_opacity(0.95)
        t.move_to(letter_mob.get_center() + _screen_vec(scene, dx, dy))
        return t

    names_x, names_y, names_z = axis_names
    lbl_x = axis_label(names_x, axes.x_label, 0.60, -0.02)
    lbl_y = axis_label(names_y, axes.y_label, 0.31 * unit, 0.62)
    lbl_z = axis_label(names_z, axes.z_label, 0.52, 0.0)
    ar_labels = VGroup(lbl_x, lbl_y, lbl_z)
    # اسم محور الشمال بعيد في الخلفية: نفرزه بالعمق عشان يترسم خلف الهليكوبتر والمسار والأرضية
    lbl_y.set_shade_in_3d(True, z_index_as_group=True)
    scene.renderer.camera.add_fixed_orientation_mobjects(*ar_labels)
    axes.face_camera(scene)

    # رمز المتجه v على مسار الحركة: ذهبي (نفس لون v في الحلقة 02)، على يسار المسار بإزاحة 0.55 عمودية عليه على الشاشة
    extra3d = []
    if vec_label:
        s0, s1 = _project(scene, [O, goal])
        d = (s1 - s0) / np.linalg.norm(s1 - s0)
        nrm = np.array([-d[1], d[0]])
        v_lbl = MathTex(r"\vec{v}", tex_template=mach_math_template, font_size=96, color=GOLD_BRIGHT)
        stroked(v_lbl, width=10)
        v_lbl.move_to(O + 0.5 * (goal - O) + _screen_vec(scene, 0.55 * nrm[0], 0.55 * nrm[1]))
        scene.renderer.camera.add_fixed_orientation_mobjects(v_lbl)
        extra3d.append(v_lbl)

    scene.add(*glows, *room_parts, axes, floor_fill, shadow, rulers, trail, drops, heli, ar_labels, *extra3d)

    # ---------------- العناصر ثنائية الأبعاد (HUD)
    x0, x1, y0, y1 = region
    bg = backdrop(np.array([(x0 + x1) / 2, (y0 + y1) / 2, 0.0]) - np.array([0.8, 1.2, 0.0]), ltr=ltr)
    bg.set_z_index(-10)
    frame = channel_frame().set_z_index(25)
    brand = brand_mark_at(UR if ltr else UL)

    title = title_block(
        line1, line2, badge_text,
        ltr=ltr, margin=MARGIN,
        line1_width=line1_width, line2_width=line2_width, badge_width=badge_width,
        line2_y=0.70 if ltr else 0.55, badge_gap=0.24,
    )

    rows = VGroup()
    extra = (0.0, 0.65, 1.20)
    for (tex, col), ex in zip(lists, extra):
        m = MathTex(tex, tex_template=mach_math_template, color=col)
        m.set(width=LIST_WIDTH + ex)
        stroked(m, width=6)
        rows.add(m)
    rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT if ltr else RIGHT)
    # القوائم تنزل لتحت: المساحة الفاضية بين الخط التحتي وحافة الإطار تتوزع بالتساوي فوق القوائم وتحتها (بين 0.50 و0.95)
    free = (title[2].get_bottom()[1] + FRAME_TOP) - rows.height
    rows.next_to(title[2], DOWN, buff=float(np.clip(free / 2, 0.50, 0.95)))
    text_left = -FRAME_FX + MARGIN
    if ltr:
        rows.align_to(np.array([text_left + 1.30, 0.0, 0.0]), LEFT)
    else:
        rows.align_to(title[3], RIGHT).shift(LEFT * 0.12)
    for r in rows:
        r.set_z_index(30)

    brace = Brace(rows, direction=LEFT, color=GOLD_LIGHT, buff=0.16)
    brace.set_stroke(GOLD_LIGHT, width=1.5).set_z_index(30)
    eq = stroked(MathTex(r"=", tex_template=mach_math_template, font_size=72, color=GOLD_LIGHT), width=6)
    eq.next_to(brace, LEFT, buff=0.14).set_z_index(30)
    cluster = [rows, brace, eq]
    if vec_label:
        v_eq = stroked(MathTex(r"\vec{v}", tex_template=mach_math_template, font_size=84, color=GOLD_BRIGHT), width=8)
        v_eq.next_to(eq, LEFT, buff=0.20).set_z_index(30)
        cluster.append(v_eq)
    if ltr:
        dx = text_left - min(m.get_left()[0] for m in cluster)  # الكتلة (v = {…}) على بعد MARGIN من الإطار
        for m in cluster:
            m.shift(RIGHT * dx)

    _hud(scene, bg, frame, brand, title, *cluster)