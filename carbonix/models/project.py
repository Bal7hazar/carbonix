"""Project module."""

from datetime import datetime
from functools import _lru_cache_wrapper

import numpy as np

from carbonix.models.explorer import Explorer
from carbonix.resources import DATA_BASE


class Project:
    """Project class."""

    def __init__(self, address) -> None:
        """Build a project."""
        self._address = address
        self._explorer = Explorer()

        # properties
        self.__presale_height = self._presale_height()
        self.__presale_timestamp = self._presale_timestamp()
        self.__sale_height = self._sale_height()
        self.__sale_timestamp = self._sale_timestamp()
        self.__admins = self._admins()
        self.__whitelists = self._whitelists()
        self.__mints = self._mints()
        self.__height_timedelta = self._height_timedelta()
        self.__max_buy_at_once = self._max_buy_at_once()
        self.__name = self._name()
        self.__description = self._description()
        self.__image = self._image()
        self.__price = self._price()
        self.__unit = self._unit()
        self.__total_market_supply = self._total_market_supply()
        self.__total_reserved_supply = self._total_reserved_supply()
        self.__total_whitelist_supply = self._total_whitelist_supply()
        self.__total_public_supply = self._total_public_supply()
        self.__total_supply = self._total_supply()
        self.__total_market_minted = self._total_market_minted()
        self.__total_reserved_minted = self._total_reserved_minted()
        self.__total_whitelist_minted = self._total_whitelist_minted()
        self.__total_public_minted = self._total_public_minted()
        self.__total_minted = self._total_minted()

        # update features
        self.check_update()

    def check_update(self):
        """Check if there are new txs then clear cache accordingly."""
        txs = self._explorer.txs(self._address, force=False)
        force_txs = self._explorer.txs(self._address, force=True)
        if len(txs) != len(force_txs):  # new txs
            self.cache_clear(self._explorer)  # cleear Explorer cache
            strftime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_name = f"{DATA_BASE.stem}_{strftime}{DATA_BASE.suffix}"
            DATA_BASE.rename(DATA_BASE.parent / backup_name)

            # update properties
            self.__presale_height = self._presale_height()
            self.__presale_timestamp = self._presale_timestamp()
            self.__sale_height = self._sale_height()
            self.__sale_timestamp = self._sale_timestamp()
            self.__admins = self._admins()
            self.__whitelists = self._whitelists()
            self.__mints = self._mints()
            self.__height_timedelta = self._height_timedelta()
            self.__max_buy_at_once = self._max_buy_at_once()
            self.__name = self._name()
            self.__description = self._description()
            self.__image = self._image()
            self.__price = self._price()
            self.__unit = self._unit()
            self.__total_market_supply = self._total_market_supply()
            self.__total_reserved_supply = self._total_reserved_supply()
            self.__total_whitelist_supply = self._total_whitelist_supply()
            self.__total_public_supply = self._total_public_supply()
            self.__total_supply = self._total_supply()
            self.__total_market_minted = self._total_market_minted()
            self.__total_reserved_minted = self._total_reserved_minted()
            self.__total_whitelist_minted = self._total_whitelist_minted()
            self.__total_public_minted = self._total_public_minted()
            self.__total_minted = self._total_minted()

    @staticmethod
    def cache_clear(instance):
        """Clean cache of the specified instance."""
        for method_name in dir(instance.__class__):
            method = getattr(instance.__class__, method_name)
            print(method_name, type(method))
            if isinstance(method, property):
                method.fget.cache_clear()
            elif isinstance(method, _lru_cache_wrapper):
                method.cache_clear()

    @property
    def address(self):
        """Return address.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.address)
            juno17ctm453vqp0qvummupzln8q7cayeka0cfu7kfgm22qlqgl7zua0s32v5ld
        """
        return self._address

    @property
    def mintscan(self):
        """Return mintscan url."""
        return f"https://www.mintscan.io/juno/wasm/contract/{self.address}"

    @property
    def price(self):
        """Return NFT price.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.price)
            9800000
        """
        return self.__price

    def _price(self):
        """Return NFT price."""
        txn = sorted(
            self._explorer.price_txs(self.address), key=lambda txn: txn.height
        )[-1]
        price = txn.message.get("update_price").get("price")
        return int(price.get("amount"))

    @property
    def unit(self):
        """Return NFT price unit.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.unit)
            ujuno
        """
        return self.__unit

    def _unit(self):
        """Return NFT price unit."""
        txn = sorted(
            self._explorer.price_txs(self.address), key=lambda txn: txn.height
        )[-1]
        price = txn.message.get("update_price").get("price")
        return price.get("denom")

    @property
    def total_market_supply(self):
        """Return total market supply.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_market_supply)
            160
        """
        return self.__total_market_supply

    def _total_market_supply(self):
        """Return total market supply."""
        txn = sorted(
            self._explorer.supply_txs(self.address), key=lambda txn: txn.height
        )[-1]
        return int(txn.message.get("update_supply").get("market_supply"))

    @property
    def total_reserved_supply(self):
        """Return total reserved supply.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_reserved_supply)
            0
        """
        return self.__total_reserved_supply

    def _total_reserved_supply(self):
        """Return total reserved supply."""
        txn = sorted(
            self._explorer.supply_txs(self.address), key=lambda txn: txn.height
        )[-1]
        return int(txn.message.get("update_supply").get("reserved_supply"))

    @property
    def total_whitelist_supply(self):
        """Return total whitelist supply.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_whitelist_supply)
            149
        """
        return self.__total_whitelist_supply

    def _total_whitelist_supply(self):
        """Return total whitelist supply."""
        return sum(self.whitelists().values())

    @property
    def total_public_supply(self):
        """Return total public supply.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_public_supply)
            11
        """
        return self.__total_public_supply

    def _total_public_supply(self):
        """Return total public supply."""
        return self.total_market_supply - self.total_whitelist_supply

    @property
    def total_supply(self):
        """Return total supply.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_supply)
            160
        """
        return self.__total_supply

    def _total_supply(self):
        """Return total supply."""
        return self.total_market_supply + self.total_reserved_supply

    @property
    def total_market_minted(self):
        """Return total market minted.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_market_minted)
            160
        """
        return self.__total_market_minted

    def _total_market_minted(self):
        """Return total market minted."""
        txs = self.mints()
        price = self.price
        return sum(int(txn.amount / price) for txn in txs)

    @property
    def total_reserved_minted(self):
        """Return total reserved minted.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_reserved_minted)
            0
        """
        return self.__total_reserved_minted

    def _total_reserved_minted(self):
        """Return total reserved minted."""
        return self.total_reserved_supply  # FIXME: how to find reserved mints?

    @property
    def total_whitelist_minted(self):
        """Return total whitelist minted.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_whitelist_minted)
            118
        """
        return self.__total_whitelist_minted

    def _total_whitelist_minted(self):
        """Return total whitelist minted."""
        txs = self.mints()
        price = self.price
        sale_height = self.sale_height
        return sum(int(txn.amount / price) for txn in txs if txn.height <= sale_height)

    @property
    def total_public_minted(self):
        """Return total public minted.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_public_minted)
            42
        """
        return self.__total_public_minted

    def _total_public_minted(self):
        """Return total public minted."""
        return self.total_market_minted - self.total_whitelist_minted

    @property
    def total_minted(self):
        """Return total minted.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_minted)
            160
        """
        return self.__total_minted

    def _total_minted(self):
        """Return total minted."""
        return self.total_market_minted + self.total_reserved_minted

    @property
    def max_buy_at_once(self):
        """Return max buy at once.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.max_buy_at_once)
            5
        """
        return self.__max_buy_at_once

    def _max_buy_at_once(self):
        """Return max buy at once."""
        txn = sorted(
            self._explorer.max_buy_txs(self.address), key=lambda txn: txn.height
        )[-1]
        return int(txn.message.get("max_buy_at_once"))

    @property
    def name(self):
        """Return project name.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.name)
            Banegas Farm
        """
        return self.__name

    def _name(self):
        """Return project name."""
        txn = sorted(
            self._explorer.metadata_txs(self.address), key=lambda txn: txn.height
        )[-1]
        metadata = txn.message.get("update_metadata").get("metadata")
        return metadata.get("name")

    @property
    def description(self):
        """Return project description.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.description)
            Invest in decarbonation through our Green DeFi Launchpad.
        """
        return self.__description

    def _description(self):
        """Return project description."""
        txn = sorted(
            self._explorer.metadata_txs(self.address), key=lambda txn: txn.height
        )[-1]
        metadata = txn.message.get("update_metadata").get("metadata")
        return metadata.get("description")

    @property
    def image(self):
        """Return project image.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.image)  # doctest: +ELLIPSIS
            https://firebasestorage.googleapis.com/...
        """
        return self.__image

    def _image(self):
        """Return project image."""
        txn = sorted(
            self._explorer.metadata_txs(self.address), key=lambda txn: txn.height
        )[-1]
        metadata = txn.message.get("update_metadata").get("metadata")
        return metadata.get("image")

    @property
    def presale_timestamp(self):
        """Return project presale timestamp.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.presale_timestamp)
            2022-05-06 12:59:10+00:00
        """
        return self.__presale_timestamp

    def _presale_timestamp(self):
        """Return project presale timestamp."""
        txs = self._explorer.pre_sell_mode_txs(self.address)
        enabled_txs = [
            txn for txn in txs if txn.message.get("pre_sell_mode").get("enable")
        ]
        txn = sorted(enabled_txs, key=lambda txn: txn.height)[-1]
        return txn.timestamp

    @property
    def presale_height(self):
        """Return project presale height.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.presale_height)
            2976558
        """
        return self.__presale_height

    def _presale_height(self):
        """Return project presale height."""
        txs = self._explorer.pre_sell_mode_txs(self.address)
        enabled_txs = [
            txn for txn in txs if txn.message.get("pre_sell_mode").get("enable")
        ]
        txn = sorted(enabled_txs, key=lambda txn: txn.height)[-1]
        return txn.height

    @property
    def sale_timestamp(self):
        """Return project sale timestamp.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.sale_timestamp)
            2022-05-06 14:58:54+00:00
        """
        return self.__sale_timestamp

    def _sale_timestamp(self):
        """Return project sale timestamp."""
        txs = self._explorer.sell_mode_txs(self.address)
        enabled_txs = [txn for txn in txs if txn.message.get(
            "sell_mode").get("enable")]
        txn = sorted(enabled_txs, key=lambda txn: txn.height)[-1]
        return txn.timestamp

    @property
    def sale_height(self):
        """Return project sale height.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.sale_height)
            2977724
        """
        return self.__sale_height

    def _sale_height(self):
        """Return project sale height."""
        txs = self._explorer.sell_mode_txs(self.address)
        enabled_txs = [txn for txn in txs if txn.message.get(
            "sell_mode").get("enable")]
        txn = sorted(enabled_txs, key=lambda txn: txn.height)[-1]
        return txn.height

    @property
    def height_timedelta(self):
        """Return estimated height time duration.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.height_timedelta)
            0 days 00:00:06
        """
        return self.__height_timedelta

    def _height_timedelta(self):
        """Return estimated height time duration."""
        txs = self._explorer.txs(self.address)
        times, heights = zip(*[(txn.timestamp, txn.height) for txn in txs])
        timedeltas = np.diff(np.unique(times)) / np.diff(np.unique(heights))
        return np.median(timedeltas).round("1s")

    @staticmethod
    def to_juno(value, unit):
        """Return value in Juno from value in defined unit.

        Example:
            >>> from carbonix.models.project import Project
            >>> value, unit = Project.to_juno(9000000, unit="ujuno")
            >>> print(f"{value} {unit}")
            9.0 Junø
        """
        if unit == "ujuno":  # micro juno
            return int(value) / 1e6, "Junø"
        raise ValueError("Unexpected unit.")

    @staticmethod
    def short(address):
        """Return shorten address.

        Example:
            >>> from carbonix.models.project import Project
            >>> address = "juno10p9em0g53eddvjnmclqt5mef9dk2rp7l3t39vz"
            >>> print(Project.short(address))
            juno10p...3t39vz
        """
        return f"{address[:7]}...{address[-6:]}"

    def admins(self):
        """Return admins.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> admins = project.admins()
            >>> print(admins)
            ['juno1a500tdpehjejf8vcerte8a5kd2vgqkevwy8j3g', 'juno1vdekn9mfycsx5yhytzj2n0hg63w09w5c5kq7gz']
        """
        return self.__admins

    def _admins(self):
        """Return admins."""
        txs = self._explorer.admin_txs(self.address)
        senders = {txn.sender for txn in txs}
        admins = {txn.message.get("add_admin").get("address") for txn in txs}
        return list(sorted(senders.union(admins)))

    def whitelists(self):
        """Return whitelist addresses.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> whitelists = project.whitelists()
            >>> print(len(whitelists))
            53
            >>> print(sum(whitelists.values()))
            149
        """
        return self.__whitelists

    def _whitelists(self):
        """Return whitelist addresses."""
        presale_height = self.presale_height
        return {
            entry.get("address"): int(entry.get("nb_slots"))
            for txn in self._explorer.whitelist_txs(self.address)
            if txn.height <= presale_height
            and len(txn.message.get("add_to_whitelist").get("entries")) > 1
            for entry in txn.message.get("add_to_whitelist").get("entries")
        }

    def mints(self):
        """Return mint event txs.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> txs = project.mints()
            >>> print(txs[0].sender)
            juno1lt0q0pdza2zcalm75fru5v9528w6gu0wmr3ke7
        """
        return self.__mints

    def _mints(self):
        """Return mint event txs."""
        txs = sorted(self._explorer.mint_txs(
            self.address), key=lambda txn: txn.hash)
        return sorted(txs, key=lambda txn: txn.height)
