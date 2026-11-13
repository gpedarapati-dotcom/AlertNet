import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from dataset import get_dataset


# Load dataset
texts, labels = get_dataset()

print(f"Training examples: {len(texts)}")


# Create AI pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 5)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            class_weight="balanced",
            max_iter=1000
        )
    )
])


# Train the model
model.fit(texts, labels)


# Save trained model
model_path = os.path.join(
    os.path.dirname(__file__),
    "model.joblib"
)

joblib.dump(model, model_path)


print("Model trained successfully")
print(f"Model saved to: {model_path}")