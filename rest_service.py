"""REST microservice that exposes the wine model through FastAPI."""

from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from predictor import SAMPLE, predict

app = FastAPI(title="Wine Recognition API")


class WineFeatures(BaseModel):
    """The 13 measurements of a wine sample."""

    alcohol: float = Field(json_schema_extra={"example": SAMPLE["alcohol"]})
    malic_acid: float = Field(json_schema_extra={"example": SAMPLE["malic_acid"]})
    ash: float = Field(json_schema_extra={"example": SAMPLE["ash"]})
    alcalinity_of_ash: float = Field(json_schema_extra={"example": SAMPLE["alcalinity_of_ash"]})
    magnesium: float = Field(json_schema_extra={"example": SAMPLE["magnesium"]})
    total_phenols: float = Field(json_schema_extra={"example": SAMPLE["total_phenols"]})
    flavanoids: float = Field(json_schema_extra={"example": SAMPLE["flavanoids"]})
    nonflavanoid_phenols: float = Field(json_schema_extra={"example": SAMPLE["nonflavanoid_phenols"]})
    proanthocyanins: float = Field(json_schema_extra={"example": SAMPLE["proanthocyanins"]})
    color_intensity: float = Field(json_schema_extra={"example": SAMPLE["color_intensity"]})
    hue: float = Field(json_schema_extra={"example": SAMPLE["hue"]})
    od280_od315: float = Field(json_schema_extra={"example": SAMPLE["od280_od315"]})
    proline: float = Field(json_schema_extra={"example": SAMPLE["proline"]})


class Prediction(BaseModel):
    """Predicted wine class (1, 2 or 3)."""

    label: int


@app.get("/")
def health_check() -> dict:
    """Confirms the service is running."""
    return {"status": "ok"}


@app.get("/predict")
def predict_wine(features: Annotated[WineFeatures, Query()]) -> Prediction:
    """Predicts the wine class from the measurements sent as query parameters."""
    return Prediction(**predict(features.model_dump()))
