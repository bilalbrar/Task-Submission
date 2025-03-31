import os
import sys
import argparse
import joblib
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from app.core.logging import logger


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Download NLTK data
nltk.download('punkt', quiet=True)

def get_sentiment_label(star: int) -> str:
    """
    Convert star rating to sentiment label.
    
    Args:
        star: Star rating (1-5)
        
    Returns:
        Sentiment label: negative (1-2), neutral (3), or positive (4-5)
    """
    if star <= 2:
        return 'negative'
    elif star == 3:
        return 'neutral'
    else:
        return 'positive'

def preprocess_data(data_path: str, output_path: str = None):
    """
    Preprocess the raw review data.
    
    Args:
        data_path: Path to the raw data file
        output_path: Path to save the preprocessed data (optional)
        
    Returns:
        DataFrame with preprocessed data
    """
    logger.info(f"Loading data from {data_path}")
    
    try:
        # Load the data
        df = pd.read_json(data_path, lines=True)
        logger.info(f"Loaded {len(df)} reviews")
        
        # Identify the review text and rating columns
        review_text_col = 'text'
        rating_col = 'rating'
        
        if review_text_col not in df.columns:
            raise ValueError(f"Column '{review_text_col}' not found in the dataset")
        
        # Split each review into sentences and assign sentiment labels
        rows = []
        for idx, row in df.iterrows():
            review_text = row[review_text_col]
            if pd.isnull(review_text):
                continue
                
            sentences = sent_tokenize(review_text)
            
            try:
                star = int(row[rating_col])
            except Exception:
                continue  # Skip rows with invalid ratings
                
            label = get_sentiment_label(star)
            
            for sentence in sentences:
                rows.append({"sentence": sentence, "label": label})
        
        # Create DataFrame with sentences and labels
        df_sentences = pd.DataFrame(rows)
        logger.info(f"Extracted {len(df_sentences)} sentences with labels")
        
        # Save preprocessed data to output path provided
        if output_path:
            df_sentences.to_csv(output_path, index=False)
            logger.info(f"Saved preprocessed data to {output_path}")
        
        return df_sentences
        
    except Exception as e:
        logger.error(f"Error preprocessing data: {str(e)}")
        raise

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
        
        logger.info(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")
        
        # Build the model pipeline
        model_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english')),
            ('clf', LogisticRegression(max_iter=200, random_state=random_state))
        ])
        
        # Train the model
        logger.info("Training the model...")
        model_pipeline.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = model_pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"Model accuracy: {accuracy:.4f}")
        
        report = classification_report(y_test, y_pred)
        logger.info(f"Classification report:\n{report}")
        
        # Save the model
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(model_pipeline, model_path)
        logger.info(f"Model saved to {model_path}")
        
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess review data and train a sentiment analysis model")
    parser.add_argument("--data_path", type=str, required=True, help="Path to the raw data file")
    parser.add_argument("--output_path", type=str, help="Path to save the preprocessed data")
    parser.add_argument("--model_path", type=str, required=True, help="Path to save the trained model")
    parser.add_argument("--test_size", type=float, default=0.2, help="Proportion of data to use for testing")
    parser.add_argument("--random_state", type=int, default=42, help="Random seed for reproducibility")
    
    args = parser.parse_args()
    preprocess_data(args.data_path, args.output_path)
    train_model(args.data_path, args.model_path, args.test_size, args.random_state)
