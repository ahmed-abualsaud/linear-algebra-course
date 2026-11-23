from manim import *

from common.thumbnails_addition import *

# ---------------- إعدادات سريعة ----------------
TITLE_LINE1 = "كيف"
TITLE_LINE2 = "نجمع المتجهات؟"
BADGE_TEXT = "الجبر الخطي • الحلقة 05"


class Episode05Thumbnail(Scene):
    def construct(self):
        # RTL: الرسمة والأيقونات على الشمال، والعنوان والمعادلة على اليمين
        build_vector_addition(
            self, ltr=False,
            line1=TITLE_LINE1, line2=TITLE_LINE2, badge_text=BADGE_TEXT,
            line1_width=1.7, line2_width=5.6,
        )