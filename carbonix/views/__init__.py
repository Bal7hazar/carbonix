"""Views package."""
from colour import Color

PURPLE = Color("#A048FE")
GREEN = Color("#83DA90")
PIECHART_LAYOUT = dict(
    template="presentation",
    barmode="stack",
    font=dict(size=12),
    font_color="white",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)
HISTOGRAM_LAYOUT = dict(
    template="presentation",
    barmode="stack",
    font=dict(size=12),
    font_color="white",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)
