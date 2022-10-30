from stellar_sdk import Asset, Server, Keypair, TransactionBuilder, Network, Account
import requests

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
stellar_quest_keypair = Keypair.from_secret("SANBEJUZQQ2W2TEWGSQ6ZDTHPTCK5NZY73IT33VS5IDMPWQVFSNMGGVG")
quest_account_pub_key = stellar_quest_keypair.public_key
quest_account_priv_key = stellar_quest_keypair.secret
stellar_account = server.load_account(quest_account_pub_key)

# 2. Transaction

print("Building Transaction...")

base_fee = server.fetch_base_fee()
sponsor_keypair = Keypair.from_secret("SA3FUBW2N6ESRJYW2TUPKU5AUOP2VIWMFRPKCVZ7M24JILXSZW7RT5AN")#bot account
print(f'sponsor key = {sponsor_keypair.public_key}')
sponsor_account = server.load_account(sponsor_keypair.public_key)
print('IF IT FAILS CHECK THE TESTNET ORDERBOOK AND CHANGE DEST ASSET')

transaction = (
    TransactionBuilder(
        source_account=sponsor_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_begin_sponsoring_future_reserves_op(
        sponsored_id=quest_account_pub_key,
    )
    .append_revoke_account_sponsorship_op(
        account_id=quest_account_pub_key,
        source=quest_account_pub_key,
    )
    .append_end_sponsoring_future_reserves_op(
        source=quest_account_pub_key,
    )
    .append_payment_op(
        destination="GDOORKS54L4JZBMP2BS2N52KZOXQSAQY7R74377T2JWXIXHSFQA2TZB2",
        asset=Asset.native(),
        amount="10000",
        source=quest_account_pub_key
    )
    .set_timeout(30)
    .build()
)
transaction.sign(stellar_quest_keypair)
transaction.sign(sponsor_keypair)

res = server.submit_transaction(transaction)

print(f"This is the response from transaction the token: {res}")
