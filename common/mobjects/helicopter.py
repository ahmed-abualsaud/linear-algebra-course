"""هيلكوبتر ثلاثية الأبعاد حقيقية (أسطح Manim 3D) بمروحة رئيسية وذيلية تدوران.

الاستخدام (داخل ThreeDScene):
    from common.mobjects.helicopter import make_helicopter, fly_along_3d

    heli = make_helicopter(scale=1.0)
    heli.set_pose(path.point_from_proportion(0))
    heli.start_rotors(scene)                    # تدوير المراوح باستمرار (حتى أثناء الأنيميشن)
    scene.play(fly_along_3d(heli, path, run_time=2.2))

المحاور المحلية: المقدمة +X، الأعلى +Z. الطول الكلي ≈ 2.6 وحدة × scale.
المراوح تدور بتحديث مباشر للنقاط (لا تتأثر بـ opacity أو animate)، لذلك استخدم
heli.set_pose(..., scale=s) بدل heli.scale() بعد إنشاء الطائرة.
"""

from manim import *
import numpy as np

from common.palette import COPPER_TERRA, IVORY_WHITE


def _mix(c1, c2, t):
    return interpolate_color(ManimColor(c1), ManimColor(c2), t)


def _ellipsoid(center, radii, color, opacity=1.0, res=(18, 30)):
    s = Sphere(radius=1.0, resolution=res)
    s.stretch(radii[0], 0).stretch(radii[1], 1).stretch(radii[2], 2)
    s.shift(np.array(center, dtype=float))
    s.set_fill(color, opacity=opacity)
    s.set_stroke(width=0)
    return s


def _flat(points, color, opacity=1.0):
    p = Polygon(*[np.array(q, dtype=float) for q in points])
    p.set_fill(color, opacity=opacity).set_stroke(width=0)
    p.set_shade_in_3d(True)
    return p


