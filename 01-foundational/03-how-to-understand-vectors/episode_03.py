from manim import *

# استيراد الإنترو والأوترو والفريم
from common.identity import IntroScene, OutroScene

# استيراد المشاهد مباشرة وبمنتهى النظافة
from scene01_vectors import play_scene01
from scene02_arrow_method import play_scene02
from scene03_vector_example import play_scene03
from scene04_abstract_concept import play_scene04
from scene05_list_of_numbers import play_scene05
from scene06_dimension_limit import play_scene06
from scene07_feature_engineering import play_scene07
from scene08_helicopter import play_scene08
from scene09_helicopter import play_scene09
from scene10_helicopter import play_scene10
from scene11_helicopter import play_scene11
from scene12_helicopter import play_scene12
from scene13_conclusion import play_scene13


class Episode03(ThreeDScene):
    def construct(self):
        # ---------------- SECTION 1: INTRO ----------------
        self.next_section("01_intro")
        IntroScene.construct(self)

        # ---------------- SECTION 2: SCENE 01 ----------------
        self.next_section("02_vectors")
        play_scene01(self)

        # ---------------- SECTION 3: SCENE 02 ----------------
        self.next_section("03_arrow_method")
        play_scene02(self)

        # ---------------- SECTION 4: SCENE 03 ----------------
        self.next_section("04_vector_example")
        play_scene03(self)

        # ---------------- SECTION 5: SCENE 04 ----------------
        self.next_section("05_abstract_concept")
        play_scene04(self)

        # ---------------- SECTION 6: SCENE 05 ----------------
        self.next_section("06_list_of_numbers")
        play_scene05(self)

        # ---------------- SECTION 7: SCENE 06 ----------------
        self.next_section("07_dimension_limit")
        play_scene06(self)

        # ---------------- SECTION 8: SCENE 07 ----------------
        self.next_section("08_feature_engineering")
        play_scene07(self)

        # ---------------- SECTION 9: SCENE 08 ----------------
        self.next_section("09_meter_example")
        play_scene08(self)

        # ---------------- SECTION 10: SCENE 09 ----------------
        self.next_section("10_centimeter_example")
        play_scene09(self)

        # ---------------- SECTION 11: SCENE 10 ----------------
        self.next_section("11_custom_meter_example")
        play_scene10(self)

        # ---------------- SECTION 12: SCENE 11 ----------------
        self.next_section("12_vector_lists")
        play_scene11(self)

        # ---------------- SECTION 13: SCENE 12 ----------------
        self.next_section("13_real_vector")
        play_scene12(self)

        # ---------------- SECTION 14: SCENE 13 ----------------
        self.next_section("14_conclusion")
        play_scene13(self)

        # ---------------- SECTION 15: OUTRO ----------------
        self.next_section("15_outro")
        OutroScene.construct(self)