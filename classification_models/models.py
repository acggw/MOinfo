import joblib
from .config import BILL_CLASSIFICATION_IDF_MODEL

bill_classificiation_tfidf_model = joblib.load(BILL_CLASSIFICATION_IDF_MODEL)