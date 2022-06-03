"""Dashboard controller module."""

import pickle

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pyvis.network import Network

from carbonix.models.project import Project
from carbonix.resources import CONTRACT_ADDRESSES, RESOURCES_PATH
from carbonix.views import GREEN, HISTOGRAM_LAYOUT, PIECHART_LAYOUT, PURPLE
from carbonix.views.dashboard import Dashboard


class DashboardController:
    """DashboardController class."""

    pyvis_template_path = (RESOURCES_PATH / "pyvis_template.html").as_posix()

    def __init__(self, name) -> None:
        """Build a dashboard controller."""
        projects = [self.load_project(address) for address in CONTRACT_ADDRESSES]
        self.projects = {project.name: project for project in projects}
        self.view = Dashboard(self, name)
        for project in reversed(projects):
            self.update_view(project)
        self.view.show()

    @staticmethod
    def load_project(address):
        """Load project."""
        path = (RESOURCES_PATH / address).with_suffix(".pickle")
        if not path.exists():
            project = Project(address)
            with open(path.as_posix(), "wb") as pickle_file:
                pickle.dump(project, pickle_file)
            return project

        with open(path.as_posix(), "rb") as pickle_file:
            return pickle.load(pickle_file)

    def update_view(self, project):
        """Update the whole view."""
        if project:
            project.check_update()
            self.update_contract(project)
            self.update_distribution(project)
            self.update_sale(project)

    def update_contract(self, project):
        """Update contract view of the project."""
        # metrics
        price, unit = project.to_juno(project.price, project.unit)
        self.view.contract.name = project.name
        self.view.contract.description = project.description
        self.view.contract.price = price
        self.view.contract.unit = unit
        self.view.contract.address = project.short(project.address)
        self.view.contract.mintscan = project.mintscan
        self.view.contract.max_buy_at_once = project.max_buy_at_once

        self.view.contract.total_supply = project.total_supply
        self.view.contract.total_market_supply = project.total_market_supply
        self.view.contract.total_reserved_supply = project.total_reserved_supply
        self.view.contract.total_minted = project.total_minted
        self.view.contract.total_market_minted = project.total_market_minted
        self.view.contract.total_reserved_minted = project.total_reserved_minted

        # supply
        data = pd.DataFrame.from_dict(
            {
                "whitelist": project.total_whitelist_supply,
                "reserved": project.total_reserved_supply,
                "public": project.total_public_supply,
            },
            orient="index",
            columns=["supply"],
        )
        data["name"] = data.index.to_series()
        colors = [color.hex_l for color in PURPLE.range_to(GREEN, data.shape[0])]
        fig = go.Figure(data=[go.Pie(labels=data.name, values=data.supply)])
        fig.update_traces(
            hoverinfo="label+percent",
            textinfo="value",
            textfont_size=20,
            marker=dict(colors=colors, line=dict(color="#000000", width=2)),
        )
        fig.update_layout(PIECHART_LAYOUT)
        self.view.contract.supply_figure = fig

        # minted
        data = pd.DataFrame.from_dict(
            {
                "whitelist": project.total_whitelist_minted,
                "reserved": project.total_reserved_minted,
                "public": project.total_public_minted,
            },
            orient="index",
            columns=["minted"],
        )
        data["name"] = data.index.to_series()
        colors = [color.hex_l for color in PURPLE.range_to(GREEN, data.shape[0])]
        fig = go.Figure(data=[go.Pie(labels=data.name, values=data.minted)])
        fig.update_traces(
            hoverinfo="label+percent",
            textinfo="value",
            textfont_size=20,
            marker=dict(colors=colors, line=dict(color="#000000", width=2)),
        )
        fig.update_layout(PIECHART_LAYOUT)
        self.view.contract.minted_figure = fig

    def update_distribution(self, project):
        """Update distribution view of the project."""
        # data
        txs = project.mints()
        price = project.price
        tokens = dict()
        for txn in txs:
            address = txn.sender
            token = txn.amount / price
            tokens[address] = tokens.get(address, 0) + token
        unique_count = len(tokens)
        data = pd.DataFrame.from_dict(
            tokens,
            orient="index",
            columns=["token"],
        ).sort_values(by="token")

        # metrics
        self.view.distribution.unique = unique_count
        self.view.distribution.mean = f"{data.token.mean():.1f}"
        self.view.distribution.median = f"{data.token.median():.1f}"

        # histogram
        maximum = int(max(data.token))
        colors = [color.hex_l for color in PURPLE.range_to(GREEN, maximum)]
        color_map = dict(enumerate(colors, start=1))

        fig = px.histogram(
            data.sort_values(by="token"),
            x="token",
            nbins=maximum,
            color="token",
            color_discrete_map=color_map,
            template=HISTOGRAM_LAYOUT.get("template"),
            labels={"token": "Token owned per address"},
        )
        layout = HISTOGRAM_LAYOUT.copy()
        layout.update(
            {
                "bargap": 0.4,
            }
        )
        fig.update_layout(layout)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(marker={"line": {"color": "black", "width": 2}})

        self.view.distribution.histogram_figure = fig

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

        self.view.distribution.network_figure = network.generate_html()

    def update_sale(self, project):
        """Update sale view of the project."""
        # data
        txs = project.mints()
        price = project.price
        sale_timestamp = project.sale_timestamp
        presale_timestamp = project.presale_timestamp
        last_timestamp = txs[-1].timestamp

        mints = {
            txn.hash: dict(
                timestamp=txn.timestamp,
                height=txn.height,
                amount=txn.amount,
            )
            for txn in txs
        }
        
        data = pd.DataFrame.from_dict(mints, orient="index")
        data["mint"] = data.amount.div(price)
        data["cumulative"] = data.mint.cumsum()

        pre_sale_filter = data.timestamp < sale_timestamp
        sale_filter = data.timestamp >= sale_timestamp
        public_duration = str(
            data[sale_filter].timestamp.max()
            - data[sale_filter].timestamp.min()
            + project.height_timedelta
        )
        public_height = (
            data[sale_filter].height.max() - data[sale_filter].height.min() + 1
        )

        self.view.sale.total_presale_mint = data[pre_sale_filter].shape[0]
        self.view.sale.total_public_mint = data[sale_filter].shape[0]
        self.view.sale.public_duration = public_duration
        self.view.sale.public_height = public_height

        # histogram
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(
                x=data[pre_sale_filter].timestamp,
                y=data[pre_sale_filter].mint,
                xperiod=60e3,
                xperiodalignment="middle",
                marker_color=PURPLE.hex_l,
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
                marker_color=GREEN.hex_l,
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
        layout = HISTOGRAM_LAYOUT.copy()
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
        self.view.sale.histogram_figure = fig

    def run(self, debug=False):
        """Run application."""
        self.view.run_server(debug=debug)
