from manim import *
import numpy as np

from common.palette import (
    GOLD_BRIGHT,
    GOLD_LIGHT,
    GOLD,
    GOLD_MUTED,
    STONE_AXIS,
    STONE_DASH,
    COPPER_TERRA,
    IVORY_WHITE,
)
from common.latex import mach_math_template
from common.thumbnails import *
from common.mobjects.coordinate_systems import MachAxes3D
from common.mobjects.helicopter import make_helicopter

# ---------------- إعدادات سريعة ----------------
TITLE_LINE1 = "أمثلة لتوضيح"
TITLE_LINE2 = "المتجهات"
BADGE_TEXT = "الجبر الخطي • الحلقة 03"

# نفس الحركة بثلاث قوائم مختلفة (المتر، السنتيمتر، الخشبة مع الزمن)
LISTS = [
    (r"(3,\;4,\;5,\;10)", GOLD_BRIGHT),
    (r"(300,\;400,\;500,\;10)", COPPER_TERRA),
    (r"(0.769,\;1.025,\;1.282,\;10)", GOLD_LIGHT),
]
LIST_WIDTH = 2.45  # العرض الأساسي لضبط تناسق حجم الخط

# إحداثيات وموضع الرسمة ثلاثية الأبعاد (مكبرة ومنزلة لأسفل)
MOVE = (3, 4, 5)
UNIT = 0.54
AXES_CENTER = np.array([-1.9, -2.6, -1.60])


def _hud(scene, *mobs):
    if isinstance(scene, ThreeDScene):
        scene.renderer.camera.add_fixed_in_frame_mobjects(*mobs)
    return mobs[0] if len(mobs) == 1 else mobs


def _ar(txt, size=22, color=IVORY_WHITE, bold=False):
    body = f"<b>{txt}</b>" if bold else txt
    return MarkupText(body, font="Cairo", font_size=size, color=color)


def _round_joints(mob):
    for sm in mob.family_members_with_points():
        sm.joint_type = LineJointType.ROUND
    return mob


def solid_text(text, width, color_a=IVORY_WHITE, color_b=GOLD_BRIGHT, glow=GOLD_LIGHT,
               stroke_w=0.7, outline_w=2.4, halo_w=(9, 4)):
    """نص عربي عريض بحدود خفيفة متناسبة مع العرض عشان الحروف ما تلزقش في بعض."""
    main = MarkupText(f"<b>{text}</b>", font=THUMB_FONT, font_size=96)
    if len(main.family_members_with_points()) == 0:
        main = Text(text, font=THUMB_FONT, font_size=96, weight=BOLD)
    main.set(width=width)
    main.set_color_by_gradient(color_a, color_b)
    for sm in main.family_members_with_points():
        sm.set_stroke(sm.get_fill_color(), width=stroke_w, opacity=1)
    _round_joints(main)
    outline = _round_joints(main.copy().set_fill(opacity=0).set_stroke(THUMB_BG, width=outline_w, opacity=0.9))
    halo = VGroup(
        main.copy().set_fill(opacity=0).set_stroke(glow, width=halo_w[0], opacity=0.07),
        main.copy().set_fill(opacity=0).set_stroke(glow, width=halo_w[1], opacity=0.11),
    )
    _round_joints(halo)
    return VGroup(halo, outline, main)


