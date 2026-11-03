from manim import *

# استيراد الإنترو والأوترو والفريم
from common.identity import IntroScene, OutroScene

# استيراد المشاهد مباشرة وبمنتهى النظافة
from scene01_why_notation import play_scene01
from scene02_formula import play_scene02
from scene03_abstract_basis import play_scene03
from scene04_infinite_lists import play_scene04
from scene05_airplane_properties import play_scene05
from scene06_scaffolding import play_scene06
from scene07_measuring import play_scene07
from scene08_change_basis import play_scene08
from scene09_path_basis import play_scene09
from scene10_closing import play_scene10


class Episode04(ThreeDScene):
    def construct(self):
        # ---------------- SECTION 1: INTRO ----------------
        self.next_section("01_intro")
        IntroScene.construct(self)

        # ---------------- SECTION 2: SCENE 01 ----------------
        self.next_section("02_why_notation")
        play_scene01(self)

        # ---------------- SECTION 3: SCENE 02 ----------------
        self.next_section("03_formula")
        play_scene02(self)

        # ---------------- SECTION 4: SCENE 03 ----------------
        self.next_section("04_abstract_basis")
        play_scene03(self)

        # ---------------- SECTION 5: SCENE 04 ----------------
        self.next_section("05_infinite_lists")
        play_scene04(self)

        # ---------------- SECTION 6: SCENE 05 ----------------
        self.next_section("06_airplane_properties")
        play_scene05(self)

        # ---------------- SECTION 7: SCENE 06 ----------------
        self.next_section("07_scaffolding")
        play_scene06(self)

        # ---------------- SECTION 8: SCENE 07 ----------------
        self.next_section("08_measuring")
        play_scene07(self, keep_drawing=True)
        # print("END07", self.renderer.num_plays, flush=True)

        # ---------------- SECTION 9: SCENE 08 ----------------
        self.next_section("09_change_basis")
        play_scene08(self, keep_drawing=True)
        # print("END08", self.renderer.num_plays, flush=True)

        # ---------------- SECTION 10: SCENE 09 ----------------
        self.next_section("10_path_basis")
        play_scene09(self)
        # print("END09", self.renderer.num_plays, flush=True)

        # ---------------- SECTION 11: SCENE 10 ----------------
        self.next_section("11_closing")
        play_scene10(self)

        # ---------------- SECTION 12: OUTRO ----------------
        self.next_section("12_outro")
        OutroScene.construct(self)