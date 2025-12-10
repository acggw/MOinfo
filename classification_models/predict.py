import numpy as np

def predict_policy_area(model, bill_text: str) -> str:
    """
    Predict the policy area for a bill based on its text.

    Parameters
    ----------
    model : sklearn Pipeline
        A trained TF-IDF + classifier model.
    bill_text : str
        Full text of the bill.

    Returns
    -------
    str
        The predicted policy area label.
    """
    prediction = model.predict([bill_text])
    return prediction[0]

def predict_top_k_policy_areas(model, bill_text: str, k: int = 3):
    """
    Predict the top-k policy areas for a bill based on its text.

    Parameters
    ----------
    model : sklearn Pipeline
        A trained TF-IDF + LinearSVC model.
    bill_text : str
        Full text of the bill.
    k : int, optional
        Number of top predictions to return (default is 3).

    Returns
    -------
    List[Tuple[str, float]]
        List of tuples (policy_area, score) sorted by score descending.
        Scores are raw decision function values.
    """
    # Get decision scores from the classifier
    df = model.decision_function([bill_text])  # shape: (1, n_classes)
    df = df[0]  # flatten to (n_classes,)

    # Get class labels
    classes = model.named_steps['clf'].classes_

    # Pair labels with scores
    label_scores = list(zip(classes, df))

    # Sort by score descending and take top k
    top_k = sorted(label_scores, key=lambda x: x[1], reverse=True)[:k]

    return top_k

def predict_more_likely_than_p(model, bill_text: str, p: float = 0.8):
    return 0
