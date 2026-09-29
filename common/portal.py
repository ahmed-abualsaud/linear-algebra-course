from manim import *
import numpy as np

from common.identity import FRAME_HALF_W, FRAME_HALF_H, get_mach_frame


class MachPortal:
    """
    أداة البوابة (The Portal Engine) لقناة MACH-MATH:
    تسمح باختراق جدران الفريم دون مسح أو قطع أي ضلع من أضلاع الفريم.
    """
    def __init__(self, scene):
        self.scene = scene
        self.w_inner = FRAME_HALF_W
        self.h_inner = FRAME_HALF_H
        self.w_outer = config.frame_width / 2 * 1.05
        self.h_outer = config.frame_height / 2 * 1.05

        self._build_masks()

    def _build_masks(self):
        # الجدار الأيمن
        self.mask_right = Polygon(
            [self.w_inner, self.h_inner, 0], [self.w_outer, self.h_outer, 0],
            [self.w_outer, -self.h_outer, 0], [self.w_inner, -self.h_inner, 0],
            fill_color=BLACK, fill_opacity=1.0, stroke_width=0
        ).set_z_index(8)

        # الجدار الأيسر
        self.mask_left = Polygon(
            [-self.w_inner, self.h_inner, 0], [-self.w_outer, self.h_outer, 0],
            [-self.w_outer, -self.h_outer, 0], [-self.w_inner, -self.h_inner, 0],
            fill_color=BLACK, fill_opacity=1.0, stroke_width=0
        ).set_z_index(8)

        # السقف (الأعلى)
        self.mask_up = Polygon(
            [-self.w_inner, self.h_inner, 0], [-self.w_outer, self.h_outer, 0],
            [self.w_outer, self.h_outer, 0], [self.w_inner, self.h_inner, 0],
            fill_color=BLACK, fill_opacity=1.0, stroke_width=0
        ).set_z_index(8)

        # الأرضية (الأسفل)
        self.mask_down = Polygon(
            [-self.w_inner, -self.h_inner, 0], [-self.w_outer, -self.h_outer, 0],
            [self.w_outer, -self.h_outer, 0], [self.w_inner, -self.h_inner, 0],
            fill_color=BLACK, fill_opacity=1.0, stroke_width=0
        ).set_z_index(8)

        self.masks = {
            "RIGHT": self.mask_right,
            "LEFT": self.mask_left,
            "UP": self.mask_up,
            "DOWN": self.mask_down,
        }

    def _get_direction_key(self, direction):
        if np.array_equal(direction, RIGHT): return "RIGHT"
        if np.array_equal(direction, LEFT): return "LEFT"
        if np.array_equal(direction, UP): return "UP"
        return "DOWN"

    def _ensure_frame_on_top(self):
        """رفع الفريم فقط إذا كان النيون مفعلاً حتى لا يتشوه الفريم الهادئ."""
        if hasattr(self.scene, "neon_overlay"):
            for mob in self.scene.mobjects:
                if isinstance(mob, VGroup) and len(mob.submobjects) == 2:
                    mob.set_z_index(20)

    def enter(self, mobject, direction=RIGHT, distance=4.5, run_time=1.2):
        key = self._get_direction_key(direction)
        mask = self.masks[key]

        self.scene.add(mask)
        self._ensure_frame_on_top()

        target_pos = mobject.get_center()
        start_pos = target_pos + direction * distance

        mobject.set_z_index(5)
        mobject.move_to(start_pos)
        self.scene.add(mobject)

        self.scene.play(
            mobject.animate.move_to(target_pos),
            run_time=run_time,
            rate_func=rate_functions.ease_out_cubic
        )
        self.scene.remove(mask)

    def exit(self, mobject, direction=LEFT, distance=4.5, run_time=1.0):
        key = self._get_direction_key(direction)
        mask = self.masks[key]

        self.scene.add(mask)
        self._ensure_frame_on_top()

        mobject.set_z_index(5)
        current_pos = mobject.get_center()
        exit_pos = current_pos + direction * distance

        self.scene.play(
            mobject.animate.move_to(exit_pos),
            run_time=run_time,
            rate_func=rate_functions.ease_in_cubic
        )
        self.scene.remove(mobject, mask)