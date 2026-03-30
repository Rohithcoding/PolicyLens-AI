import random
import json
from typing import Dict, List, Optional, Any
from models.policy import SyntheticPopulation, PolicyAnalysis, PolicySector
from utils.logger import logger
import numpy as np

class SimulationAgent:
    def __init__(self):
        self.base_population_data = self._load_base_population_data()
    
    def _load_base_population_data(self) -> Dict[str, Any]:
        """Load base population data for simulation"""
        return {
            "total_population": 1000000,
            "age_distribution": {
                "18-25": 0.20,
                "26-35": 0.25,
                "36-50": 0.25,
                "51-65": 0.20,
                "65+": 0.10
            },
            "income_levels": {
                "low": 0.40,      # Below $25,000
                "middle": 0.45,   # $25,000 - $75,000
                "high": 0.15      # Above $75,000
            },
            "urban_rural_split": 0.35,  # 35% urban
            "employment_sectors": {
                "agriculture": 0.25,
                "manufacturing": 0.20,
                "services": 0.35,
                "technology": 0.10,
                "government": 0.10
            },
            "education_levels": {
                "primary": 0.30,
                "secondary": 0.40,
                "graduate": 0.25,
                "postgraduate": 0.05
            }
        }
    
    async def create_population(self, policy_analysis: PolicyAnalysis, target_demographic: Optional[str] = None) -> SyntheticPopulation:
        """
        Create synthetic population based on policy analysis
        """
        try:
            base_data = self.base_population_data.copy()
            
            # Adjust population based on policy sector
            if policy_analysis.sector == PolicySector.AGRICULTURE:
                base_data["employment_sectors"]["agriculture"] = 0.35
                base_data["urban_rural_split"] = 0.25
            elif policy_analysis.sector == PolicySector.TECHNOLOGY:
                base_data["employment_sectors"]["technology"] = 0.20
                base_data["urban_rural_split"] = 0.45
            elif policy_analysis.sector == PolicySector.SOCIAL_WELFARE:
                base_data["income_levels"]["low"] = 0.50
            
            # Create demographic breakdown
            demographics = self._create_demographics(base_data)
            income_distribution = self._create_income_distribution(base_data)
            employment_data = self._create_employment_data(base_data)
            regional_data = self._create_regional_data(base_data)
            
            population = SyntheticPopulation(
                total_population=base_data["total_population"],
                demographics=demographics,
                income_distribution=income_distribution,
                employment_data=employment_data,
                regional_data=regional_data
            )
            
            logger.info(f"Created synthetic population: {population.total_population:,} people")
            return population
            
        except Exception as e:
            logger.error(f"Error creating population: {str(e)}")
            raise
    
    async def create_default_population(self) -> SyntheticPopulation:
        """Create default synthetic population"""
        return await self.create_population(
            PolicyAnalysis(
                sector=PolicySector.ECONOMY,
                key_changes=["Default policy"],
                stakeholders=[],
                confidence_score=0.8
            )
        )
    
    async def create_custom_population(
        self, 
        total_population: int = 1000000,
        urban_ratio: float = 0.35,
        median_income: float = 50000
    ) -> SyntheticPopulation:
        """Create custom population with specified parameters"""
        base_data = self.base_population_data.copy()
        base_data["total_population"] = total_population
        base_data["urban_rural_split"] = urban_ratio
        
        # Adjust income distribution based on median income
        if median_income < 30000:
            base_data["income_levels"]["low"] = 0.60
            base_data["income_levels"]["middle"] = 0.35
            base_data["income_levels"]["high"] = 0.05
        elif median_income > 75000:
            base_data["income_levels"]["low"] = 0.20
            base_data["income_levels"]["middle"] = 0.50
            base_data["income_levels"]["high"] = 0.30
        
        demographics = self._create_demographics(base_data)
        income_distribution = self._create_income_distribution(base_data)
        employment_data = self._create_employment_data(base_data)
        regional_data = self._create_regional_data(base_data)
        
        return SyntheticPopulation(
            total_population=total_population,
            demographics=demographics,
            income_distribution=income_distribution,
            employment_data=employment_data,
            regional_data=regional_data
        )
    
    def _create_demographics(self, base_data: Dict[str, Any]) -> Dict[str, int]:
        """Create demographic breakdown"""
        total = base_data["total_population"]
        demographics = {}
        
        for age_group, percentage in base_data["age_distribution"].items():
            demographics[age_group] = int(total * percentage)
        
        return demographics
    
    def _create_income_distribution(self, base_data: Dict[str, Any]) -> Dict[str, int]:
        """Create income distribution"""
        total = base_data["total_population"]
        income_distribution = {}
        
        for level, percentage in base_data["income_levels"].items():
            income_distribution[level] = int(total * percentage)
        
        return income_distribution
    
    def _create_employment_data(self, base_data: Dict[str, Any]) -> Dict[str, float]:
        """Create employment data"""
        total_population = base_data["total_population"]
        employment_data = {}
        
        # Calculate employment rates by sector
        for sector, percentage in base_data["employment_sectors"].items():
            employed_people = int(total_population * percentage * 0.65)  # 65% employment rate
            employment_data[sector] = employed_people
        
        # Add overall employment rate
        employment_data["overall_employment_rate"] = 0.65
        employment_data["unemployment_rate"] = 0.35
        
        return employment_data
    
    def _create_regional_data(self, base_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Create regional data"""
        total_population = base_data["total_population"]
        urban_population = int(total_population * base_data["urban_rural_split"])
        rural_population = total_population - urban_population
        
        regional_data = {
            "urban": {
                "population": urban_population,
                "avg_income": 65000,
                "education_level": "higher",
                "main_sectors": ["technology", "services", "manufacturing"],
                "infrastructure_quality": 0.8
            },
            "rural": {
                "population": rural_population,
                "avg_income": 35000,
                "education_level": "moderate",
                "main_sectors": ["agriculture", "manufacturing", "services"],
                "infrastructure_quality": 0.4
            },
            "suburban": {
                "population": int(total_population * 0.15),
                "avg_income": 50000,
                "education_level": "moderate",
                "main_sectors": ["services", "manufacturing", "technology"],
                "infrastructure_quality": 0.6
            }
        }
        
        return regional_data
    
    def generate_individual_profiles(self, count: int = 1000) -> List[Dict[str, Any]]:
        """
        Generate individual profiles for detailed simulation
        """
        profiles = []
        
        for _ in range(count):
            profile = {
                "age": random.randint(18, 80),
                "income": random.randint(15000, 150000),
                "education": random.choice(["primary", "secondary", "graduate", "postgraduate"]),
                "employment_sector": random.choice(["agriculture", "manufacturing", "services", "technology", "government", "unemployed"]),
                "location": random.choice(["urban", "rural", "suburban"]),
                "family_size": random.randint(1, 6),
                "has_dependents": random.choice([True, False]),
                "health_status": random.choice(["excellent", "good", "fair", "poor"]),
                "property_owner": random.choice([True, False])
            }
            profiles.append(profile)
        
        return profiles
    
    def calculate_vulnerability_index(self, population: SyntheticPopulation) -> Dict[str, float]:
        """
        Calculate vulnerability index for different demographic groups
        """
        vulnerability = {}
        
        # Income vulnerability
        low_income_ratio = population.income_distribution.get("low", 0) / population.total_population
        vulnerability["income_vulnerability"] = min(low_income_ratio * 2, 1.0)
        
        # Age vulnerability (elderly and young)
        elderly = population.demographics.get("65+", 0)
        youth = population.demographics.get("18-25", 0)
        age_vulnerability = (elderly + youth) / population.total_population
        vulnerability["age_vulnerability"] = min(age_vulnerability * 1.5, 1.0)
        
        # Regional vulnerability (rural areas)
        rural_pop = population.regional_data.get("rural", {}).get("population", 0)
        regional_vulnerability = rural_pop / population.total_population
        vulnerability["regional_vulnerability"] = min(regional_vulnerability * 1.2, 1.0)
        
        # Overall vulnerability
        vulnerability["overall"] = sum(vulnerability.values()) / len(vulnerability)
        
        return vulnerability
    
    def simulate_policy_impact_on_population(
        self, 
        population: SyntheticPopulation, 
        policy_changes: List[str]
    ) -> Dict[str, Any]:
        """
        Simulate how policy changes affect the population
        """
        impact_summary = {
            "directly_affected": 0,
            "indirectly_affected": 0,
            "beneficiaries": 0,
            "adversely_affected": 0,
            "impact_distribution": {}
        }
        
        # Simple heuristic-based impact calculation
        for change in policy_changes:
            if "tax" in change.lower():
                # Tax changes affect income distribution
                affected_ratio = 0.8
                impact_summary["directly_affected"] += int(population.total_population * affected_ratio)
            elif "subsidy" in change.lower() or "benefit" in change.lower():
                # Benefits affect lower income groups more
                affected_ratio = 0.4
                impact_summary["beneficiaries"] += int(population.total_population * affected_ratio)
            elif "education" in change.lower():
                # Education policies affect young population
                young_pop = population.demographics.get("18-25", 0) + population.demographics.get("26-35", 0)
                impact_summary["directly_affected"] += young_pop
            elif "health" in change.lower():
                # Health policies affect elderly and children
                elderly_pop = population.demographics.get("65+", 0)
                impact_summary["directly_affected"] += elderly_pop
        
        # Calculate indirect effects (usually 2-3x direct effects)
        impact_summary["indirectly_affected"] = impact_summary["directly_affected"] * 2
        
        # Create impact distribution by region
        for region, data in population.regional_data.items():
            region_impact = data["population"] * 0.6  # Assume 60% affected in each region
            impact_summary["impact_distribution"][region] = int(region_impact)
        
        return impact_summary
