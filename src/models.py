from pydantic import BaseModel, Field, conint, confloat, field_validator, ValidationInfo
from typing import List, Literal

class Fuels(BaseModel):
    gas_euro_mwh: confloat(gt=0) = Field(alias="gas(euro/MWh)")
    kerosine_euro_mwh: confloat(gt=0) = Field(alias="kerosine(euro/MWh)")
    co2_euro_ton: confloat(gt=0) = Field(alias="co2(euro/ton)")
    wind_percentage: confloat(ge=0, le=100) = Field(alias="wind(%)")

class PowerPlant(BaseModel):
    name: str
    type: Literal["gasfired", "turbojet", "windturbine"]
    efficiency: confloat(gt=0, le=100)
    pmin: conint(ge=0)
    pmax: conint(gt=0)

    @field_validator("efficiency")
    def check_efficiency(cls, v: str, info: ValidationInfo) -> str:
        if "type" in info.data and info.data["type"] == "windturbine" and v != 1:
            raise ValueError("Efficiency must be 1 for wind turbines")
        return v

class ProductionPlanRequest(BaseModel):
    load: conint(gt=0)
    fuels: Fuels
    powerplants: List[PowerPlant]

class PowerPlantOutput(BaseModel):
    name: str
    p: confloat(ge=0)