def _Rz(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def _Ry(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def _Rx(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


class MachHelicopter(VGroup):
    """هيلكوبتر 3D: مقدمة +X، أعلى +Z، المركز عند الأصل حتى تُوضَع بـ set_pose."""

    MAIN_HUB = np.array([-0.10, 0.0, 0.64])
    TAIL_HUB = np.array([-1.74, 0.07, 0.40])

    def __init__(self, body_color=IVORY_WHITE, accent_color=COPPER_TERRA,
                 glass_color="#16252E", dark_color="#26221D",
                 scale=1.0, rotor_speed=16.0, **kwargs):
        super().__init__(**kwargs)
        body_shade = _mix(body_color, "#000000", 0.14)
        metal = _mix(body_color, "#000000", 0.30)

        self.body = VGroup()
        self.main_rotor = VGroup()
        self.tail_rotor = VGroup()

        # ---- الجسم والقمرة ----
        cabin = _ellipsoid([0.05, 0, 0.0], [0.64, 0.34, 0.37], body_color, res=(30, 56))
        glass_hi = _mix(glass_color, "#FFFFFF", 0.10)
        for f in cabin.family_members_with_points():
            x, y, z = f.get_center()
            if x > 0.30 and z > -0.06:                       # زجاج القمرة الأمامي
                f.set_fill(glass_color if z < 0.20 else glass_hi, 1.0)
            elif -0.12 < x < 0.36 and 0.03 < z < 0.20 and abs(y) > 0.18:  # نوافذ جانبية
                f.set_fill(glass_color, 1.0)
            elif -0.16 < z < -0.07 and x < 0.55:             # شريط الهوية السفلي
                f.set_fill(accent_color, 1.0)
        self.body.add(cabin)
        # غطاء المحرك فوق الكابينة
        self.body.add(_ellipsoid([-0.12, 0, 0.36], [0.34, 0.17, 0.11], metal, res=(12, 20)))

        # ---- ذيل الهيكل (مخروط يضيق نحو الذيل) ----
        boom = Cone(base_radius=0.14, height=1.40, direction=LEFT, show_base=False,
                    resolution=(2, 18), fill_color=body_shade, fill_opacity=1.0, stroke_width=0)
        boom.shift(np.array([-1.76, 0.0, 0.07]))
        self.body.add(boom)

        # زعانف الذيل
        self.body.add(_flat([(-1.34, 0, 0.12), (-1.78, 0, 0.12), (-1.86, 0, 0.58), (-1.66, 0, 0.58)], accent_color))
        self.body.add(_flat([(-1.38, 0, 0.10), (-1.70, 0, 0.10), (-1.64, 0, -0.15)], _mix(accent_color, "#000000", 0.2)))
        for s in (1, -1):
            self.body.add(_flat([(-1.42, 0, 0.10), (-1.60, s * 0.30, 0.10), (-1.70, s * 0.30, 0.10), (-1.64, 0, 0.10)],
                                body_shade))

        # ---- حاملات الهبوط (Skids) ----
        for s in (1, -1):
            skid = Cylinder(radius=0.024, height=1.15, direction=RIGHT, resolution=(1, 10))
            skid.set_fill(dark_color, 1.0).set_stroke(width=0)
            skid.shift(np.array([0.10, s * 0.25, -0.50]))
            self.body.add(skid)
            tip = Cylinder(radius=0.024, height=0.16, direction=np.array([1.0, 0, 0.8]), resolution=(1, 8))
            tip.set_fill(dark_color, 1.0).set_stroke(width=0)
            tip.shift(np.array([0.72, s * 0.25, -0.46]))
            self.body.add(tip)
            for x in (0.38, -0.22):
                st = Line3D(np.array([x, s * 0.25, -0.50]), np.array([x, s * 0.16, -0.30]),
                            thickness=0.020, color=dark_color)
                self.body.add(st)

        # ---- الصاري ----
        mast = Cylinder(radius=0.04, height=0.22, direction=OUT, resolution=(1, 10))
        mast.set_fill(dark_color, 1.0).set_stroke(width=0)
        mast.shift(np.array([-0.10, 0, 0.52]))
        self.body.add(mast)
        self.body.add(_ellipsoid(self.MAIN_HUB, [0.07, 0.07, 0.04], dark_color, res=(8, 12)))

        # ---- المروحة الرئيسية: 4 ريش + قرص نصف شفاف يوحي بالدوران ----
        hx, hy, hz = self.MAIN_HUB
        blade_len, w = 1.30, 0.045
        for k in range(4):
            a = k * np.pi / 2
            def P(x, y, dz, a=a):
                ca, sa = np.cos(a), np.sin(a)
                return (hx + x * ca - y * sa, hy + x * sa + y * ca, hz + dz)
            self.main_rotor.add(_flat([P(0.06, -w, 0), P(blade_len, -w * 0.8, -0.04),
                                       P(blade_len, w * 0.8, -0.04), P(0.06, w, 0)], dark_color))
            self.main_rotor.add(_flat([P(blade_len - 0.20, -w * 0.8, -0.038), P(blade_len, -w * 0.8, -0.04),
                                       P(blade_len, w * 0.8, -0.04), P(blade_len - 0.20, w * 0.8, -0.038)], accent_color))
        disc = Circle(radius=blade_len, stroke_width=0).set_fill("#FFFFFF", 0.07).shift(self.MAIN_HUB)
        disc.set_shade_in_3d(True)
        self.main_rotor.add(disc)

        # ---- مروحة الذيل ----
        tx, ty, tz = self.TAIL_HUB
        for s in (1, -1):
            self.tail_rotor.add(_flat([(tx - 0.018, ty, tz), (tx + 0.018, ty, tz),
                                       (tx + 0.014, ty, tz + s * 0.24), (tx - 0.014, ty, tz + s * 0.24)], dark_color))
        tdisc = Circle(radius=0.24, stroke_width=0).set_fill(body_color, 0.05)
        tdisc.rotate(PI / 2, axis=RIGHT).shift(self.TAIL_HUB)
        tdisc.set_shade_in_3d(True)
        self.tail_rotor.add(tdisc)

        self.add(self.body, self.main_rotor, self.tail_rotor)

        # حفظ نقاط الوضعية الأصلية لكل جزء
        self._leaves = []
        for grp, kind in ((self.body, "body"), (self.main_rotor, "main"), (self.tail_rotor, "tail")):
            for m in grp.family_members_with_points():
                self._leaves.append((m, m.points.copy(), kind))

        self._orig_opacity = [(m, m.get_fill_opacity(), m.get_stroke_opacity()) for m, _, _ in self._leaves]

        self.rotor_speed = float(rotor_speed)
        self._main_angle = 0.0
        self._tail_angle = 0.0
        self._pos = np.zeros(3)
        self._heading = 0.0
        self._bank = 0.0
        self._pitch = 0.0
        self._scale = float(scale)
        self._refresh()

    # ------------------------------------------------------------------
    def _refresh(self):
        R = _Rz(self._heading) @ _Ry(self._pitch) @ _Rx(self._bank)
        Rm, Rt = _Rz(self._main_angle), _Ry(self._tail_angle)
        for m, pts, kind in self._leaves:
            p = pts
            if kind == "main":
                p = (p - self.MAIN_HUB) @ Rm.T + self.MAIN_HUB
            elif kind == "tail":
                p = (p - self.TAIL_HUB) @ Rt.T + self.TAIL_HUB
            m.points = (p * self._scale) @ R.T + self._pos

    def set_pose(self, point=None, heading=None, bank=None, pitch=None, scale=None):
        if point is not None:
            self._pos = np.array(point, dtype=float)
        if heading is not None:
            self._heading = float(heading)
        if bank is not None:
            self._bank = float(bank)
        if pitch is not None:
            self._pitch = float(pitch)
        if scale is not None:
            self._scale = float(scale)
        self._refresh()
        return self

    def set_fade(self, factor):
        """يضبط شفافية الهيلكوبتر كاملة بنسبة factor من شفافية كل جزء الأصلية
        (بدل set_opacity الذي يجعل قرص المروحة الشفاف رمادياً معتماً)."""
        for m, fo, so in self._orig_opacity:
            m.set_fill(opacity=fo * factor)
            m.set_stroke(opacity=so * factor)
        return self

    def advance(self, dt):
        """تقدّم دوران المراوح بمقدار dt ثانية."""
        self._main_angle += self.rotor_speed * dt
        self._tail_angle += self.rotor_speed * 2.2 * dt
        self._refresh()

    def start_rotors(self, scene):
        """يبدأ تدوير المراوح باستمرار (مستقل عن الأنيميشن الجاري)."""
        driver = Mobject()
        driver.add_updater(lambda _m, dt: self.advance(dt))
        scene.add(driver)
        self._driver = driver
        return driver

    def stop_rotors(self, scene):
        d = getattr(self, "_driver", None)
        if d is not None:
            d.clear_updaters()
            scene.remove(d)
            self._driver = None


def make_helicopter(scale=1.0, **kwargs):
    return MachHelicopter(scale=scale, **kwargs)


def _tangent(path, alpha, eps=0.01):
    a0, a1 = max(0.0, alpha - eps), min(1.0, alpha + eps)
    return path.point_from_proportion(a1) - path.point_from_proportion(a0)


def path_heading_3d(path, alpha):
    d = _tangent(path, alpha)
    return float(np.arctan2(d[1], d[0]))


def fly_along_3d(heli, path, run_time=2.5, rate_func=smooth, nose_down=0.12, bank_gain=2.2, **kwargs):
    """تحليق: تتبع المسار، تدير المقدمة مع المماس، تميل للأمام وتنحرف (bank) في المنعطفات."""
    state = {"h": heli._heading, "b": heli._bank}

    def update(m, alpha):
        d = _tangent(path, alpha)
        target = float(np.arctan2(d[1], d[0]))
        dh = (target - state["h"] + np.pi) % (2 * np.pi) - np.pi
        state["h"] += dh * (0.30 if alpha > 0 else 1.0)
        # الانحراف يتناسب مع سرعة تغيّر الاتجاه
        nxt = _tangent(path, min(1.0, alpha + 0.03))
        turn = (np.arctan2(nxt[1], nxt[0]) - target + np.pi) % (2 * np.pi) - np.pi
        state["b"] += (-np.clip(turn * bank_gain, -0.45, 0.45) - state["b"]) * 0.2
        horiz = max(1e-6, np.hypot(d[0], d[1]))
        climb = np.arctan2(d[2], horiz)
        m.set_pose(path.point_from_proportion(alpha), state["h"], state["b"], nose_down - 0.6 * climb)

    return UpdateFromAlphaFunc(heli, update, run_time=run_time, rate_func=rate_func,
                               suspend_mobject_updating=False, **kwargs)