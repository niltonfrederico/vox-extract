# VoxExtract - Animal Vocalization Isolation Tool

VoxExtract is a Python tool for isolating animal vocalizations from audio recordings. Originally designed for monkey vocalizations, the tool can be adapted for other species by adjusting frequency and duration parameters. Currently only setup is for monkeys of the species Callithrix penicillata, Callithrix aurita and C. penicillata-C. aurita hybrid.

## Features

- Isolate vocalizations based on custom frequency range and duration
- Visualize audio spectrograms with marked vocalization segments
- Save isolated vocalizations and visualization results
- Adjustable sensitivity through threshold parameters
- Command-line interface for easy batch processing

## Installation

```bash
# Clone the repository
git clone https://github.com/niltonfrederico/voxextract.git
cd voxextract

# Install dependencies
pip install librosa numpy matplotlib scipy

# or

poetry install

# Optional: Install in development mode
pip install -e .
```

## Dependencies

- Python 3.12+
- librosa - For audio processing and feature extraction
- numpy - For numerical operations
- matplotlib - For visualization
- scipy - For audio file I/O

## Usage

### Command Line Interface

```bash
# Basic usage
python -m voxextract /path/to/your/audio_file.wav

# Custom frequency range (in Hz)
python -m voxextract /path/to/your/audio_file.wav -hz 3000 8000

# Custom duration range (in seconds)
python -m voxextract /path/to/your/audio_file.wav -d 0.2 2.5

# Custom threshold (in dB)
python -m voxextract /path/to/your/audio_file.wav -dB -35

# Save without displaying visualizations
python -m voxextract /path/to/your/audio_file.wav --save-only
```

### Python API

```python
from voxextract import isolate_vocalization
from voxextract.utils import visualize_results, save_results

# Isolate vocalizations
audio_file = "path/to/audio.wav"
isolated_audio, sample_rate, timestamps = isolate_vocalization(
    audio_file,
    frequency_range=(4000, 10000),  # Hz
    duration_range=(0.3, 3.0),      # seconds
    threshold_db=-40
)

# Visualize results
visualize_results(audio_file, isolated_audio, sample_rate, timestamps)

# Save results (creates a folder with the audio filename)
save_results(audio_file, isolated_audio, sample_rate, timestamps)
```

## Parameters

| Parameter         | Description                                                    | Default       |
| ----------------- | -------------------------------------------------------------- | ------------- |
| `frequency_range` | Frequency range in Hz (min, max) for vocalization detection    | (4000, 10000) |
| `duration_range`  | Duration range in seconds (min, max) for vocalization segments | (0.3, 3.0)    |
| `threshold_db`    | Energy threshold in dB for detection                           | -40           |
| `n_fft`           | FFT window size for spectral analysis                          | 2048          |
| `hop_length`      | Hop length for STFT                                            | 512           |

## Output

For each processed audio file, VoxExtract creates a folder named after the audio file containing:

1. `sample.wav` - Original audio sample
2. `filtered.wav` - Isolated vocalization audio
3. `original_spectrogram.png` - Spectrogram of original audio with marked vocalizations
4. `filtered_spectrogram.png` - Spectrogram of isolated vocalizations
5. `combined_spectrograms.png` - Combined view of original and filtered spectrograms

## How It Works

1. The audio is loaded and converted to a spectrogram using Short-Time Fourier Transform (STFT)
2. A frequency mask is applied to focus on the target frequency range
3. Energy thresholding identifies potential vocalization segments
4. Duration filtering removes segments that are too short or too long
5. The identified segments are isolated from the original audio
6. Results are saved and/or visualized

## Processing Multiple Files

To process multiple audio files in a directory:

```bash
# Using bash to process all wav files in a directory
for file in /path/to/directory/*.wav; do
    python -m voxextract "$file"
done
```

## License

See [LICENSE](LICENSE) for details.

## Contributors

<!-- readme: contributors -start -->
<table>
	<tbody>
		<tr>
            <td align="center">
                <a href="https://github.com/niltonfrederico">
                    <img src="https://avatars.githubusercontent.com/u/9078708?v=4" width="100;" alt="niltonfrederico"/>
                    <br />
                    <sub><b>Nilton Frederico Teixeira</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/Rafamsa">
                    <img src="https://avatars.githubusercontent.com/u/139396742?v=4" width="100;" alt="Rafamsa"/>
                    <br />
                    <sub><b>Rafael Martins</b></sub>
                </a>
            </td>
		</tr>
	<tbody>
</table>
<!-- readme: contributors -end -->

## Contributing

Please see [CONTRIBUTE.md](CONTRIBUTE.md) for details on how to contribute to this project.

## Citation

If you use VoxExtract in your research (Let us now! We'll be happy to help!), please cite (the example is in ABNT style, but you can adapt it to your preferred citation style):

```
MARTINS-AFETO, R.S.; TEIXEIRA, N. F. VoxExtract. 2025. Disponível em: [https://github.com/niltonfrederico/voxextract](https://github.com/niltonfrederico/voxextract). Acesso em: 20 de maio de 2025.
```
