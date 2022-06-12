"""Explorer main module."""

import base64
import json
import pickle
import re
from copy import deepcopy
from functools import lru_cache

import pandas as pd
import requests

from carbonix.resources import DATA_BASE


class Explorer:
    """Explorer class to extract block information."""

    base = "https://rpc.junomint.com"

    def __init__(self):
        """Build an explorer."""
        self.__database = DataBase()

    def _txs(self, address, action, force, **kwargs):
        """Return <action> txs at specified address by batch of 100."""
        command = "tx_search"

        query_value = f"{action}=%27{address}%27"
        query = f'query="{query_value}"'

        prove_value = str(kwargs.get("prove", False)).lower()
        prove = f"prove={prove_value}"

        page_value = kwargs.get("page", 1)
        page = f"page={page_value}"

        per_page_value = kwargs.get("per_page", 30)
        per_page = f"per_page={per_page_value}"

        order_by_value = kwargs.get("order_by", "asc")
        order_by = f'order_by="{order_by_value}"'

        api = f"{self.base}/{command}?{query}&{prove}&{page}&{per_page}&{order_by}"

        if force:  # force the request what ever the database content
            return deepcopy(requests.get(api).json())
        return deepcopy(
            self.__database.get(api)
            or self.__database.setdefault(api, requests.get(api).json())
        )

    def txs(self, address, force=False):
        """Return txs executed by the specified address.

        Txs are sorted by execution timestamp.

        Example:
            >>> import numpy as np
            >>> from carbonix.models.explorer import Explorer
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> explorer = Explorer()
            >>> print(address)
            juno17ctm453vqp0qvummupzln8q7cayeka0cfu7kfgm22qlqgl7zua0s32v5ld
            >>> txs = explorer.txs(address)
            >>> print(len(txs))
            135
            >>> print(sorted({method for txn in txs for method in txn.methods}))
            ['add_admin', 'add_to_whitelist', 'buy', 'max_buy_at_once', 'multi_buy', 'pre_sell_mode', 'sell_mode', 'update_metadata', 'update_nft_contract', 'update_price', 'update_supply', 'withdraw']
        """
        # instantiate
        action = "instantiate._contract_address"
        instantiate_txs = self._txs(address, action, force=force).get("result", {})
        txs_total = int(instantiate_txs.get("total_count"))
        txs_number = len(instantiate_txs.get("txs"))
        page = 1
        while txs_number < txs_total:
            page += 1
            response = self._txs(address, action, force=force, page=page).get(
                "result", {}
            )
            instantiate_txs["txs"] += response.get("txs")
            txs_number += len(response.get("txs"))

        # execute
        action = "execute._contract_address"
        execute_txs = self._txs(address, action, force=force).get("result", {})
        txs_total = int(execute_txs.get("total_count", 0))
        txs_number = len(execute_txs.get("txs", []))
        page = 1
        while txs_number < txs_total:
            page += 1
            response = self._txs(address, action, force=force, page=page).get(
                "result", {}
            )
            execute_txs["txs"] += response.get("txs")
            txs_number += len(response.get("txs"))

        return set(
            Txn(txn, self.__database)
            for txn in instantiate_txs.get("txs") + execute_txs.get("txs")
        )

    def mint_txs(self, address):
        """Return txs for which receivers are the specifed address.

        Example:
            >>> from pprint import pprint
            >>> from carbonix.models.explorer import Explorer
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> explorer = Explorer()
            >>> txs = explorer.mint_txs(address)
            >>> print(len(txs))
            98
        """
        keywords = {"buy", "multi_buy"}
        return set(
            txn for txn in self.txs(address) if keywords.intersection(txn.methods)
        )

    def whitelist_txs(self, address):
        """Return whitelist txs defined for the specied contract address.

        Example:
            >>> from pprint import pprint
            >>> from carbonix.models.explorer import Explorer
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> explorer = Explorer()
            >>> txs = explorer.whitelist_txs(address)
            >>> print(len(txs))
            17
        """
        keywords = {"add_to_whitelist"}
        return set(
            txn for txn in self.txs(address) if keywords.intersection(txn.methods)
        )

    def admin_txs(self, address):
        """Return admin txs defined for the specied contract address.

        Example:
            >>> from pprint import pprint
            >>> from carbonix.models.explorer import Explorer
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> explorer = Explorer()
            >>> txs = explorer.admin_txs(address)
            >>> print(len(txs))
            1
        """
        keywords = {"add_admin"}
        return set(
            txn for txn in self.txs(address) if keywords.intersection(txn.methods)
        )

    def pre_sell_mode_txs(self, address):
        """Return presale txs defined for the specied contract address.

        Example:
            >>> from pprint import pprint
            >>> from carbonix.models.explorer import Explorer
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> explorer = Explorer()
            >>> txs = explorer.pre_sell_mode_txs(address)
            >>> print(len(txs))
            6
        """
        keywords = {"pre_sell_mode"}
        return set(
            txn
            for txn in self.txs(address)
            if keywords.intersection(txn.methods)
            and isinstance(txn.message.get(next(iter(keywords))), dict)
        )

    def sell_mode_txs(self, address):
        """Return presale txs defined for the specied contract address.

        Example:
            >>> from pprint import pprint
            >>> from carbonix.models.explorer import Explorer
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> explorer = Explorer()
            >>> txs = explorer.sell_mode_txs(address)
            >>> print(len(txs))
            3
        """
        keywords = {"sell_mode"}
        return set(
            txn
            for txn in self.txs(address)
            if keywords.intersection(txn.methods)
            and isinstance(txn.message.get(next(iter(keywords))), dict)
        )

    def price_txs(self, address):
        """Return update price txs defined for the specied contract address.

        Example:
            >>> from pprint import pprint
            >>> from carbonix.models.explorer import Explorer
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> explorer = Explorer()
            >>> txs = explorer.price_txs(address)
            >>> print(len(txs))
            4
        """
        keywords = {"update_price"}
        return set(
            txn for txn in self.txs(address) if keywords.intersection(txn.methods)
        )

    def supply_txs(self, address):
        """Return update supply txs defined for the specied contract address.

        Example:
            >>> from pprint import pprint
            >>> from carbonix.models.explorer import Explorer
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> explorer = Explorer()
            >>> txs = explorer.supply_txs(address)
            >>> print(len(txs))
            2
        """
        keywords = {"update_supply"}
        return set(
            txn for txn in self.txs(address) if keywords.intersection(txn.methods)
        )

    def metadata_txs(self, address):
        """Return update supply txs defined for the specied contract address.

        Example:
            >>> from pprint import pprint
            >>> from carbonix.models.explorer import Explorer
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> explorer = Explorer()
            >>> txs = explorer.metadata_txs(address)
            >>> print(len(txs))
            1
        """
        keywords = {"update_metadata"}
        return set(
            txn for txn in self.txs(address) if keywords.intersection(txn.methods)
        )

    def max_buy_txs(self, address):
        """Return update supply txs defined for the specied contract address.

        Example:
            >>> from pprint import pprint
            >>> from carbonix.models.explorer import Explorer
            >>> from carbonix.resources import CONTRACT_ADDRESSES
            >>> address = next(iter(CONTRACT_ADDRESSES))
            >>> explorer = Explorer()
            >>> txs = explorer.max_buy_txs(address)
            >>> print(len(txs))
            1
        """
        keywords = {"max_buy_at_once"}
        return set(
            txn for txn in self.txs(address) if keywords.intersection(txn.methods)
        )

    def contacts(self, address):
        """Return all direct address which ever interacted with the specified address.

        Example:
            >>> from pprint import pprint
            >>> from carbonix.models.explorer import Explorer
            >>> explorer = Explorer()
            >>> address = "juno10p9em0g53eddvjnmclqt5mef9dk2rp7l3t39vz"
            >>> contacts = explorer.contacts(address)
            >>> pprint(contacts)
            {'juno17ctm453vqp0qvummupzln8q7cayeka0cfu7kfgm22qlqgl7zua0s32v5ld',
             'juno1a53udazy8ayufvy0s434pfwjcedzqv34q7p7vj',
             'juno1fl7vq8hwej2lr67f08w3xmsgsctupngeyd5cl6650pj3g0ddslasctjvf0'}
        """
        action = "transfer.sender"
        sent_txs = self._txs(address, action, force=True).get("result", {})
        txs_total = int(sent_txs.get("total_count"))
        txs_number = len(sent_txs.get("txs"))
        page = 1
        while txs_number < txs_total:
            page += 1
            response = self._txs(address, action, force=True, page=page).get(
                "result", {}
            )
            sent_txs["txs"] += response.get("txs")
            txs_number += len(response.get("txs"))
        recipients = {
            Txn(txn, self.__database).recipient for txn in sent_txs.get("txs")
        }

        action = "transfer.recipient"
        received_txs = self._txs(address, action, force=True).get("result", {})
        txs_total = int(received_txs.get("total_count"))
        txs_number = len(received_txs.get("txs"))
        page = 1
        while txs_number < txs_total:
            page += 1
            response = self._txs(address, action, force=True, page=page).get(
                "result", {}
            )
            received_txs["txs"] += response.get("txs")
            txs_number += len(response.get("txs"))
        senders = {Txn(txn, self.__database).sender for txn in received_txs.get("txs")}

        contacts = recipients.union(senders)
        # remove address if included
        return contacts.symmetric_difference({address}).intersection(contacts)


