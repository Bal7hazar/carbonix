"""Distribution view module."""

import plotly.graph_objects as go
from dash import dcc, html

from carbonix.views import HISTOGRAM_LAYOUT
from carbonix.views.section import Section


class Distribution(Section):
    """Distribution class."""

    def __init__(self):
        """Build a distribution."""
        # metrics
        self._unique = None
        self._mean = None
        self._median = None

        # supply
        self._histogram_figure = go.Figure(layout=HISTOGRAM_LAYOUT)

        # minted
        self._network_figure = go.Figure(layout=HISTOGRAM_LAYOUT)

    @property
    def unique(self):
        """Return unique."""
        return f"- `Unique addresses: {self._unique}`"

    @unique.setter
    def unique(self, unique):
        self._unique = unique

    @property
    def mean(self):
        """Return mean."""
        return f"- `Mean: {self._mean}`"

    @mean.setter
    def mean(self, mean):
        self._mean = mean

    @property
    def median(self):
        """Return median."""
        return f"- `Median: {self._median}`"

    @median.setter
    def median(self, median):
        self._median = median

    @property
    def histogram_figure(self):
        """Return histogram figure."""
        return self._histogram_figure

    @histogram_figure.setter
    def histogram_figure(self, figure):
        self._histogram_figure = figure

    @property
    def network_figure(self):
        """Return network figure."""
        return self._network_figure

    @network_figure.setter
    def network_figure(self, network_figure):
        self._network_figure = network_figure

    def section(self):
        """Return section."""
        return html.Div(
            children=[
                html.H3(
                    children="DISTRIBUTION",
                    style={"textAlign": "left"},
                ),
                html.Hr(className="section-underline"),
                html.Div(
                    id="distribution-content",
                    children=self.children(),
                    style={"display": "flex"},
                ),
            ],
            className="section",
        )

    def children(self):
        """Return children."""
        return [
            html.Div(
                children=[self.metrics(), self.histogram()],
                style={"width": "50%"},
            ),
            self.network(),
        ]

    def metrics(self):
        """Return metrics."""
        children = [
            html.H5(children=self.linear_gradian_spans("MetriX")),
            html.Hr(className="topic-underline"),
            dcc.Markdown(self.unique, id="distribution-unique"),
            dcc.Markdown(self.mean, id="distribution-mean"),
            dcc.Markdown(self.median, id="distribution-median"),
        ]
        return html.Div(
            children=children,
            className="topic",
        )

    def histogram(self):
        """Return histogram of distribution."""
        children = [
            html.H5("Minters"),
            html.Hr(className="topic-underline"),
            dcc.Graph(
                id="distribution-histogram_figure",
                figure=self.histogram_figure,
            ),
        ]
        return html.Div(
            children=children,
            className="topic",
        )

    def network(self):
        """Return network of distribution."""
        children = [
            html.H5("Network"),
            html.Hr(className="topic-underline"),
            html.Iframe(
                srcDoc=self.network_figure,
                id="distribution-network_figure",
                style={"border": "none", "width": "100%", "height": "100%"},
            ),
        ]
        return html.Div(children=children, className="topic", style={"width": "50%"})
