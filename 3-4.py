from stellar_sdk import Asset, Server, Keypair, TransactionBuilder, Network
import requests

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
quest_keypair = Keypair.from_secret("SBRYGIXCUTFIHE2WIVBY6PONG3TRVIHTCNLMJNAXUAN5Y73QZIVGSZKR")
quest_account_pub_key = quest_keypair.public_key
quest_account_priv_key = quest_keypair.secret
destinationKeypair =Keypair.random()
print("destinationKeypair public key: ", destinationKeypair.public_key)
print("destinationKeypair scret key: ", destinationKeypair.secret)
# 2. Transaction
url = "https://friendbot.stellar.org"
frientbot_response = requests.get(url, params={"addr": destinationKeypair.public_key})

print("Building Transaction...")

base_fee = server.fetch_base_fee()
stellar_account = server.load_account(quest_account_pub_key)
destinationAccount = server.load_account(destinationKeypair.public_key)

print('IF IT FAILS CHECK THE TESTNET ORDERBOOK AND CHANGE DEST ASSET')
transaction = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_set_options_op(
        set_flags=10,
    )
    .set_timeout(30)
    .build()
)

print('Signing Transaction...')
transaction.sign(quest_account_priv_key)
response = server.submit_transaction(transaction)

print(f"This is the response from selling the token: {response}")

print('second request ')

clawbackAsset = Asset(
    code="CLAWBACK",
    issuer=quest_keypair.public_key,
)
paymentTransaction = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_change_trust_op(
        asset=clawbackAsset,
        source=destinationKeypair.public_key,
    )
    .append_payment_op(
        destination=destinationKeypair.public_key,
        asset=clawbackAsset,
        amount="500"
    )
    .set_timeout(30)
    .build()
)
paymentTransaction.sign(quest_keypair)
paymentTransaction.sign(destinationKeypair)

paymentResponse = server.submit_transaction(paymentTransaction)

print(f"paymentResponse: {paymentResponse}")

print('burn clawback')

clawbackTransaction = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_clawback_op(
        asset=clawbackAsset,
        amount="250",
        from_= destinationKeypair.public_key,
    )
    .set_timeout(30)
    .build()
)
clawbackTransaction.sign(quest_keypair)


clawbackResponse = server.submit_transaction(clawbackTransaction)

print(f"clawbackResponse: {clawbackResponse}")
