"""Dashboard view module."""

from dash import Dash, Input, Output, dcc, html

from carbonix.views.contract import Contract
from carbonix.views.distribution import Distribution
from carbonix.views.sale import Sale


class Dashboard(Dash):
    """Dashboard class."""

    donation_addresses = [
        "tips.bal7hazar.eth",
        "0x4Ae827EcDB6Bc203846d904c3F7Dac0F72602d53",
    ]

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
            className="body",
            children=[
                self.header(),
                self.main(),
                self.footer(),
            ],
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
        """Return header markup."""
        title = "CarboniX"
        suffix = "A carbonABLE analytics story"
        project_names = list(self._controller.projects)
        return html.Header(
            className="header",
            children=[
                html.H1(
                    children=title,
                    className="header-title rainbow",
                ),
                html.Div(
                    children=dcc.Dropdown(
                        options=project_names,
                        value=project_names[0],
                        id="projects-dropdown",
                        className="header-projects",
                    ),
                    className="dropdown-container",
                )
            ],
        )

    def main(self):
        """Return main markup."""
        return html.Main(
            className="main",
            children=[
                self.contract.section(),
                self.distribution.section(),
                self.sale.section(),
            ],
        )

    def footer(self):
        """Return footer markup."""
        donation_content = (
            "This dashboard relies on donations, your support is welcome:"
        )
        links = dict(
            github=("https://github.com/Bal7hazar/carbonix", "./assets/images/github.svg"),
            carbonable=("https://carbonable.io", "https://media-exp1.licdn.com/dms/image/C4E0BAQHEBIyofLboAw/company-logo_200_200/0/1626797273186?e=2147483647&v=beta&t=oZD83CvpjbnISmIHklklRHUY26GvUtORBFaTUHA43Cc"),
            twitter=("https://twitter.com/Carbonable_io", "./assets/images/twitter.svg"),
            discord=("https://discord.gg/zUy9UvB7cd", "./assets/images/discord.svg"),
            linkedin=("https://fr.linkedin.com/company/carbonable", "./assets/images/linkedin.svg"),
            medium=("https://carbonable.medium.com/", "./assets/images/medium.svg"),
        )
        return html.Footer(
            className="footer",
            children=[
                html.Div(
                    className="footer-donation",
                    children=[
                        html.P(
                            donation_content,
                            className="footer-donation-content",
                        ),
                        html.Ul(
                            className="footer-donation-addresses",
                            children=[
                                html.Li(address, className="footer-donation-address")
                                for address in self.donation_addresses
                            ],
                        ),
                    ],
                ),
                html.Ul(
                    className="footer-links",
                    children=[
                        html.Li(
                            children=[
                                html.A(
                                    html.Img(
                                        src=logo,
                                        alt=platform,
                                        className="logo-brand",
                                    ),
                                    href=link,
                                )
                            ],
                            className="footer-link",
                        )
                        for platform, (link, logo) in links.items()
                    ],
                ),
            ],
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
