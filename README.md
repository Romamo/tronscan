# Tronscan Client

A client for interacting with the [Tronscan API](https://docs.tronscan.org/)

## Prerequisites

Get an API Key: https://docs.tronscan.org/#get-an-api-key 

```shell
export TRONSCAN_API_KEY=your-api-key
export TRONSCAN_HTTP_PROVIDER_URI=https://apilist.tronscanapi.com/
```

## Installation

To install the package, use pip:

```sh
pip install tronscan
```

## Usage

```python
from tronscan import Client

client = Client()
# Get last USDT transactions
response = client.get_trc20_and_trc721_transfers(contract_address='TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')
print(response)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
