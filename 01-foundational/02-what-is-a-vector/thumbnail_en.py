from manim import *

from common.thumbnails import *

# ---------------- Quick settings ----------------
TITLE_LINE1 = "What is a"
TITLE_LINE2 = "Vector?"
BADGE_TEXT = "Linear Algebra • Episode 02"


class Episode02ThumbnailEN(Scene):
    def construct(self):
        self.camera.background_color = THUMB_BG
        O = VECTOR_ORIGIN_LTR  # LTR: text on the left, drawing on the right

        grid, under, hero = vector_demo(O)

        title = title_block(
            TITLE_LINE1, TITLE_LINE2, BADGE_TEXT,
            ltr=True, margin=MARGIN,
            line1_width=4.0, line2_width=3.4, badge_width=3.9,
            line2_y=0.70,  # underline at line2_y - 0.75, line 1 at line2_y + 1.25
        )
        vec = place_matrix_under(column_vector(), title, ltr=True, gap=1.0)

        self.add(
            backdrop(O + np.array([1.8, 1.2, 0]), ltr=True), grid, under,
            channel_frame().set_z_index(25), hero, vec,
            title, brand_mark_at(UR),
        )