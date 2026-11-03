from manim import *
import numpy as np

from common.palette import GOLD_LIGHT, GOLD_BRIGHT, GOLD_MUTED, GOLD_DARK, COPPER_TERRA, IVORY_WHITE

# ==============================================================
# كف إيد بتشاور (ثنائية الأبعاد) — تتستخدم في أي مشهد
#   make_pointing_hand(pointing)       -> الكف لوحدها
#   hand_pointing_at(target, side)     -> الكف متظبطة جنب عنصر معين
#   hand_enter(hand, side)             -> أنيميشن دخول من الجنب
#   add_hand_bob(hand, direction)      -> حركة نبض خفيفة ناحية الهدف
# ملحوظة: لو المشهد 3D، سجّلها كـ fixed_in_frame (hud_add / add_fixed_in_frame_mobjects)
# ==============================================================

SKIN = GOLD_LIGHT          # لون الجلد
SKIN_HI = GOLD_BRIGHT      # إضاءة
SKIN_SH = GOLD_MUTED       # ظل
LINE = GOLD_DARK           # حدود وثنيات


def _poly(pts, fill, r=0.05, sw=1.6, op=1.0, stroke=True):
    """شكل عضوي: مضلع بزوايا مدورة."""
    m = Polygon(*[np.array([x, y, 0.0]) for x, y in pts])
    m.round_corners(r)
    m.set_fill(fill, op)
    if stroke:
        m.set_stroke(LINE, sw, 1.0)
    else:
        m.set_stroke(width=0, opacity=0)
    return m


def _crease(p, q, sw=1.1, op=0.85):
    return Line([p[0], p[1], 0], [q[0], q[1], 0], color=LINE, stroke_width=sw, stroke_opacity=op)


