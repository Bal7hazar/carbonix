"""Explorer main module."""

import pandas as pd
import requests


class Explorer:
    """Explorer class to extract block information."""

    def __init__(self):
        """Build an explorer."""
        self.base = "https://lcd-juno.itastakers.com"
        self.__txs = {}

    def _txs(self, address, action, offset=0):
        """Return <action> txs at specified address by batch of 100."""
        command = "cosmos/tx/v1beta1"
        option = "txs"
        event_option = "events"
        event_value = f"{action}._contract_address='{address}'"
        pagination_option = "pagination.offset"
        pagination_value = f"{offset}"
        api = f"{self.base}/{command}/{option}?{event_option}={event_value}&{pagination_option}={pagination_value}"
        return self.__txs.setdefault(api, requests.get(api).json())

    def txs(self, address):
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
        action = "instantiate"
        instantiate_txs = self._txs(address, action)
        txs_total = int(instantiate_txs.get("pagination").get("total"))
        txs_number = len(instantiate_txs.get("txs"))
        while txs_number < txs_total:
            response = self._txs(address, action, offset=txs_number)
            instantiate_txs["txs"] += response.get("txs")
            instantiate_txs["tx_responses"] += response.get("tx_responses")
            txs_number += len(response.get("txs"))

        # execute
        action = "execute"
        execute_txs = self._txs(address, action)
        txs_total = int(execute_txs.get("pagination").get("total"))
        txs_number = len(execute_txs.get("txs"))
        while txs_number < txs_total:
            response = self._txs(address, action, offset=txs_number)
            execute_txs["txs"] += response.get("txs")
            execute_txs["tx_responses"] += response.get("tx_responses")
            txs_number += len(response.get("txs"))

        return [
            Txn(txn, tx_response)
            for txn, tx_response in zip(
                instantiate_txs.get("txs") + execute_txs.get("txs"),
                instantiate_txs.get("tx_responses") + execute_txs.get("tx_responses"),
            )
        ]

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
            >>> print(txs[0].message)
            {'multi_buy': {'quantity': 5}}
        """
        keywords = {"buy", "multi_buy"}
        return [txn for txn in self.txs(address) if keywords.intersection(txn.methods)]

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
            >>> print(txs[-1].message)
            {'add_to_whitelist': {'entries': [{'address': 'juno1q0f955ref9a8afzjrhv7gph3sv75sssdrad4qe', 'nb_slots': 1}]}}
        """
        keywords = {"add_to_whitelist"}
        return [txn for txn in self.txs(address) if keywords.intersection(txn.methods)]

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
            >>> print(txs[-1].message)
            {'add_admin': {'address': 'juno1vdekn9mfycsx5yhytzj2n0hg63w09w5c5kq7gz'}}
        """
        keywords = {"add_admin"}
        return [txn for txn in self.txs(address) if keywords.intersection(txn.methods)]

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
            >>> print(txs[-1].message)
            {'pre_sell_mode': {'enable': False}}
        """
        keywords = {"pre_sell_mode"}
        return [
            txn
            for txn in self.txs(address)
            if keywords.intersection(txn.methods)
            and isinstance(txn.message.get(next(iter(keywords))), dict)
        ]

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
            >>> print(txs[-1].message)
            {'sell_mode': {'enable': True}}
        """
        keywords = {"sell_mode"}
        return [
            txn
            for txn in self.txs(address)
            if keywords.intersection(txn.methods)
            and isinstance(txn.message.get(next(iter(keywords))), dict)
        ]

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
            >>> print(txs[-1].message)
            {'update_price': {'price': {'denom': 'ujuno', 'amount': '9800000'}}}
        """
        keywords = {"update_price"}
        return [txn for txn in self.txs(address) if keywords.intersection(txn.methods)]

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
            >>> print(txs[-1].message)
            {'update_supply': {'reserved_supply': 0, 'market_supply': 160}}
        """
        keywords = {"update_supply"}
        return [txn for txn in self.txs(address) if keywords.intersection(txn.methods)]

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
        return [txn for txn in self.txs(address) if keywords.intersection(txn.methods)]

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
        return [txn for txn in self.txs(address) if keywords.intersection(txn.methods)]

    def contacts(self, address):
        """Return all direct address which ever interacted with the specified address.

        Example:
            >>> from pprint import pprint
            >>> from carbonix.models.explorer import Explorer
            >>> explorer = Explorer()
            >>> address = "juno10p9em0g53eddvjnmclqt5mef9dk2rp7l3t39vz"
            >>> contacts = explorer.contacts(address)
            >>> print(contacts)
            ['osmo10p9em0g53eddvjnmclqt5mef9dk2rp7l0zpwav']
        """
        command = "cosmos/tx/v1beta1"
        option = "txs"
        event_option = "events"
        contacts = list()

        # receivers
        event_value = f"transfer.sender='{address}'"
        count_option = "pagination.count_total"
        count_value = "true"
        api = f"{self.base}/{command}/{option}?{event_option}={event_value}&{count_option}={count_value}"
        response = requests.get(api).json()
        for txn in response.get("tx_responses"):
            receiver = txn.get("tx").get("body").get("messages")[0].get("receiver")
            if receiver is not None and receiver != address:  # None = contract
                contacts.append(receiver)

        # sender
        event_value = f"transfer.recipient='{address}'"
        count_option = "pagination.count_total"
        count_value = "true"
        api = f"{self.base}/{command}/{option}?{event_option}={event_value}&{count_option}={count_value}"
        response = requests.get(api).json()
        for txn in response.get("tx_responses"):
            sender = txn.get("tx").get("body").get("messages")[0].get("sender")
            if sender is not None and sender != address:  # None = contract
                contacts.append(sender)

        return contacts


class Txn:
    """Txn class.

    Example:
        >>> from pprint import pprint
        >>> from carbonix.models.explorer import Explorer
        >>> from carbonix.resources import CONTRACT_ADDRESSES
        >>> address = next(iter(CONTRACT_ADDRESSES))
        >>> explorer = Explorer()
        >>> txn = explorer.txs(address)[101]
        >>> print(txn.hash)
        9723B2C4BDEDE9CF3369A85A25E5468A39F0A6242C8615D19036791A51C77FD3
        >>> print(txn.memo)
        Buy
        >>> print(txn.methods)
        ['buy']
        >>> print(txn.message)
        {'buy': {}}
        >>> print(txn.height)
        2977691
        >>> print(txn.timestamp)
        2022-05-06 14:55:29+00:00
        >>> print(txn.sender)
        juno12mqgfxh25tqrl4xz39z0t67r4q024c7qyrh54e
        >>> print(txn.amount)
        9800000
    """

    def __init__(self, txn, tx_response):
        """Build a txn."""
        self._txn = txn
        self._tx_response = tx_response

    @property
    def hash(self):
        """Return tx hash."""
        return self._tx_response.get("txhash")

    @property
    def height(self):
        """Return height."""
        return int(self._tx_response.get("height"))

    @property
    def timestamp(self):
        """Return timestamp."""
        return pd.Timestamp(self._tx_response.get("timestamp"))

    @property
    def sender(self):
        """Return sender."""
        messages = self._tx_response.get("tx").get("body").get("messages")
        if not messages:
            return
        return messages[0].get("sender")

    @property
    def amount(self):
        """Return amount."""
        funds = self._tx_response.get("tx").get("body").get("messages")[0].get("funds")
        if not funds:
            return
        return int(funds[0].get("amount"))

    @property
    def message(self):
        """Return tx message."""
        messages = self._tx_response.get("tx").get("body").get("messages")
        if not messages:
            return
        return messages[0].get("msg")

    @property
    def memo(self):
        """Return tx memo."""
        return self._tx_response.get("tx").get("body").get("memo")

    @property
    def methods(self):
        """Return tx methods."""
        return list(self.message)
