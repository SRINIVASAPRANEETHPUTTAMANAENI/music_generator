"""
Audio Processing Module for AI Music Composition
Handles audio conversion, normalization, format conversion and visualization
"""

import logging
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf
import io
from typing import Dict, List, Optional, Tuple, Any, Union
from pydub import AudioSegment
import scipy.io.wavfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioProcessor:
    """
    Audio processing class for handling audio conversion, normalization and visualization
    """

    def __init__(self):
        """Initialize AudioProcessor"""
        logger.info("Initializing AudioProcessor...")
        self.temp_files = []  # Track temporary files for cleanup

    def normalize_audio(
        self, 
        audio_array: np.ndarray, 
        target_rms: float = 0.1,
        max_gain_db: float = 20.0
    ) -> np.ndarray:
        """
        Normalize audio to target RMS level

        Args:
            audio_array (np.ndarray): Input audio array
            target_rms (float): Target RMS level (0-1)
            max_gain_db (float): Maximum gain in dB

        Returns:
            np.ndarray: Normalized audio array
        """
        try:
            if len(audio_array) == 0:
                return audio_array

            # Calculate current RMS
            current_rms = np.sqrt(np.mean(audio_array ** 2))

            if current_rms == 0:
                logger.warning("Audio has zero RMS, returning original")
                return audio_array

            # Calculate required gain
            gain = target_rms / current_rms
            gain_db = 20 * np.log10(gain) if gain > 0 else 0

            # Limit maximum gain
            if gain_db > max_gain_db:
                gain = 10 ** (max_gain_db / 20)
                logger.warning(f"Limiting gain to {max_gain_db} dB")

            # Apply gain
            normalized_audio = audio_array * gain

            # Prevent clipping
            max_val = np.max(np.abs(normalized_audio))
            if max_val > 1.0:
                normalized_audio = normalized_audio / max_val
                logger.info("Applied anti-clipping normalization")

            logger.info(f"Audio normalized: RMS {current_rms:.4f} -> {np.sqrt(np.mean(normalized_audio ** 2)):.4f}")

            return normalized_audio.astype(np.float32)

        except Exception as e:
            logger.error(f"Error normalizing audio: {str(e)}")
            return audio_array

    def adjust_volume_by_energy(
        self, 
        audio_array: np.ndarray, 
        energy_level: int,
        base_volume: float = 0.7
    ) -> np.ndarray:
        """
        Adjust audio volume based on energy level (1-10 scale)

        Args:
            audio_array (np.ndarray): Input audio array
            energy_level (int): Energy level from mood analysis (1-10)
            base_volume (float): Base volume multiplier

        Returns:
            np.ndarray: Volume-adjusted audio array
        """
        try:
            # Map energy level to volume multiplier
            # Energy 1-3: Quieter, 4-6: Normal, 7-10: Louder
            if energy_level <= 3:
                volume_multiplier = base_volume * 0.6  # Quieter
            elif energy_level <= 6:
                volume_multiplier = base_volume  # Normal
            else:
                volume_multiplier = base_volume * 1.3  # Louder

            adjusted_audio = audio_array * volume_multiplier

            # Prevent clipping
            max_val = np.max(np.abs(adjusted_audio))
            if max_val > 1.0:
                adjusted_audio = adjusted_audio / max_val

            logger.info(f"Volume adjusted for energy level {energy_level}: multiplier = {volume_multiplier:.2f}")

            return adjusted_audio.astype(np.float32)

        except Exception as e:
            logger.error(f"Error adjusting volume: {str(e)}")
            return audio_array

    def tensor_to_wav_bytes(
        self, 
        audio_array: np.ndarray, 
        sample_rate: int
    ) -> bytes:
        """
        Convert audio array to WAV bytes

        Args:
            audio_array (np.ndarray): Audio array
            sample_rate (int): Sample rate

        Returns:
            bytes: WAV file bytes
        """
        try:
            # Create a BytesIO buffer
            wav_buffer = io.BytesIO()

            # Convert float32 to int16 for WAV compatibility
            if audio_array.dtype == np.float32:
                # Scale and convert to int16
                audio_int16 = (audio_array * 32767).astype(np.int16)
            else:
                audio_int16 = audio_array.astype(np.int16)

            # Write WAV data to buffer
            scipy.io.wavfile.write(wav_buffer, sample_rate, audio_int16)
            wav_bytes = wav_buffer.getvalue()

            logger.info(f"Converted audio to WAV: {len(wav_bytes)} bytes")
            return wav_bytes

        except Exception as e:
            logger.error(f"Error converting to WAV bytes: {str(e)}")
            # Return empty bytes as fallback
            return b''

    def wav_to_mp3_bytes(
        self, 
        wav_bytes: bytes,
        bitrate: str = "128k"
    ) -> bytes:
        """
        Convert WAV bytes to MP3 bytes using pydub

        Args:
            wav_bytes (bytes): WAV file bytes
            bitrate (str): MP3 bitrate

        Returns:
            bytes: MP3 file bytes
        """
        try:
            if not wav_bytes:
                return b''

            # Load WAV from bytes
            wav_buffer = io.BytesIO(wav_bytes)
            audio_segment = AudioSegment.from_wav(wav_buffer)

            # Export to MP3
            mp3_buffer = io.BytesIO()
            audio_segment.export(
                mp3_buffer, 
                format="mp3", 
                bitrate=bitrate,
                parameters=["-q:a", "2"]  # High quality
            )

            mp3_bytes = mp3_buffer.getvalue()
            logger.info(f"Converted to MP3: {len(mp3_bytes)} bytes at {bitrate} bitrate")

            return mp3_bytes

        except Exception as e:
            logger.error(f"Error converting to MP3: {str(e)}")
            return wav_bytes  # Return WAV bytes as fallback

    def process_generated_audio(
        self,
        audio_array: np.ndarray,
        sample_rate: int,
        energy_level: int = 5,
        output_format: str = "mp3"
    ) -> Dict[str, Any]:
        """
        Complete audio processing pipeline

        Args:
            audio_array (np.ndarray): Generated audio array
            sample_rate (int): Sample rate
            energy_level (int): Energy level for volume adjustment
            output_format (str): Output format ("wav" or "mp3")

        Returns:
            Dict containing processed audio data and metadata
        """
        try:
            logger.info("Starting audio processing pipeline...")

            # Step 1: Normalize audio
            normalized_audio = self.normalize_audio(audio_array)

            # Step 2: Adjust volume based on energy level
            volume_adjusted_audio = self.adjust_volume_by_energy(normalized_audio, energy_level)

            # Step 3: Convert to WAV bytes
            wav_bytes = self.tensor_to_wav_bytes(volume_adjusted_audio, sample_rate)

            # Step 4: Convert to requested format
            if output_format.lower() == "mp3":
                final_bytes = self.wav_to_mp3_bytes(wav_bytes)
                mime_type = "audio/mp3"
                file_extension = "mp3"
            else:
                final_bytes = wav_bytes
                mime_type = "audio/wav"
                file_extension = "wav"

            # Calculate audio statistics
            duration = len(volume_adjusted_audio) / sample_rate
            max_amplitude = np.max(np.abs(volume_adjusted_audio))
            rms_level = np.sqrt(np.mean(volume_adjusted_audio ** 2))

            result = {
                "audio_bytes": final_bytes,
                "processed_array": volume_adjusted_audio,
                "sample_rate": sample_rate,
                "duration": duration,
                "max_amplitude": float(max_amplitude),
                "rms_level": float(rms_level),
                "file_size": len(final_bytes),
                "format": output_format,
                "mime_type": mime_type,
                "file_extension": file_extension,
                "energy_level": energy_level
            }

            logger.info(f"Audio processing complete: {duration:.2f}s, {len(final_bytes)} bytes")
            return result

        except Exception as e:
            logger.error(f"Error in audio processing pipeline: {str(e)}")
            # Return minimal fallback result
            return {
                "audio_bytes": b'',
                "processed_array": audio_array,
                "sample_rate": sample_rate,
                "duration": len(audio_array) / sample_rate if len(audio_array) > 0 else 0,
                "max_amplitude": 0.0,
                "rms_level": 0.0,
                "file_size": 0,
                "format": "wav",
                "mime_type": "audio/wav",
                "file_extension": "wav",
                "energy_level": energy_level,
                "error": str(e)
            }

    def create_waveform_plot(
        self,
        audio_array: np.ndarray,
        sample_rate: int,
        title: str = "Generated Music Waveform"
    ) -> bytes:
        """
        Create waveform visualization plot

        Args:
            audio_array (np.ndarray): Audio array to visualize
            sample_rate (int): Sample rate
            title (str): Plot title

        Returns:
            bytes: PNG image bytes of the plot
        """
        try:
            # Create figure
            plt.figure(figsize=(12, 4))

            # Use librosa for better waveform display
            librosa.display.waveshow(
                audio_array, 
                sr=sample_rate,
                alpha=0.8,
                color='#1f77b4'
            )

            plt.title(title, fontsize=14, pad=20)
            plt.xlabel('Time (seconds)', fontsize=12)
            plt.ylabel('Amplitude', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()

            # Save to bytes
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_bytes = img_buffer.getvalue()

            # Clean up
            plt.close()

            logger.info("Waveform plot created successfully")
            return img_bytes

        except Exception as e:
            logger.error(f"Error creating waveform plot: {str(e)}")
            # Create a simple fallback plot
            try:
                plt.figure(figsize=(12, 4))
                time_axis = np.linspace(0, len(audio_array) / sample_rate, len(audio_array))
                plt.plot(time_axis, audio_array, alpha=0.7)
                plt.title(title)
                plt.xlabel('Time (seconds)')
                plt.ylabel('Amplitude')
                plt.grid(True, alpha=0.3)
                plt.tight_layout()

                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
                img_bytes = img_buffer.getvalue()
                plt.close()

                return img_bytes
            except:
                return b''

    def get_audio_info(self, audio_array: np.ndarray, sample_rate: int) -> Dict[str, Any]:
        """
        Get comprehensive audio information

        Args:
            audio_array (np.ndarray): Audio array
            sample_rate (int): Sample rate

        Returns:
            Dict with audio analysis information
        """
        try:
            duration = len(audio_array) / sample_rate
            max_amplitude = np.max(np.abs(audio_array))
            rms_level = np.sqrt(np.mean(audio_array ** 2))

            # Basic spectral analysis using librosa
            spectral_centroids = librosa.feature.spectral_centroid(y=audio_array, sr=sample_rate)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_array, sr=sample_rate)[0]

            return {
                "duration_seconds": float(duration),
                "sample_rate": int(sample_rate),
                "total_samples": int(len(audio_array)),
                "max_amplitude": float(max_amplitude),
                "rms_level": float(rms_level),
                "dynamic_range_db": float(20 * np.log10(max_amplitude / (rms_level + 1e-10))),
                "spectral_centroid_mean": float(np.mean(spectral_centroids)),
                "spectral_rolloff_mean": float(np.mean(spectral_rolloff)),
                "zero_crossing_rate": float(np.mean(librosa.feature.zero_crossing_rate(audio_array)[0]))
            }

        except Exception as e:
            logger.error(f"Error analyzing audio: {str(e)}")
            return {
                "duration_seconds": len(audio_array) / sample_rate if len(audio_array) > 0 else 0,
                "sample_rate": sample_rate,
                "total_samples": len(audio_array),
                "max_amplitude": 0.0,
                "rms_level": 0.0,
                "error": str(e)
            }

    def cleanup_temp_files(self):
        """Clean up any temporary files created during processing"""
        for file_path in self.temp_files:
            try:
                import os
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Cleaned up temp file: {file_path}")
            except Exception as e:
                logger.error(f"Error cleaning up {file_path}: {str(e)}")

        self.temp_files.clear()
