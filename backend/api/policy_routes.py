from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.policy import PolicyInput, SimulationResult, WhatIfScenario
from agents.policy_understanding_agent import PolicyUnderstandingAgent
from agents.simulation_agent import SimulationAgent
from agents.impact_prediction_agent import ImpactPredictionAgent
from agents.sentiment_agent import SentimentAgent
from utils.logger import logger
import asyncio

router = APIRouter()

# Initialize agents
policy_agent = PolicyUnderstandingAgent()
simulation_agent = SimulationAgent()
impact_agent = ImpactPredictionAgent()
sentiment_agent = SentimentAgent()

@router.post("/analyze", response_model=SimulationResult)
async def analyze_policy(policy_input: PolicyInput):
    """
    Analyze a policy and return comprehensive simulation results
    """
    try:
        logger.info(f"Starting policy analysis for: {policy_input.title or 'Untitled Policy'}")
        
        # Step 1: Policy Understanding
        policy_analysis = await policy_agent.analyze_policy(policy_input.text)
        
        # Step 2: Create Synthetic Population
        synthetic_population = await simulation_agent.create_population(policy_analysis)
        
        # Step 3: Impact Prediction
        economic_impact, social_impact = await impact_agent.predict_impacts(
            policy_analysis, synthetic_population
        )
        
        # Step 4: Sentiment Analysis
        sentiment_result = await sentiment_agent.analyze_sentiment(policy_input.text)
        
        # Step 5: Compile Results
        simulation_result = SimulationResult(
            policy_analysis=policy_analysis,
            economic_impact=economic_impact,
            social_impact=social_impact,
            sentiment=sentiment_result,
            risk_assessment=await impact_agent.assess_risks(policy_analysis),
            recommendations=await impact_agent.generate_recommendations(policy_analysis),
            confidence_score=min(
                policy_analysis.confidence_score,
                0.85  # Overall confidence cap
            )
        )
        
        logger.info("Policy analysis completed successfully")
        return simulation_result
        
    except Exception as e:
        logger.error(f"Error in policy analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Policy analysis failed: {str(e)}")

@router.post("/what-if", response_model=SimulationResult)
async def what_if_simulation(scenario: WhatIfScenario):
    """
    Run 'What If' simulation with policy adjustments
    """
    try:
        logger.info(f"Starting 'What If' simulation with adjustments: {scenario.adjustments}")
        
        # Step 1: Analyze base policy
        policy_analysis = await policy_agent.analyze_policy(scenario.policy_text)
        
        # Step 2: Apply adjustments to policy
        adjusted_policy = await policy_agent.apply_adjustments(
            policy_analysis, scenario.adjustments
        )
        
        # Step 3: Create targeted population if specified
        synthetic_population = await simulation_agent.create_population(
            adjusted_policy, scenario.target_demographic
        )
        
        # Step 4: Predict impacts with adjustments
        economic_impact, social_impact = await impact_agent.predict_impacts(
            adjusted_policy, synthetic_population, scenario.adjustments
        )
        
        # Step 5: Sentiment analysis
        sentiment_result = await sentiment_agent.analyze_sentiment(scenario.policy_text)
        
        # Step 6: Compile results
        simulation_result = SimulationResult(
            policy_analysis=adjusted_policy,
            economic_impact=economic_impact,
            social_impact=social_impact,
            sentiment=sentiment_result,
            risk_assessment=await impact_agent.assess_risks(adjusted_policy),
            recommendations=await impact_agent.generate_recommendations(adjusted_policy),
            confidence_score=min(
                adjusted_policy.confidence_score,
                0.80  # Slightly lower confidence for what-if scenarios
            )
        )
        
        logger.info("'What If' simulation completed successfully")
        return simulation_result
        
    except Exception as e:
        logger.error(f"Error in 'What If' simulation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"'What If' simulation failed: {str(e)}")

@router.get("/sectors")
async def get_policy_sectors():
    """
    Get list of available policy sectors
    """
    from models.policy import PolicySector
    return {"sectors": [sector.value for sector in PolicySector]}

@router.get("/health")
async def health_check():
    """
    Health check for policy analysis endpoints
    """
    return {"status": "healthy", "service": "policy-analysis"}
