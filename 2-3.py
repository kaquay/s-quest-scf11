from stellar_sdk import Asset, Server, Keypair, TransactionBuilder, Network
import requests

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
stellar_quest_keypair = Keypair.from_secret("SDU7PPT53A6PLDJ2OR25SHX3U7LPKNSBL5ETK62OXAEC7SJLLOL2D47M")
quest_account_pub_key = stellar_quest_keypair.public_key
quest_account_priv_key = stellar_quest_keypair.secret

# 2. Transaction

print("Building Transaction...")

base_fee = server.fetch_base_fee()
stellar_account = server.load_account(quest_account_pub_key)
print('IF IT FAILS CHECK THE TESTNET ORDERBOOK AND CHANGE DEST ASSET')
transaction = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_set_options_op(
       home_domain="aml7u44b63ss.runkit.sh"
    )
    .set_timeout(30)
    .build()
)

print('Signing Transaction...')
transaction.sign(quest_account_priv_key)
response = server.submit_transaction(transaction)

print(f"This is the response from selling the token: {response}")