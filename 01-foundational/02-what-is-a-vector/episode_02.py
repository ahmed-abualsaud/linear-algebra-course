from manim import *

# استيراد الإنترو والأوترو والفريم
from common.identity import IntroScene, OutroScene, get_mach_frame

# استيراد المشاهد مباشرة وبمنتهى النظافة
from scene01_asking import play_scene01
from scene02_comparison import play_scene02
from scene03_mathematician import play_scene03
from scene04_examples import play_scene04
from scene05_abstraction import play_scene05
from scene06_number_sets import play_scene06
from scene07_vector_space import play_scene07
from scene08_core_operations import play_scene08
from scene09_teacher_analogy import play_scene09


class FullEpisode02(Scene):
    def construct(self):
        # ---------------- SECTION 1: INTRO ----------------
        self.next_section("01_intro")
        IntroScene.construct(self)

        # ---------------- SECTION 2: SCENE 01 ----------------
        self.next_section("02_asking")
        play_scene01(self)

        # ---------------- SECTION 3: SCENE 02 ----------------
        self.next_section("03_comparison")
        play_scene02(self)

        # ---------------- SECTION 4: SCENE 03 ----------------
        self.next_section("04_mathematician")
        play_scene03(self)

        # ---------------- SECTION 5: SCENE 04 ----------------
        self.next_section("05_examples")
        play_scene04(self)

        # ---------------- SECTION 6: SCENE 05 ----------------
        self.next_section("06_abstraction")
        play_scene05(self)

        # ---------------- SECTION 7: SCENE 06 ----------------
        self.next_section("07_number_sets")
        play_scene06(self)

        # ---------------- SECTION 8: SCENE 07 ----------------
        self.next_section("07_vector_space")
        play_scene07(self)

        # ---------------- SECTION 9: SCENE 08 ----------------
        self.next_section("08_core_operations")
        play_scene08(self)

        # ---------------- SECTION 10: SCENE 09 ----------------
        self.next_section("09_teacher_analogy")
        play_scene09(self)

        # ---------------- SECTION 11: OUTRO ----------------
        self.next_section("10_outro")
        OutroScene.construct(self)