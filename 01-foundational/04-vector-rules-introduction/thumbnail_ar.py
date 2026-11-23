from manim import *

from common.thumbnails_basis import *

# ---------------- إعدادات سريعة ----------------
TITLE_LINE1 = "تمهيد لقواعد"
TITLE_LINE2 = "المتجهات"
BADGE_TEXT = "الجبر الخطي • الحلقة 04"


class Episode04Thumbnail(Scene):
    def construct(self):
        # RTL: الرسمة على الشمال والعنوان والمعادلات على اليمين
        build_basis_change(
            self, ltr=False,
            line1=TITLE_LINE1, line2=TITLE_LINE2, badge_text=BADGE_TEXT,
            line1_width=3.6, line2_width=5.4,
        )