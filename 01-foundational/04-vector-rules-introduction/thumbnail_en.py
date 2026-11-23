from manim import *

from common.thumbnails_basis import *

# ---------------- Quick settings ----------------
TITLE_LINE1 = "Before You Learn"
TITLE_LINE2 = "Vector Rules"
BADGE_TEXT = "Linear Algebra • Episode 04"


class Episode04ThumbnailEN(Scene):
    def construct(self):
        # LTR: text and equations on the left, the drawing on the right
        build_basis_change(
            self, ltr=True,
            line1=TITLE_LINE1, line2=TITLE_LINE2, badge_text=BADGE_TEXT,
            line1_width=4.8, line2_width=4.8, badge_width=3.9,
        )