import os
import sys
import argparse
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app.core.logging import logger
from scripts.preprocess_data import preprocess_data

def train_model(data_path: str, model_path: str, test_size: float = 0.2, random_state: int = 42):
    """
    Train a sentiment analysis model.
    
    Args:
        data_path: Path to the raw data file
        model_path: Path to save the trained model
        test_size: Proportion of data to use for testing
        random_state: Random seed for reproducibility
    """
    try:
        # Preprocess the data
        df_sentences = preprocess_data(data_path)
        
        # Split into features and target
        X = df_sentences['sentence']
        y = df_sentences['label']
        
        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")
        
        # Build the model pipeline
        model_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english')),
            ('clf', LogisticRegression(max_iter=200, random_state=random_state))
        ])
        
        # Train the model
        print("Training the model...")
        model_pipeline.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = model_pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.4f}")
        
        report = classification_report(y_test, y_pred)
        print(f"Classification report:\n{report}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save the model
        joblib.dump(model_pipeline, model_path)
        print(f"Model saved to {model_path}")
        
    except Exception as e:
        print(f"Error training model: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a sentiment analysis model")
    parser.add_argument("--data_path", type=str, required=True, help="Path to the raw data file")
    parser.add_argument("--model_path", type=str, required=True, help="Path to save the trained model")
    parser.add_argument("--test_size", type=float, default=0.2, help="Proportion of data to use for testing")
    parser.add_argument("--random_state", type=int, default=42, help="Random seed for reproducibility")
    
    args = parser.parse_args()
    train_model(args.data_path, args.model_path, args.test_size, args.random_state) 