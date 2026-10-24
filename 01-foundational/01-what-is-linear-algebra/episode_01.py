from manim import *

# استيراد الإنترو والأوترو والفريم
from common.identity import IntroScene, OutroScene, get_mach_frame

# استيراد المشاهد مباشرة وبمنتهى النظافة
from scene01_hook import play_scene01
from scene02_arithmetic import play_scene02
from scene03_dialogue import play_scene03
from scene04_calculus import play_scene04
from scene05_thinking import play_scene05
from scene06_comparison import play_scene06
from scene07_master_table import play_scene07


class FullEpisode01(Scene):
    def construct(self):
        # ---------------- SECTION 1: INTRO ----------------
        self.next_section("01_intro")
        IntroScene.construct(self)

        # ---------------- SECTION 2: SCENE 01 ----------------
        self.next_section("02_hook_question")
        play_scene01(self)

        # ---------------- SECTION 3: SCENE 02 ----------------
        self.next_section("03_arithmetic")
        play_scene02(self)

        # ---------------- SECTION 4: SCENE 03 ----------------
        self.next_section("04_dialogue")
        play_scene03(self)

        # ---------------- SECTION 5: SCENE 04 ----------------
        self.next_section("05_calculus")
        play_scene04(self)

        # ---------------- SECTION 6: SCENE 05 ----------------
        self.next_section("06_thinking")
        play_scene05(self)

        # ---------------- SECTION 7: SCENE 06 ----------------
        self.next_section("07_comparison")
        play_scene06(self)

        # ---------------- SECTION 8: SCENE 07 ----------------
        self.next_section("08_master_table")
        play_scene07(self)

        # ---------------- SECTION 9: OUTRO ----------------
        self.next_section("09_outro")
        OutroScene.construct(self)