def make_pointing_hand(pointing=RIGHT, scale=0.5):
    """كف واقعية بتشاور بالسبّابة. pointing = RIGHT أو LEFT (اتجاه صباع الإشارة)."""
    # --- السبّابة (مدببة شوية ناحية الطرف) — بتترسم الأول عشان قاعدتها تستخبى ورا الكف ---
    index = _poly([(0.08, 0.275), (0.52, 0.255), (0.86, 0.225), (0.88, 0.105), (0.52, 0.092), (0.08, 0.085)],
                  SKIN, r=0.05, sw=1.8)
    index_hi = _poly([(0.20, 0.250), (0.55, 0.238), (0.80, 0.215), (0.80, 0.200), (0.55, 0.222), (0.20, 0.232)],
                     SKIN_HI, r=0.01, op=0.7, stroke=False)
    index_sh = _poly([(0.14, 0.135), (0.55, 0.142), (0.86, 0.150), (0.86, 0.110), (0.55, 0.098), (0.14, 0.092)],
                     SKIN_SH, r=0.02, op=0.40, stroke=False)
    nail = _poly([(0.64, 0.236), (0.83, 0.222), (0.85, 0.185), (0.64, 0.205)], IVORY_WHITE, r=0.02, sw=0.9, op=0.92)
    joints = VGroup(
        _crease((0.36, 0.250), (0.37, 0.178)), _crease((0.38, 0.150), (0.385, 0.098), op=0.6),
        _crease((0.62, 0.232), (0.63, 0.190), op=0.6),
    )

    # --- الكُم والرسغ ---
    wrist = _poly([(-0.34, 0.20), (-0.20, 0.22), (-0.20, -0.30), (-0.34, -0.30)], SKIN, r=0.03)
    cuff = _poly([(-0.52, 0.34), (-0.32, 0.34), (-0.32, -0.42), (-0.52, -0.42)], COPPER_TERRA, r=0.03, sw=1.8)
    cuff_fold = VGroup(_crease((-0.46, 0.30), (-0.46, -0.38), op=0.5), _crease((-0.36, 0.30), (-0.36, -0.38), op=0.35))

    # --- الكف (قبضة) ---
    fist = _poly([(-0.26, 0.23), (0.10, 0.25), (0.28, 0.10), (0.46, 0.07), (0.50, -0.30), (0.20, -0.40), (-0.26, -0.36)],
                 SKIN, r=0.08, sw=1.9)
    fist_sh = _poly([(-0.24, -0.34), (0.20, -0.38), (0.48, -0.30), (0.48, -0.22), (0.10, -0.26), (-0.24, -0.22)],
                    SKIN_SH, r=0.04, op=0.38, stroke=False)

    # --- الأصابع المطبوقة (وسطى، بنصر، خنصر) ---
    curled = VGroup(
        _poly([(0.20, 0.060), (0.50, 0.060), (0.52, -0.045), (0.20, -0.050)], SKIN, r=0.05, sw=1.6),
        _poly([(0.20, -0.060), (0.49, -0.055), (0.50, -0.160), (0.20, -0.165)], SKIN, r=0.05, sw=1.6),
        _poly([(0.20, -0.175), (0.46, -0.170), (0.47, -0.265), (0.20, -0.270)], SKIN, r=0.05, sw=1.6),
    )
    nails_c = VGroup(
        _poly([(0.44, 0.045), (0.50, 0.045), (0.505, -0.03), (0.44, -0.03)], IVORY_WHITE, r=0.02, sw=0.7, op=0.55),
        _poly([(0.43, -0.07), (0.485, -0.07), (0.49, -0.145), (0.43, -0.145)], IVORY_WHITE, r=0.02, sw=0.7, op=0.5),
    )

    # --- الإبهام (مدبب، مستريّح على الأصابع المطبوقة) ---
    thumb = _poly([(-0.14, 0.13), (0.10, 0.11), (0.31, 0.01), (0.34, -0.055), (0.20, -0.095), (0.02, -0.04),
                   (-0.14, -0.06)], SKIN, r=0.05, sw=1.8)
    thumb_nail = _poly([(0.22, 0.03), (0.31, 0.005), (0.325, -0.04), (0.235, -0.02)], IVORY_WHITE, r=0.015, sw=0.7,
                       op=0.85)
    thumb_crease = _crease((0.08, 0.085), (0.075, -0.015))

    hand = VGroup(index, index_sh, index_hi, nail, joints, wrist, cuff, cuff_fold, fist, fist_sh, curled, nails_c,
                  thumb, thumb_nail, thumb_crease)
    hand.index = index                      # عشان نظبط ارتفاع السبّابة مع الهدف
    hand.scale(scale)
    if np.allclose(pointing, LEFT):
        hand.flip(UP)
    return hand


def hand_pointing_at(target, side=LEFT, gap=0.12, scale=0.5):
    """الكف بتقعد على جنب `side` من الهدف (LEFT/RIGHT) وبتشاور عليه، والسبّابة في نص الهدف رأسيًا."""
    side = np.array(side, float)
    hand = make_pointing_hand(pointing=-side, scale=scale)
    hand.next_to(target, side, buff=gap)
    hand.shift(UP * (target.get_center()[1] - hand.index.get_center()[1]))
    return hand


def hand_enter(hand, side=LEFT, dist=0.6):
    """أنيميشن: الكف تدخل من الجنب لمكانها."""
    return FadeIn(hand, shift=np.array(side, float) * dist)


def add_hand_bob(hand, direction, amp=0.07, freq=1.5):
    """نبض خفيف ناحية الهدف (direction = اتجاه الإشارة). ابدأه بعد ما الكف تدخل."""
    st = {"t": 0.0, "off": 0.0}
    d = np.array(direction, float)

    def up(m, dt):
        st["t"] += dt
        new = amp * (1 - np.cos(2 * np.pi * freq * st["t"])) / 2
        m.shift(d * (new - st["off"]))
        st["off"] = new

    hand.add_updater(up)
    return hand