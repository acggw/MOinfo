import joblib
from classification_models.config import BILL_BINARIZER_IDF_MODEL, BILL_CLASSIFICATION_IDF_MODEL

model = joblib.load(BILL_CLASSIFICATION_IDF_MODEL)
mlb   = joblib.load(BILL_BINARIZER_IDF_MODEL)

def predict_areas(text):
    scores = model.decision_function([text])
    binary = (scores > 0).astype(int)
    labels = mlb.inverse_transform(binary)[0]
    return labels


