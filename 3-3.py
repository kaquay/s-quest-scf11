from time import sleep
from stellar_sdk import Asset, ClaimPredicate, Claimant, Server, Keypair, TransactionBuilder, Network
import requests

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
stellar_quest_keypair = Keypair.from_secret(
    "SB6PTKXMQLALWZTNHCMLOQ5CDZ7P4ROKNBFB4J5KEZUTKXPC2AFKLHZT")

print("stellar_quest public key: ", stellar_quest_keypair.public_key)
print("stellar_quest scret key: ", stellar_quest_keypair.secret)

# ClaimantKeypair
claimant_keypair = Keypair.random()
url = "https://friendbot.stellar.org"
frientbot_response = requests.get(url, params={"addr": claimant_keypair.public_key})
print("frientbot_response", frientbot_response)
print("claimant public key: ", claimant_keypair.public_key)
print("claimant scret key: ", claimant_keypair.secret)

time = 60 * 5

# Create Claimant
claimant = Claimant(
    destination=claimant_keypair.public_key,
    predicate=ClaimPredicate.predicate_not(
        ClaimPredicate.predicate_before_relative_time(time) # 1 minutes
    )
)

stellar_claimant = Claimant(
    destination=stellar_quest_keypair.public_key,
    predicate= ClaimPredicate.predicate_unconditional()
)

# 2. Transaction
print("Building Transaction...")
base_fee = server.fetch_base_fee()
stellar_account = server.load_account(stellar_quest_keypair.public_key)
claimant_account = server.load_account(claimant_keypair.public_key)

transaction = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_create_claimable_balance_op(
        asset=Asset.native(),
        amount="1000",
        claimants=[
            claimant,
            stellar_claimant
        ]
    )
    .set_timeout(30)
    .build()
)

print('Signing Transaction...')
transaction.sign(stellar_quest_keypair)
response = server.submit_transaction(transaction)

print("Transaction Successful! Hash: {}".format(response))

# Claim
print('waiting for {} seconds'.format(time))
sleep(time)
request_balance_id = requests.get("https://horizon-testnet.stellar.org/claimable_balances/?asset=native&claimant={}".format(claimant_keypair.public_key))
balance_id=request_balance_id.json()["_embedded"]["records"][0]["id"]
print("balance_id: ",balance_id)
claim_txn = (
    TransactionBuilder(
        source_account=claimant_account, 
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE
    )
    .append_claim_claimable_balance_op(
        balance_id=balance_id, 
    )
    .set_timeout(30)
    .build()
)

claim_txn.sign(claimant_keypair)
claim_claimable_balance_resp = server.submit_transaction(claim_txn)
print(claim_claimable_balance_resp)
