import random
import math
from typing import Dict, List, Tuple, Optional, Any
from models.policy import (
    PolicyAnalysis, SyntheticPopulation, EconomicImpact, 
    SocialImpact, PolicySector
)
from utils.logger import logger

class ImpactPredictionAgent:
    def __init__(self):
        self.impact_weights = self._initialize_impact_weights()
        self.sector_multipliers = self._initialize_sector_multipliers()
    
    def _initialize_impact_weights(self) -> Dict[str, Dict[str, float]]:
        """Initialize impact weights for different policy types"""
        return {
            "tax": {
                "gdp_change": -0.1,
                "inflation_impact": 0.05,
                "employment_change": -0.02,
                "poverty_reduction": 0.1,
                "social_inequality": -0.15
            },
            "subsidy": {
                "gdp_change": 0.08,
                "inflation_impact": 0.03,
                "employment_change": 0.05,
                "poverty_reduction": 0.2,
                "social_inequality": 0.1
            },
            "infrastructure": {
                "gdp_change": 0.12,
                "inflation_impact": 0.02,
                "employment_change": 0.08,
                "poverty_reduction": 0.05,
                "social_inequality": 0.05
            },
            "education": {
                "gdp_change": 0.06,
                "inflation_impact": 0.01,
                "employment_change": 0.03,
                "poverty_reduction": 0.15,
                "social_inequality": 0.2
            },
            "healthcare": {
                "gdp_change": 0.04,
                "inflation_impact": 0.02,
                "employment_change": 0.04,
                "poverty_reduction": 0.12,
                "social_inequality": 0.15
            },
            "environment": {
                "gdp_change": -0.02,
                "inflation_impact": 0.04,
                "employment_change": -0.01,
                "poverty_reduction": 0.08,
                "social_inequality": 0.1
            }
        }
    
    def _initialize_sector_multipliers(self) -> Dict[PolicySector, Dict[str, float]]:
        """Initialize sector-specific impact multipliers"""
        return {
            PolicySector.AGRICULTURE: {
                "gdp_multiplier": 1.2,
                "employment_multiplier": 1.5,
                "poverty_multiplier": 1.3
            },
            PolicySector.TAXATION: {
                "gdp_multiplier": 1.1,
                "employment_multiplier": 0.8,
                "poverty_multiplier": 1.2
            },
            PolicySector.HEALTHCARE: {
                "gdp_multiplier": 0.9,
                "employment_multiplier": 1.1,
                "poverty_multiplier": 1.1
            },
            PolicySector.EDUCATION: {
                "gdp_multiplier": 1.0,
                "employment_multiplier": 1.0,
                "poverty_multiplier": 1.4
            },
            PolicySector.INFRASTRUCTURE: {
                "gdp_multiplier": 1.3,
                "employment_multiplier": 1.4,
                "poverty_multiplier": 0.9
            },
            PolicySector.ENVIRONMENT: {
                "gdp_multiplier": 0.8,
                "employment_multiplier": 0.9,
                "poverty_multiplier": 1.0
            },
            PolicySector.SOCIAL_WELFARE: {
                "gdp_multiplier": 0.9,
                "employment_multiplier": 1.0,
                "poverty_multiplier": 1.6
            },
            PolicySector.ECONOMY: {
                "gdp_multiplier": 1.1,
                "employment_multiplier": 1.0,
                "poverty_multiplier": 1.0
            }
        }
    
    async def predict_impacts(
        self, 
        policy_analysis: PolicyAnalysis, 
        population: SyntheticPopulation,
        adjustments: Optional[Dict[str, float]] = None
    ) -> Tuple[EconomicImpact, SocialImpact]:
        """
        Predict economic and social impacts of a policy
        """
        try:
            # Determine policy type from key changes
            policy_type = self._determine_policy_type(policy_analysis.key_changes)
            
            # Get base impact weights
            base_weights = self.impact_weights.get(policy_type, self.impact_weights["infrastructure"])
            
            # Get sector multipliers
            sector_multipliers = self.sector_multipliers.get(policy_analysis.sector, self.sector_multipliers[PolicySector.ECONOMY])
            
            # Calculate economic impacts
            economic_impact = self._calculate_economic_impact(
                base_weights, sector_multipliers, policy_analysis, population, adjustments
            )
            
            # Calculate social impacts
            social_impact = self._calculate_social_impact(
                base_weights, sector_multipliers, policy_analysis, population, adjustments
            )
            
            logger.info(f"Impact prediction completed for {policy_analysis.sector} policy")
            return economic_impact, social_impact
            
        except Exception as e:
            logger.error(f"Error in impact prediction: {str(e)}")
            # Return default impacts
            return self._get_default_impacts()
    
    def _determine_policy_type(self, key_changes: List[str]) -> str:
        """Determine policy type from key changes"""
        changes_text = " ".join(key_changes).lower()
        
        if "tax" in changes_text:
            return "tax"
        elif "subsidy" in changes_text or "benefit" in changes_text:
            return "subsidy"
        elif "infrastructur" in changes_text or "road" in changes_text or "bridge" in changes_text:
            return "infrastructure"
        elif "education" in changes_text or "school" in changes_text:
            return "education"
        elif "health" in changes_text or "medical" in changes_text:
            return "healthcare"
        elif "environment" in changes_text or "climate" in changes_text or "pollution" in changes_text:
            return "environment"
        else:
            return "infrastructure"  # Default
    
    def _calculate_economic_impact(
        self, 
        base_weights: Dict[str, float], 
        sector_multipliers: Dict[str, float],
        policy_analysis: PolicyAnalysis,
        population: SyntheticPopulation,
        adjustments: Optional[Dict[str, float]] = None
    ) -> EconomicImpact:
        """Calculate economic impacts"""
        
        # Base impacts with randomness for realism
        gdp_change = base_weights["gdp_change"] * sector_multipliers["gdp_multiplier"]
        inflation_impact = base_weights["inflation_impact"]
        employment_change = base_weights["employment_change"] * sector_multipliers["employment_multiplier"]
        
        # Add some randomness
        gdp_change += random.uniform(-0.02, 0.02)
        inflation_impact += random.uniform(-0.01, 0.01)
        employment_change += random.uniform(-0.01, 0.01)
        
        # Budget impact
        budget_impact = policy_analysis.budget_impact or random.uniform(-500, 500)
        
        # Apply adjustments if provided
        if adjustments:
            if "budget_increase" in adjustments:
                budget_impact *= (1 + adjustments["budget_increase"])
                gdp_change *= (1 + adjustments["budget_increase"] * 0.5)
            if "tax_rate" in adjustments:
                gdp_change *= (1 - adjustments["tax_rate"] * 0.3)
                inflation_impact *= (1 + adjustments["tax_rate"] * 0.2)
        
        # Sector-specific impacts
        sector_impacts = self._calculate_sector_impacts(policy_analysis.sector, base_weights)
        
        return EconomicImpact(
            gdp_change=round(gdp_change, 3),
            inflation_impact=round(inflation_impact, 3),
            employment_change=round(employment_change, 3),
            budget_impact=round(budget_impact, 2),
            sector_impacts=sector_impacts
        )
    
    def _calculate_social_impact(
        self, 
        base_weights: Dict[str, float], 
        sector_multipliers: Dict[str, float],
        policy_analysis: PolicyAnalysis,
        population: SyntheticPopulation,
        adjustments: Optional[Dict[str, float]] = None
    ) -> SocialImpact:
        """Calculate social impacts"""
        
        # Base impacts
        poverty_reduction = base_weights["poverty_reduction"] * sector_multipliers["poverty_multiplier"]
        social_inequality = base_weights["social_inequality"]
        
        # Education and healthcare impacts (general positive trends)
        education_improvement = random.uniform(0.02, 0.08)
        healthcare_access = random.uniform(0.03, 0.10)
        
        # Adjust based on policy sector
        if policy_analysis.sector == PolicySector.EDUCATION:
            education_improvement += 0.10
        elif policy_analysis.sector == PolicySector.HEALTHCARE:
            healthcare_access += 0.12
        elif policy_analysis.sector == PolicySector.SOCIAL_WELFARE:
            poverty_reduction += 0.08
            healthcare_access += 0.05
        
        # Add randomness
        poverty_reduction += random.uniform(-0.02, 0.02)
        social_inequality += random.uniform(-0.02, 0.02)
        education_improvement += random.uniform(-0.01, 0.01)
        healthcare_access += random.uniform(-0.01, 0.01)
        
        # Apply adjustments
        if adjustments:
            if "subsidy_increase" in adjustments:
                poverty_reduction *= (1 + adjustments["subsidy_increase"])
                social_inequality *= (1 + adjustments["subsidy_increase"] * 0.5)
        
        return SocialImpact(
            poverty_reduction=round(max(0, poverty_reduction), 3),
            education_improvement=round(max(0, education_improvement), 3),
            healthcare_access=round(max(0, healthcare_access), 3),
            social_inequality=round(social_inequality, 3)
        )
    
    def _calculate_sector_impacts(self, sector: PolicySector, base_weights: Dict[str, float]) -> Dict[str, float]:
        """Calculate sector-specific economic impacts"""
        sector_impacts = {}
        
        # Base sector impacts
        sectors = ["agriculture", "manufacturing", "services", "technology", "retail"]
        
        for sec in sectors:
            impact = random.uniform(-0.05, 0.15)
            
            # Adjust based on policy sector
            if sector == PolicySector.AGRICULTURE and sec == "agriculture":
                impact += 0.10
            elif sector == PolicySector.INFRASTRUCTURE and sec in ["manufacturing", "services"]:
                impact += 0.08
            elif sector == PolicySector.TECHNOLOGY and sec == "technology":
                impact += 0.12
            elif sector == PolicySector.TAXATION:
                impact *= 0.8  # Taxes generally reduce sector growth
            
            sector_impacts[sec] = round(impact, 3)
        
        return sector_impacts
    
    def _get_default_impacts(self) -> Tuple[EconomicImpact, SocialImpact]:
        """Get default impact values for fallback"""
        economic_impact = EconomicImpact(
            gdp_change=0.05,
            inflation_impact=0.02,
            employment_change=0.03,
            budget_impact=100.0,
            sector_impacts={
                "agriculture": 0.05,
                "manufacturing": 0.06,
                "services": 0.07,
                "technology": 0.08,
                "retail": 0.04
            }
        )
        
        social_impact = SocialImpact(
            poverty_reduction=0.1,
            education_improvement=0.05,
            healthcare_access=0.06,
            social_inequality=-0.08
        )
        
        return economic_impact, social_impact
    
    async def assess_risks(self, policy_analysis: PolicyAnalysis) -> Dict[str, str]:
        """Assess risks associated with the policy"""
        risks = {}
        
        # Budget risk
        if policy_analysis.budget_impact and abs(policy_analysis.budget_impact) > 300:
            risks["budget"] = "High budget impact may strain fiscal resources"
        else:
            risks["budget"] = "Moderate budget impact within acceptable limits"
        
        # Implementation risk
        if "complex" in policy_analysis.implementation_timeframe.lower() or "phased" in policy_analysis.implementation_timeframe.lower():
            risks["implementation"] = "Complex implementation may face delays"
        else:
            risks["implementation"] = "Straightforward implementation expected"
        
        # Political risk
        high_risk_stakeholders = ["businesses", "government"]
        if any(stakeholder in high_risk_stakeholders for stakeholder in policy_analysis.stakeholders):
            risks["political"] = "May face political opposition from affected groups"
        else:
            risks["political"] = "Likely to receive broad political support"
        
        # Economic risk
        if policy_analysis.sector in [PolicySector.TAXATION, PolicySector.ENVIRONMENT]:
            risks["economic"] = "Potential short-term economic disruption"
        else:
            risks["economic"] = "Minimal economic disruption expected"
        
        # Social risk
        if policy_analysis.sector == PolicySector.SOCIAL_WELFARE:
            risks["social"] = "Social acceptance depends on benefit distribution"
        else:
            risks["social"] = "Broad social acceptance likely"
        
        return risks
    
    async def generate_recommendations(self, policy_analysis: PolicyAnalysis) -> List[str]:
        """Generate policy recommendations"""
        recommendations = []
        
        # General recommendations
        recommendations.append("Monitor implementation progress quarterly")
        recommendations.append("Establish clear metrics for success measurement")
        
        # Sector-specific recommendations
        if policy_analysis.sector == PolicySector.AGRICULTURE:
            recommendations.append("Provide training programs for farmers on new practices")
            recommendations.append("Ensure supply chain infrastructure is developed")
        elif policy_analysis.sector == PolicySector.EDUCATION:
            recommendations.append("Invest in teacher training and curriculum development")
            recommendations.append("Monitor educational outcomes across demographic groups")
        elif policy_analysis.sector == PolicySector.HEALTHCARE:
            recommendations.append("Strengthen healthcare infrastructure in rural areas")
            recommendations.append("Ensure affordable access to healthcare services")
        elif policy_analysis.sector == PolicySector.INFRASTRUCTURE:
            recommendations.append("Prioritize projects with highest economic impact")
            recommendations.append("Ensure environmental impact assessments are conducted")
        elif policy_analysis.sector == PolicySector.TAXATION:
            recommendations.append("Simplify tax compliance procedures")
            recommendations.append("Provide transition support for affected businesses")
        
        # Budget-related recommendations
        if policy_analysis.budget_impact and policy_analysis.budget_impact > 200:
            recommendations.append("Consider phased implementation to manage budget impact")
            recommendations.append("Explore public-private partnership opportunities")
        
        # Stakeholder-specific recommendations
        if StakeholderType.FARMERS in policy_analysis.stakeholders:
            recommendations.append("Engage farmer associations in policy design")
        if StakeholderType.BUSINESSES in policy_analysis.stakeholders:
            recommendations.append("Provide clear guidelines for business compliance")
        
        return recommendations[:6]  # Limit to 6 recommendations
