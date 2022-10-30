from unicodedata import name
from stellar_sdk import Asset, Server, Keypair, TransactionBuilder, Network, Account
import requests

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
stellar_quest_keypair = Keypair.from_secret("SC3URBQ7FI2F7B4VQ2IQH6HHXG24ZFJVU64CYJ4LSMZNPZFKPN63GPPB")
quest_account_pub_key = stellar_quest_keypair.public_key
quest_account_priv_key = stellar_quest_keypair.secret

# 2. Transaction

print("Building Transaction...")

base_fee = server.fetch_base_fee()
stellar_account = server.load_account(quest_account_pub_key)
print('IF IT FAILS CHECK THE TESTNET ORDERBOOK AND CHANGE DEST ASSET')
bump_transaction = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_bump_sequence_op(
       bump_to=stellar_account.sequence + 100
    )
    .set_timeout(30)
    .build()
)

print('Signing Transaction...')
bump_transaction.sign(quest_account_priv_key)
response = server.submit_transaction(bump_transaction)

print(f"This is the response from bump_transaction the token: {response}")

bump_account = Account(
    account=stellar_quest_keypair.public_key,
    sequence=stellar_account.sequence + 99,
)
next_transaction = (
    TransactionBuilder(
        source_account=bump_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_manage_data_op(
       data_name="sequence",
       data_value="bump",
    )
    .set_timeout(30)
    .build()
)
next_transaction.sign(stellar_quest_keypair)
next_res = server.submit_transaction(next_transaction)

print(f"This is the response from next_res the token: {next_res}")
