import requests
import json

from tonutils.client import TonapiClient
from tonutils.wallet import WalletV4R2

from config import (
    API_KEY, 
    IS_TESTNET, 
    MAINNET_API_BASE, 
    GET_ADDRESS_INFORMATION
)

from core.storage.database import (
    Insert,
    Update
)

class CreateWallet:
    def __init__(self) -> None:
        """
        Initialize the client and create a wallet.
        """
        client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
        # Create a wallet and retrieve its public and private keys as well as the mnemonic phrase
        self.wallet, self.public_key, self.private_key, self.mnemonic = WalletV4R2.create(client)
    
class ConnectWallet:
    def __init__(self, address: str = None) -> None:
        """
        Connect to the wallet by address and retrieve account information.
        
        :param address: The wallet address.
        """
        try:
            # Get account information via the API
            result = requests.get(f"{MAINNET_API_BASE}/{GET_ADDRESS_INFORMATION}?address={address}")
            self.raw_account_data = result.json()
            # Available balance in nano
            self.available_to_nano_balance = self.raw_account_data['result']['balance']
            # Convert balance to a more convenient format
            self.available_balance = int(self.raw_account_data['result']['balance']) / 1_000_000_000
            self.account_state = self.raw_account_data['ok']
        except requests.RequestException as e:
            self.error_message = f"Error connecting to API: {e}"
        except ValueError as ve:
            self.error_message = f"Error parsing response: {ve}"
        except Exception as e:
            self.error_message = f"An unexpected error occurred: {e}"
            
        if not result:
            self.account_state = False

class SaveWallet(CreateWallet):
    def __init__(self, value) -> None:
        """
        Save wallet information to the database.
        
        :param value: The payment amount associated with the wallet.
        """
        super().__init__()
        # Insert wallet information into the 'ton' table
        instance = Insert(
            table_name='ton', 
            columns=['address', 'mnemonic', 'value', 'state'], 
            values=[self.wallet.address.to_str(), json.dumps(self.mnemonic), value, False]
        )
        
        instance.execute()

class UpdateWallet(ConnectWallet):
    def __init__(self, tid) -> None:
        """
        Update the wallet state in the database by transaction ID.
        
        :param tid: Transaction ID.
        """
        super().__init__()
        # Update the wallet state in the 'ton' table
        instance = Update(
            table_name='ton', 
            columns=['state'], 
            values=[True], 
            where_clause=f'id = {tid}'
        )

        instance.execute()