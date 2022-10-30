from stellar_sdk import Asset, Server, Keypair, TransactionBuilder, Network, LiquidityPoolAsset, LiquidityPoolId
import requests

# 1. Load Keys
server = Server("https://horizon-testnet.stellar.org")
quest_keypair = Keypair.from_secret("SBX6GR6U5LTHHKSRY63CHXRKS2WQ3CDV2UDOGO6PPXH5CRD56EQL2DES")
quest_account_pub_key = quest_keypair.public_key
quest_account_priv_key = quest_keypair.secret
url = "https://friendbot.stellar.org"
frientbot_response = requests.get(url, params={"addr": quest_keypair.public_key})
print(f'friend bot: {frientbot_response}')
print("Building Transaction...")

base_fee = server.fetch_base_fee()
stellar_account = server.load_account(quest_account_pub_key)

print('IF IT FAILS CHECK THE TESTNET ORDERBOOK AND CHANGE DEST ASSET')

noodleAsset = Asset(
    code="NOODLE",
    issuer=quest_keypair.public_key,
)


lpAsset = LiquidityPoolAsset(
    asset_a=Asset.native(),
    asset_b=noodleAsset,
    fee=30,
)

liquidityPoolId = lpAsset.liquidity_pool_id

print(f'liquidityPoolId = {liquidityPoolId}')

lpDepositTransaction = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_change_trust_op(
       asset=lpAsset
    )
    .append_liquidity_pool_deposit_op(
        liquidity_pool_id=liquidityPoolId,
        max_amount_a="100",
        max_amount_b="100",
        min_price="1",
        max_price="1",
    )
    .set_timeout(30)
    .build()
)

print('lpDepositTransaction...')
lpDepositTransaction.sign(quest_account_priv_key)
response = server.submit_transaction(lpDepositTransaction)
print(f"lpDepositTransaction: {response}")

tradeKeypair =Keypair.random()
print("tradeKeypair public key: ", tradeKeypair.public_key)
print("tradeKeypair scret key: ", tradeKeypair.secret)
# 2. Transaction
url = "https://friendbot.stellar.org"
frientbot_response = requests.get(url, params={"addr": tradeKeypair.public_key})
print(f'friend bot: {frientbot_response}')

tradeAccount = server.load_account(tradeKeypair.public_key)

pathPaymentTransaction = (
    TransactionBuilder(
        source_account=tradeAccount,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_change_trust_op(
       asset=noodleAsset,
       source=tradeKeypair.public_key,
    )
    .append_path_payment_strict_receive_op(
        send_asset=Asset.native(),
        send_max="100",
        destination=tradeKeypair.public_key,
        dest_asset=noodleAsset,
        dest_amount="1",
        source=tradeKeypair.public_key,
        path= [noodleAsset],
    )
    # .append_path_payment_strict_send_op()
    .set_timeout(30)
    .build()
)

print('pathPaymentTransaction...')
pathPaymentTransaction.sign(tradeKeypair)
tradeResponse = server.submit_transaction(pathPaymentTransaction)
print(f"pathPaymentTransaction: {tradeResponse}")

print("lpWithdrawTransaction")

lpWithdrawTransaction = (
    TransactionBuilder(
        source_account=stellar_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .append_liquidity_pool_withdraw_op(
        liquidity_pool_id=liquidityPoolId,
        amount="100",
        min_amount_a="0",
        min_amount_b="0",

    )
    .set_timeout(30)
    .build()
)

print('pathPaymentTransaction...')
lpWithdrawTransaction.sign(quest_keypair)
lpWithdrawResponse = server.submit_transaction(lpWithdrawTransaction)
print(f"lpWithdrawResponse: {lpWithdrawResponse}")