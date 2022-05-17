"""Dashboard view module."""

from colour import Color
from dash import Dash, Input, Output, dcc, html


class Dashboard(Dash):
    """Dashboard class."""

    purple = Color("#A048FE")
    green = Color("#83DA90")

    def __init__(self, controller, *args, **kwargs):
        """Build a dashboard."""
        super().__init__(*args, **kwargs)
        self._controller = controller

        # content
        self._contract_metrics = None
        self._contract_supply = None
        self._contract_minted = None
        self._distribution_metrics = None
        self._distribution_histogram = None
        self._distribution_network = None
        self._sale_metrics = None
        self._sale_histogram = None

        # setup
        self.setup_layout()
        self.callback(
            [
                Output(component_id="contract-content", component_property="children"),
                Output(
                    component_id="distribution-content", component_property="children"
                ),
                Output(component_id="sale-content", component_property="children"),
            ],
            Input(component_id="projects-dropdown", component_property="value"),
        )(self.update)

    def setup_layout(self):
        """Set up layout."""
        self.title = "Carbonix"
        self.layout = html.Div(
            children=[
                self.header(),
                self.project(),
                self.contract_section(),
                self.distribution_section(),
                self.sale_section(),
                self.garbage(),
            ]
        )

    def header(self):
        """Return title view."""
        title = "CarboniX"
        colors = [color.hex_l for color in self.purple.range_to(self.green, len(title))]
        return html.Div(
            children=[
                html.H1(
                    children=[
                        html.Span(letter, style={"color": f"{color}"})
                        for letter, color in zip(title, colors)
                    ],
                    style={
                        "textAlign": "center",
                        "margin-top": "50px",
                    },
                ),
                html.H6("A carbonABLE analytics story", style={"textAlign": "center"}),
            ]
        )

    def project(self):
        """Return project selection view."""
        project_names = list(self._controller.projects)
        return html.Div(
            children=[
                dcc.Dropdown(
                    options=project_names,
                    value=project_names[0],
                    id="projects-dropdown",
                    className="dropdown-menu-center",
                ),
            ],
            style={"margin": "0% 40% 0% 40%"},
        )

    def garbage(self):
        """Return garbage view."""
        return html.Div(id="garbage", style={"display": "none"})

    def update(self, project_name):
        """Trigger the controller update method."""
        project = self._controller.projects.get(project_name)
        self._controller.update(project)
        return [
            self.contract_children(),
            self.distribution_children(),
            self.sale_children(),
        ]

    def contract_section(self):
        """Return contract header."""
        header = html.H3(
            children="CONTRACT",
            style={
                "textAlign": "left",
            },
        )
        return html.Div(
            children=[
                header,
                html.Hr(className="section-underline"),
                self.contract_content(),
            ],
            className="section",
        )

    def contract_content(self):
        """Return contract content."""
        return html.Div(
            id="contract-content",
            children=self.contract_children(),
            style={"display": "flex"},
        )

    def contract_children(self):
        """Return contract children."""
        return [
            self.contract_metrics,
            self.contract_supply,
            self.contract_minted,
        ]

    @property
    def contract_metrics(self):
        """Return contract information."""
        return self._contract_metrics

    @contract_metrics.setter
    def contract_metrics(self, kwargs):
        title = "MetriX"
        colors = [color.hex_l for color in self.purple.range_to(self.green, len(title))]
        children = [
            html.H5(
                children=[
                    html.Span(letter, style={"color": f"{color}"})
                    for letter, color in zip(title, colors)
                ]
            ),
            html.Hr(className="topic-underline"),
            dcc.Markdown(f"- `Name: {kwargs.get('name')}`"),
            dcc.Markdown(f"- `Description: {kwargs.get('description')}`"),
            dcc.Markdown(
                f"- `Contract: `[`{kwargs.get('address')}`]({kwargs.get('mintscan')})"
            ),
            dcc.Markdown(f"- `Price: {kwargs.get('price')} ${kwargs.get('unit')}`"),
            dcc.Markdown(f"- `Total supply: {kwargs.get('total_supply')}`"),
            dcc.Markdown(
                f"- `Total market supply: {kwargs.get('total_market_supply')}`"
            ),
            dcc.Markdown(
                f"- `Total reserved supply: {kwargs.get('total_reserved_supply')}`"
            ),
            dcc.Markdown(f"- `Total minted: {kwargs.get('total_minted')}`"),
            dcc.Markdown(
                f"- `Total market minted: {kwargs.get('total_market_minted')}`"
            ),
            dcc.Markdown(
                f"- `Total reserved minted: {kwargs.get('total_reserved_minted')}`"
            ),
            dcc.Markdown(
                f"- `Total market supply: {kwargs.get('total_market_supply')}`"
            ),
            dcc.Markdown(f"- `Max buy at once: {kwargs.get('max_buy_at_once')}`"),
        ]
        self._contract_metrics = html.Div(
            children=children, className="topic", style={"width": "30%"}
        )

    @property
    def contract_supply(self):
        """Return contract supply."""
        return self._contract_supply

    @contract_supply.setter
    def contract_supply(self, kwargs):
        children = [
            html.H5("Total supply"),
            html.Hr(className="topic-underline"),
            dcc.Graph(
                id="contract_supply_figure", figure=kwargs.get("contract_supply_figure")
            ),
        ]
        self._contract_supply = html.Div(
            children=children, className="topic", style={"width": "35%"}
        )

    @property
    def contract_minted(self):
        """Return contract minted."""
        return self._contract_minted

    @contract_minted.setter
    def contract_minted(self, kwargs):
        children = [
            html.H5("Total minted"),
            html.Hr(className="topic-underline"),
            dcc.Graph(
                id="contract_minted_figure", figure=kwargs.get("contract_minted_figure")
            ),
        ]
        self._contract_minted = html.Div(
            children=children, className="topic", style={"width": "35%"}
        )

    def distribution_section(self):
        """Return distribution header."""
        header = html.H3(
            children="DISTRIBUTION",
            style={
                "textAlign": "left",
            },
        )
        return html.Div(
            children=[
                header,
                html.Hr(className="section-underline"),
                self.distribution_content(),
            ],
            className="section",
        )

    def distribution_content(self):
        """Return distribution content."""
        return html.Div(
            id="distribution-content",
            children=self.distribution_children(),
            style={"display": "flex"},
        )

    def distribution_children(self):
        """Return distribution children."""
        return [
            html.Div(
                children=[self.distribution_metrics, self.distribution_histogram],
                style={"width": "50%"},
            ),
            self.distribution_network,
        ]

    @property
    def distribution_metrics(self):
        """Return distribution metrics."""
        return self._distribution_metrics

    @distribution_metrics.setter
    def distribution_metrics(self, kwargs):
        title = "MetriX"
        colors = [color.hex_l for color in self.purple.range_to(self.green, len(title))]
        children = [
            html.H5(
                children=[
                    html.Span(letter, style={"color": f"{color}"})
                    for letter, color in zip(title, colors)
                ]
            ),
            html.Hr(className="topic-underline"),
            dcc.Markdown(f"- `Unique addresses: {kwargs.get('unique_count')}`"),
            dcc.Markdown(f"- `Mean: {kwargs.get('mean')}`"),
            dcc.Markdown(f"- `Median: {kwargs.get('median')}`"),
        ]
        self._distribution_metrics = html.Div(
            children=children,
            className="topic",
        )

    @property
    def distribution_histogram(self):
        """Return histogram of distribution."""
        return self._distribution_histogram

    @distribution_histogram.setter
    def distribution_histogram(self, kwargs):
        children = [
            html.H5("Minters"),
            html.Hr(className="topic-underline"),
            dcc.Graph(
                id="distribution_histogram", figure=kwargs.get("distribution_histogram")
            ),
        ]
        self._distribution_histogram = html.Div(
            children=children,
            className="topic",
        )

    @property
    def distribution_network(self):
        """Return network of distribution."""
        return self._distribution_network

    @distribution_network.setter
    def distribution_network(self, kwargs):
        children = [
            html.H5("Network"),
            html.Hr(className="topic-underline"),
            html.Iframe(
                srcDoc=kwargs.get("distribution_network"),
                style={"border": "none", "width": "100%", "height": "100%"},
            ),
        ]
        self._distribution_network = html.Div(
            children=children, className="topic", style={"width": "50%"}
        )

    def sale_section(self):
        """Return sale section."""
        header = html.H3(
            children="SALE",
            style={
                "textAlign": "left",
            },
        )
        return html.Div(
            children=[
                header,
                html.Hr(className="section-underline"),
                self.sale_content(),
            ],
            className="section",
        )

    def sale_content(self):
        """Return sale content."""
        return html.Div(
            id="sale-content", children=self.sale_children(), style={"display": "flex"}
        )

    def sale_children(self):
        """Return sale children."""
        return [
            self.sale_metrics,
            self.sale_histogram,
        ]

    @property
    def sale_metrics(self):
        """Return sale metrics."""
        return self._sale_metrics

    @sale_metrics.setter
    def sale_metrics(self, kwargs):
        title = "MetriX"
        colors = [color.hex_l for color in self.purple.range_to(self.green, len(title))]
        children = [
            html.H5(
                children=[
                    html.Span(letter, style={"color": f"{color}"})
                    for letter, color in zip(title, colors)
                ]
            ),
            html.Hr(className="topic-underline"),
            dcc.Markdown(
                f"- `Total presale mint events: {kwargs.get('total_pre_sale_mint')}`"
            ),
            dcc.Markdown(
                f"- `Total public sale mint events: {kwargs.get('total_sale_mint')}`"
            ),
            dcc.Markdown(f"- `Public sale duration: {kwargs.get('total_sale_time')}`"),
            dcc.Markdown(
                f"- `Public sale sold out over {kwargs.get('total_sale_height')} heights`"
            ),
        ]
        self._sale_metrics = html.Div(
            children=children, className="topic", style={"width": "20%"}
        )

    @property
    def sale_histogram(self):
        """Return historgram of sales event."""
        return self._sale_histogram

    @sale_histogram.setter
    def sale_histogram(self, kwargs):
        children = [
            html.H5("Mint events"),
            html.Hr(className="topic-underline"),
            dcc.Graph(id="sale_histogram", figure=kwargs.get("sale_histogram")),
        ]
        self._sale_histogram = html.Div(
            children=children, className="topic", style={"width": "100%"}
        )
