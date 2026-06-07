
import logging
import numpy as np
from typing import Dict
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config import Config

# Basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MoodAnalyzer:
    """Simple mood analyzer for converting text to mood parameters."""
    
    def __init__(self):
        """Initialize with basic models."""
        print("Loading models...")
        
        # Load sentiment model
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=Config.SENTIMENT_MODEL,
            return_all_scores=True
        )
        
        # Load embedding model
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        
        # Pre-compute mood embeddings
        self.mood_embeddings = {}
        for mood, description in Config.MOOD_CATEGORIES.items():
            embedding = self.embedding_model.encode(description)
            self.mood_embeddings[mood] = embedding
        
        print("Models loaded successfully!")
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Simple sentiment analysis."""
        try:
            results = self.sentiment_pipeline(text)
            
            # Process results
            sentiment_scores = {}
            if results and len(results) > 0:
                for score_dict in results[0]:
                    label = score_dict['label'].lower()
                    if 'positive' in label:
                        sentiment_scores['positive'] = score_dict['score']
                    elif 'negative' in label:
                        sentiment_scores['negative'] = score_dict['score']
                    elif 'neutral' in label:
                        sentiment_scores['neutral'] = score_dict['score']
            
            # Get primary sentiment
            if sentiment_scores:
                primary = max(sentiment_scores, key=sentiment_scores.get)
                confidence = sentiment_scores[primary]
            else:
                primary = 'neutral'
                confidence = 0.5
                sentiment_scores = {'positive': 0.33, 'negative': 0.33, 'neutral': 0.34}
            
            return {
                'primary_sentiment': primary,
                'confidence': confidence,
                'scores': sentiment_scores
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return {
                'primary_sentiment': 'neutral',
                'confidence': 0.5,
                'scores': {'positive': 0.33, 'negative': 0.33, 'neutral': 0.34}
            }
    
    def classify_mood(self, text: str) -> Dict:
        """Simple mood classification using similarity."""
        try:
            # Get text embedding
            text_embedding = self.embedding_model.encode(text)
            
            # Calculate similarities
            similarities = {}
            for mood, mood_embedding in self.mood_embeddings.items():
                similarity = cosine_similarity(
                    text_embedding.reshape(1, -1), 
                    mood_embedding.reshape(1, -1)
                )[0][0]
                similarities[mood] = float(similarity)
            
            # Find best mood
            best_mood = max(similarities, key=similarities.get)
            confidence = similarities[best_mood]
            
            return {
                'mood': best_mood,
                'confidence': confidence,
                'all_similarities': similarities
            }
            
        except Exception as e:
            logger.error(f"Mood classification error: {e}")
            return {
                'mood': 'calm',
                'confidence': 0.5,
                'all_similarities': {mood: 0.5 for mood in Config.MOOD_CATEGORIES.keys()}
            }
    
    def calculate_energy_level(self, text: str, sentiment_result: Dict) -> Dict:
        """Simple energy level calculation."""
        try:
            text_lower = text.lower()
            
            # Count energy keywords
            high_energy_count = sum(1 for keyword in Config.HIGH_ENERGY_KEYWORDS 
                                  if keyword in text_lower)
            low_energy_count = sum(1 for keyword in Config.LOW_ENERGY_KEYWORDS 
                                 if keyword in text_lower)
            
            # Base energy calculation
            base_energy = Config.BASE_ENERGY
            sentiment_boost = Config.SENTIMENT_ENERGY_BOOST.get(
                sentiment_result.get('primary_sentiment', 'neutral'), 0
            )
            keyword_adjustment = (high_energy_count * 1.5) - (low_energy_count * 1.0)
            
            final_energy = base_energy + sentiment_boost + keyword_adjustment
            final_energy = max(1, min(10, final_energy))  # Clamp to 1-10
            
            return {
                'energy_level': int(round(final_energy)),
                'base_energy': base_energy,
                'sentiment_boost': sentiment_boost,
                'keyword_adjustment': keyword_adjustment,
                'high_energy_words': high_energy_count,
                'low_energy_words': low_energy_count
            }
            
        except Exception as e:
            logger.error(f"Energy calculation error: {e}")
            return {
                'energy_level': 5,
                'base_energy': 5,
                'sentiment_boost': 0,
                'keyword_adjustment': 0,
                'high_energy_words': 0,
                'low_energy_words': 0
            }
    
    def analyze_mood(self, text: str) -> Dict:
        """Main analysis function - combines all steps."""
        try:
            if not text or not text.strip():
                raise ValueError("Input text cannot be empty")
            
            # Step 1: Sentiment Analysis
            sentiment_result = self.analyze_sentiment(text)
            
            # Step 2: Mood Classification  
            mood_result = self.classify_mood(text)
            
            # Step 3: Energy Level Calculation
            energy_result = self.calculate_energy_level(text, sentiment_result)
            
            # Combine results
            return {
                'input_text': text,
                'sentiment': sentiment_result,
                'mood': mood_result,
                'energy': energy_result
            }
            
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return {
                'input_text': text,
                'sentiment': {'primary_sentiment': 'neutral', 'confidence': 0.5, 'scores': {}},
                'mood': {'mood': 'calm', 'confidence': 0.5, 'all_similarities': {}},
                'energy': {'energy_level': 5, 'base_energy': 5, 'sentiment_boost': 0, 'keyword_adjustment': 0, 'high_energy_words': 0, 'low_energy_words': 0},
                'error': str(e)
            }
    
    def get_model_info(self) -> Dict:
        """Get basic model information."""
        return {
            'sentiment_model': Config.SENTIMENT_MODEL,
            'embedding_model': Config.EMBEDDING_MODEL,
            'device': Config.DEVICE,
            'mood_categories': list(Config.MOOD_CATEGORIES.keys())
        }