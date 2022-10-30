from stellar_sdk import Asset, Server, Keypair, TransactionBuilder, Network

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
stellar_quest_keypair = Keypair.from_secret("SBFK2ZFJD65CBELCWD6L6WJUM5F4W7MXUWULC3SE7H4VQ57WYPGTTDIM")
quest_account_pub_key = stellar_quest_keypair.public_key
quest_account_priv_key = stellar_quest_keypair.secret

# 2. Path
path = [
    Asset("USDT", "GDOORKS54L4JZBMP2BS2N52KZOXQSAQY7R74377T2JWXIXHSFQA2TZB2"),
    Asset("BTC", "GDOORKS54L4JZBMP2BS2N52KZOXQSAQY7R74377T2JWXIXHSFQA2TZB2"),
]

# 3. Transaction

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
     .append_path_payment_strict_receive_op(
        destination="GDOORKS54L4JZBMP2BS2N52KZOXQSAQY7R74377T2JWXIXHSFQA2TZB2",
        send_asset=Asset.native(),
        send_max="1000",
        dest_asset=Asset(
            "SOL", "GDOORKS54L4JZBMP2BS2N52KZOXQSAQY7R74377T2JWXIXHSFQA2TZB2"
        ),
        dest_amount=".1",
        path=path,
    )
    .set_timeout(30)
    .build()
)

print('Signing Transaction...')
transaction.sign(quest_account_priv_key)
response = server.submit_transaction(transaction)

print(f"This is the response from selling the token: {response}")