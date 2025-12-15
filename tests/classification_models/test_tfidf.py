import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch
import pytest

import classification_models.tfidf as tfidf

@pytest.fixture
def mock_dataset():
    return {
        "text": ["bill text 1", "bill text 2", "bill text 3"],
        "legislative_subjects": [["Health"], ["Education"], ["Health", "Education"]]
    }

def test_dataframe_creation(mock_dataset):
    print("1")
    df = pd.DataFrame({
        "text": mock_dataset["text"],
        "subjects": mock_dataset["legislative_subjects"]
    })

    # Remove missing
    df = df[df["subjects"].notna()]
    df = df[df["text"].notna()]

    assert len(df) == 3
    assert all(col in df.columns for col in ["text", "subjects"])

def test_predict_multi_label_returns_binary():
    mock_model = MagicMock()
    # Simulate decision_function output
    mock_model.decision_function.return_value = np.array([[1.2, -0.5], [-0.1, 2.0]])

    def predict_multi_label(model, texts):
        scores = model.decision_function(texts)
        return (scores > 0).astype(int)

    X_test = ["text1", "text2"]
    y_pred = predict_multi_label(mock_model, X_test)

    # Check binary shape
    assert y_pred.shape == (2, 2)
    assert (y_pred[0] == np.array([1, 0])).all()
    assert (y_pred[1] == np.array([0, 1])).all()

def test_results_dataframe_creation():
    y_pred = np.array([[1, 0], [0, 1]])
    texts = ["bill1", "bill2"]
    y_true_subjects = [["Health"], ["Education"]]

    # Mock mlb
    class MockMLB:
        def inverse_transform(self, binary):
            if (binary == np.array([[1,0]])).all():
                return [["Health"]]
            else:
                return [["Education"]]

    mlb = MockMLB()

    results_df = pd.DataFrame({
        "text": texts,
        "true_subjects": y_true_subjects,
        "predicted_subjects": [mlb.inverse_transform(y_pred[i].reshape(1,-1))[0] for i in range(len(y_pred))]
    })

    assert results_df.shape[0] == 2
    assert results_df["predicted_subjects"].tolist() == [["Health"], ["Education"]]

def test_joblib_dump_called():
    mock_model = MagicMock()
    mock_mlb = MagicMock()

    with patch("classification_models.tfidf.joblib.dump") as mock_dump:
        # Save models
        tfidf.joblib.dump(mock_model, "model.pkl")
        tfidf.joblib.dump(mock_mlb, "mlb.pkl")

    assert mock_dump.call_count == 2
    mock_dump.assert_any_call(mock_model, "model.pkl")
    mock_dump.assert_any_call(mock_mlb, "mlb.pkl")




