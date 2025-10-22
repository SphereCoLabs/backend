# Packages
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from decouple import config
from web3 import Web3

# Internal Config
from contract_config import CONTRACT_ADDRESS, CONTRACT_ABI
from openai_config import get_response

route = APIRouter(prefix='/chat')

RPC_URL = config("RPC_URL", "http://127.0.0.1:8545")
w3 = Web3(Web3.HTTPProvider(RPC_URL))



@route.get(
    path="/recommended-applicants"
)
async def recommended_applicants(
    campaign_id: int
):
    try:
        if w3.is_connected():
            print("Connecting to Ethereum node.")
            contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
            print("Connected to Ethereum node.")
        else:
            print("Failed to connect to Ethereum node.")
            raise Exception()
        
    except Exception as e:
        print(f"Warning: Could not initialize contract: {e}")
        contract = None
    
    if not contract:
        raise HTTPException(status_code=500, detail="Smart contract not initialized")
    
    print("START CREATE")
    PRIVATE_KEY = '0xdf57089febbacf7ba0bc227dafbffa9fc08a93fdc68e1e42411a14efcf23656e'  # NEVER hard-code in production; load securely!
    ACCOUNT_ADDRESS = w3.eth.account.from_key(PRIVATE_KEY).address  # Derive address from key

    # Build the transaction
    # tx = contract.functions.registerUser(
    #     "Michael",
    #     "An experienced person with total 5+ years in blockchain environment.",
    #     1  # Assuming 1 corresponds to UserRole.Campaigner; adjust per your enum
    # ).build_transaction({
    #     'from': ACCOUNT_ADDRESS,
    #     'gas': 200000,  # Estimate with w3.eth.estimate_gas(tx) for accuracy
    #     'gasPrice': w3.to_wei('5', 'gwei'),  # Or use 'maxFeePerGas' and 'maxPriorityFeePerGas' for EIP-1559 chains
    #     'nonce': w3.eth.get_transaction_count(ACCOUNT_ADDRESS),
    #     'chainId': w3.eth.chain_id,  # Required for signed tx
    # })

    # # Sign the transaction
    # signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

    # # Send the transaction
    # tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # # Wait for receipt (confirms mining and success)
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)  # Adjust timeout as needed

    # print(f"DONE. Tx hash: {tx_hash.hex()}")
    # print(f"Receipt: {tx_receipt}")

    # # Optional: Check event emission in the receipt
    # if tx_receipt.status == 1:  # Success
    #     # Parse logs if you have event ABI defined
    #     event = contract.events.UserRegistered().process_receipt(tx_receipt)
    #     if event:
    #         print(f"Event emitted: {event[0]['args']}")
    # else:
    #     print("Transaction failed!")
    # print("DONE")
    
    print("START CALL")
    user = contract.functions.getUser().call({
        'from': ACCOUNT_ADDRESS
    })
    print(user)
    print("DONE")
    # campaign_id = contract.functions.createCampaign("Campaign SUI Network", "Must be have 1 year experience about influencing blockchain network (Including SUI network), global environtment so you can work on WFH system.").call()

    # campaigns = contract.functions.getAllCampaignIds().call()

    # campaign = contract.functions.getCampaign(campaign_id).call()

    


    # # Collect Campaign Data
    # campaign = contract.functions.getCampaign(campaign_id).call()
    
    # # Collect Campaign Applicant
    # applicants = contract.functions.getAllApplication(campaign_id).call()

    # applicant_result = []

    # for x in applicants:
    #     applicant = contract.functions.getApplication.call(x)
    #     applicant_result.append(applicant)
    
    # # Setup AI to deep dive think
    # # Send data collected to AI so he can make recommendations
    # # TODO Need to format campaign and applications data
    response = get_response(
        campaign_data={
            "title": "Campaign SUI Network", 
            "description": "Must be have 1 year experience about influencing blockchain network (Including SUI network), global environtment so you can work on WFH system."
        }, 
        applicant_data=[
            {
                "address": "0xdf57089febbacf7ba0bc227dafbffa9fc08a93fdc68e1e42411a14efcf23656e",
                "name": user[0],
                "summary": user[1],
            }
        ]
    )
    print(response)

    return JSONResponse(
        content={
            "message": response
        },
        status_code=200
    )