from pathlib import Path

import librosa
import numpy as np


def apply_wiener_filter(
    stft_magnitude: np.ndarray,
    stft_phase: np.ndarray,
    noise_estimate: np.ndarray,
    noise_threshold: float = 0.01,
) -> np.ndarray:
    """Apply Wiener filter without excessive suppression."""

    wiener_gain = np.maximum(1 - noise_estimate / (stft_magnitude + noise_threshold), 0)
    filtered_magnitude = stft_magnitude * wiener_gain

    return filtered_magnitude * stft_phase


def load_and_preprocess(audio_file: Path, n_fft: int, hop_length: int):
    """Load audio and compute STFT with magnitude and phase"""
    y, sr = librosa.load(audio_file, sr=None)
    stft = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    stft_magnitude, stft_phase = librosa.magphase(stft)
    noise_estimate = np.mean(stft_magnitude, axis=1, keepdims=True)
    filtered_stft_magnitude = apply_wiener_filter(
        stft_magnitude,
        stft_phase,
        noise_estimate=np.broadcast_to(noise_estimate, stft_magnitude.shape),
    )
    stft_magnitude_db = librosa.amplitude_to_db(
        np.abs(filtered_stft_magnitude), ref=np.max
    )

    freq_bins = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    times = librosa.times_like(stft_magnitude, sr=sr, hop_length=hop_length)

    return y, sr, stft_magnitude, stft_phase, stft_magnitude_db, freq_bins, times


def create_frequency_mask(stft_magnitude, freq_bins, frequency_range):
    """Create frequency mask with buffer."""
    mask = np.zeros_like(stft_magnitude, dtype=bool)
    max_freq = frequency_range[1]
    freq_buffer = 0.1 * max_freq  # 10% buffer
    for i, freq in enumerate(freq_bins):
        if frequency_range[0] <= freq <= max_freq + freq_buffer:
            mask[i, :] = True
    return mask


def identify_vocalization_segments(
    stft_magnitude_db, mask, threshold_db, times, duration_range, hop_length, sr
):
    """Identify vocalization segments based on threshold and duration"""
    vocalization_mask = np.zeros_like(stft_magnitude_db, dtype=bool)
    vocalization_mask[mask] = stft_magnitude_db[mask] > threshold_db

    # Find slices by energy
    time_activity = np.any(vocalization_mask, axis=0)

    # Identify contiguous segments
    activity_diff = np.diff(time_activity.astype(int), prepend=0)
    start_indices = np.nonzero(activity_diff == 1)[0]
    end_indices = np.nonzero(activity_diff == -1)[0]

    # Handle case where audio ends with vocalization
    if len(start_indices) > 0 and (
        len(end_indices) == 0 or start_indices[-1] > end_indices[-1]
    ):
        end_indices = np.append(end_indices, len(times) - 1)

    # Filter by duration
    timestamps = []
    for start, end in zip(start_indices, end_indices):
        start_time = times[start]
        # Dynamically determine padding based on signal characteristics
        fade_out_duration = 0.02  # Default value
        end_padding = int(fade_out_duration * sr / hop_length)
        end_time = times[min(end + end_padding, len(times) - 1)]
        _duration = end_time - start_time
        if duration_range[0] <= _duration <= duration_range[1]:
            timestamps.append((start_time, end_time))

    return timestamps


def create_full_mask(
    stft_magnitude, timestamps, times, freq_bins, frequency_range, hop_length, sr
):
    """Create a full mask with fade out padding."""
    full_mask = np.zeros_like(stft_magnitude)
    fade_out_padding = int(0.02 * sr / hop_length)  # Pad in samples

    for start_time, end_time in timestamps:
        start_index = np.argmin(np.abs(times - start_time))
        end_index = np.argmin(np.abs(times - end_time))
        end_index_padded = min(
            int(end_index + fade_out_padding), int(stft_magnitude.shape[1])
        )

        for i, freq in enumerate(freq_bins):
            if frequency_range[0] <= freq <= frequency_range[1]:
                full_mask[i, start_index:end_index_padded] = 1

    return full_mask


def isolate_vocalization(
    audio_file: Path,
    frequency_range: tuple[int, int],
    duration_range: tuple[float, float],
    n_fft: int = 2048,
    hop_length: int = 512,
    threshold_db: int = -20,
    fade_duration: float = 0.3,
) -> tuple[np.ndarray, float, list[tuple[float, float]]]:
    """
    Isolate monkey vocalizations in an audio file based on frequency and duration ranges.

    Returns:
        tuple: (isolated audio, sample rate, list of timestamps)
    """
    # Load and preprocess audio
    y, sr, stft_magnitude, stft_phase, stft_magnitude_db, freq_bins, times = (
        load_and_preprocess(audio_file, n_fft, hop_length)
    )

    # Create frequency mask
    mask = create_frequency_mask(stft_magnitude, freq_bins, frequency_range)

    # Identify vocalization segments
    timestamps = identify_vocalization_segments(
        stft_magnitude_db, mask, threshold_db, times, duration_range, hop_length, sr
    )

    # Create full mask for the vocalization segments
    full_mask = create_full_mask(
        stft_magnitude, timestamps, times, freq_bins, frequency_range, hop_length, sr
    )

    # Apply the mask to get isolated vocalization
    stft_filtered = stft_magnitude * full_mask * stft_phase

    # Inverse STFT to get the isolated vocalization
    y_isolated = librosa.istft(stft_filtered, hop_length=hop_length)

    # Apply fade in/out
    fade_samples = int(fade_duration * sr)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)

    y_isolated[:fade_samples] = y_isolated[:fade_samples] * fade_in
    y_isolated[-fade_samples:] = y_isolated[-fade_samples:] * fade_out

    # Ensure the output is the same length as the original audio
    if len(y_isolated) > len(y):
        y_isolated = y_isolated[: len(y)]
    else:
        y_isolated = np.pad(y_isolated, (0, len(y) - len(y_isolated)))

    return y_isolated, sr, timestamps
