"""Sale view module."""

import plotly.graph_objects as go
from dash import dcc, html

from carbonix.views import HISTOGRAM_LAYOUT
from carbonix.views.section import Section


class Sale(Section):
    """Sale class."""

    def __init__(self):
        """Build a sale."""
        # metrics
        self._unique = None
        self._mean = None
        self._median = None

        # supply
        self._histogram_figure = go.Figure(layout=HISTOGRAM_LAYOUT)

        # minted
        self._network_figure = go.Figure(layout=HISTOGRAM_LAYOUT)

    @property
    def total_presale_mint(self):
        """Return total presale mint events."""
        return f"- `Total presale mint events: {self._total_presale_mint}`"

    @total_presale_mint.setter
    def total_presale_mint(self, total_presale_mint):
        self._total_presale_mint = total_presale_mint

    @property
    def total_public_mint(self):
        """Return total public mint events."""
        return f"- `Total public sale mint events: {self._total_public_mint}`"

    @total_public_mint.setter
    def total_public_mint(self, total_public_mint):
        self._total_public_mint = total_public_mint

    @property
    def public_duration(self):
        """Return public sale duration."""
        return f"- `Public sale sold out duration: {self._public_duration}`"

    @public_duration.setter
    def public_duration(self, public_duration):
        self._public_duration = public_duration

    @property
    def public_height(self):
        """Return public sale height."""
        return f"- `Public sale sold out over {self._public_height} heights`"

    @public_height.setter
    def public_height(self, public_height):
        self._public_height = public_height

    @property
    def histogram_figure(self):
        """Return histogram figure."""
        return self._histogram_figure

    @histogram_figure.setter
    def histogram_figure(self, figure):
        self._histogram_figure = figure

    def section(self):
        """Return section."""
        return html.Div(
            children=[
                html.H3(
                    children="SALE",
                    style={"textAlign": "left"},
                ),
                html.Hr(className="section-underline"),
                html.Div(
                    id="sale-content",
                    children=self.children(),
                    style={"display": "flex"},
                ),
            ],
            className="section",
        )

    def children(self):
        """Return children."""
        return [
            self.metrics(),
            self.histogram(),
        ]

    def metrics(self):
        """Return metrics."""
        children = [
            html.H5(children=self.linear_gradian_spans("MetriX")),
            html.Hr(className="topic-underline"),
            dcc.Markdown(self.total_presale_mint, id="sale-total_presale_mint"),
            dcc.Markdown(self.total_public_mint, id="sale-total_public_mint"),
            dcc.Markdown(self.public_duration, id="sale-public_duration"),
            dcc.Markdown(self.public_height, id="sale-public_height"),
        ]
        return html.Div(
            children=children,
            className="topic",
        )

    def histogram(self):
        """Return historgram of sales event."""
        children = [
            html.H5("Mint events"),
            html.Hr(className="topic-underline"),
            dcc.Graph(id="sale-histogram_figure", figure=self.histogram_figure),
        ]
        return html.Div(children=children, className="topic", style={"width": "100%"})
