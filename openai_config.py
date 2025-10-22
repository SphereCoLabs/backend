from google import genai
from google.genai import types
from decouple import config
import json

client = genai.Client(api_key=config('GEMINI_API_KEY'))

def get_response(campaign_data, applicant_data):
    system_instruction = """You are a KOL recruitment specialist analyzing campaign-applicant matches.
    ANALYZE: Campaign details + applicant profiles
    OUTPUT: Text-only recommendation suitable for HTML display

    STRUCTURE:
    Opening: "I evaluated applicants based on [criteria]..."
    Body: Each recommended applicant with:
    - Address: 0x...
    - Why recommended: [specific reasons]
    Closing: 
    - Top pick with strongest rationale
    - "This analysis aids your decision-making. Final selection remains yours."

    RULES:
    - Recommend 1+ applicants (quality over quantity)
    - Be specific, avoid generic praise
    - Focus on campaign-applicant alignment
    """

    user_instruction = f"""Please analyze this campaign and recommend the best-fit KOL applicants.

    CAMPAIGN:
    Title: {campaign_data['title']}
    Description: {campaign_data['description']}

    APPLICANTS:
    {[json.dumps(x, indent=2) for x in applicant_data]}

    Identify the top matches and provide your recommendations."""

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.3
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_instruction,
        config=config,
    )
    
    result = response.text

    return result

