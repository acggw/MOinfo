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
from .config import BILL_CLASSIFICATION_IDF_MODEL

# -------------------------------------------------------
# 1. Initialize PyTerrier
# -------------------------------------------------------
if not pt.started():
    pt.init()

# -------------------------------------------------------
# 2. Load bill dataset (HuggingFace)
# -------------------------------------------------------
print("Loading dataset...")
ds = load_dataset("dreamproit/bill_labels_us", split="train")

print(ds.column_names)

# Convert to pandas DataFrame
df = pd.DataFrame({
    "text": ds["text"],
    "label": ds["policy_area"]
})

# Remove missing labels
df = df[df["label"].notna()]
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
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=5000,
        min_df=5,
        max_df=0.8,
        ngram_range=(1,2),
        stop_words="english"
    )),
    ("clf", LinearSVC())
])

# -------------------------------------------------------
# 5. Train model
# -------------------------------------------------------
print("\nTraining model...")
pipeline.fit(train_df["text"], train_df["label"])

# -------------------------------------------------------
# 6. Evaluate
# -------------------------------------------------------
print("\nEvaluating...")
preds = pipeline.predict(test_df["text"])
print(classification_report(test_df["label"], preds))

# -------------------------------------------------------
# 7. Save model
# -------------------------------------------------------
joblib.dump(pipeline, BILL_CLASSIFICATION_IDF_MODEL)
print("Saved model as bill_topic_classifier.pkl")

# -------------------------------------------------------
# 8. Predict topics for NEW bills
# -------------------------------------------------------
def predict_topic(text):
    return pipeline.predict([text])[0]

print("\nExample prediction:")
example_text = """
    A bill to provide funding for renewable energy development,
    including solar power incentives and green infrastructure grants.
"""
print(predict_topic(example_text))
