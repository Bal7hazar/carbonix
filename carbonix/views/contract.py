"""Contract view module."""

import plotly.graph_objects as go
from dash import dcc, html

from carbonix.views import PIECHART_LAYOUT
from carbonix.views.section import Section


class Contract(Section):
    """Contract class."""

    def __init__(self):
        """Build a contract."""
        # metrics
        self._name = None
        self._description = None
        self._address = None
        self._mintscan = None
        self._price = None
        self._unit = None
        self._total_supply = None
        self._total_market_supply = None
        self._total_reserved_supply = None
        self._total_minted = None
        self._total_market_minted = None
        self._total_reserved_minted = None
        self._max_buy_at_once = None

        # supply
        self._supply_figure = go.Figure(go.Pie(), layout=PIECHART_LAYOUT)

        # minted
        self._minted_figure = go.Figure(go.Pie(), layout=PIECHART_LAYOUT)

    @property
    def name(self):
        """Return name."""
        return html.P(f"Name: {self._name}", id="contract-name")

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        """Return description."""
        return html.P(f"Description: {self._description}", id="contract-description")

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def address(self):
        """Return address."""
        href = self.mintscan if self._address else "#"
        return html.P(
            children=[
                "Contract: ",
                html.A(self._address, href=href),
            ],
            id="contract-address"
        )

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def mintscan(self):
        """Return mintscan."""
        return self._mintscan

    @mintscan.setter
    def mintscan(self, mintscan):
        self._mintscan = mintscan

    @property
    def price(self):
        """Return price."""
        if self._price:
            return html.P(f"Price: {self._price} ${self.unit}", id="contract-price")
        return html.P(f"Price: {self._price}", id="contract-price")

    @price.setter
    def price(self, price):
        self._price = price

    @property
    def unit(self):
        """Return unit."""
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = unit

    @property
    def total_supply(self):
        """Return total supply."""
        return html.P(f"Total supply: {self._total_supply}", id="contract-total_supply")

    @total_supply.setter
    def total_supply(self, total_supply):
        self._total_supply = total_supply

    @property
    def total_market_supply(self):
        """Return total market supply."""
        return html.P(f"Total market supply: {self._total_market_supply}", id="contract-total_market_supply")

    @total_market_supply.setter
    def total_market_supply(self, total_market_supply):
        self._total_market_supply = total_market_supply

    @property
    def total_reserved_supply(self):
        """Return total reserved supply."""
        return html.P(f"Total reserved supply: {self._total_reserved_supply}", id="contract-total_reserved_supply")

    @total_reserved_supply.setter
    def total_reserved_supply(self, total_reserved_supply):
        self._total_reserved_supply = total_reserved_supply

    @property
    def total_minted(self):
        """Return total minted."""
        return html.P(f"Total minted: {self._total_minted}", id="contract-total_minted")

    @total_minted.setter
    def total_minted(self, total_minted):
        self._total_minted = total_minted

    @property
    def total_market_minted(self):
        """Return total market minted."""
        return html.P(f"Total market minted: {self._total_market_minted}", id="contract-total_market_minted")

    @total_market_minted.setter
    def total_market_minted(self, total_market_minted):
        self._total_market_minted = total_market_minted

    @property
    def total_reserved_minted(self):
        """Return total reserved minted."""
        return html.P(f"Total reserved minted: {self._total_reserved_minted}", id="contract-total_reserved_minted")

    @total_reserved_minted.setter
    def total_reserved_minted(self, total_reserved_minted):
        self._total_reserved_minted = total_reserved_minted

    @property
    def max_buy_at_once(self):
        """Return max buy at once."""
        return html.P(f"Max buy at once: {self._max_buy_at_once}", id="contract-max_buy_at_once")

    @max_buy_at_once.setter
    def max_buy_at_once(self, max_buy_at_once):
        self._max_buy_at_once = max_buy_at_once

    @property
    def supply_figure(self):
        """Return supply figure."""
        return self._supply_figure

    @supply_figure.setter
    def supply_figure(self, figure):
        self._supply_figure = figure

    @property
    def minted_figure(self):
        """Return minted figure."""
        return self._minted_figure

    @minted_figure.setter
    def minted_figure(self, figure):
        self._minted_figure = figure

    def section(self):
        """Return header."""
        return html.Div(
            children=[
                html.H3("Contract", className="section-title"),
                html.Div(
                    id="contract-content",
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
            self.supply(),
            self.minted(),
        ]

    def metrics(self):
        """Return contract information."""
        infos = [
            self.name,
            self.description,
            self.address,
            self.price,
            self.total_supply,
            self.total_market_supply,
            self.total_reserved_supply,
            self.total_minted,
            self.total_market_minted,
            self.total_reserved_minted,
            self.max_buy_at_once,
        ]
        children = [
            html.H4("MetriX", className="topic-title rainbow"),
            html.Ul(
                children=[
                    html.Li(info, className="metrics-item")
                    for info in infos
                ],
                className="metrics-container",
            )
        ]
        return html.Div(children=children, className="topic")

    def supply(self):
        """Return contract supply."""
        children = [
            html.H4("Total supply", className="topic-title"),
            dcc.Graph(id="contract-supply_figure", figure=self.supply_figure),
        ]
        return html.Div(children=children, className="topic", id="contract-supply-figure")

    def minted(self):
        """Return contract minted."""
        children = [
            html.H4("Total minted", className="topic-title"),
            dcc.Graph(id="contract-minted_figure", figure=self.minted_figure),
        ]
        return html.Div(children=children, className="topic", id="contract-minted-figure")
