from enum import Enum
from fastapi import APIRouter
from sqlalchemy import table

class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

router = APIRouter(
    prefix='/models',
    tags=['Models']
)

@router.get("/{model_name}")
def get_models(model_name : ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name,
            "message":"Deep Learning FTW!"
        }
    if model_name.value == "lenet":
        return {"model_name":model_name.value,
            "message":"LeCNN all the images"
        }
