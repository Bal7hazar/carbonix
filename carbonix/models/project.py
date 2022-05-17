"""Project module."""

from functools import cached_property

import numpy as np

from carbonix.models.explorer import Explorer


class Project:
    """Project class."""

    def __init__(self, address) -> None:
        """Build a project."""
        self._address = address
        self._explorer = Explorer()

    @cached_property
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

    @cached_property
    def mintscan(self):
        """Return mintscan url."""
        return f"https://www.mintscan.io/juno/wasm/contract/{self.address}"

    @cached_property
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
        txn = self._explorer.price_txs(self.address)[-1]
        price = txn.message.get("update_price").get("price")
        return int(price.get("amount"))

    @cached_property
    def unit(self):
        """Return NFT price.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.unit)
            ujuno
        """
        txn = self._explorer.price_txs(self.address)[-1]
        price = txn.message.get("update_price").get("price")
        return price.get("denom")

    @cached_property
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
        txn = self._explorer.supply_txs(self.address)[-1]
        return int(txn.message.get("update_supply").get("market_supply"))

    @cached_property
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
        txn = self._explorer.supply_txs(self.address)[-1]
        return int(txn.message.get("update_supply").get("reserved_supply"))

    @cached_property
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
        return sum(self.whitelists().values())

    @cached_property
    def total_public_supply(self):
        """Reutn total public supply.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_public_supply)
            160
        """
        return self.total_market_supply - self.total_whitelist_supply

    @cached_property
    def total_supply(self):
        """Reutn total supply.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_supply)
            160
        """
        return self.total_market_supply + self.total_reserved_supply

    @cached_property
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
        mints = self.mints()
        price = self.price
        return sum(int(mint.get("amount") / price) for mint in mints.values())

    @cached_property
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
        return self.total_reserved_supply  # FIXME: how to find reserved mints?

    @cached_property
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
        mints = self.mints()
        price = self.price
        sale_timestamp = self.sale_timestamp
        return sum(
            int(mint.get("amount") / price)
            for mint in mints.values()
            if mint.get("timestamp") <= sale_timestamp
        )

    @cached_property
    def total_public_minted(self):
        """Reutn total public minted.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_public_minted)
            160
        """
        return self.total_market_minted - self.total_whitelist_minted

    @cached_property
    def total_minted(self):
        """Reutn total minted.

        Example:
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> print(project.total_minted)
            160
        """
        return self.total_market_minted + self.total_reserved_minted

    @cached_property
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
        txn = self._explorer.max_buy_txs(self.address)[-1]
        return int(txn.message.get("max_buy_at_once"))

    @cached_property
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
        txn = self._explorer.metadata_txs(self.address)[-1]
        metadata = txn.message.get("update_metadata").get("metadata")
        return metadata.get("name")

    @cached_property
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
        txn = self._explorer.metadata_txs(self.address)[-1]
        metadata = txn.message.get("update_metadata").get("metadata")
        return metadata.get("description")

    @cached_property
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
        txn = self._explorer.metadata_txs(self.address)[-1]
        metadata = txn.message.get("update_metadata").get("metadata")
        return metadata.get("image")

    @cached_property
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
        txs = self._explorer.pre_sell_mode_txs(self.address)
        enabled_txs = [
            txn for txn in txs if txn.message.get("pre_sell_mode").get("enable")
        ]
        return enabled_txs[-1].timestamp

    @cached_property
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
        txs = self._explorer.sell_mode_txs(self.address)
        enabled_txs = [txn for txn in txs if txn.message.get("sell_mode").get("enable")]
        return enabled_txs[-1].timestamp

    @cached_property
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
            >>> address, slot = list(whitelists.items())[0]
            >>> print(f"{address}: {slot}")
            juno1h4...2avzr5: 5
            >>> print(len(whitelists))
            53
            >>> print(sum(whitelists.values()))
            149
        """
        admin_addresses = self.admins()
        presale_timestamp = self.presale_timestamp
        return {
            entry.get("address"): int(entry.get("nb_slots"))
            for txn in self._explorer.whitelist_txs(self.address)
            for entry in txn.message.get("add_to_whitelist").get("entries")
            if txn.timestamp <= presale_timestamp  # focus before the pre sale
            # FIXME: some users get 2 addresses because of ledger issue
            and len(txn.message.get("add_to_whitelist").get("entries")) > 1
            and entry.get("address") not in admin_addresses  # remove admins
        }

    def mints(self):
        """Return mint event txs.

        Example:
            >>> from pprint import pprint
            >>> from carbonix.models.project import Project
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> project = Project(address)
            >>> mints = project.mints()
            >>> hash, txn = list(mints.items())[0]
            >>> pprint(txn)
            {'address': 'juno1lt0q0pdza2zcalm75fru5v9528w6gu0wmr3ke7',
             'amount': 49000000,
             'height': 2976560,
             'timestamp': Timestamp('2022-05-06 12:59:22+0000', tz='UTC')}
        """
        txs = self._explorer.mint_txs(self.address)
        mints = {
            txn.hash: dict(
                height=txn.height,
                timestamp=txn.timestamp,
                address=txn.sender,
                amount=txn.amount,
            )
            for txn in txs
        }
        return mints
