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
        return html.P(f"Unique addresses: {self._unique}", id="distribution-unique")

    @unique.setter
    def unique(self, unique):
        self._unique = unique

    @property
    def mean(self):
        """Return mean."""
        return html.P(f"Mean: {self._mean}", id="distribution-mean")

    @mean.setter
    def mean(self, mean):
        self._mean = mean

    @property
    def median(self):
        """Return median."""
        return html.P(f"Median: {self._median}", id="distribution-median")

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
                html.H3("Distribution", className="section-title"),
                html.Div(
                    id="distribution-container",
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
            self.network(),
        ]

    def metrics(self):
        """Return metrics."""
        infos = [
            self.unique,
            self.mean,
            self.median,
        ]
        children = [
            html.H4("MetriX", className="topic-title rainbow"),
            html.Ul(
                children=[html.Li(info, className="metrics-item") for info in infos],
                className="metrics-container",
            ),
        ]
        return html.Div(children=children, className="topic", id="distirbution-metrics")

    def histogram(self):
        """Return histogram of distribution."""
        children = [
            html.H4("Minters", className="topic-title"),
            dcc.Graph(
                id="distribution-histogram_figure",
                figure=self.histogram_figure,
            ),
        ]
        return html.Div(
            children=children, className="topic", id="distribution-histogram-figure"
        )

    def network(self):
        """Return network of distribution."""
        children = [
            html.H4("Network", className="topic-title"),
            html.Iframe(
                srcDoc=self.network_figure,
                id="distribution-network_figure",
            ),
        ]
        return html.Div(
            children=children, className="topic", id="distribution-network-figure"
        )
