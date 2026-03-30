from fastapi import APIRouter, HTTPException
from models.policy import SyntheticPopulation, SimulationResult
from agents.simulation_agent import SimulationAgent
from utils.logger import logger

router = APIRouter()
simulation_agent = SimulationAgent()

@router.get("/population/default", response_model=SyntheticPopulation)
async def get_default_population():
    """
    Get default synthetic population data
    """
    try:
        population = await simulation_agent.create_default_population()
        return population
    except Exception as e:
        logger.error(f"Error creating default population: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create default population")

@router.post("/population/custom", response_model=SyntheticPopulation)
async def create_custom_population(
    total_population: int = 1000000,
    urban_ratio: float = 0.35,
    median_income: float = 50000
):
    """
    Create custom synthetic population with specified parameters
    """
    try:
        population = await simulation_agent.create_custom_population(
            total_population, urban_ratio, median_income
        )
        return population
    except Exception as e:
        logger.error(f"Error creating custom population: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create custom population")

@router.get("/demographics")
async def get_demographic_options():
    """
    Get available demographic options for simulation
    """
    return {
        "age_groups": ["18-25", "26-35", "36-50", "51-65", "65+"],
        "income_levels": ["low", "middle", "high"],
        "regions": ["urban", "rural", "suburban"],
        "employment_sectors": ["agriculture", "manufacturing", "services", "technology"]
    }
