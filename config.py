import os

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
TESTNET_API_BASE = "https://testnet.toncenter.com/api/v2"
MAINNET_API_BASE = "https://toncenter.com/api/v2"
GET_ADDRESS_INFORMATION = "getAddressInformation"
IS_TESTNET = False