from manim import *
import numpy as np

from common.palette import (
    GOLD_LIGHT,
    GOLD_BRIGHT,
    GOLD_MUTED,
    GOLD_DARK,
    COPPER_TERRA,
    IVORY_WHITE,
    STONE_AXIS,
)
from common.latex import mach_math_template

# ==============================================================
# الحلقة 04 — الأدوات المشتركة بين كل المشاهد
# ==============================================================

ERR_RED = "#C0443A"

def _ar(txt, size=22, color=IVORY_WHITE, bold=False):
    """نص عربي بـ MarkupText."""
    body = f"<b>{txt}</b>" if bold else txt
    return MarkupText(body, font="Cairo", font_size=size, color=color)


def _tex(s, size=44, color=IVORY_WHITE):
    return MathTex(s, tex_template=mach_math_template, font_size=size, color=color)


def _column(entries, size=44, color=IVORY_WHITE):
    rows = r" \\ ".join(entries)
    return _tex(r"\begin{bmatrix}" + rows + r"\end{bmatrix}", size, color)


def _ruler(length, tick_step, color, unit_lbl):
    base = Line(LEFT * length / 2, RIGHT * length / 2, color=color, stroke_width=3.0)
    ticks = VGroup()
    n = int(length / tick_step) + 1
    for k in range(n + 1):
        x = -length / 2 + k * tick_step
        if x > length / 2 + 1e-6:
            break
        h = 0.16 if k % 5 == 0 else 0.09
        ticks.add(Line([x, 0, 0], [x, h, 0], color=color, stroke_width=1.6))
    lbl = _ar(unit_lbl, 17, color).next_to(base, RIGHT, buff=0.28)
    return VGroup(base, ticks, lbl)


def _mini_ruler(color, step, width=1.0):
    base = Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=3.0)
    ticks = VGroup()
    k = 0
    while -width / 2 + k * step <= width / 2 + 1e-6:
        x = -width / 2 + k * step
        h = 0.17 if k % 5 == 0 else 0.10
        ticks.add(Line([x, 0, 0], [x, h, 0], color=color, stroke_width=1.6))
        k += 1
    return VGroup(base, ticks)


def _unit_matrix(r, c, size=34, color=COPPER_TERRA):
    rows = [["1" if (i == r and j == c) else "0" for j in range(2)] for i in range(2)]
    body = r" \\ ".join(" & ".join(rw) for rw in rows)
    return _tex(r"\begin{bmatrix}" + body + r"\end{bmatrix}", size, color)


def _list_card(numbers, basis_syms, accent):
    nums = _column(numbers, 34, IVORY_WHITE)
    basis = VGroup(*[_tex(b, 28, COPPER_TERRA) for b in basis_syms])
    basis.arrange(DOWN, buff=0.275, aligned_edge=LEFT)
    basis.next_to(nums, RIGHT, buff=0.35)
    basis.match_y(nums)
    content = VGroup(nums, basis)
    frame = RoundedRectangle(corner_radius=0.18, width=content.width + 0.55, height=content.height + 0.5,
                             stroke_color=accent, stroke_width=1.8, stroke_opacity=0.8,
                             fill_color="#14100A", fill_opacity=0.9)
    frame.move_to(content)
    return VGroup(frame, content)


def _clip(p, q, box):
    """قص مقطع مستقيم بمستطيل box=(xmin,xmax,ymin,ymax) (Liang–Barsky)."""
    x0, x1, y0, y1 = box
    p, q = np.asarray(p, float), np.asarray(q, float)
    d = q - p
    t0, t1 = 0.0, 1.0
    for pk, qk in ((-d[0], p[0] - x0), (d[0], x1 - p[0]), (-d[1], p[1] - y0), (d[1], y1 - p[1])):
        if abs(pk) < 1e-9:
            if qk < 0:
                return None
            continue
        r = qk / pk
        if pk < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return None
    return p + t0 * d, p + t1 * d


def _lattice(origin, e1, e2, box, n=14, color=GOLD_LIGHT, width=1.4, opacity=0.8, dashed=False):
    o = np.array([origin[0], origin[1], 0.0])
    a = np.array([e1[0], e1[1], 0.0])
    b = np.array([e2[0], e2[1], 0.0])
    g = VGroup()
    L = 40.0
    for fam_dir, step in ((b, a), (a, b)):
        for k in range(-n, n + 1):
            base = o + k * step
            seg = _clip(base - L * fam_dir, base + L * fam_dir, box)
            if seg is None:
                continue
            if dashed:
                ln = DashedLine(seg[0], seg[1], dash_length=0.08, color=color,
                                stroke_width=width, stroke_opacity=opacity)
            else:
                ln = Line(seg[0], seg[1], color=color, stroke_width=width, stroke_opacity=opacity)
            g.add(ln)
    return g


