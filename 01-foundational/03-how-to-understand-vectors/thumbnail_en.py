from manim import *

from common.thumbnails_3d import *

# ---------------- Quick settings ----------------
TITLE_LINE1 = "Examples of"
TITLE_LINE2 = "Vectors"
BADGE_TEXT = "Linear Algebra • Episode 03"
AXIS_NAMES = ("East", "North", "Up")


class Episode03ThumbnailEN(ThreeDScene):
    def construct(self):
        # LTR: text and lists on the left, the 3D drawing on the right
        build_vector_examples(
            self, ltr=True,
            line1=TITLE_LINE1, line2=TITLE_LINE2, badge_text=BADGE_TEXT, axis_names=AXIS_NAMES,
            line1_width=4.3, line2_width=3.6, badge_width=3.9,
        )