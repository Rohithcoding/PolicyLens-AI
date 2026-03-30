from textblob import TextBlob
import re
import random
from typing import List, Dict, Tuple
from models.policy import SentimentResult
from utils.logger import logger

class SentimentAgent:
    def __init__(self):
        self.positive_words = [
            "good", "great", "excellent", "beneficial", "positive", "helpful",
            "effective", "successful", "improve", "advantage", "progress",
            "growth", "opportunity", "support", "favorable", "promising"
        ]
        
        self.negative_words = [
            "bad", "poor", "negative", "harmful", "damage", "problem",
            "difficult", "challenge", "oppose", "against", "concern",
            "risk", "threat", "burden", "unfair", "inadequate"
        ]
        
        self.concern_keywords = [
            "cost", "expense", "budget", "implementation", "delay",
            "complex", "difficult", "opposition", "protest", "resistance",
            "corruption", "mismanagement", "inefficiency", "bureaucracy"
        ]
    
    async def analyze_sentiment(self, policy_text: str) -> SentimentResult:
        """
        Analyze sentiment of policy text
        """
        try:
            # Clean and preprocess text
            cleaned_text = self._clean_text(policy_text)
            
            # Calculate sentiment using TextBlob
            blob = TextBlob(cleaned_text)
            sentiment_score = blob.sentiment.polarity
            
            # Determine overall sentiment
            overall_sentiment = self._determine_sentiment(sentiment_score)
            
            # Extract key concerns
            key_concerns = self._extract_concerns(cleaned_text)
            
            # Calculate public support percentage
            public_support = self._calculate_public_support(sentiment_score, key_concerns)
            
            result = SentimentResult(
                overall_sentiment=overall_sentiment,
                sentiment_score=round(sentiment_score, 3),
                key_concerns=key_concerns,
                public_support_percentage=round(public_support, 1)
            )
            
            logger.info(f"Sentiment analysis completed: {overall_sentiment} ({sentiment_score:.3f})")
            return result
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            # Return default sentiment
            return self._get_default_sentiment()
    
    def _clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text.lower()
    
    def _determine_sentiment(self, score: float) -> str:
        """Determine sentiment category from score"""
        if score > 0.1:
            return "Positive"
        elif score < -0.1:
            return "Negative"
        else:
            return "Neutral"
    
    def _extract_concerns(self, text: str) -> List[str]:
        """Extract key concerns from text"""
        concerns = []
        
        # Look for concern keywords
        for keyword in self.concern_keywords:
            if keyword in text:
                # Create a concern phrase based on context
                concern = f"Potential {keyword} issues"
                if concern not in concerns:
                    concerns.append(concern)
        
        # Add some common policy concerns based on text analysis
        if "budget" in text or "cost" in text:
            concerns.append("Budget constraints and cost management")
        
        if "implement" in text:
            concerns.append("Implementation challenges and timeline")
        
        if "tax" in text:
            concerns.append("Tax burden on affected groups")
        
        if "regulation" in text:
            concerns.append("Compliance and regulatory burden")
        
        # Limit concerns to top 5
        return concerns[:5] if concerns else ["Implementation complexity", "Stakeholder acceptance"]
    
    def _calculate_public_support(self, sentiment_score: float, concerns: List[str]) -> float:
        """
        Calculate public support percentage based on sentiment and concerns
        """
        # Base support from sentiment score
        base_support = (sentiment_score + 1) * 50  # Convert -1 to 1 range to 0-100
        
        # Adjust based on number of concerns
        concern_penalty = len(concerns) * 5  # Each concern reduces support by 5%
        
        # Add some randomness for realism
        random_factor = random.uniform(-5, 5)
        
        support_percentage = base_support - concern_penalty + random_factor
        support_percentage = max(10, min(90, support_percentage))  # Clamp between 10-90
        
        return support_percentage
    
    def _get_default_sentiment(self) -> SentimentResult:
        """Get default sentiment for fallback"""
        return SentimentResult(
            overall_sentiment="Neutral",
            sentiment_score=0.0,
            key_concerns=["Implementation complexity", "Stakeholder acceptance"],
            public_support_percentage=50.0
        )
    
    async def analyze_stakeholder_sentiment(self, policy_text: str, stakeholder_groups: List[str]) -> Dict[str, SentimentResult]:
        """
        Analyze sentiment for specific stakeholder groups
        """
        stakeholder_sentiments = {}
        
        # Different sentiment tendencies for different groups
        stakeholder_biases = {
            "farmers": {"bias": -0.1, "concerns": ["Market prices", "Input costs", "Weather risks"]},
            "workers": {"bias": 0.0, "concerns": ["Job security", "Wage levels", "Working conditions"]},
            "businesses": {"bias": -0.2, "concerns": ["Regulatory burden", "Tax impact", "Compliance costs"]},
            "government": {"bias": 0.1, "concerns": ["Implementation capacity", "Budget impact", "Political feasibility"]},
            "consumers": {"bias": 0.05, "concerns": ["Price impact", "Service quality", "Accessibility"]},
            "students": {"bias": 0.15, "concerns": ["Educational quality", "Future prospects", "Affordability"]},
            "elderly": {"bias": 0.1, "concerns": ["Healthcare access", "Social security", "Cost of living"]},
            "youth": {"bias": 0.0, "concerns": ["Employment opportunities", "Education access", "Future outlook"]}
        }
        
        # Get base sentiment
        base_sentiment = await self.analyze_sentiment(policy_text)
        
        for stakeholder in stakeholder_groups:
            bias_info = stakeholder_biases.get(stakeholder.lower(), {"bias": 0.0, "concerns": ["General concerns"]})
            
            # Adjust sentiment based on stakeholder bias
            adjusted_score = base_sentiment.sentiment_score + bias_info["bias"]
            adjusted_score = max(-1, min(1, adjusted_score))  # Clamp to valid range
            
            # Determine adjusted sentiment
            adjusted_sentiment = self._determine_sentiment(adjusted_score)
            
            # Calculate adjusted support
            adjusted_support = self._calculate_public_support(adjusted_score, bias_info["concerns"])
            
            stakeholder_sentiments[stakeholder] = SentimentResult(
                overall_sentiment=adjusted_sentiment,
                sentiment_score=round(adjusted_score, 3),
                key_concerns=bias_info["concerns"],
                public_support_percentage=round(adjusted_support, 1)
            )
        
        return stakeholder_sentiments
    
    def _analyze_sentiment_by_keywords(self, text: str) -> Tuple[float, Dict[str, int]]:
        """
        Analyze sentiment using keyword counting as backup method
        """
        words = text.split()
        
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return 0.0, {"positive": 0, "negative": 0}
        
        # Calculate sentiment score
        sentiment_score = (positive_count - negative_count) / len(words)
        
        word_counts = {
            "positive": positive_count,
            "negative": negative_count
        }
        
        return sentiment_score, word_counts
    
    async def predict_sentiment_change(self, current_sentiment: SentimentResult, policy_changes: List[str]) -> SentimentResult:
        """
        Predict how sentiment might change with policy modifications
        """
        # Analyze the changes
        change_text = " ".join(policy_changes).lower()
        
        # Determine if changes are positive or negative
        change_sentiment = 0.0
        
        positive_changes = ["increase", "improve", "expand", "enhance", "boost", "strengthen"]
        negative_changes = ["reduce", "cut", "decrease", "limit", "restrict", "burden"]
        
        for change in policy_changes:
            change_lower = change.lower()
            if any(pos in change_lower for pos in positive_changes):
                change_sentiment += 0.1
            elif any(neg in change_lower for neg in negative_changes):
                change_sentiment -= 0.1
        
        # Adjust current sentiment
        new_score = current_sentiment.sentiment_score + change_sentiment
        new_score = max(-1, min(1, new_score))  # Clamp to valid range
        
        # Determine new sentiment
        new_sentiment = self._determine_sentiment(new_score)
        
        # Adjust concerns
        new_concerns = current_sentiment.key_concerns.copy()
        if change_sentiment < -0.1:
            new_concerns.append("Negative public reaction to changes")
        elif change_sentiment > 0.1:
            # Remove some concerns if sentiment improves
            new_concerns = new_concerns[:-1] if len(new_concerns) > 1 else new_concerns
        
        # Calculate new support
        new_support = self._calculate_public_support(new_score, new_concerns)
        
        return SentimentResult(
            overall_sentiment=new_sentiment,
            sentiment_score=round(new_score, 3),
            key_concerns=new_concerns[:5],
            public_support_percentage=round(new_support, 1)
        )