def _bg_grid(box, step=0.55, opacity=0.2):
    return _lattice([0, 0], [step, 0], [0, step], box, n=30, color=STONE_AXIS, width=0.8, opacity=opacity)


def _arrow(start, end, color, width=5):
    return Arrow([start[0], start[1], 0], [end[0], end[1], 0], buff=0, color=color,
                 stroke_width=width, max_tip_length_to_length_ratio=0.25, max_stroke_width_to_length_ratio=12)


def _grid_lines(a, b, box, origin=(0, 0, 0), n=14, color=COPPER_TERRA, width=1.4, opacity=0.6, dashed=False):
    a = np.array(a, float)
    b = np.array(b, float)
    o = np.array(origin, float)
    g = VGroup()
    for fam, step in ((b, a), (a, b)):
        if np.linalg.norm(fam) < 1e-6:
            continue
        for i in range(-n, n + 1):
            c = o + i * step
            seg = _clip(c - 60 * fam, c + 60 * fam, box)
            if seg is None or np.linalg.norm(seg[1] - seg[0]) < 1e-3:
                continue
            if dashed:
                ln = DashedLine(seg[0], seg[1], dash_length=0.09, dashed_ratio=0.5)
            else:
                ln = Line(seg[0], seg[1])
            ln.set_stroke(color, width, opacity)
            g.add(ln)
    return g


def _piece_swap(scene, cur, new, y, buff=0.24, run_time=1.1, replace=(), extra=(), max_width=12.6, center=None):
    """يدعم وضع المعادلة في أي مركز مخصص (center=[x, y, 0])."""
    tmp = VGroup(*[m.copy() for m in new]).arrange(RIGHT, buff=buff)
    k = 1.0
    if tmp.width > max_width:
        k = max_width / tmp.width
        tmp.scale(k)
    c = center if center is not None else [0, y, 0]
    tmp.move_to(c)
    pos = {id(m): t.get_center() for m, t in zip(new, tmp)}
    rep_old = {id(o): n for o, n in replace}
    new_ids = {id(m) for m in new}
    anims = []
    for m in cur:
        if id(m) in new_ids:
            anims.append(m.animate.move_to(pos[id(m)]))
        elif id(m) in rep_old:
            n = rep_old[id(m)]
            n.move_to(pos[id(n)])
            if hasattr(scene, "add_fixed_in_frame_mobjects"):
                scene.add_fixed_in_frame_mobjects(n)
            anims.append(ReplacementTransform(m, n))
        else:
            anims.append(FadeOut(m))
    old_ids = {id(m) for m in cur}
    rep_new = {id(n) for _, n in replace}
    for m in new:
        if id(m) not in old_ids and id(m) not in rep_new:
            m.move_to(pos[id(m)])
            if hasattr(scene, "add_fixed_in_frame_mobjects"):
                scene.add_fixed_in_frame_mobjects(m)
            anims.append(FadeIn(m))
    scene.play(*anims, *extra, run_time=run_time)
    return list(new), k


def _chip(txt, color, w=2.7, h=0.55, size=17, filled=False):
    box = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=1.8,
                           fill_color=color if filled else "#14100A", fill_opacity=0.22 if filled else 0.9)
    t = _ar(txt, size, color, True).move_to(box)
    return VGroup(box, t)


class _Cap:
    """سطر التعليق السفلي: يدعم الموضع الأفقي x."""
    def __init__(self, scene, y=-3.35, x=0.0):
        self.scene, self.y, self.x, self.cur = scene, y, x, None

    def set(self, txt, color=GOLD_LIGHT, size=24, run_time=0.7, extra=()):
        new = _ar(txt, size, color, True).move_to([self.x, self.y, 0])
        if hasattr(self.scene, "add_fixed_in_frame_mobjects"):
            self.scene.add_fixed_in_frame_mobjects(new)
        if self.cur is None:
            self.scene.play(FadeIn(new, shift=UP * 0.1), *extra, run_time=run_time)
        else:
            self.scene.play(ReplacementTransform(self.cur, new), *extra, run_time=run_time)
        self.cur = new
        return new

    def clear(self, run_time=0.5):
        if self.cur is not None:
            self.scene.play(FadeOut(self.cur), run_time=run_time)
            self.cur = None


def _hud_fix(scene):
    cam = scene.camera
    if getattr(cam, "_hud_fixed", False):
        return
    cam._fc_ctx = np.zeros(3)
    orig_cache = cam.cache_cairo_context
    orig_tr = cam.transform_points_pre_display

    def cache(pixel_array, ctx):
        cam._fc_ctx = np.array(cam.frame_center, dtype=float)
        return orig_cache(pixel_array, ctx)

    def patched(mobject, points):
        pts = orig_tr(mobject, points)
        if mobject in cam.fixed_in_frame_mobjects:
            pts = pts + cam._fc_ctx
        return pts

    cam.cache_cairo_context = cache
    cam.transform_points_pre_display = patched
    cam._hud_fixed = True