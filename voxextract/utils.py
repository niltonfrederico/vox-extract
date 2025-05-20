from pathlib import Path
import librosa

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


def visualize_results(file_path, isolated_audio, sr, timestamps):
    """Visualize original and filtered spectrograms with vocalization markers"""
    # Load original audio
    y, sr = librosa.load(file_path, sr=sr)

    plt.figure(figsize=(12, 10))

    # Original spectrogram
    plt.subplot(2, 1, 1)
    d_orig = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    img = librosa.display.specshow(d_orig, x_axis="time", y_axis="log", sr=sr)
    plt.colorbar(img, format="%+2.0f dB")
    plt.title("Original Spectrogram")

    # Mark detected vocalizations on original spectrogram
    for start, end in timestamps:
        plt.axvline(x=start, color="r", linestyle="--", alpha=0.7)
        plt.axvline(x=end, color="r", linestyle="--", alpha=0.7)

    # Filtered spectrogram
    plt.subplot(2, 1, 2)
    d_filtered = librosa.amplitude_to_db(
        np.abs(librosa.stft(isolated_audio)), ref=np.max
    )
    img = librosa.display.specshow(d_filtered, x_axis="time", y_axis="log", sr=sr)
    plt.colorbar(img, format="%+2.0f dB")
    plt.title("Filtered Spectrogram (Isolated Monkey Vocalization)")

    plt.tight_layout()
    plt.show()


def save_results(file_path, isolated_audio, sr, timestamps):
    """Visualize original and filtered spectrograms with vocalization markers"""

    # Extract the base filename to use as folder name

    # Convert file_path to Path object if it's a string
    if isinstance(file_path, str):
        file_path = Path(file_path)

    # Get the base name without extension
    folder_name = file_path.stem

    # Create folder if it doesn't exist
    output_dir = Path(folder_name)
    output_dir.mkdir(exist_ok=True)

    # Load original audio
    y, sr = librosa.load(file_path, sr=sr)

    # Save the original audio as sample.wav in the folder
    wavfile.write(output_dir / "sample.wav", sr, (y * 32767).astype(np.int16))

    # Save the filtered audio as filtered.wav in the folder
    wavfile.write(
        output_dir / "filtered.wav", sr, (isolated_audio * 32767).astype(np.int16)
    )

    # Compute spectrograms once
    d_orig = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    d_filtered = librosa.amplitude_to_db(
        np.abs(librosa.stft(isolated_audio)), ref=np.max
    )

    # Create figure for original spectrogram
    plt.figure(figsize=(12, 5))
    img = librosa.display.specshow(d_orig, x_axis="time", y_axis="log", sr=sr)
    plt.colorbar(img, format="%+2.0f dB")
    plt.title("Original Spectrogram")

    # Mark detected vocalizations on original spectrogram
    for start, end in timestamps:
        plt.axvline(x=start, color="r", linestyle="--", alpha=0.7)
        plt.axvline(x=end, color="r", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(output_dir / "original_spectrogram.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Create figure for filtered spectrogram
    plt.figure(figsize=(12, 5))
    img = librosa.display.specshow(d_filtered, x_axis="time", y_axis="log", sr=sr)
    plt.colorbar(img, format="%+2.0f dB")
    plt.title("Filtered Spectrogram (Isolated Monkey Vocalization)")

    plt.tight_layout()
    plt.savefig(output_dir / "filtered_spectrogram.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Create the combined visualization
    plt.figure(figsize=(12, 10))

    # Original spectrogram
    plt.subplot(2, 1, 1)
    img = librosa.display.specshow(d_orig, x_axis="time", y_axis="log", sr=sr)
    plt.colorbar(img, format="%+2.0f dB")
    plt.title("Original Spectrogram")

    # Mark detected vocalizations on original spectrogram
    for start, end in timestamps:
        plt.axvline(x=start, color="r", linestyle="--", alpha=0.7)
        plt.axvline(x=end, color="r", linestyle="--", alpha=0.7)

    # Filtered spectrogram
    plt.subplot(2, 1, 2)
    img = librosa.display.specshow(d_filtered, x_axis="time", y_axis="log", sr=sr)
    plt.colorbar(img, format="%+2.0f dB")
    plt.title("Filtered Spectrogram (Isolated Monkey Vocalization)")

    plt.tight_layout()
    plt.savefig(output_dir / "combined_spectrograms.png", dpi=300, bbox_inches="tight")
    plt.close()  # Close the figure instead of showing it
