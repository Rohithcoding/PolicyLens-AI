from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import random
import math

app = FastAPI(
    title="PolicyLens AI API",
    description="AI-powered policy analysis and simulation platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class PolicyInput(BaseModel):
    text: str
    title: Optional[str] = None
    adjustments: Optional[Dict[str, float]] = {}

class PolicyAnalysis(BaseModel):
    sector: str
    key_changes: List[str]
    stakeholders: List[str]
    budget_impact: Optional[float] = None
    implementation_timeframe: Optional[str] = None
    confidence_score: float

class EconomicImpact(BaseModel):
    gdp_change: float
    inflation_impact: float
    employment_change: float
    budget_impact: float
    sector_impacts: Dict[str, float]

class SocialImpact(BaseModel):
    poverty_reduction: float
    education_improvement: float
    healthcare_access: float
    social_inequality: float

class SentimentResult(BaseModel):
    overall_sentiment: str
    sentiment_score: float
    key_concerns: List[str]
    public_support_percentage: float

class SimulationResult(BaseModel):
    policy_analysis: PolicyAnalysis
    economic_impact: EconomicImpact
    social_impact: SocialImpact
    sentiment: SentimentResult
    risk_assessment: Dict[str, str]
    recommendations: List[str]
    confidence_score: float

# Helper Functions
def detect_sector(text: str) -> str:
    """Simple sector detection based on keywords"""
    text_lower = text.lower()
    sectors = {
        "agriculture": ["farm", "agriculture", "crop", "irrigation", "farmer", "rural"],
        "taxation": ["tax", "revenue", "income tax", "gst", "taxation", "fiscal"],
        "healthcare": ["health", "medical", "hospital", "doctor", "medicine", "healthcare"],
        "education": ["education", "school", "college", "student", "teacher", "university"],
        "infrastructure": ["road", "bridge", "infrastructure", "transport", "highway", "railway"],
        "environment": ["environment", "climate", "pollution", "green", "sustainability", "carbon"],
        "social_welfare": ["welfare", "social", "poverty", "employment", "rural development"],
        "economy": ["economy", "economic", "gdp", "growth", "investment", "finance"]
    }
    
    sector_scores = {}
    for sector, keywords in sectors.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        sector_scores[sector] = score
    
    return max(sector_scores, key=sector_scores.get) if sector_scores else "economy"

def extract_key_changes(text: str) -> List[str]:
    """Extract key changes from policy text"""
    sentences = text.split('.')
    changes = []
    change_indicators = ["will", "shall", "intends to", "aims to", "proposes", "introduces", "implements"]
    
    for sentence in sentences[:5]:
        if any(indicator in sentence.lower() for indicator in change_indicators):
            clean_sentence = sentence.strip()
            if len(clean_sentence) > 20:
                changes.append(clean_sentence[:100] + "..." if len(clean_sentence) > 100 else clean_sentence)
    
    return changes[:3] if changes else ["Policy implementation planned", "Regulatory changes expected"]

def identify_stakeholders(text: str) -> List[str]:
    """Identify stakeholders from text"""
    text_lower = text.lower()
    stakeholder_keywords = {
        "farmers": ["farmer", "farm", "agriculture", "rural"],
        "workers": ["worker", "labor", "employee", "wage"],
        "businesses": ["business", "company", "corporate", "industry"],
        "government": ["government", "state", "central", "administration"],
        "consumers": ["consumer", "customer", "public", "citizen"],
        "students": ["student", "education", "school", "college"],
        "elderly": ["elderly", "senior", "old age", "pension"],
        "youth": ["youth", "young", "graduate", "job"]
    }
    
    identified = []
    for stakeholder, keywords in stakeholder_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            identified.append(stakeholder)
    
    return identified if identified else ["consumers", "government"]

def analyze_sentiment(text: str) -> SentimentResult:
    """Simple sentiment analysis"""
    positive_words = ["good", "great", "excellent", "beneficial", "positive", "helpful", "effective", "successful", "improve"]
    negative_words = ["bad", "poor", "negative", "harmful", "damage", "problem", "difficult", "challenge", "oppose"]
    
    words = text.lower().split()
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    
    if positive_count > negative_count:
        sentiment = "Positive"
        score = min(0.8, (positive_count - negative_count) / len(words) * 10)
    elif negative_count > positive_count:
        sentiment = "Negative"
        score = max(-0.8, (negative_count - positive_count) / len(words) * 10)
    else:
        sentiment = "Neutral"
        score = 0.0
    
    concerns = ["Implementation complexity", "Budget constraints", "Stakeholder acceptance"][:2]
    support = max(20, min(85, 50 + score * 30))
    
    return SentimentResult(
        overall_sentiment=sentiment,
        sentiment_score=round(score, 3),
        key_concerns=concerns,
        public_support_percentage=round(support, 1)
    )

def calculate_impacts(sector: str, adjustments: Dict[str, float]) -> tuple[EconomicImpact, SocialImpact]:
    """Calculate economic and social impacts"""
    # Base impacts by sector
    base_impacts = {
        "agriculture": {"gdp": 0.08, "employment": 0.05, "poverty": 0.15, "budget": 500},
        "education": {"gdp": 0.06, "employment": 0.03, "education": 0.25, "budget": 300},
        "healthcare": {"gdp": 0.04, "employment": 0.04, "healthcare": 0.35, "budget": 1200},
        "infrastructure": {"gdp": 0.12, "employment": 0.08, "poverty": 0.05, "budget": 2000},
        "taxation": {"gdp": 0.15, "employment": 0.12, "poverty": 0.08, "budget": -8000},
        "environment": {"gdp": 0.12, "employment": 0.08, "poverty": 0.08, "budget": 2000},
        "social_welfare": {"gdp": 0.05, "employment": 0.02, "poverty": 0.20, "budget": 800},
        "economy": {"gdp": 0.10, "employment": 0.06, "poverty": 0.10, "budget": 1000}
    }
    
    base = base_impacts.get(sector, base_impacts["economy"])
    
    # Apply adjustments
    budget_multiplier = 1 + adjustments.get("budget_increase", 0)
    tax_effect = adjustments.get("tax_rate", 0)
    subsidy_effect = adjustments.get("subsidy_increase", 0)
    
    gdp_change = base["gdp"] + tax_effect * 0.3 + subsidy_effect * 0.2
    employment_change = base["employment"] + subsidy_effect * 0.1
    inflation_impact = 0.02 + tax_effect * 0.1
    budget_impact = base["budget"] * budget_multiplier
    
    # Economic impact
    sector_impacts = {
        "agriculture": random.uniform(-0.05, 0.15),
        "manufacturing": random.uniform(-0.03, 0.12),
        "services": random.uniform(-0.02, 0.10),
        "technology": random.uniform(-0.01, 0.18),
        "retail": random.uniform(-0.04, 0.08)
    }
    
    economic_impact = EconomicImpact(
        gdp_change=round(gdp_change, 3),
        inflation_impact=round(inflation_impact, 3),
        employment_change=round(employment_change, 3),
        budget_impact=round(budget_impact, 2),
        sector_impacts={k: round(v, 3) for k, v in sector_impacts.items()}
    )
    
    # Social impact
    social_impact = SocialImpact(
        poverty_reduction=round(base["poverty"] + subsidy_effect * 0.3, 3),
        education_improvement=round(base.get("education", 0.05) + subsidy_effect * 0.1, 3),
        healthcare_access=round(base.get("healthcare", 0.06) + subsidy_effect * 0.05, 3),
        social_inequality=round(-0.08 + subsidy_effect * 0.2, 3)
    )
    
    return economic_impact, social_impact

# API Routes
@app.get("/")
async def root():
    return {"message": "PolicyLens AI API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/policy/sectors")
async def get_policy_sectors():
    return {
        "sectors": [
            "agriculture", "taxation", "healthcare", "education",
            "infrastructure", "environment", "social_welfare", "economy"
        ]
    }

@app.post("/api/policy/analyze", response_model=SimulationResult)
async def analyze_policy(policy_input: PolicyInput):
    """Analyze policy and return comprehensive simulation results"""
    try:
        # Policy analysis
        sector = detect_sector(policy_input.text)
        key_changes = extract_key_changes(policy_input.text)
        stakeholders = identify_stakeholders(policy_input.text)
        
        policy_analysis = PolicyAnalysis(
            sector=sector,
            key_changes=key_changes,
            stakeholders=stakeholders,
            budget_impact=random.uniform(-500, 2000),
            implementation_timeframe="12-18 months",
            confidence_score=0.85
        )
        
        # Impact calculations
        adjustments = policy_input.adjustments or {}
        economic_impact, social_impact = calculate_impacts(sector, adjustments)
        
        # Sentiment analysis
        sentiment = analyze_sentiment(policy_input.text)
        
        # Risk assessment
        risk_assessment = {
            "budget": "Moderate budget impact within acceptable limits",
            "implementation": "Complex implementation may face delays",
            "political": "Likely to receive broad political support",
            "economic": "Minimal economic disruption expected",
            "social": "Broad social acceptance likely"
        }
        
        # Recommendations
        recommendations = [
            "Monitor implementation progress quarterly",
            "Establish clear metrics for success measurement",
            "Engage stakeholder groups early in the process",
            "Consider phased implementation approach",
            "Build in flexibility for adjustments"
        ]
        
        # Confidence score
        confidence_score = min(0.90, policy_analysis.confidence_score)
        
        return SimulationResult(
            policy_analysis=policy_analysis,
            economic_impact=economic_impact,
            social_impact=social_impact,
            sentiment=sentiment,
            risk_assessment=risk_assessment,
            recommendations=recommendations,
            confidence_score=confidence_score
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Policy analysis failed: {str(e)}")

@app.post("/api/policy/what-if", response_model=SimulationResult)
async def what_if_simulation(scenario: dict):
    """Run 'What If' simulation with policy adjustments"""
    try:
        policy_text = scenario.get("policy_text", "")
        adjustments = scenario.get("adjustments", {})
        
        # Reuse the analyze logic with adjustments
        policy_input = PolicyInput(text=policy_text, adjustments=adjustments)
        return await analyze_policy(policy_input)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"What-if simulation failed: {str(e)}")

@app.get("/api/simulation/population/default")
async def get_default_population():
    """Get default synthetic population data"""
    return {
        "total_population": 1000000,
        "demographics": {
            "18-25": 200000,
            "26-35": 250000,
            "36-50": 250000,
            "51-65": 200000,
            "65+": 100000
        },
        "income_distribution": {
            "low": 400000,
            "middle": 450000,
            "high": 150000
        },
        "employment_data": {
            "agriculture": 162500,
            "manufacturing": 130000,
            "services": 227500,
            "technology": 65000,
            "government": 65000,
            "overall_employment_rate": 0.65,
            "unemployment_rate": 0.35
        },
        "regional_data": {
            "urban": {
                "population": 350000,
                "avg_income": 65000,
                "education_level": "higher",
                "main_sectors": ["technology", "services", "manufacturing"],
                "infrastructure_quality": 0.8
            },
            "rural": {
                "population": 500000,
                "avg_income": 35000,
                "education_level": "moderate",
                "main_sectors": ["agriculture", "manufacturing", "services"],
                "infrastructure_quality": 0.4
            },
            "suburban": {
                "population": 150000,
                "avg_income": 50000,
                "education_level": "moderate",
                "main_sectors": ["services", "manufacturing", "technology"],
                "infrastructure_quality": 0.6
            }
        }
    }

@app.get("/api/simulation/demographics")
async def get_demographic_options():
    """Get available demographic options for simulation"""
    return {
        "age_groups": ["18-25", "26-35", "36-50", "51-65", "65+"],
        "income_levels": ["low", "middle", "high"],
        "regions": ["urban", "rural", "suburban"],
        "employment_sectors": ["agriculture", "manufacturing", "services", "technology"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
