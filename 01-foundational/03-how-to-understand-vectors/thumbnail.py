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
TITLE_LINE1 = "ما هو"
TITLE_LINE2 = "المتجه؟"
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

        # كتلة العنوان
        title = title_block(TITLE_LINE1, TITLE_LINE2, BADGE_TEXT, line1_width=2.9, line2_width=5.2)
        title.set_z_index(30)

        # وسم (الجزء الثاني)
        part_tag = Text(
            "الجزء الثاني",
            font=THUMB_FONT,
            font_size=24,
            weight=SEMIBOLD,
            color=COPPER_TERRA,
        )
        part_tag.set_stroke(THUMB_BG, width=2.5, background=True)
        part_tag.next_to(title[3], DOWN, buff=0.18).align_to(title[3], RIGHT).shift(LEFT * 0.18)
        part_tag.set_z_index(30)

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

        # موضع القوائم تحت وسم (الجزء الثاني) ومحاذاة لليمين
        rows.next_to(part_tag, DOWN, buff=0.30).align_to(title[3], RIGHT).shift(LEFT * 0.12)
        for r in rows:
            r.set_z_index(30)

        # القوس الحاضن على يسار القوائم
        brace = Brace(rows, direction=LEFT, color=GOLD_LIGHT, buff=0.16)
        brace.set_stroke(GOLD_LIGHT, width=1.5).set_z_index(30)

        # علامة المساواة على يسار القوس
        eq = stroked(MathTex(r"=", tex_template=mach_math_template, font_size=72, color=GOLD_LIGHT), width=6)
        eq.next_to(brace, LEFT, buff=0.14).set_z_index(30)

        # تسجيل جميع عناصر الـ HUD وتثبيتها
        hud_elements = [frame, brand, glow, char, title, part_tag, rows, brace, eq]
        _hud(self, *hud_elements)
        self.add(*hud_elements)