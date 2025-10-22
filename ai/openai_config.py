from google import genai
from google.genai import types
from decouple import config
import json

from types import KOLAnalysis

client = genai.Client(api_key=config('GEMINI_API_KEY'))

def get_recommended_applicant(campaign_data: dict, applicant_data: List[dict]):
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


def get_applicant_insight(campaign_data: dict, applicant_data: dict):
    system_instruction = """You are an expert KOL campaign analyst providing AI-powered insights.

    ANALYZE: Single KOL profile against campaign requirements
    OUTPUT: JSON with insights array, score, and justification

    EVALUATION:
    - Analyze engagement rate and content quality
    - Assess audience alignment with campaign demographics
    - Review experience with similar brands/campaigns
    - Evaluate conversion potential and community responsiveness

    SCORING: 0-100 scale
    - 90-100: Exceptional match
    - 80-89: Strong match
    - 70-79: Good match
    - Below 70: Moderate/weak match

    INSIGHTS: Provide 4-6 specific points explaining:
    - Quantifiable strengths (engagement, reach, ROI)
    - Relevant experience and track record
    - Audience alignment factors
    - Community quality indicators

    Return ONLY valid JSON in this format:
    {
    "insights": ["point 1", "point 2", ...],
    "score": 98,
    "score_justification": "brief explanation"
    }
    """

    user_instruction = f"""Analyze this KOL's fit for the campaign.

    CAMPAIGN:
    Title: {campaign_data['title']}
    Description: {campaign_data['description']}

    KOL PROFILE:
    {json.dumps(applicant_data, indent=2)}

    Provide insights and match score as JSON."""

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        temperature=0.3,
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_instruction,
        config=config,
    )

    # Parse response
    result_json = json.loads(response.text)
    result = KOLAnalysis(**result_json)

    return result

