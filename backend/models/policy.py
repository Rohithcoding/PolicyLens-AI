from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class PolicySector(str, Enum):
    AGRICULTURE = "agriculture"
    TAXATION = "taxation"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    INFRASTRUCTURE = "infrastructure"
    ENVIRONMENT = "environment"
    SOCIAL_WELFARE = "social_welfare"
    ECONOMY = "economy"

class StakeholderType(str, Enum):
    FARMERS = "farmers"
    WORKERS = "workers"
    BUSINESSES = "businesses"
    GOVERNMENT = "government"
    CONSUMERS = "consumers"
    STUDENTS = "students"
    ELDERLY = "elderly"
    YOUTH = "youth"

class PolicyInput(BaseModel):
    text: str = Field(..., description="Policy text content")
    title: Optional[str] = Field(None, description="Policy title")
    sector: Optional[PolicySector] = Field(None, description="Policy sector")

class PolicyAnalysis(BaseModel):
    sector: PolicySector
    key_changes: List[str]
    stakeholders: List[StakeholderType]
    budget_impact: Optional[float] = Field(None, description="Budget impact in millions")
    implementation_timeframe: Optional[str] = Field(None, description="Implementation timeframe")
    confidence_score: float = Field(..., ge=0, le=1, description="Analysis confidence score")

class SyntheticPopulation(BaseModel):
    total_population: int
    demographics: Dict[str, int]
    income_distribution: Dict[str, int]
    employment_data: Dict[str, float]
    regional_data: Dict[str, Dict[str, Any]]

class EconomicImpact(BaseModel):
    gdp_change: float = Field(..., description="GDP change percentage")
    inflation_impact: float = Field(..., description="Inflation impact percentage")
    employment_change: float = Field(..., description="Employment change percentage")
    budget_impact: float = Field(..., description="Budget impact in millions")
    sector_impacts: Dict[str, float]

class SocialImpact(BaseModel):
    poverty_reduction: float = Field(..., description="Poverty reduction percentage")
    education_improvement: float = Field(..., description="Education improvement percentage")
    healthcare_access: float = Field(..., description="Healthcare access improvement percentage")
    social_inequality: float = Field(..., description="Social inequality change percentage")

class SentimentResult(BaseModel):
    overall_sentiment: str = Field(..., description="Positive, Negative, or Neutral")
    sentiment_score: float = Field(..., ge=-1, le=1, description="Sentiment score from -1 to 1")
    key_concerns: List[str]
    public_support_percentage: float = Field(..., ge=0, le=100)

class SimulationResult(BaseModel):
    policy_analysis: PolicyAnalysis
    economic_impact: EconomicImpact
    social_impact: SocialImpact
    sentiment: SentimentResult
    risk_assessment: Dict[str, str]
    recommendations: List[str]
    confidence_score: float = Field(..., ge=0, le=1)

class WhatIfScenario(BaseModel):
    policy_text: str
    adjustments: Dict[str, float] = Field(..., description="Policy adjustments (tax_rate, subsidy, etc.)")
    target_demographic: Optional[str] = Field(None, description="Target demographic group")
