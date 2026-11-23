from manim import *

from common.thumbnails_addition import *

# ---------------- Quick settings ----------------
TITLE_LINE1 = "How Do We Add"
TITLE_LINE2 = "Vectors?"
BADGE_TEXT = "Linear Algebra • Episode 05"


class Episode05ThumbnailEN(Scene):
    def construct(self):
        # LTR: text and equation on the left, the drawing and rule icons on the right
        build_vector_addition(
            self, ltr=True,
            line1=TITLE_LINE1, line2=TITLE_LINE2, badge_text=BADGE_TEXT,
            line1_width=4.4, line2_width=3.8, badge_width=3.9,
        )