from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

ann_model = joblib.load("assists/mnist_ann.model.joblib")
cnn_model = joblib.load("assists/mnst_cnn.model.joblib")

app.frontend("/", directory="dist/")


class PredictionRequest(BaseModel):
    pixels: list[float]
    model: str


@app.post("/predict")
def predict(data: PredictionRequest):
    x = np.array(data.pixels, dtype=np.float32)

    if x.shape[0] != 784:
        return {"error": "Expected 784 values."}

    x = x.reshape(1, 784)

    print(data.model, "MODEL")
    prediction = (
        ann_model.predict(x)
        if data.model == "ann"
        else cnn_model.predict(x.reshape(1, 28, 28, 1))
    )

    digit = np.argmax(prediction)

    result = {"digit": int(digit)}

    return result
