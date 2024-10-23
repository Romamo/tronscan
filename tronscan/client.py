import backoff
import requests

from .providers.http import HTTPProvider


class Client:
    def __init__(self, provider: HTTPProvider = None):
        if provider is None:
            self._provider = HTTPProvider()
        elif isinstance(provider, (HTTPProvider,)):
            self._provider = provider
        else:
            raise TypeError("provider is not a HTTPProvider")

    def transaction(self, start: int = 0, limit: int = 10, start_timestamp=None, end_timestamp=None, fromAddress=None, toAddress=None, tokens=None, block=None, type=None, method=None) -> dict:
        response = self._provider.make_request(
            'transaction',
            get={
                'start': start,
                'limit': limit,
                'start_timestamp': start_timestamp,
                'end_timestamp': end_timestamp,
                'fromAddress': fromAddress,
                'toAddress': toAddress,
                'tokens': tokens,
                'block': block,
                'type': type,
                'method': method
            }
        )
        return response

    @backoff.on_exception(backoff.expo, requests.exceptions.ReadTimeout, max_time=60)
    def get_trc20_and_trc721_transfers(self, start: int = 0, limit: int = 10,
                                       contract_address: str = None, start_timestamp=None, end_timestamp=None,
                                       confirm: bool = True, related_address=None, from_address=None,
                                       to_address=None) -> dict:
        response = self._provider.make_request(
            'api/token_trc20/transfers',
            get={
                'start': start,
                'limit': limit,
                'contract_address': contract_address,
                'start_timestamp': start_timestamp,
                'end_timestamp': end_timestamp,
                'confirm': confirm,
                'relatedAddress': related_address,
                'fromAddress': from_address,
                'toAddress': to_address
            }
        )
        return response