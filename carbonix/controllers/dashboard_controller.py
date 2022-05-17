"""Dashboard controller module."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from colour import Color
from plotly.subplots import make_subplots
from pyvis.network import Network

from carbonix.models.project import Project
from carbonix.resources import CONTRACT_ADDRESSES, RESOURCES_PATH
from carbonix.views.dashboard import Dashboard


class DashboardController:
    """DashboardController class."""

    piechart_layout = dict(
        template="presentation",
        barmode="stack",
        font=dict(size=12),
        font_color="white",
        width=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    histogram_layout = dict(
        template="presentation",
        barmode="stack",
        font=dict(size=12),
        font_color="white",
        width=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    pyvis_template_path = (RESOURCES_PATH / "pyvis_template.html").as_posix()

    purple = Color("#A048FE")
    green = Color("#83DA90")

    def __init__(self) -> None:
        """Build a dashboard controller."""
        projects = [Project(address) for address in CONTRACT_ADDRESSES]
        self.projects = {project.name: project for project in projects}
        self.view = Dashboard(self)
        self.update(next(iter(self.projects.values())))

    def update(self, project):
        """Update the whole view."""
        self.update_contract(project)
        self.update_distribution(project)
        self.update_sale(project)
        self.view.setup_layout()

    def update_contract(self, project):
        """Update contract view of the project."""
        # data
        market_supply = project.total_market_supply
        whitelist_supply = project.total_whitelist_supply
        reserved_supply = project.total_reserved_supply
        public_supply = market_supply - whitelist_supply - reserved_supply

        market_minted = project.total_market_minted
        whitelist_minted = project.total_whitelist_minted
        reserved_minted = project.total_reserved_minted
        public_minted = market_minted - whitelist_minted - reserved_minted

        # metrics
        price, unit = project.to_juno(project.price, unit=project.price_unit)
        self.view.contract_metrics = {
            "total_supply": market_supply + reserved_supply,
            "total_market_supply": market_supply,
            "total_reserved_supply": reserved_supply,
            "total_minted": market_supply + reserved_supply,
            "total_market_minted": market_minted,
            "total_reserved_minted": reserved_supply,
            "max_buy_at_once": project.max_buy_at_once,
            "price": price,
            "unit": unit,
            "name": project.name,
            "description": project.description,
            "image": project.image,
            "address": project.short(project.address),
            "mintscan": project.mintscan,
        }

        # supply
        data = pd.DataFrame.from_dict(
            {
                "whitelist": whitelist_supply,
                "reserved": reserved_supply,
                "public": public_supply,
            },
            orient="index",
            columns=["supply"],
        )
        data["name"] = data.index.to_series()

        colors = [
            color.hex_l for color in self.purple.range_to(self.green, data.shape[0])
        ]
        fig = go.Figure(data=[go.Pie(labels=data.name, values=data.supply)])
        fig.update_traces(
            hoverinfo="label+percent",
            textinfo="value",
            textfont_size=20,
            marker=dict(colors=colors, line=dict(color="#000000", width=2)),
        )
        fig.update_layout(self.piechart_layout)
        self.view.contract_supply = {
            "total_market_supply": market_supply + reserved_supply,
            "contract_supply_figure": fig,
        }

        # minted
        data = pd.DataFrame.from_dict(
            {
                "whitelist": whitelist_minted,
                "reserved": reserved_minted,
                "public": public_minted,
            },
            orient="index",
            columns=["minted"],
        )
        data["name"] = data.index.to_series()

        colors = [
            color.hex_l for color in self.purple.range_to(self.green, data.shape[0])
        ]
        fig = go.Figure(data=[go.Pie(labels=data.name, values=data.minted)])
        fig.update_traces(
            hoverinfo="label+percent",
            textinfo="value",
            textfont_size=20,
            marker=dict(colors=colors, line=dict(color="#000000", width=2)),
        )
        fig.update_layout(self.piechart_layout)
        self.view.contract_minted = {
            "total_market_minted": market_minted + reserved_minted,
            "contract_minted_figure": fig,
        }

    def update_distribution(self, project):
        """Update distribution view of the project."""
        # data
        mints = project.mints()
        price = project.price
        tokens = dict()
        for _, tx_info in mints.items():
            address = tx_info.get("address")
            token = tx_info.get("amount") / price
            tokens[address] = tokens.get(address, 0) + token
        unique_count = len(tokens)
        data = pd.DataFrame.from_dict(
            tokens,
            orient="index",
            columns=["token"],
        ).sort_values(by="token")

        # metrics
        self.view.distribution_metrics = {
            "median": f"{data.token.median():.1f}",
            "mean": f"{data.token.mean():.1f}",
            "unique_count": unique_count,
        }

        # histogram
        maximum = int(max(data.token))
        colors = [color.hex_l for color in self.purple.range_to(self.green, maximum)]
        color_map = {idx: color for idx, color in enumerate(colors, start=1)}

        fig = px.histogram(
            data.sort_values(by="token"),
            x="token",
            nbins=maximum,
            color="token",
            color_discrete_map=color_map,
            template=self.histogram_layout.get("template"),
            labels={"token": "Token owned per address"},
        )
        layout = self.histogram_layout.copy()
        layout.update(
            {
                "bargap": 0.4,
            }
        )
        fig.update_layout(layout)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(marker={"line": {"color": "black", "width": 2}})

        self.view.distribution_histogram = {
            "distribution_histogram": fig,
        }

        # network
        network = Network(
            height="650px", width="100%", font_color="white", bgcolor="rgba(0,0,0,0)"
        )
        network.path = self.pyvis_template_path
        for address in tokens:
            amount = int(tokens.get(address))

            color = colors[int(amount) - 1]
            network.add_node(
                address,
                label=str(amount),
                title=address,
                size=amount * 10,
                color=color,
            )

        self.view.distribution_network = {
            "distribution_network": network.generate_html(),
        }

    def update_sale(self, project):
        """Update sale view of the project."""
        # data
        mints = project.mints()
        price = project.price
        sale_timestamp = project.sale_timestamp
        presale_timestamp = project.presale_timestamp
        last_timestamp = list(mints.values())[-1].get("timestamp")
        data = pd.DataFrame.from_dict(mints, orient="index")
        data["mint"] = data.amount.div(price)
        data["cumulative"] = data.mint.cumsum()

        pre_sale_filter = data.timestamp < sale_timestamp
        sale_filter = data.timestamp >= sale_timestamp

        self.view.sale_metrics = {
            "total_pre_sale_mint": data[pre_sale_filter].shape[0],
            "total_sale_mint": data[sale_filter].shape[0],
            "total_sale_time": str(
                data[sale_filter].timestamp.max()
                - data[sale_filter].timestamp.min()
                + project.height_timedelta
            ),
            "total_sale_height": data[sale_filter].height.max()
            - data[sale_filter].height.min()
            + 1,
        }

        # histogram
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(
                x=data[pre_sale_filter].timestamp,
                y=data[pre_sale_filter].mint,
                xperiod=60e3,
                xperiodalignment="middle",
                marker_color=self.purple.hex_l,
                name="Mint (whitelist)",
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Bar(
                x=data[sale_filter].timestamp,
                y=data[sale_filter].mint,
                xperiod=60e3,
                xperiodalignment="middle",
                marker_color=self.green.hex_l,
                name="Mint (public)",
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=data.timestamp,
                y=data.cumulative,
                xperiod=60e3,
                xperiodalignment="middle",
                name="Cumulative mints",
                line=dict(color="lightgrey", width=1),
                visible="legendonly",
            ),
            secondary_y=True,
        )

        # update layout
        layout = self.histogram_layout.copy()
        layout.update(
            {
                "bargap": 0.1,
            }
        )
        fig.update_layout(layout)
        fig.update_traces(marker={"line": {"color": "black", "width": 2}})
        time_offset = pd.Timedelta(minutes=5)
        fig.update_xaxes(
            range=[presale_timestamp - time_offset, last_timestamp + time_offset],
            dtick=10 * 60e3,
        )
        fig.update_yaxes(
            title_text="Mint events [1]", secondary_y=False, showgrid=False
        )
        fig.update_yaxes(
            title_text="Cumulative mints [1]",
            secondary_y=True,
            showgrid=False,
            range=[0, int(data.cumulative.max())],
        )

        # update view
        self.view.sale_histogram = {"sale_histogram": fig}

    def run(self):
        """Run application."""
        self.view.run_server(debug=True)
