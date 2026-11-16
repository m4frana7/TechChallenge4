"""
Data preparation module for the RAG pipeline
Handles loading, cleaning, and preprocessing of review data
"""

import pandas as pd
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from .config import REVIEWS_CSV, DATA_PATH
from .utils import clean_text, classify_sentiment, prepare_document_text

logger = logging.getLogger(__name__)


class DataPreparation:
    """Class to handle data preparation for RAG pipeline"""
    
    def __init__(self, csv_path: Optional[Path] = None):
        """
        Initialize DataPreparation
        
        Args:
            csv_path: Path to reviews CSV file (default: from config)
        """
        self.csv_path = csv_path or REVIEWS_CSV
        self.df_raw = None
        self.df_clean = None
        self.documents = []
        
    def load_data(self) -> pd.DataFrame:
        """
        Load reviews data from CSV
        
        Returns:
            DataFrame with reviews
        """
        logger.info(f"Loading data from {self.csv_path}")
        
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"Reviews CSV not found at {self.csv_path}. "
                "Please run the EDA notebook first to generate this file."
            )
        
        self.df_raw = pd.read_csv(self.csv_path)
        logger.info(f"Loaded {len(self.df_raw)} reviews")
        
        return self.df_raw
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean and preprocess the data
        
        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning data...")
        
        if self.df_raw is None:
            self.load_data()
        
        df = self.df_raw.copy()
        
        # Remove rows without comments
        df = df[df['review_comment_message'].notna()].copy()
        df = df[df['review_comment_message'].str.strip() != ''].copy()
        
        logger.info(f"Filtered to {len(df)} reviews with valid comments")
        
        # Clean text fields
        df['clean_comment'] = df['review_comment_message'].apply(clean_text)
        
        if 'review_comment_title' in df.columns:
            df['clean_title'] = df['review_comment_title'].fillna('').apply(clean_text)
        
        # Add sentiment classification
        df['sentiment'] = df['review_score'].apply(classify_sentiment)
        
        # Remove very short comments (less than 10 characters)
        df = df[df['clean_comment'].str.len() >= 10].copy()
        logger.info(f"After removing very short comments: {len(df)} reviews")
        
        # Fill missing values
        df['product_category_name_english'] = df['product_category_name_english'].fillna('unknown')
        df['delivery_status'] = df['delivery_status'].fillna('unknown')
        
        self.df_clean = df
        logger.info("Data cleaning completed")
        
        return self.df_clean
    
    def prepare_documents(self) -> List[Dict[str, Any]]:
        """
        Prepare documents for embedding
        Each document contains text and metadata
        
        Returns:
            List of documents with text and metadata
        """
        logger.info("Preparing documents for embedding...")
        
        if self.df_clean is None:
            self.clean_data()
        
        documents = []
        
        for idx, row in self.df_clean.iterrows():
            # Prepare document text
            text = prepare_document_text(row)
            
            # Create document with metadata
            doc = {
                'id': f"review_{row['review_id']}",
                'text': text,
                'metadata': {
                    'review_id': row['review_id'],
                    'order_id': row.get('order_id', ''),
                    'review_score': int(row['review_score']),
                    'sentiment': row['sentiment'],
                    'product_category': row.get('product_category_name_english', 'unknown'),
                    'delivery_status': row.get('delivery_status', 'unknown'),
                    'review_date': str(row.get('review_creation_date', '')),
                    'comment_length': len(row['clean_comment'])
                }
            }
            
            documents.append(doc)
        
        self.documents = documents
        logger.info(f"Prepared {len(documents)} documents")
        
        return documents
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the prepared data
        
        Returns:
            Dictionary with statistics
        """
        if self.df_clean is None:
            self.clean_data()
        
        stats = {
            'total_reviews': len(self.df_clean),
            'score_distribution': self.df_clean['review_score'].value_counts().to_dict(),
            'sentiment_distribution': self.df_clean['sentiment'].value_counts().to_dict(),
            'avg_comment_length': self.df_clean['clean_comment'].str.len().mean(),
            'top_categories': self.df_clean['product_category_name_english'].value_counts().head(10).to_dict(),
            'delivery_status': self.df_clean['delivery_status'].value_counts().to_dict()
        }
        
        return stats
    
    def save_prepared_data(self, output_path: Optional[Path] = None):
        """
        Save prepared data to CSV
        
        Args:
            output_path: Path to save file (default: data/prepared_reviews.csv)
        """
        if self.df_clean is None:
            self.clean_data()
        
        output_path = output_path or (DATA_PATH / "prepared_reviews.csv")
        self.df_clean.to_csv(output_path, index=False)
        logger.info(f"Saved prepared data to {output_path}")


def main():
    """Main function to test data preparation"""
    logging.basicConfig(level=logging.INFO)
    
    print("🔧 Data Preparation Test\n")
    print("="*60)
    
    # Initialize
    prep = DataPreparation()
    
    # Load and clean data
    prep.load_data()
    prep.clean_data()
    
    # Prepare documents
    documents = prep.prepare_documents()
    
    # Show statistics
    stats = prep.get_statistics()
    
    print("\n📊 Statistics:")
    print(f"  Total reviews: {stats['total_reviews']:,}")
    print(f"  Avg comment length: {stats['avg_comment_length']:.1f} chars")
    
    print("\n⭐ Score distribution:")
    for score, count in sorted(stats['score_distribution'].items()):
        print(f"  Score {score}: {count:,}")
    
    print("\n😊 Sentiment distribution:")
    for sentiment, count in stats['sentiment_distribution'].items():
        print(f"  {sentiment}: {count:,}")
    
    print("\n📦 Top 5 categories:")
    for i, (cat, count) in enumerate(list(stats['top_categories'].items())[:5], 1):
        print(f"  {i}. {cat}: {count:,}")
    
    print("\n📝 Sample documents:")
    for i, doc in enumerate(documents[:3], 1):
        print(f"\nDocument {i}:")
        print(f"  ID: {doc['id']}")
        print(f"  Text: {doc['text'][:100]}...")
        print(f"  Metadata: {doc['metadata']}")
    
    print("\n✅ Data preparation completed successfully!")


if __name__ == "__main__":
    main()