class Txn:
    """Txn class.

    Example:
        >>> from pprint import pprint
        >>> from carbonix.models.explorer import Explorer
        >>> from carbonix.resources import CONTRACT_ADDRESSES
        >>> address = next(iter(CONTRACT_ADDRESSES))
        >>> explorer = Explorer()
        >>> txn = list(sorted(explorer.txs(address), key=lambda txn: txn.height))[50]
        >>> print(txn.hash)
        E71EF591DCCDC8F917B4E90CAE55F95030CC44F201DF827DEA949A208113728F
        >>> print(txn.height)
        2976623
        >>> print(txn.timestamp)
        2022-05-06 13:05:51+00:00
        >>> print(txn.sender)
        juno1kehrw27yzqyctv42drh8q08nx3cgs53t88ah7z
        >>> print(txn.recipient)
        juno17ctm453vqp0qvummupzln8q7cayeka0cfu7kfgm22qlqgl7zua0s32v5ld
        >>> print(txn.amount)
        29400000
        >>> print(txn.unit)
        ujuno
        >>> print(txn.methods)
        ['multi_buy']
        >>> print(txn.message)
        {'multi_buy': {'quantity': 3}}
    """

    message_pattern = r"\{.*\}"
    amount_pattern = r"(?P<amount>[0-9]+)(?P<unit>[a-z]+)"

    def __init__(self, txn, database):
        """Build a txn."""
        self._txn = txn
        self._data = base64.b64decode(self._txn.get("tx")).decode(
            encoding="utf-8", errors="ignore"
        )
        self._logs = json.loads(self._txn.get("tx_result").get("log"))
        self._sender, self._recipient, self._amount = self._transfer()
        self.__database = database

    def _transfer(self):
        """Extract transfer information."""
        events = [event for log in self._logs for event in log.get("events")]
        senders = [
            attribute.get("value")
            for event in events
            for attribute in event.get("attributes")
            if attribute.get("key") == "sender"
        ]
        recipients = [
            attribute.get("value")
            for event in events
            for attribute in event.get("attributes")
            if attribute.get("key") in ("recipient", "_contract_address")
        ]
        amounts = [
            attribute.get("value")
            for event in events
            if event.get("type") == "transfer"
            for attribute in event.get("attributes")
            if attribute.get("key") == "amount"
        ]
        return (
            senders[0] if senders else None,
            recipients[0] if recipients else None,
            amounts[0] if amounts else None,
        )

    def _timestamp(self):
        """Return timestamp."""
        command = "block"
        height = f"height={self.height}"
        api = f"{Explorer.base}/{command}?{height}"
        return self.__database.get(api) or self.__database.setdefault(
            api,
            pd.Timestamp(
                requests.get(api)
                .json()
                .get("result")
                .get("block")
                .get("header")
                .get("time")
            ).round(freq="S")
            + "a",
        )

    @property
    @lru_cache(maxsize=None)
    def hash(self):
        """Return tx hash."""
        return self._txn.get("hash")

    @property
    @lru_cache(maxsize=None)
    def height(self):
        """Return height."""
        return int(self._txn.get("height"))

    @property
    @lru_cache(maxsize=None)
    def timestamp(self):
        """Return timestamp."""
        return self._timestamp()

    @property
    @lru_cache(maxsize=None)
    def sender(self):
        """Return sender."""
        return self._sender

    @property
    @lru_cache(maxsize=None)
    def recipient(self):
        """Return recipient."""
        return self._recipient

    @property
    @lru_cache(maxsize=None)
    def amount(self):
        """Return amount."""
        match = re.match(self.amount_pattern, self._amount)
        return int(match.group("amount"))

    @property
    @lru_cache(maxsize=None)
    def unit(self):
        """Return unit."""
        match = re.match(self.amount_pattern, self._amount)
        return match.group("unit")

    @property
    @lru_cache(maxsize=None)
    def methods(self):
        """Return tx methods."""
        return list(self.message)

    @property
    @lru_cache(maxsize=None)
    def message(self):
        """Return tx methods."""
        inputs = re.findall(self.message_pattern, self._data)[0]
        message = json.loads(inputs)
        return message


class DataBase(dict):
    """DataBase class."""

    database = DATA_BASE

    def __init__(self, *args, **kwargs):
        """Build a DataBase."""
        super().__init__(*args, **kwargs)
        if self.database.exists():
            with open(self.database, "rb") as database:
                self.update(pickle.load(database))

    def setdefault(self, *args):
        """Override setdefault method."""
        if args[0] in self:  # do not update database
            return super().setdefault(*args)
        result = super().setdefault(*args)
        with open(self.database, "wb") as database:
            pickle.dump(self, database)
        return result
