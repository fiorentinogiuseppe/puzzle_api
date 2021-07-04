import orjson

from fastapi import FastAPI
from pydantic import BaseModel, typing
from starlette.responses import JSONResponse
from group_formation import Ga
import numpy as np
import sys

sys.path.insert(1, '..')


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_NAIVE_UTC | orjson.OPT_SERIALIZE_NUMPY)


app = FastAPI(default_response_class=ORJSONResponse)


# pydantic models

class StockIn(BaseModel):
    # lenght of class
    tam_class: int
    # number of group per class
    tam_group: int
    # length of people per group
    ppg: int
    # number of generation
    iterations: int
    # Number of characteristics
    numcarac: int
    # c1 , c2, c3
    carac: list
    # number of interation of each people of class
    interations: list


class StockOut(BaseModel):
    formacao: list


# routes

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.post("/get_group", response_model=StockOut, status_code=200)
def get_prediction(payload: StockIn):
    if not payload.interations:
        interations = np.ones(payload.tam_class)
    else:
        interations = payload.interations
    rept = Ga.GaConfig(payload.tam_group, payload.tam_class, payload.iterations, payload.carac, payload.ppg,
                       payload.numcarac, interations, False, 0)
    rept.setGa()
    return {"formacao": rept.best_class.tolist()}


"""# lenght of class
    tam_class = 10
    # number of group per class
    tam_group = 5
    # length of people per group
    ppg = 2
    # number of generation
    iterations = 5
    # Number of characteristics
    numcarac = 3
    # c1 , c2, c3
    carac = [[10.0, 0.8, 120.0],  # 0
             [20.0, 0.6, 200.0],  # 1
             [10.0, 0.9, 0.0],  # 2
             [50.0, 0.0, 560.0],  # 3
             [30.0, 0.3, 800.0],  # 4
             [30.0, 0.9, 700.0],  # 5
             [20.0, 0.8, 230.0],  # 6
             [30.0, 0.7, 300.0],  # 7
             [40.0, 1, 100.0],  # 8
             [60.0, 0.1, 670.0],  # 9
             ]
             
    [0, 9, 41, 3, 59, 67, 100, 2, 33, 80]"""
