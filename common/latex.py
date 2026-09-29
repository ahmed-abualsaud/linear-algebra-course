"""
قالب LaTeX الموحّد لكل معادلات الكورس — خط رياضي حديث (cmbright) بدل الافتراضي.
"""
from manim import TexTemplate

mach_math_template = TexTemplate()
mach_math_template.add_to_preamble(r"\usepackage{cmbright}")