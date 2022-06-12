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
        return html.P(
            f"Total presale mint events: {self._total_presale_mint}",
            id="sale-total_presale_mint",
        )

    @total_presale_mint.setter
    def total_presale_mint(self, total_presale_mint):
        self._total_presale_mint = total_presale_mint

    @property
    def total_public_mint(self):
        """Return total public mint events."""
        return html.P(
            f"Total public sale mint events: {self._total_public_mint}",
            id="sale-total_public_mint",
        )

    @total_public_mint.setter
    def total_public_mint(self, total_public_mint):
        self._total_public_mint = total_public_mint

    @property
    def public_duration(self):
        """Return public sale duration."""
        return html.P(
            f"Public sale sold out duration: {self._public_duration}",
            id="sale-public_duration",
        )

    @public_duration.setter
    def public_duration(self, public_duration):
        self._public_duration = public_duration

    @property
    def public_height(self):
        """Return public sale height."""
        return html.P(
            f"Public sale sold out over {self._public_height} heights",
            id="sale-public_height",
        )

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
                html.H3("Sale", className="section-title"),
                html.Div(
                    id="sale-content",
                    className="topic-container",
                    children=self.children(),
                ),
            ],
            className="section-container",
        )

    def children(self):
        """Return children."""
        return [
            self.metrics(),
            self.histogram(),
        ]

    def metrics(self):
        """Return metrics."""
        infos = [
            self.total_presale_mint,
            self.total_public_mint,
            self.public_duration,
            self.public_height,
        ]
        children = [
            html.H4("MetriX", className="topic-title rainbow"),
            html.Ul(
                children=[html.Li(info, className="metrics-item") for info in infos],
                className="metrics-container",
            ),
        ]
        return html.Div(children=children, className="topic")

    def histogram(self):
        """Return historgram of sales event."""
        children = [
            html.H4("Mint events", className="topic-title"),
            dcc.Graph(id="sale-histogram_figure", figure=self.histogram_figure),
        ]
        return html.Div(
            children=children, className="topic", id="sale-histogram-figure"
        )
