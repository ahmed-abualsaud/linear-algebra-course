from manim import *

from common.thumbnails import *

# ---------------- إعدادات سريعة ----------------
TITLE_LINE1 = "ما هو"
TITLE_LINE2 = "المتجه؟"
BADGE_TEXT = "الجبر الخطي • الحلقة 02"


class Episode02Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = THUMB_BG
        O = VECTOR_ORIGIN  # RTL: الرسمة على الشمال والعنوان على اليمين

        grid, under, hero = vector_demo(O)

        title = title_block(
            TITLE_LINE1, TITLE_LINE2, BADGE_TEXT,
            line1_width=2.4, line2_width=4.2,
            line2_y=0.55, badge_gap=0.24, margin=MARGIN,
        )
        vec = place_matrix_under(column_vector(), title, ltr=False)

        self.add(
            backdrop(O + np.array([1.8, 1.2, 0])), grid, under,
            channel_frame().set_z_index(25), hero, vec,
            title, brand_mark_at(UL),
        )