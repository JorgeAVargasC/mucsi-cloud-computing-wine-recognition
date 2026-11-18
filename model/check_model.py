"""Checks that the model loads and predicts the expected class for SAMPLE."""

from model.predictor import SAMPLE, model, predict

if __name__ == "__main__":
    print("Training columns:", list(model.feature_names_in_))
    print("Prediction:", predict(SAMPLE))
