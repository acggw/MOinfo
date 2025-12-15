import numpy as np
from unittest.mock import MagicMock, patch
import importlib

def test_predict_areas_returns_labels():
    mock_model = MagicMock()
    mock_mlb = MagicMock()

    # decision_function returns scores
    mock_model.decision_function.return_value = np.array([[1.2, -0.5, 0.8]])

    # inverse_transform returns labels
    mock_mlb.inverse_transform.return_value = [("Health", "Education")]

    with patch("classification_models.predict.joblib.load") as mock_load:
        mock_load.side_effect = [mock_model, mock_mlb]

        # Reload module so mocked joblib.load is used
        predict = importlib.reload(
            importlib.import_module("classification_models.predict")
        )

        result = predict.predict_areas("Some bill text")

    assert result == ("Health", "Education")

    mock_model.decision_function.assert_called_once_with(["Some bill text"])
    mock_mlb.inverse_transform.assert_called_once()
