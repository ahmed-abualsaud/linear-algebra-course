from manim import *

# استيراد الإنترو والأوترو والفريم
from common.identity import IntroScene, OutroScene

# استيراد المشاهد مباشرة وبمنتهى النظافة
from scene01_intro import play_scene01
from scene02_recall_numbers import play_scene02
from scene03_adding_numbers import play_scene03
from scene04_build_from_lines import play_scene04
from scene05_adding_vectors import play_scene05
from scene06_closure import play_scene06
from scene07_zero_vector import play_scene07
from scene08_inverse import play_scene08
from scene09_commutativity import play_scene09
from scene10_associativity import play_scene10
from scene11_conclusion import play_scene11


class Episode05(Scene):
    def construct(self):
        # ---------------- SECTION 1: INTRO ----------------
        self.next_section("01_intro")
        IntroScene.construct(self)

        self.next_section("chapter_01")
        play_scene01(self)
        print("END01", self.renderer.num_plays, flush=True)

        self.next_section("chapter_02")
        play_scene02(self)
        print("END02", self.renderer.num_plays, flush=True)

        self.next_section("chapter_03")
        play_scene03(self)
        print("END03", self.renderer.num_plays, flush=True)

        self.next_section("chapter_04")
        play_scene04(self)
        print("END04", self.renderer.num_plays, flush=True)

        self.next_section("chapter_05")
        play_scene05(self)
        print("END05", self.renderer.num_plays, flush=True)

        self.next_section("chapter_06")
        play_scene06(self)
        print("END06", self.renderer.num_plays, flush=True)

        self.next_section("chapter_07")
        play_scene07(self)
        print("END07", self.renderer.num_plays, flush=True)

        self.next_section("chapter_08")
        play_scene08(self)
        print("END08", self.renderer.num_plays, flush=True)

        self.next_section("chapter_09")
        play_scene09(self)
        print("END09", self.renderer.num_plays, flush=True)

        self.next_section("chapter_10")
        play_scene10(self)
        print("END10", self.renderer.num_plays, flush=True)

        self.next_section("chapter_11")
        play_scene11(self)
        print("END11", self.renderer.num_plays, flush=True)

        # ---------------- SECTION 12: OUTRO ----------------
        self.next_section("12_outro")
        OutroScene.construct(self)
