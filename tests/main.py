from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_production_plan_success():
    response = client.post("/productionplan", json={
        "load": 480,
        "fuels":
        {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60
        },
        "powerplants": [
            {
            "name": "gasfiredbig1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
            },
            {
            "name": "gasfiredbig2",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
            },
            {
            "name": "gasfiredsomewhatsmaller",
            "type": "gasfired",
            "efficiency": 0.37,
            "pmin": 40,
            "pmax": 210
            },
            {
            "name": "tj1",
            "type": "turbojet",
            "efficiency": 0.3,
            "pmin": 0,
            "pmax": 16
            },
            {
            "name": "windpark1",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 150
            },
            {
            "name": "windpark2",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 36
            }
        ]
    })
    
    assert response.status_code == 200

    data = response.json()
    expected_output = [
        {"name": "windpark1", "p": 90.0},
        {"name": "windpark2", "p": 21.6},
        {"name": "gasfiredbig1", "p": 368.4},
        {"name": "gasfiredbig2", "p": 0.0},
        {"name": "gasfiredsomewhatsmaller", "p": 0.0},
        {"name": "tj1", "p": 0.0},
    ]
    assert data == expected_output
    
def test_production_plan_not_enough_capacity():
    response = client.post("/productionplan", json={
        "load": 480,
        "fuels":
        {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 0
        },
        "powerplants": [
            {
            "name": "gasfiredbig1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
            },
            {
            "name": "gasfiredbig2",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
            },
            {
            "name": "gasfiredsomewhatsmaller",
            "type": "gasfired",
            "efficiency": 0.37,
            "pmin": 40,
            "pmax": 210
            },
            {
            "name": "tj1",
            "type": "turbojet",
            "efficiency": 0.3,
            "pmin": 0,
            "pmax": 16
            },
            {
            "name": "windpark1",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 150
            },
            {
            "name": "windpark2",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 36
            }
        ]
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot meet the required load with the available power plants"}

def test_production_plan_min_power():
    response = client.post("/productionplan", json={
        "load": 50,
        "fuels": {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20.0,
            "wind(%)": 60.0
        },
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460
            },
            {
                "name": "windpark1",
                "type": "windturbine",
                "efficiency": 1.0,
                "pmin": 0,
                "pmax": 150
            }
        ]
    })

    assert response.status_code == 200

    data = response.json()
    expected_output = [
        {"name": "windpark1", "p": 50.0},
        {"name": "gasfiredbig1", "p": 0.0},
    ]
    assert data == expected_output

def test_production_plan_invalid_input():
    response = client.post("/productionplan", json={
        "load": -100,  # Invalid load
        "fuels": {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20.0,
            "wind(%)": 60.0
        },
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460
            },
            {
                "name": "windpark1",
                "type": "windturbine",
                "efficiency": 1.0,
                "pmin": 0,
                "pmax": 150
            }
        ]
    })
    assert response.status_code == 422  # Unprocessable Entity for invalid input
