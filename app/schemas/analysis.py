from pydantic import BaseModel
from typing import Optional

class AnalysisRequest(BaseModel):
    """
    Represents a request to the AI model for diagnosis for analysis.

    Attributes:
        data (str): The data to be analyzed (JSON).
    """
    data: dict

class AnalysisResponse(BaseModel):
    """
    Represents the response from the AI model for analysis.

    Attributes:
        texto (Optional[str]): The text of the analysis result.
    """
    analysis: Optional[str] = None
