# Packages
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from decouple import config
from web3 import Web3

# Internal Config
from contract.contract_config import CONTRACT_ADDRESS, CONTRACT_ABI
from ai.openai_config import get_recommended_applicant, get_applicant_insight

route = APIRouter(prefix='/chat')

RPC_URL = config("RPC_URL", "http://127.0.0.1:8545")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

PRIVATE_KEY = config('PRIVATE_KEY', None)
ACCOUNT_ADDRESS = w3.eth.account.from_key(PRIVATE_KEY).address

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

    # Collect Campaign Data
    campaign = contract.functions.getCampaign(campaign_id).call()
    
    # Collect Campaign Applicant
    applicants = contract.functions.getAllApplication(campaign_id).call()

    applicant_result = []

    for x in applicants:
        applicant = contract.functions.getApplication(x).call()
        applicant_result.append(applicant)
    
    response = get_recommended_applicant(
        campaign_data={
            "title": campaign[0], 
            "description": campaign[1]
        }, 
        applicant_data=[
            {
                "address": x[1],
                "title": x[2],
                "proposal": x[3],
            } for x in applicant_result
        ]
    )

    return JSONResponse(
        content={
            "message": response
        },
        status_code=200
    )


@route.get(
    path="/applicant-insight"
)
async def applicant_insight(
    campaign_id: int,
    applicant_id: int,
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

    # Collect Campaign Data
    campaign = contract.functions.getCampaign(campaign_id).call()
    
    # Collect Campaign Applicant
    applicant = contract.functions.getApplication(x).call()
    
    response = get_applicant_insight(
        campaign_data={
            "title": campaign[0], 
            "description": campaign[1]
        }, 
        applicant_data={
            "address": applicant[1],
            "title": applicant[2],
            "proposal": applicant[3],
        }
    )

    return JSONResponse(
        content={
            "message": response
        },
        status_code=200
    )