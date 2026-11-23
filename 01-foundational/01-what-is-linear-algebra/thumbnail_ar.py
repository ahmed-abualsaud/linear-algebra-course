from manim import *

from common.thumbnails import *

# ---------------- إعدادات سريعة ----------------
TITLE_LINE1 = "ما هو"
TITLE_LINE2 = "الجبر الخطي؟"
BADGE_TEXT = "الجبر الخطي • الحلقة 01"


class Episode01Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = THUMB_BG
        O = GRID_ORIGIN

        grid, tilted_grid, det_visual, hero = transform_demo(O, side="left")

        title = title_block(
            TITLE_LINE1, TITLE_LINE2, BADGE_TEXT,
            line1_width=2.4, line2_width=5.1,
            line2_y=0.55, badge_gap=0.24, margin=MARGIN,
        )
        mat = place_matrix_under(matrix_A(), title, ltr=False)

        self.add(
            backdrop(O), grid, tilted_grid, det_visual,
            channel_frame().set_z_index(25), hero, mat,
            title, brand_mark_at(UL),
        )