import logging
from cartesi.router import DAppAddressRouter
from cartesi.wallet.ether import EtherWallet
from cartesi import DApp, Rollup, RollupData, JSONRouter, ABIRouter, ABILiteralHeader, ABIFunctionSelectorHeader, URLRouter, URLParameters

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

ETHER_PORTAL_ADDRESS = '0xffdbe43d4c855bf7e0f105c400a50857f53ab044'
ADDRESS_RELAY_ADDRESS = '0xf5de34d6bbc0446e2a45719e718efebaae179dae'


dapp = DApp()
abi_router = ABIRouter()
url_router = URLRouter()
json_router = JSONRouter()
dapp_address = DAppAddressRouter(relay_address=ADDRESS_RELAY_ADDRESS)
ether_wallet = EtherWallet(portal_address=ETHER_PORTAL_ADDRESS, dapp_address_router=dapp_address)


dapp.add_router(abi_router)
dapp.add_router(url_router)
dapp.add_router(json_router)
dapp.add_router(ether_wallet)
dapp.add_router(dapp_address)

# As a user, i want to request the balance of Ether in all wallet on layer 2. ( url parameters )
# As a user, I want to deploy any contract. ( abiliteral )
# As a user, I want to request the minting of an NFT (ERC721) for an address on Layer 1. ( abifunction )
# As a user, I want to request the minting of NFTs (ERC1155) for an address on Layer 1. (json)
# As a user, I want to request the minting of tokens (ERC20) for an address on Layer 1. ( abit literal )


def str2hex(str):
    """Encodes a string as a hex string"""
    return "0x" + str.encode("utf-8").hex()

# As a user, I want to withdraw my deposit in Ether. (abifunction)


@url_router.inspect('balance/ether/{address}')
def balance_of_wallet(rollup: Rollup, params: URLParameters) -> bool:
    """
    This function returns the balance of a specified Ether wallet. It takes a Rollup object and URLParameters object as input parameters, and returns a boolean value.
    """
    msg = f"Balance: {ether_wallet.balance.get(params.path_params['address'].lower(), 0)} wei"
    rollup.report('0x' + msg.encode('utf-8').hex())
    return True

# @dapp.advance()
# def handle_advance(rollup: Rollup, data: RollupData) -> bool:
#     payload = data.str_payload()
#     LOGGER.debug("Echoing '%s'", payload)
#     rollup.notice(str2hex(payload))
#     return True


# @dapp.inspect()
# def handle_inspect(rollup: Rollup, data: RollupData) -> bool:
#     payload = data.str_payload()
#     LOGGER.debug("Echoing '%s'", payload)
#     rollup.report(str2hex(payload))
#     return True


if __name__ == '__main__':
    dapp.run()
