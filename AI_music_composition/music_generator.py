"""
Music Generation Engine for AI Music Composition
Integrates MusicGen model for text-to-music generation
"""

import logging
import torch
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MusicGenerator:
    """
    Main music generation engine using MusicGen from Hugging Face
    """

    def __init__(self, model_name: str = "facebook/musicgen-small"):
        """
        Initialize the MusicGenerator with specified model

        Args:
            model_name (str): Hugging Face model name for MusicGen
        """
        self.model_name = model_name
        self.model = None
        self.processor = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.sample_rate = None

        logger.info(f"Initializing MusicGenerator with {model_name}")
        logger.info(f"Using device: {self.device}")

        # Load models
        self._load_models()

    def _load_models(self):
        """Load MusicGen model and processor"""
        try:
            logger.info("Loading MusicGen processor...")
            self.processor = AutoProcessor.from_pretrained(self.model_name)

            logger.info("Loading MusicGen model...")
            self.model = MusicgenForConditionalGeneration.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32  # Use float32 for better compatibility
            )

            # Move model to device
            self.model = self.model.to(self.device)

            # Get sample rate from model config
            self.sample_rate = self.model.config.audio_encoder.sampling_rate

            logger.info(f"Models loaded successfully!")
            logger.info(f"Sample rate: {self.sample_rate}")

        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            raise RuntimeError(f"Failed to load MusicGen models: {str(e)}")

    def generate_text_prompt(self, musical_parameters: Dict[str, Any]) -> str:
        """
        Convert musical parameters to text prompt for MusicGen

        Args:
            musical_parameters (Dict): Musical parameters from mood analysis

        Returns:
            str: Text prompt for music generation
        """
        try:
            # Extract key parameters
            mood = musical_parameters.get('mood', 'calm')
            tempo = musical_parameters.get('tempo', 100)
            key = musical_parameters.get('key', 'major')
            energy = musical_parameters.get('energy', 5)
            instruments = musical_parameters.get('instruments', ['piano'])
            sentiment = musical_parameters.get('sentiment', 'neutral')

            # Build prompt components
            prompt_parts = []

            # Add mood and sentiment
            if mood == 'happy' and sentiment == 'positive':
                prompt_parts.append("upbeat happy cheerful")
            elif mood == 'sad' and sentiment == 'negative':
                prompt_parts.append("melancholic sad emotional")
            elif mood == 'calm':
                prompt_parts.append("calm peaceful relaxing")
            elif mood == 'energetic':
                prompt_parts.append("energetic dynamic powerful")
            elif mood == 'mysterious':
                prompt_parts.append("mysterious dark atmospheric")
            elif mood == 'romantic':
                prompt_parts.append("romantic tender loving")
            else:
                prompt_parts.append(f"{mood} {sentiment}")

            # Add tempo indication
            if tempo >= 140:
                prompt_parts.append("fast tempo")
            elif tempo >= 120:
                prompt_parts.append("moderate tempo")
            elif tempo >= 80:
                prompt_parts.append("medium tempo")
            else:
                prompt_parts.append("slow tempo")

            # Add key signature
            if key == 'major':
                prompt_parts.append("in major key")
            else:
                prompt_parts.append("in minor key")

            # Add instruments (limit to top 3)
            top_instruments = instruments[:3] if len(instruments) > 3 else instruments
            instrument_text = []

            for instrument in top_instruments:
                if instrument == 'electric_guitar':
                    instrument_text.append("electric guitar")
                elif instrument == 'acoustic_guitar':
                    instrument_text.append("acoustic guitar")
                elif instrument == 'soft_strings':
                    instrument_text.append("strings")
                elif instrument == 'ambient_pads':
                    instrument_text.append("ambient pads")
                else:
                    instrument_text.append(instrument)

            if instrument_text:
                prompt_parts.append(f"with {' and '.join(instrument_text)}")

            # Add energy level description
            if energy >= 8:
                prompt_parts.append("high energy intense")
            elif energy >= 6:
                prompt_parts.append("moderate energy")
            elif energy <= 3:
                prompt_parts.append("low energy gentle")

            # Combine all parts
            full_prompt = " ".join(prompt_parts)

            # Ensure prompt is not too long (MusicGen has token limits)
            if len(full_prompt) > 200:
                full_prompt = full_prompt[:200]

            logger.info(f"Generated prompt: {full_prompt}")
            return full_prompt

        except Exception as e:
            logger.error(f"Error generating text prompt: {str(e)}")
            return "calm instrumental music"  # Fallback prompt

    def generate_music(
        self, 
        musical_parameters: Dict[str, Any],
        duration: float = 30.0,
        guidance_scale: float = 3.0,
        do_sample: bool = True
    ) -> Tuple[np.ndarray, int]:
        """
        Generate music from musical parameters

        Args:
            musical_parameters (Dict): Musical parameters from mood analysis
            duration (float): Duration in seconds (max 30 for small model)
            guidance_scale (float): Guidance scale for generation
            do_sample (bool): Whether to use sampling

        Returns:
            Tuple[np.ndarray, int]: Generated audio array and sample rate
        """
        try:
            if self.model is None or self.processor is None:
                raise RuntimeError("Models not loaded. Please initialize the generator first.")

            # Generate text prompt
            text_prompt = self.generate_text_prompt(musical_parameters)

            logger.info(f"Generating music for: {text_prompt}")
            logger.info(f"Duration: {duration}s, Guidance: {guidance_scale}")

            # Process text input
            inputs = self.processor(
                text=[text_prompt],
                padding=True,
                return_tensors="pt",
            ).to(self.device)

            # Calculate max_new_tokens based on duration
            # MusicGen generates at 50 Hz, so tokens per second = 50
            max_new_tokens = int(duration * 50)  # 50 tokens per second
            max_new_tokens = min(max_new_tokens, 1503)  # Limit for small model

            logger.info(f"Generating {max_new_tokens} tokens...")

            # Set generation parameters on model
            self.model.generation_config.guidance_scale = guidance_scale
            self.model.generation_config.do_sample = do_sample
            self.model.generation_config.max_new_tokens = max_new_tokens

            # Generate audio
            with torch.no_grad():
                audio_values = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    guidance_scale=guidance_scale,
                    do_sample=do_sample
                )

            # Convert to numpy array
            audio_array = audio_values[0, 0].cpu().numpy()

            logger.info(f"Generated audio shape: {audio_array.shape}")
            logger.info(f"Audio duration: {len(audio_array) / self.sample_rate:.2f}s")

            return audio_array, self.sample_rate

        except Exception as e:
            logger.error(f"Error generating music: {str(e)}")
            # Generate a simple fallback audio (silence)
            fallback_duration = min(duration, 10.0)  # Max 10s fallback
            silence_samples = int(fallback_duration * 22050)  # 22050 is common sample rate
            fallback_audio = np.zeros(silence_samples, dtype=np.float32)
            return fallback_audio, 22050

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return {
            "model_name": self.model_name,
            "device": str(self.device),
            "sample_rate": self.sample_rate,
            "model_loaded": self.model is not None,
            "processor_loaded": self.processor is not None
        }

    def set_generation_params(
        self,
        max_duration: float = 30.0,
        guidance_scale: float = 3.0,
        do_sample: bool = True
    ):
        """
        Set default generation parameters

        Args:
            max_duration (float): Maximum generation duration
            guidance_scale (float): Guidance scale for generation
            do_sample (bool): Whether to use sampling
        """
        self.max_duration = max_duration
        self.guidance_scale = guidance_scale
        self.do_sample = do_sample

        logger.info(f"Generation parameters set: duration={max_duration}s, guidance={guidance_scale}, sample={do_sample}")
