import requests
import json
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# List of available Lotus JSON-RPC methods with hints for expected parameters
lotus_methods = {
    "ChainNotify": "No parameters.",
    "ChainHead": "No parameters.",
    "ChainGetRandomnessFromTickets": "Params: [TipSetKey, DomainSeparationTag, ChainEpoch, Entropy (bytes)]",
    "ChainGetRandomnessFromBeacon": "Params: [TipSetKey, DomainSeparationTag, ChainEpoch, Entropy (bytes)]",
    "ChainGetBlock": "Params: [Block CID]",
    "ChainGetTipSet": "Params: [TipSetKey]",
    "ChainGetBlockMessages": "Params: [Block CID]",
    "ChainGetParentReceipts": "Params: [Block CID]",
    "ChainGetParentMessages": "Params: [Block CID]",
    "ChainGetMessagesInTipset": "Params: [TipSetKey]",
    "ChainGetTipSetByHeight": "Params: [ChainEpoch, TipSetKey]",
    "ChainReadObj": "Params: [CID]",
    "ChainPutObj": "Params: [Block]",
    "ChainHasObj": "Params: [CID]",
    "ChainStatObj": "Params: [Object CID, Base CID]",
    "ChainSetHead": "Params: [TipSetKey]",
    "ChainGetGenesis": "No parameters.",
    "ChainTipSetWeight": "Params: [TipSetKey]",
    "StateAccountKey": "Params: [Address, TipSetKey]",
    "StateNetworkName": "No parameters.",
    "StateGetActor": "Params: [Actor Address, TipSetKey]",
    "StateCall": "Params: [Message, TipSetKey]",
    "MpoolPushMessage": "Params: [Message, SendSpec]"
}

methods_completer = WordCompleter(list(lotus_methods.keys()), ignore_case=True)

url = 'http://127.0.0.1:1234/rpc/v0'

def lotus_rpc_call(method, params):
    headers = {
        'Content-Type': 'application/json',
    }

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": params
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": f"Failed with status code {response.status_code}",
            "response": response.text
        }

if __name__ == "__main__":
    # Prompt user for method with autocomplete
    selected_method = prompt("Select a method: ", completer=methods_completer)

    # Automatically prepend "Filecoin." to the selected method
    method = f"Filecoin.{selected_method}"

    # Show hint about the method's expected parameters
    print(f"Hint: {lotus_methods.get(selected_method, 'No hint available')}")

    # Ask for params input as a JSON array
    params = input("Enter the params as a JSON array (e.g., [\"t017880\", null]): ")

    try:
        params = json.loads(params)  # Ensure the input is a valid JSON array
    except json.JSONDecodeError:
        print("Invalid JSON array for params.")
        exit(1)

    # Make the RPC call
    result = lotus_rpc_call(method, params)
    print("Response:", json.dumps(result, indent=2))
