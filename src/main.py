import logging
from fastapi import FastAPI, HTTPException
from src.models import PowerPlant, ProductionPlanRequest, PowerPlantOutput
from typing import List

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/productionplan")
def production_plan(request: ProductionPlanRequest) -> List[PowerPlantOutput]:
    """
    Unit-commitment solver. 
    """
    
    load = request.load
    fuels = request.fuels
    powerplants = request.powerplants

    # 1. Sort the power plants by cost-effectiveness, the cheapest going first
    def plant_cost_effectiveness(plant: PowerPlant) -> float:
        if plant.type == "windturbine":
            return 0
        elif plant.type == "gasfired":
            return fuels.gas_euro_mwh / plant.efficiency + 0.3 * fuels.co2_euro_ton
        elif plant.type == "turbojet":
            return fuels.kerosine_euro_mwh / plant.efficiency
        else:
            return float("NaN")
        
    sorted_powerplants = sorted(powerplants, key=plant_cost_effectiveness)

    # 2. Start allocating the load to each powerplant
    allocation = {plant.name: 0 for plant in sorted_powerplants}

    remaining_load = load
    for plant in sorted_powerplants:
        if remaining_load <= 0:
            break

        if plant.type == "windturbine":
            min_power = (plant.pmin * fuels.wind_percentage) / 100
            max_power = (plant.pmax * fuels.wind_percentage) / 100
        else:
            min_power = plant.pmin
            max_power = plant.pmax

        if remaining_load < min_power: # The plant is too powerful to produce the remaining load
            continue 
        elif remaining_load <= max_power: # The plant can fully meet the remaining load within its capacity range
            allocation[plant.name] = remaining_load
            remaining_load = 0
            break
        else: # The plant is not powerful enough to produce all of the remanining load
            allocation[plant.name] = max_power
            remaining_load -= max_power

    # 3. Make some checks on the load
    if remaining_load > 0:
        logger.error("Cannot meet the required load with the available power plants")
        raise HTTPException(status_code=400, detail="Cannot meet the required load with the available power plants")
    
    total_allocated_power = sum(allocation.values())
    if total_allocated_power != load:
        logger.error("Total allocated power does not match the required load")
        raise HTTPException(status_code=500, detail="The total allocated power does not match the required load")

    output = [{"name": name, "p": round(p, 1)} for name, p in allocation.items()]
    logger.info("Production plan calculated successfully")

    return output
