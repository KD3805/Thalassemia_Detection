# File: models.py
"""
This defines the Pydantic model to handle incoming image URLs.
"""

from pydantic import BaseModel, Field

class BloodReportModel(BaseModel):
    sex: str = Field(..., example="female")
    hb: float = Field(..., example=10.8)
    pcv: float = Field(..., example=35.2)
    rbc: float = Field(..., example=5.12)
    mcv: float = Field(..., example=68.7)
    mch: float = Field(..., example=21.2)
    mchc: float = Field(..., example=30.8)
    rdw: float = Field(..., example=13.4)
    wbc: float = Field(..., example=9.6)
    neut: float = Field(..., example=53)
    lymph: float = Field(..., example=33)
    plt: float = Field(..., example=309)
    hba: float = Field(..., example=88.5)
    hba2: float = Field(..., example=2.6)
    hbf: float = Field(..., example=0.11)