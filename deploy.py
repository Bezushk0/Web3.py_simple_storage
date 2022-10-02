from dis import Bytecode
from solcx import compile_standard, install_solc

install_solc("0.6.0")
import json
from web3 import Web3
import os

from dotenv import load_dotenv

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x58b8D1cc36d311847599B9DE9903dc72ddC5c0C8"
private_key = os.getenv("TWILIO_ACCOUNT_SID")
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(my_address)

transaction = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)

print(private_key)
