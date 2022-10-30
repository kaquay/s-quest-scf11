from stellar_sdk import Asset, Server, Keypair, TransactionBuilder, Network, TrustLineFlags
import requests

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
stellar_quest_keypair = Keypair.from_secret("SBNFWBJ7QGAZQOKXOYKO4TKEKI5IXCASLVLHLHCSPLL7Q4EK3J2T2Z6D")
quest_account_pub_key = stellar_quest_keypair.public_key
quest_account_priv_key = stellar_quest_keypair.secret
issue_keypair = Keypair.random()
# 2. Transaction

print("Building Transaction...")

base_fee = server.fetch_base_fee()
stellar_account = server.load_account(quest_account_pub_key)
print('IF IT FAILS CHECK THE TESTNET ORDERBOOK AND CHANGE DEST ASSET')

# create issure account
issuer_txn = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_create_account_op(
        destination=issue_keypair.public_key, starting_balance="120"
    )
    .set_timeout(30)
    .build()
)
issuer_txn.sign(stellar_quest_keypair)
res = server.submit_transaction(issuer_txn)
print("issue_keypair.public_key", issue_keypair.public_key)
print("Issuer account: ", res)

print("Building Set Flag Transaction...")
issue_asset = Asset(
    code="Zeizei",
    issuer=issue_keypair.public_key
)
issuer = server.load_account(issue_keypair.public_key)


transaction = (
    TransactionBuilder(
        source_account=issuer,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_set_options_op(
       set_flags=3
    )
    .append_change_trust_op(
        asset=issue_asset,
        source=quest_account_pub_key,
    )
    .append_set_trust_line_flags_op(
        trustor=quest_account_pub_key,
        asset=issue_asset,
        set_flags=TrustLineFlags(1)
    )
    .append_payment_op(
        destination=quest_account_pub_key,
        asset=issue_asset,
        amount='100'
    )
    .append_set_trust_line_flags_op(
        trustor=quest_account_pub_key,
        asset=issue_asset,
        clear_flags=TrustLineFlags(1)
    )
    .set_timeout(30)
    .build()
)

print('Signing Transaction...')
transaction.sign(issue_keypair)
transaction.sign(quest_account_priv_key)
response = server.submit_transaction(transaction)

print(f"This is the response from selling the token: {response}")