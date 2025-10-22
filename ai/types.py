from pydantic import BaseModel
from typing import List

class KOLAnalysis(BaseModel):
    insights: List[str]
    score: int
    score_justification: str