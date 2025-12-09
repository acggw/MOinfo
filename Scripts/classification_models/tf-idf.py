import pyterrier as pt
import pandas as pd
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from config import BILL_CLASSIFICATION_IDF_MODEL, BILL_BINARIZER_IDF_MODEL

# -------------------------------------------------------
# 1. Initialize PyTerrier
# -------------------------------------------------------
if not pt.java.started():
    pt.init()

# -------------------------------------------------------
# 2. Load bill dataset (HuggingFace)
# -------------------------------------------------------
print("Loading dataset...")
ds = load_dataset("dreamproit/bill_labels_us", split="train[:10%]")

print(ds.column_names)

# Convert to pandas DataFrame
df = pd.DataFrame({
    "text": ds["text"],
    "subjects": ds["legislative_subjects"]
})

# Remove missing labels
df = df[df["subjects"].notna()]
df = df[df["text"].notna()]

print("Total labeled bills:", len(df))

# -------------------------------------------------------
# 3. Train/test split
# -------------------------------------------------------
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# -------------------------------------------------------
# 4. Define a text classification pipeline
# -------------------------------------------------------
# You can replace the classifier with SVM, BERT embeddings, etc.

mlb = MultiLabelBinarizer()
y_multi = mlb.fit_transform(train_df["subjects"].tolist())

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_df=0.80,
        min_df=10,
        ngram_range=(1, 1),
    )),
    ("clf", OneVsRestClassifier(LinearSVC()))
])

#Fit Model
model.fit(train_df["text"].tolist(), y_multi)


#Store Model
joblib.dump(model, BILL_CLASSIFICATION_IDF_MODEL)
joblib.dump(mlb, BILL_BINARIZER_IDF_MODEL)


#model = joblib.load("bill_subject_model.pkl")
#mlb   = joblib.load("bill_subject_mlb.pkl")

# ---------------------------------------------------------
# Predict for entire test_df
# ---------------------------------------------------------

def predict_multi_label(model, texts):
    """Return binary label matrix for a list of texts."""
    scores = model.decision_function(texts)  # shape (n_samples, n_classes)
    # Convert raw SVM scores > 0 to predictions
    return (scores > 0).astype(int)

# X_test: bill texts
X_test = test_df["text"].tolist()

# y_true: ground truth subjects
y_true = mlb.transform(test_df["subjects"])

# y_pred: predicted labels
y_pred = predict_multi_label(model, X_test)

# ---------------------------------------------------------
# Print classification metrics
# ---------------------------------------------------------

print("\n====== CLASSIFICATION REPORT ======\n")
print(classification_report(
    y_true,
    y_pred,
    target_names=mlb.classes_,
    zero_division=0
))

# ---------------------------------------------------------
# Produce a DataFrame with true vs predicted
# ---------------------------------------------------------

def decode_labels(binary_row):
    """Convert binary vector to list of labels."""
    return mlb.inverse_transform(binary_row.reshape(1, -1))[0]

results_df = pd.DataFrame({
    "text": test_df["text"],
    "true_subjects": test_df["subjects"],
    "predicted_subjects": [
        decode_labels(y_pred[i]) for i in range(len(y_pred))
    ]
})

print("\nPreview of prediction results:")
print(results_df.head())

# Optionally save it
results_df.to_csv("bill_subject_predictions.csv", index=False)
print("\nSaved results to bill_subject_predictions.csv")