class Episode03Thumbnail(ThreeDScene):
    def construct(self):
        self.camera.background_color = THUMB_BG

        # 1. المنظور ثلاثي الأبعاد
        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-55 * DEGREES,
            gamma=-4 * DEGREES
        )

        # ==============================================================
        # 2. الرسمة ثلاثية الأبعاد: المحاور + الهليكوبتر + المسار
        # ==============================================================
        axes = MachAxes3D(
            center=AXES_CENTER,
            grid_step=UNIT,
            x_range=(0, 6),
            y_range=(0, 6),
            z_range=(0, 6),
            show_negative_arrows=False,
            show_minor_ticks=False,
            number_font_size=14,
        )
        O = axes.get_origin()

        def P(x, y, z):
            return O + np.array([x, y, z]) * UNIT

        goal = P(*MOVE)

        # مجسم الهليكوبتر بحجم بارز ومائل في اتجاه الحركة
        heli = make_helicopter(scale=0.74)
        climb = np.arctan2(MOVE[2], np.hypot(MOVE[0], MOVE[1]))
        heli.set_pose(
            goal,
            heading=float(np.arctan2(MOVE[1], MOVE[0])),
            bank=0.0,
            pitch=0.12 - 0.6 * climb
        )

        # مسار الإزاحة المتوهج
        trail = VGroup(
            Line(O, goal, color=COPPER_TERRA, stroke_width=5.0, stroke_opacity=0.95),
            Line(O, goal, color=COPPER_TERRA, stroke_width=16, stroke_opacity=0.25),
        )
        trail.set_shade_in_3d(True)

        # خطوط الإسقاط المنقطة
        foot = np.array([goal[0], goal[1], O[2]])
        kw = dict(dash_length=0.09, stroke_width=2.0, stroke_opacity=0.85, color=GOLD_LIGHT)
        drops = VGroup(
            DashedLine(goal, foot, **kw),
            DashedLine(foot, np.array([goal[0], O[1], O[2]]), **kw),
            DashedLine(foot, np.array([O[0], goal[1], O[2]]), **kw),
        ).set_shade_in_3d(True)

        # المساطر المضيئة على المحاور
        rulers = VGroup(
            Line(O, np.array([goal[0], O[1], O[2]]), color=GOLD_BRIGHT, stroke_width=6.5),
            Line(O, np.array([O[0], goal[1], O[2]]), color=GOLD_BRIGHT, stroke_width=6.5),
            Line(O, np.array([O[0], O[1], goal[2]]), color=GOLD_BRIGHT, stroke_width=6.5),
        ).set_shade_in_3d(True)

        # تسميات المحاور بالعربي
        SCREEN_RIGHT = np.array([np.cos(np.radians(35)), np.sin(np.radians(35)), 0.0])

        def ar_label(txt, letter_mob, gap=0.46, color=GOLD_LIGHT):
            t = _ar(txt, 19, color, True)
            t.set_opacity(0.92)
            t.move_to(letter_mob.get_center() + SCREEN_RIGHT * gap)
            return t

        ar_labels = VGroup(
            ar_label("شرق", axes.x_label),
            ar_label("شمال", axes.y_label, gap=0.70),
            ar_label("فوق", axes.z_label, gap=0.44),
        )
        self.renderer.camera.add_fixed_orientation_mobjects(*ar_labels)
        axes.face_camera(self)

        self.add(axes, rulers, trail, drops, heli)

        # ==============================================================
        # 3. العناصر ثنائية الأبعاد (HUD): الشخصية + العنوان + القوائم الثلاث
        # ==============================================================
        frame = channel_frame()
        brand = brand_mark().set_z_index(30)

        # شخصية عالم الرياضيات على اليسار
        glow, char = mathematician_with_glow()

        # كتلة العنوان (رفعنا line1_width من 2.9 إلى 3.9 + حروف أنضف بـ solid_text)
        title = title_block(TITLE_LINE1, TITLE_LINE2, BADGE_TEXT, line1_width=3.9, line2_width=5.2)

        def _pick_text_mob(m):
            if isinstance(m, VGroup) and len(m) > 1 and len(m[1].family_members_with_points()) > 0:
                return m[1]
            return m

        old_l2 = _pick_text_mob(title[2])
        new_l2 = solid_text(TITLE_LINE2, old_l2.width, GOLD_BRIGHT, GOLD, glow=GOLD,
                            stroke_w=1.5, outline_w=7, halo_w=(18, 9))
        new_l2.move_to(old_l2.get_center())
        title.submobjects[2] = new_l2

        old_l1 = _pick_text_mob(title[1])
        new_l1 = solid_text(TITLE_LINE1, old_l1.width, IVORY_WHITE, GOLD_BRIGHT, glow=GOLD_LIGHT,
                            stroke_w=0.7, outline_w=2.4, halo_w=(9, 4))
        new_l1.next_to(new_l2, UP, buff=0.34).align_to(new_l2, RIGHT)
        title.submobjects[1] = new_l1

        # تأكيد إن الـ badge فوق السطر الأول بمسافة مريحة
        if title[0].get_bottom()[1] < new_l1.get_top()[1] + 0.20:
            title[0].next_to(new_l1, UP, buff=0.24).align_to(new_l1, RIGHT)

        title.set_z_index(30)

        # ---------------- القوائم الثلاث مع القوس وعلامة المساواة ----------------
        rows = VGroup()
        for tex, col in LISTS:
            m = MathTex(tex, tex_template=mach_math_template, color=col)
            m.set(width=LIST_WIDTH)
            stroked(m, width=6)
            rows.add(m)

        # موازنة بصرية للأعراض بحسب عدد الخانات
        rows[1].set(width=LIST_WIDTH + 0.65)
        rows[2].set(width=LIST_WIDTH + 1.20)
        rows.arrange(DOWN, buff=0.28, aligned_edge=RIGHT)

        # موضع القوائم تحت العنوان ومحاذاة لليمين
        rows.next_to(
            title,
            DOWN,
            buff=0.30
        ).align_to(title[3], RIGHT).shift(LEFT * 0.12)
        for r in rows:
            r.set_z_index(30)

        # القوس الحاضن على يسار القوائم
        brace = Brace(rows, direction=LEFT, color=GOLD_LIGHT, buff=0.16)
        brace.set_stroke(GOLD_LIGHT, width=1.5).set_z_index(30)

        # علامة المساواة على يسار القوس
        eq = stroked(MathTex(r"=", tex_template=mach_math_template, font_size=72, color=GOLD_LIGHT), width=6)
        eq.next_to(brace, LEFT, buff=0.14).set_z_index(30)

        # تسجيل جميع عناصر الـ HUD وتثبيتها
        hud_elements = [
            frame,
            brand,
            glow,
            char, title,
            rows,
            brace,
            eq
        ]
        _hud(self, *hud_elements)
        self.add(*hud_elements)