"""
Shared setup for every Mach-Math scene: importing this package (which happens
automatically the moment any lesson does `from common... import ...`) applies
the channel-wide render config once, in one place.
"""
from manim import config

config.background_color = "#000000"