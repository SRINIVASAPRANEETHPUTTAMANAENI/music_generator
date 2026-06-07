
import logging
from typing import Dict, List, Tuple, Any
import random

from config import Config

# Configure logging
logger = logging.getLogger(__name__)


class MusicParametersMapper:
    """Maps mood analysis results to detailed musical parameters."""
    
    def __init__(self):
        """Initialize the MusicParametersMapper."""
        logger.info("Initializing MusicParametersMapper...")
        self.tempo_cache = {}
        logger.info("MusicParametersMapper initialization complete.")
    
    def map_mood_to_tempo(self, mood: str, energy_level: int) -> Dict[str, Any]:
        """
        Map mood and energy level to tempo (BPM).
        
        Args:
            mood (str): The detected mood
            energy_level (int): Energy level on 1-10 scale
            
        Returns:
            Dict[str, Any]: Tempo information including BPM and adjustments
        """
        try:
            logger.debug(f"Mapping tempo for mood: {mood}, energy: {energy_level}")
            
            # Get base tempo for mood
            mood_config = Config.MOOD_TO_TEMPO.get(mood, Config.MOOD_TO_TEMPO["calm"])
            base_tempo = mood_config["base"]
            tempo_range = mood_config["range"]
            
            # Adjust tempo based on energy level
            # Energy level 5 is neutral, above increases tempo, below decreases
            energy_adjustment = (energy_level - 5) * Config.TEMPO_ENERGY_MULTIPLIER
            adjusted_tempo = base_tempo + energy_adjustment
            
            # Ensure tempo stays within reasonable bounds for the mood
            min_tempo, max_tempo = tempo_range
            final_tempo = max(min_tempo, min(max_tempo, adjusted_tempo))
            
            result = {
                "tempo": int(round(final_tempo)),
                "base_tempo": base_tempo,
                "energy_adjustment": energy_adjustment,
                "tempo_range": tempo_range,
                "mood_influence": mood,
                "energy_influence": energy_level
            }
            
            logger.debug(f"Tempo mapping result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error mapping tempo: {str(e)}")
            return {
                "tempo": 100,
                "base_tempo": 100,
                "energy_adjustment": 0,
                "tempo_range": (80, 120),
                "mood_influence": mood,
                "energy_influence": energy_level,
                "error": str(e)
            }
    
    def map_sentiment_to_key(self, sentiment: str, mood: str) -> Dict[str, Any]:
        """
        Map sentiment and mood to musical key.
        
        Args:
            sentiment (str): Primary sentiment (positive/negative/neutral)
            mood (str): Detected mood
            
        Returns:
            Dict[str, Any]: Key information including key type and reasoning
        """
        try:
            logger.debug(f"Mapping key for sentiment: {sentiment}, mood: {mood}")
            
            # Get base key from mood
            base_key = Config.MOOD_TO_KEY.get(mood, "major")
            
            # Sentiment can override mood-based key selection
            sentiment_key_map = {
                "positive": "major",
                "negative": "minor", 
                "neutral": base_key
            }
            
            final_key = sentiment_key_map.get(sentiment, base_key)
            
            # Add some musical theory context
            key_characteristics = {
                "major": {
                    "feeling": "bright, happy, uplifting",
                    "common_chords": ["I", "vi", "IV", "V"],
                    "scale_notes": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Ti"]
                },
                "minor": {
                    "feeling": "dark, melancholic, introspective", 
                    "common_chords": ["i", "iv", "V", "VI"],
                    "scale_notes": ["Do", "Re", "Me", "Fa", "Sol", "Le", "Te"]
                }
            }
            
            result = {
                "key": final_key,
                "base_key_from_mood": base_key,
                "sentiment_influence": sentiment,
                "characteristics": key_characteristics.get(final_key, {}),
                "reasoning": f"Key '{final_key}' chosen based on {sentiment} sentiment and {mood} mood"
            }
            
            logger.debug(f"Key mapping result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error mapping key: {str(e)}")
            return {
                "key": "major",
                "base_key_from_mood": "major",
                "sentiment_influence": sentiment,
                "characteristics": {},
                "reasoning": f"Default major key due to error: {str(e)}",
                "error": str(e)
            }
    
    def map_mood_to_instruments(self, mood: str, energy_level: int) -> Dict[str, Any]:
        """
        Map mood and energy level to instrument selection.
        
        Args:
            mood (str): The detected mood
            energy_level (int): Energy level on 1-10 scale
            
        Returns:
            Dict[str, Any]: Instrument selection and configuration
        """
        try:
            logger.debug(f"Mapping instruments for mood: {mood}, energy: {energy_level}")
            
            # Get base instruments for mood
            base_instruments = Config.MOOD_TO_INSTRUMENTS.get(mood, Config.MOOD_TO_INSTRUMENTS["calm"])
            
            # Select primary instruments based on energy level
            if energy_level >= 7:  # High energy
                # Favor more energetic instruments
                energy_boost_instruments = ["drums", "electric_guitar", "bass", "brass", "synthesizer"]
                primary_instruments = list(set(base_instruments + energy_boost_instruments))
            elif energy_level <= 3:  # Low energy  
                # Favor more mellow instruments
                mellow_instruments = ["piano", "acoustic_guitar", "flute", "harp", "soft_strings"]
                primary_instruments = list(set(base_instruments + mellow_instruments))
            else:  # Medium energy
                primary_instruments = base_instruments.copy()
            
            # Limit to reasonable number of instruments (3-5)
            if len(primary_instruments) > 5:
                primary_instruments = primary_instruments[:5]
            elif len(primary_instruments) < 3:
                # Add some default instruments if too few
                default_additions = ["piano", "strings", "drums"]
                for instrument in default_additions:
                    if instrument not in primary_instruments:
                        primary_instruments.append(instrument)
                        if len(primary_instruments) >= 3:
                            break
            
            # Define instrument roles and characteristics
            instrument_roles = {
                "piano": {"role": "melody/harmony", "prominence": "high", "texture": "polyphonic"},
                "guitar": {"role": "rhythm/melody", "prominence": "medium", "texture": "strummed/picked"},
                "electric_guitar": {"role": "lead/rhythm", "prominence": "high", "texture": "distorted/clean"},
                "acoustic_guitar": {"role": "rhythm/accompaniment", "prominence": "medium", "texture": "fingerpicked/strummed"},
                "drums": {"role": "rhythm/percussion", "prominence": "foundation", "texture": "percussive"},
                "bass": {"role": "bassline", "prominence": "foundation", "texture": "low-frequency"},
                "strings": {"role": "harmony/texture", "prominence": "medium", "texture": "sustained/legato"},
                "soft_strings": {"role": "atmosphere", "prominence": "background", "texture": "gentle/sustained"},
                "brass": {"role": "melody/fanfare", "prominence": "high", "texture": "bold/bright"},
                "synthesizer": {"role": "texture/effects", "prominence": "variable", "texture": "electronic"},
                "flute": {"role": "melody", "prominence": "medium", "texture": "airy/light"},
                "harp": {"role": "accompaniment", "prominence": "background", "texture": "arpeggiated"},
                "cello": {"role": "melody/harmony", "prominence": "medium", "texture": "expressive/sustained"},  
                "violin": {"role": "melody", "prominence": "high", "texture": "expressive/agile"},
                "saxophone": {"role": "melody/solo", "prominence": "high", "texture": "smooth/jazzy"},
                "ambient_pads": {"role": "atmosphere", "prominence": "background", "texture": "ethereal/sustained"},
                "percussion": {"role": "rhythm/color", "prominence": "accent", "texture": "varied/textural"}
            }
            
            # Add role information for selected instruments
            instruments_with_roles = {}
            for instrument in primary_instruments:
                instruments_with_roles[instrument] = instrument_roles.get(instrument, {
                    "role": "general", 
                    "prominence": "medium", 
                    "texture": "varied"
                })
            
            result = {
                "primary_instruments": primary_instruments,
                "base_instruments": base_instruments,
                "instruments_with_roles": instruments_with_roles,
                "total_instruments": len(primary_instruments),
                "energy_influence": energy_level,
                "mood_influence": mood,
                "arrangement_suggestion": self._suggest_arrangement(primary_instruments, energy_level)
            }
            
            logger.debug(f"Instruments mapping result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error mapping instruments: {str(e)}")
            return {
                "primary_instruments": ["piano", "strings", "drums"],
                "base_instruments": ["piano", "strings", "drums"],
                "instruments_with_roles": {},
                "total_instruments": 3,
                "energy_influence": energy_level,
                "mood_influence": mood,
                "arrangement_suggestion": "Simple arrangement due to error",
                "error": str(e)
            }
    
    def _suggest_arrangement(self, instruments: List[str], energy_level: int) -> str:
        """
        Suggest an arrangement style based on instruments and energy level.
        
        Args:
            instruments (List[str]): Selected instruments
            energy_level (int): Energy level on 1-10 scale
            
        Returns:
            str: Arrangement suggestion
        """
        try:
            arrangement_suggestions = []
            
            # Energy-based suggestions
            if energy_level >= 7:
                arrangement_suggestions.append("full, driving arrangement with strong rhythmic foundation")
            elif energy_level <= 3:
                arrangement_suggestions.append("sparse, intimate arrangement with space for breathing")
            else:
                arrangement_suggestions.append("balanced arrangement with moderate dynamics")
            
            # Instrument-based suggestions  
            if "drums" in instruments and "bass" in instruments:
                arrangement_suggestions.append("solid rhythm section provides foundation")
            
            if "piano" in instruments:
                arrangement_suggestions.append("piano as primary harmonic and melodic voice")
            
            if any("guitar" in inst for inst in instruments):
                arrangement_suggestions.append("guitar adds textural and rhythmic interest")
            
            if "strings" in instruments or "soft_strings" in instruments:
                arrangement_suggestions.append("strings provide lush harmonic backdrop")
            
            return "; ".join(arrangement_suggestions)
            
        except Exception as e:
            logger.error(f"Error generating arrangement suggestion: {str(e)}")
            return "Standard arrangement"
    
    def generate_musical_parameters(self, mood_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate complete musical parameters from mood analysis results.
        
        Args:
            mood_analysis (Dict[str, Any]): Results from MoodAnalyzer
            
        Returns:
            Dict[str, Any]: Complete musical parameters
        """
        try:
            logger.info("Generating complete musical parameters...")
            
            # Extract key information from mood analysis
            mood = mood_analysis.get('mood', {}).get('mood', 'calm')
            energy_level = mood_analysis.get('energy', {}).get('energy_level', 5)
            sentiment = mood_analysis.get('sentiment', {}).get('primary_sentiment', 'neutral')
            
            # Generate all musical parameters
            tempo_params = self.map_mood_to_tempo(mood, energy_level)
            key_params = self.map_sentiment_to_key(sentiment, mood)
            instrument_params = self.map_mood_to_instruments(mood, energy_level)
            
            # Additional musical characteristics
            additional_params = self._generate_additional_parameters(mood, energy_level, sentiment)
            
            # Combine all parameters
            musical_parameters = {
                "tempo": tempo_params["tempo"],
                "key": key_params["key"],
                "mood": mood,
                "energy": energy_level,
                "instruments": instrument_params["primary_instruments"],
                "sentiment": sentiment,
                
                # Detailed breakdowns
                "tempo_details": tempo_params,
                "key_details": key_params, 
                "instrument_details": instrument_params,
                "additional_parameters": additional_params,
                
                # Summary for quick reference
                "summary": {
                    "style": self._determine_style(mood, energy_level),
                    "complexity": self._determine_complexity(energy_level, len(instrument_params["primary_instruments"])),
                    "emotional_target": f"{sentiment} {mood} with {energy_level}/10 energy",
                    "recommended_duration": self._suggest_duration(mood, energy_level)
                },
                
                # Source analysis reference
                "source_analysis": {
                    "input_text": mood_analysis.get('input_text', ''),
                    "mood_confidence": mood_analysis.get('mood', {}).get('confidence', 0),
                    "sentiment_confidence": mood_analysis.get('sentiment', {}).get('confidence', 0)
                }
            }
            
            logger.info("Musical parameters generation complete.")
            return musical_parameters
            
        except Exception as e:
            logger.error(f"Error generating musical parameters: {str(e)}")
            # Return basic fallback parameters
            return {
                "tempo": 100,
                "key": "major",
                "mood": "calm",
                "energy": 5,
                "instruments": ["piano", "strings", "drums"],
                "sentiment": "neutral",
                "error": str(e),
                "summary": {
                    "style": "generic",
                    "complexity": "medium",
                    "emotional_target": "neutral calm with 5/10 energy",
                    "recommended_duration": "3-4 minutes"
                }
            }
    
    def _generate_additional_parameters(self, mood: str, energy_level: int, sentiment: str) -> Dict[str, Any]:
        """
        Generate additional musical parameters like dynamics, articulation, etc.
        
        Args:
            mood (str): The detected mood
            energy_level (int): Energy level on 1-10 scale
            sentiment (str): Primary sentiment
            
        Returns:
            Dict[str, Any]: Additional musical parameters
        """
        try:
            # Dynamics based on energy level
            if energy_level >= 8:
                dynamics = "forte (loud)"
            elif energy_level >= 6:
                dynamics = "mezzo-forte (moderately loud)"
            elif energy_level >= 4:
                dynamics = "mezzo-piano (moderately soft)"
            else:
                dynamics = "piano (soft)"
            
            # Articulation based on mood and energy
            articulation_map = {
                ("happy", "high"): "staccato, bouncy",
                ("happy", "medium"): "legato, flowing",
                ("happy", "low"): "tenuto, sustained",
                ("sad", "high"): "marcato, emphasized",
                ("sad", "medium"): "legato, expressive",
                ("sad", "low"): "sostenuto, very sustained",
                ("calm", "high"): "portato, gently separated",
                ("calm", "medium"): "legato, smooth",
                ("calm", "low"): "molto legato, very smooth",
                ("energetic", "high"): "staccato, sharp",
                ("energetic", "medium"): "tenuto, marked",
                ("energetic", "low"): "legato, flowing",
                ("mysterious", "high"): "staccato, mysterious",
                ("mysterious", "medium"): "tenuto, enigmatic",
                ("mysterious", "low"): "legato, dark",
                ("romantic", "high"): "espressivo, expressive",
                ("romantic", "medium"): "dolce, sweetly",
                ("romantic", "low"): "molto dolce, very sweetly"
            }
            
            energy_category = "high" if energy_level >= 7 else "medium" if energy_level >= 4 else "low"
            articulation = articulation_map.get((mood, energy_category), "legato, natural")
            
            # Time signature suggestions
            time_signature_map = {
                "happy": "4/4 or 6/8",
                "sad": "4/4 or 3/4",
                "calm": "4/4",
                "energetic": "4/4 or 2/4",
                "mysterious": "4/4 or 5/4", 
                "romantic": "4/4 or 3/4"
            }
            
            time_signature = time_signature_map.get(mood, "4/4")
            
            return {
                "dynamics": dynamics,
                "articulation": articulation,
                "time_signature": time_signature,
                "suggested_form": self._suggest_form(mood, energy_level),
                "harmonic_rhythm": self._suggest_harmonic_rhythm(mood, energy_level),
                "texture": self._suggest_texture(mood, energy_level)
            }
            
        except Exception as e:
            logger.error(f"Error generating additional parameters: {str(e)}")
            return {
                "dynamics": "mezzo-forte",
                "articulation": "legato",
                "time_signature": "4/4",
                "suggested_form": "ABA",
                "harmonic_rhythm": "moderate",
                "texture": "homophonic"
            }
    
    def _suggest_form(self, mood: str, energy_level: int) -> str:
        """Suggest musical form based on mood and energy."""
        if energy_level >= 7:
            return "ABACA (rondo with energetic returns)" 
        elif mood in ["sad", "romantic"]:
            return "ABA (ternary with contrasting middle)"
        else:
            return "AABA (song form with bridge)"
    
    def _suggest_harmonic_rhythm(self, mood: str, energy_level: int) -> str:
        """Suggest harmonic rhythm based on parameters."""
        if energy_level >= 7:
            return "fast (chord changes every 1-2 beats)"
        elif energy_level <= 3:
            return "slow (chord changes every 4-8 beats)"
        else:
            return "moderate (chord changes every 2-4 beats)"
    
    def _suggest_texture(self, mood: str, energy_level: int) -> str:
        """Suggest musical texture based on parameters."""
        if energy_level >= 7:
            return "polyphonic (multiple independent melodic lines)"
        elif mood == "calm":
            return "homophonic (melody with accompaniment)"
        else:
            return "melody-dominated homophony (clear melody with supporting harmony)"
    
    def _determine_style(self, mood: str, energy_level: int) -> str:
        """Determine overall musical style."""
        style_map = {
            ("happy", "high"): "upbeat pop/rock",
            ("happy", "medium"): "folk/acoustic",
            ("happy", "low"): "gentle ballad",
            ("sad", "high"): "emotional rock/alternative",
            ("sad", "medium"): "melancholic indie",
            ("sad", "low"): "ambient/atmospheric",
            ("calm", "high"): "new age/meditative",
            ("calm", "medium"): "ambient/chillout",
            ("calm", "low"): "drone/minimal",
            ("energetic", "high"): "electronic/dance",
            ("energetic", "medium"): "rock/pop-rock",
            ("energetic", "low"): "indie/alternative",
            ("mysterious", "high"): "dark electronic",
            ("mysterious", "medium"): "cinematic/film score",
            ("mysterious", "low"): "dark ambient",
            ("romantic", "high"): "passionate ballad",
            ("romantic", "medium"): "romantic pop",
            ("romantic", "low"): "intimate acoustic"
        }
        
        energy_category = "high" if energy_level >= 7 else "medium" if energy_level >= 4 else "low"
        return style_map.get((mood, energy_category), "contemporary instrumental")
    
    def _determine_complexity(self, energy_level: int, num_instruments: int) -> str:
        """Determine arrangement complexity."""
        complexity_score = (energy_level / 10) + (num_instruments / 10)
        
        if complexity_score >= 0.8:
            return "high (complex arrangement with multiple layers)"
        elif complexity_score >= 0.5:
            return "medium (balanced arrangement with good variety)"
        else:
            return "low (simple, focused arrangement)"
    
    def _suggest_duration(self, mood: str, energy_level: int) -> str:
        """Suggest composition duration."""
        if mood in ["energetic"] and energy_level >= 7:
            return "2-3 minutes (high energy, shorter attention span)"
        elif mood in ["calm", "mysterious"] and energy_level <= 4:
            return "4-6 minutes (ambient, longer development)"
        else:
            return "3-4 minutes (standard song length)"