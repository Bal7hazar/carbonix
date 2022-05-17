"""Dashboard view module."""

from colour import Color
from dash import Dash, Input, Output, dcc, html

from carbonix.views.contract import Contract
from carbonix.views.distribution import Distribution
from carbonix.views.sale import Sale


class Dashboard(Dash):
    """Dashboard class."""

    purple = Color("#A048FE")
    green = Color("#83DA90")

    def __init__(self, controller, *args, **kwargs):
        """Build a dashboard."""
        super().__init__(*args, **kwargs)
        self._controller = controller

        # content
        self.contract = Contract()
        self.distribution = Distribution()
        self.sale = Sale()

    def show(self):
        """Set up layout."""
        self.title = "Carbonix"
        self.layout = html.Div(
            children=[
                self.header(),
                self.project(),
                self.contract.section(),
                self.distribution.section(),
                self.sale.section(),
            ]
        )
        self.setup_callbacks()

    def setup_callbacks(self):
        """Set up callbacks."""
        self.callback(
            [
                Output(component_id="contract-name", component_property="children"),
                Output(
                    component_id="contract-description", component_property="children"
                ),
                Output(component_id="contract-address", component_property="children"),
                Output(component_id="contract-price", component_property="children"),
                Output(
                    component_id="contract-total_supply", component_property="children"
                ),
                Output(
                    component_id="contract-total_market_supply",
                    component_property="children",
                ),
                Output(
                    component_id="contract-total_reserved_supply",
                    component_property="children",
                ),
                Output(
                    component_id="contract-total_minted", component_property="children"
                ),
                Output(
                    component_id="contract-total_market_minted",
                    component_property="children",
                ),
                Output(
                    component_id="contract-total_reserved_minted",
                    component_property="children",
                ),
                Output(
                    component_id="contract-max_buy_at_once",
                    component_property="children",
                ),
                Output(
                    component_id="contract-supply_figure", component_property="figure"
                ),
                Output(
                    component_id="contract-minted_figure", component_property="figure"
                ),
                Output(
                    component_id="distribution-unique", component_property="children"
                ),
                Output(component_id="distribution-mean", component_property="children"),
                Output(
                    component_id="distribution-median", component_property="children"
                ),
                Output(
                    component_id="distribution-histogram_figure",
                    component_property="figure",
                ),
                Output(
                    component_id="distribution-network_figure",
                    component_property="srcDoc",
                ),
                Output(
                    component_id="sale-total_presale_mint",
                    component_property="children",
                ),
                Output(
                    component_id="sale-total_public_mint", component_property="children"
                ),
                Output(
                    component_id="sale-public_duration", component_property="children"
                ),
                Output(
                    component_id="sale-public_height", component_property="children"
                ),
                Output(
                    component_id="sale-histogram_figure", component_property="figure"
                ),
            ],
            Input(component_id="projects-dropdown", component_property="value"),
        )(self.update)

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

    def update(self, project_name):
        """Trigger the controller update method."""
        project = self._controller.projects.get(project_name)
        self._controller.update_view(project)
        return [
            self.contract.name,
            self.contract.description,
            self.contract.address,
            self.contract.price,
            self.contract.total_supply,
            self.contract.total_market_supply,
            self.contract.total_reserved_supply,
            self.contract.total_minted,
            self.contract.total_market_minted,
            self.contract.total_reserved_minted,
            self.contract.max_buy_at_once,
            self.contract.supply_figure,
            self.contract.minted_figure,
            self.distribution.unique,
            self.distribution.mean,
            self.distribution.median,
            self.distribution.histogram_figure,
            self.distribution.network_figure,
            self.sale.total_presale_mint,
            self.sale.total_public_mint,
            self.sale.public_duration,
            self.sale.public_height,
            self.sale.histogram_figure,
        ]
