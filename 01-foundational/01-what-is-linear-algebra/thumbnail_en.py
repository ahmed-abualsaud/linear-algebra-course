from manim import *

from common.thumbnails import *

# ---------------- Quick settings ----------------
TITLE_LINE1 = "What is"
TITLE_LINE2 = "Linear Algebra?"
BADGE_TEXT = "Linear Algebra • Episode 01"


class Episode01ThumbnailEN(Scene):
    def construct(self):
        self.camera.background_color = THUMB_BG
        O = GRID_ORIGIN_LTR  # LTR: text on the left, drawing on the right

        grid, tilted_grid, det_visual, hero = transform_demo(O, side="right")

        title = title_block(
            TITLE_LINE1, TITLE_LINE2, BADGE_TEXT,
            ltr=True, margin=MARGIN,
            line1_width=3.5, line2_width=5.5, badge_width=3.9,
            line2_y=0.70,  # underline at line2_y - 0.75, line 1 at line2_y + 1.25
        )
        mat = place_matrix_under(matrix_A(), title, ltr=True, gap=1.0)

        self.add(
            backdrop(O, ltr=True), grid, tilted_grid, det_visual,
            channel_frame().set_z_index(25), hero, mat,
            title, brand_mark_at(UR),
        )