import openai
import anthropic
from typing import Dict, List, Optional
from models.policy import PolicyAnalysis, PolicySector, StakeholderType
from utils.config import settings
from utils.logger import logger
import json
import re

class PolicyUnderstandingAgent:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        # Initialize available AI clients
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            self.openai_client = openai
            
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def analyze_policy(self, policy_text: str) -> PolicyAnalysis:
        """
        Analyze policy text to extract key information
        """
        try:
            # Use rule-based analysis as fallback
            if not self.openai_client and not self.anthropic_client:
                return await self._rule_based_analysis(policy_text)
            
            # Try OpenAI first, then Anthropic
            if self.openai_client:
                return await self._openai_analysis(policy_text)
            elif self.anthropic_client:
                return await self._anthropic_analysis(policy_text)
            else:
                return await self._rule_based_analysis(policy_text)
                
        except Exception as e:
            logger.error(f"Error in policy analysis: {str(e)}")
            # Fallback to rule-based analysis
            return await self._rule_based_analysis(policy_text)
    
    async def _openai_analysis(self, policy_text: str) -> PolicyAnalysis:
        """Analyze policy using OpenAI"""
        prompt = f"""
        Analyze the following government policy and extract key information:
        
        Policy Text: {policy_text}
        
        Please provide a JSON response with:
        1. sector: The main policy sector (agriculture, taxation, healthcare, education, infrastructure, environment, social_welfare, economy)
        2. key_changes: List of 3-5 main changes this policy introduces
        3. stakeholders: List of affected stakeholder groups (farmers, workers, businesses, government, consumers, students, elderly, youth)
        4. budget_impact: Estimated budget impact in millions (number)
        5. implementation_timeframe: Estimated implementation timeframe
        6. confidence_score: Confidence in analysis (0-1)
        
        Response format:
        {{
            "sector": "sector_name",
            "key_changes": ["change1", "change2", "change3"],
            "stakeholders": ["stakeholder1", "stakeholder2"],
            "budget_impact": 0.0,
            "implementation_timeframe": "timeframe",
            "confidence_score": 0.8
        }}
        """
        
        response = await self.openai_client.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        return self._convert_to_policy_analysis(result)
    
    async def _anthropic_analysis(self, policy_text: str) -> PolicyAnalysis:
        """Analyze policy using Anthropic Claude"""
        prompt = f"""
        Analyze the following government policy and extract key information:
        
        Policy Text: {policy_text}
        
        Please provide a JSON response with:
        1. sector: The main policy sector (agriculture, taxation, healthcare, education, infrastructure, environment, social_welfare, economy)
        2. key_changes: List of 3-5 main changes this policy introduces
        3. stakeholders: List of affected stakeholder groups (farmers, workers, businesses, government, consumers, students, elderly, youth)
        4. budget_impact: Estimated budget impact in millions (number)
        5. implementation_timeframe: Estimated implementation timeframe
        6. confidence_score: Confidence in analysis (0-1)
        
        Response format:
        {{
            "sector": "sector_name",
            "key_changes": ["change1", "change2", "change3"],
            "stakeholders": ["stakeholder1", "stakeholder2"],
            "budget_impact": 0.0,
            "implementation_timeframe": "timeframe",
            "confidence_score": 0.8
        }}
        """
        
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = json.loads(response.content[0].text)
        return self._convert_to_policy_analysis(result)
    
    async def _rule_based_analysis(self, policy_text: str) -> PolicyAnalysis:
        """
        Rule-based policy analysis as fallback
        """
        text_lower = policy_text.lower()
        
        # Sector detection
        sector = self._detect_sector(text_lower)
        
        # Key changes extraction
        key_changes = self._extract_key_changes(text_lower)
        
        # Stakeholder identification
        stakeholders = self._identify_stakeholders(text_lower)
        
        # Budget impact estimation
        budget_impact = self._estimate_budget_impact(text_lower)
        
        # Implementation timeframe
        timeframe = self._estimate_timeframe(text_lower)
        
        return PolicyAnalysis(
            sector=sector,
            key_changes=key_changes,
            stakeholders=stakeholders,
            budget_impact=budget_impact,
            implementation_timeframe=timeframe,
            confidence_score=0.7  # Moderate confidence for rule-based
        )
    
    def _detect_sector(self, text: str) -> PolicySector:
        """Detect policy sector from text"""
        sector_keywords = {
            PolicySector.AGRICULTURE: ["farm", "agriculture", "crop", "irrigation", "farmer", "rural"],
            PolicySector.TAXATION: ["tax", "revenue", "income tax", "gst", "taxation", "fiscal"],
            PolicySector.HEALTHCARE: ["health", "medical", "hospital", "doctor", "medicine", "healthcare"],
            PolicySector.EDUCATION: ["education", "school", "college", "student", "teacher", "university"],
            PolicySector.INFRASTRUCTURE: ["road", "bridge", "infrastructure", "transport", "highway", "railway"],
            PolicySector.ENVIRONMENT: ["environment", "climate", "pollution", "green", "sustainability", "carbon"],
            PolicySector.SOCIAL_WELFARE: ["welfare", "social", "poverty", "employment", "rural development"],
            PolicySector.ECONOMY: ["economy", "economic", "gdp", "growth", "investment", "finance"]
        }
        
        sector_scores = {}
        for sector, keywords in sector_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            sector_scores[sector] = score
        
        return max(sector_scores, key=sector_scores.get)
    
    def _extract_key_changes(self, text: str) -> List[str]:
        """Extract key changes from policy text"""
        # Look for sentences with change indicators
        change_indicators = ["will", "shall", "intends to", "aims to", "proposes", "introduces", "implements"]
        
        sentences = text.split('.')
        changes = []
        
        for sentence in sentences[:10]:  # Limit to first 10 sentences
            if any(indicator in sentence.lower() for indicator in change_indicators):
                clean_sentence = sentence.strip()
                if len(clean_sentence) > 20:  # Filter out very short sentences
                    changes.append(clean_sentence[:100] + "..." if len(clean_sentence) > 100 else clean_sentence)
        
        return changes[:5] if changes else ["Policy implementation planned", "Regulatory changes expected", "Impact on stakeholders anticipated"]
    
    def _identify_stakeholders(self, text: str) -> List[StakeholderType]:
        """Identify stakeholders from text"""
        stakeholder_keywords = {
            StakeholderType.FARMERS: ["farmer", "farm", "agriculture", "rural"],
            StakeholderType.WORKERS: ["worker", "labor", "employee", "wage"],
            StakeholderType.BUSINESSES: ["business", "company", "corporate", "industry"],
            StakeholderType.GOVERNMENT: ["government", "state", "central", "administration"],
            StakeholderType.CONSUMERS: ["consumer", "customer", "public", "citizen"],
            StakeholderType.STUDENTS: ["student", "education", "school", "college"],
            StakeholderType.ELDERLY: ["elderly", "senior", "old age", "pension"],
            StakeholderType.YOUTH: ["youth", "young", "graduate", "job"]
        }
        
        identified_stakeholders = []
        for stakeholder, keywords in stakeholder_keywords.items():
            if any(keyword in text for keyword in keywords):
                identified_stakeholders.append(stakeholder)
        
        return identified_stakeholders if identified_stakeholders else [StakeholderType.CONSUMERS, StakeholderType.GOVERNMENT]
    
    def _estimate_budget_impact(self, text: str) -> Optional[float]:
        """Estimate budget impact from text"""
        # Look for monetary values
        money_patterns = [
            r"(\d+(?:,\d+)*)\s*(?:crore|million|billion|lakh)",
            r"₹\s*(\d+(?:,\d+)*)",
            r"\$(\d+(?:,\d+)*)"
        ]
        
        for pattern in money_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Take the first match and convert to millions
                value = float(matches[0].replace(',', ''))
                if "crore" in text.lower() or "lakh" in text.lower():
                    return value * 10  # Convert to millions
                elif "billion" in text.lower():
                    return value * 1000  # Convert to millions
                else:
                    return value
        
        return None
    
    def _estimate_timeframe(self, text: str) -> str:
        """Estimate implementation timeframe"""
        time_keywords = {
            "immediate": "Immediate implementation",
            "urgent": "Immediate implementation",
            "phase": "Phased implementation",
            "gradual": "Gradual implementation",
            "year": "1-2 years",
            "month": "6-12 months",
            "week": "1-3 months"
        }
        
        for keyword, timeframe in time_keywords.items():
            if keyword in text.lower():
                return timeframe
        
        return "6-12 months"
    
    def _convert_to_policy_analysis(self, result: Dict) -> PolicyAnalysis:
        """Convert API result to PolicyAnalysis model"""
        try:
            sector = PolicySector(result.get("sector", "economy"))
            stakeholders = [StakeholderType(s) for s in result.get("stakeholders", ["consumers"])]
        except ValueError:
            sector = PolicySector.ECONOMY
            stakeholders = [StakeholderType.CONSUMERS]
        
        return PolicyAnalysis(
            sector=sector,
            key_changes=result.get("key_changes", ["Policy changes implemented"]),
            stakeholders=stakeholders,
            budget_impact=result.get("budget_impact"),
            implementation_timeframe=result.get("implementation_timeframe", "6-12 months"),
            confidence_score=float(result.get("confidence_score", 0.7))
        )
    
    async def apply_adjustments(self, policy_analysis: PolicyAnalysis, adjustments: Dict[str, float]) -> PolicyAnalysis:
        """
        Apply policy adjustments for what-if scenarios
        """
        # Create a copy of the analysis
        adjusted_analysis = PolicyAnalysis(
            sector=policy_analysis.sector,
            key_changes=policy_analysis.key_changes.copy(),
            stakeholders=policy_analysis.stakeholders.copy(),
            budget_impact=policy_analysis.budget_impact,
            implementation_timeframe=policy_analysis.implementation_timeframe,
            confidence_score=policy_analysis.confidence_score * 0.9  # Slightly lower confidence
        )
        
        # Adjust budget impact if financial adjustments are made
        if "budget_increase" in adjustments:
            if adjusted_analysis.budget_impact:
                adjusted_analysis.budget_impact *= (1 + adjustments["budget_increase"])
        
        # Add adjustment note to key changes
        adjustment_desc = []
        for key, value in adjustments.items():
            if value > 0:
                adjustment_desc.append(f"+{key}: {value*100:.1f}%")
            else:
                adjustment_desc.append(f"{key}: {value*100:.1f}%")
        
        if adjustment_desc:
            adjusted_analysis.key_changes.insert(0, f"What-if scenario: {', '.join(adjustment_desc)}")
        
        return adjusted_analysis
