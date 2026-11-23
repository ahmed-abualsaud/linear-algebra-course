from manim import *

from common.thumbnails_3d import *

# ---------------- إعدادات سريعة ----------------
TITLE_LINE1 = "أمثلة لتوضيح"
TITLE_LINE2 = "المتجهات"
BADGE_TEXT = "الجبر الخطي • الحلقة 03"
AXIS_NAMES = ("شرق", "شمال", "فوق")


class Episode03Thumbnail(ThreeDScene):
    def construct(self):
        # RTL: الرسمة على الشمال والعنوان والقوائم على اليمين
        build_vector_examples(
            self, ltr=False,
            line1=TITLE_LINE1, line2=TITLE_LINE2, badge_text=BADGE_TEXT, axis_names=AXIS_NAMES,
            line1_width=3.9, line2_width=5.2,
        )