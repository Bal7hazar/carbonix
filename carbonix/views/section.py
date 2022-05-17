"""Section view module."""

from dash import html

from carbonix.views import GREEN, PURPLE


class Section:
    """Section class."""

    @staticmethod
    def linear_gradian_spans(title):
        """Return colored spans."""
        colors = [color.hex_l for color in PURPLE.range_to(GREEN, len(title))]
        return [
            html.Span(letter, style={"color": f"{color}"})
            for letter, color in zip(title, colors)
        ]
