from argparse import ArgumentParser

from voxextract.extract import isolate_vocalization
from voxextract.utils import save_results, visualize_results


def parse_args() -> ArgumentParser:
    parser = ArgumentParser(
        description="Extract animal vocalizations from audio files."
    )
    parser.add_argument(
        "audio_file",
        type=str,
        help="Path to the input audio file (e.g., .wav, .mp3).",
    )
    parser.add_argument(
        "-hz",
        "--frequency_range",
        type=float,
        nargs=2,
        default=(4000, 11000),
        help="Frequency range for vocalization detection (in Hz).",
    )
    parser.add_argument(
        "-d",
        "--duration_range",
        type=float,
        nargs=2,
        default=(0.3, 3.0),
        help="Duration range for vocalization detection (in seconds).",
    )
    parser.add_argument(
        "-dB",
        "--threshold_db",
        type=int,
        default=-41,
        help="Threshold in dB for vocalization detection.",
    )
    parser.add_argument(
        "--save-only",
        action="store_true",
        help="Only save the isolated vocalization without visualization.",
    )

    return parser


def main():
    args = parse_args().parse_args()
    audio_file = args.audio_file
    frequency_range = tuple(args.frequency_range)
    duration_range = tuple(args.duration_range)
    threshold_db = args.threshold_db

    # Call the main function from the extract module
    isolated_vocalization, sr, timestamps = isolate_vocalization(
        audio_file,
        frequency_range=frequency_range,
        duration_range=duration_range,
        threshold_db=threshold_db,
    )

    save_results(audio_file, isolated_vocalization, sr, timestamps)

    # Visualize results
    if not args.save_only:
        visualize_results(audio_file, isolated_vocalization, sr, timestamps)
