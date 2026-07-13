from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from scripts.shorts_factory.captions import (
    CAPTION_FONT_SIZE,
    CAPTION_OUTLINE,
    CAPTION_SIDE_MARGIN,
    DEFAULT_PLAY_RES_X,
    _caption_layout,
    _group_words,
    _normalise_words,
    _text_width_px,
    build_ass_captions,
)
from scripts.shorts_factory.errors import ManifestError
from scripts.shorts_factory.graphics import (
    GRAPHICS_MANIFEST_VERSION,
    load_visual_replacements,
    replacements_for_clip,
)
from scripts.shorts_factory.qa import _validate_captions, sha256_file, verify_render
from scripts.shorts_factory.render import render_clip, render_input_fingerprint
from scripts.shorts_factory.vision import (
    build_static_analysis,
    run_visual_analysis,
    validate_visual_analysis,
)


VEGA_PYTHON = Path(
    "/Users/taylordasch_1/dasch-command/agents/vega/clipper/.venv/bin/python"
)


def _make_source(
    path: Path,
    *,
    duration_s: float = 10.4,
    audio_duration_s: float | None = None,
) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise unittest.SkipTest("ffmpeg is not installed")
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"testsrc2=size=320x180:rate=30:duration={duration_s}",
            "-f",
            "lavfi",
            "-i",
            (
                "sine=frequency=440:sample_rate=48000"
                + (f":duration={audio_duration_s}" if audio_duration_s else "")
            ),
            "-t",
            str(duration_s),
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            str(path),
        ],
        check=True,
        capture_output=True,
    )


def _make_color_source(path: Path, *, color: str, duration_s: float = 10.4) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise unittest.SkipTest("ffmpeg is not installed")
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={color}:size=320x180:rate=30:duration={duration_s}",
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency=440:sample_rate=48000:duration={duration_s}",
            "-t",
            str(duration_s),
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            str(path),
        ],
        check=True,
        capture_output=True,
    )


def _make_vertical_asset(
    path: Path,
    *,
    color: str = "blue",
    duration_s: float = 2.0,
) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise unittest.SkipTest("ffmpeg is not installed")
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={color}:size=1080x1920:rate=30:duration={duration_s}",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(path),
        ],
        check=True,
        capture_output=True,
    )


def _sample_rgb(path: Path, time_s: float) -> tuple[int, int, int]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise unittest.SkipTest("ffmpeg is not installed")
    result = subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            str(time_s),
            "-i",
            str(path),
            "-frames:v",
            "1",
            "-vf",
            "format=rgb24,crop=1:1:100:100",
            "-f",
            "rawvideo",
            "pipe:1",
        ],
        check=True,
        capture_output=True,
    )
    if len(result.stdout) < 3:
        raise AssertionError("could not sample rendered pixel")
    return tuple(result.stdout[:3])  # type: ignore[return-value]


class CaptionTests(unittest.TestCase):
    def test_karaoke_cards_are_safe_and_two_to_four_words(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "clip.ass"
            words = [
                {
                    "word": "{unsafe}" if index == 0 else f"word{index}",
                    "start": 20.0 + index * 0.36,
                    "end": 20.0 + index * 0.36 + 0.28,
                }
                for index in range(11)
            ]
            result = build_ass_captions(
                words,
                destination,
                clip_start_s=20.0,
                clip_end_s=24.5,
            )

            text = destination.read_text(encoding="utf-8")
            self.assertEqual(result["word_count"], 11)
            self.assertIn("PlayResX: 1080", text)
            self.assertIn("PlayResY: 1920", text)
            self.assertIn("Style: Karaoke,Avenir Next Condensed Heavy,92", text)
            self.assertIn("MarginV", text)
            events = [line for line in text.splitlines() if line.startswith("Dialogue:")]
            self.assertGreaterEqual(len(events), 2)
            for event in events:
                payload = event.split(",", 9)[-1]
                visible = re.sub(r"\{[^}]*\}", "", payload).replace(r"\N", " ")
                count = len(visible.split())
                self.assertGreaterEqual(count, 2)
                self.assertLessEqual(count, 4)
                self.assertLessEqual(payload.count(r"\N"), 1)
                self.assertEqual(payload.count(r"{\c&H0000D7FF&}"), 1)
            self.assertNotIn("{UNSAFE}", text)

    def test_long_caption_cards_hold_a_stable_layout_per_spoken_word(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "long.ass"
            words = [
                {"word": word, "start": index * 0.3, "end": index * 0.3 + 0.25}
                for index, word in enumerate(
                    ["EXTRATERRITORIAL", "JURISDICTION", "CHANGES", "TAXES"]
                )
            ]
            build_ass_captions(words, destination)
            events = [
                line
                for line in destination.read_text(encoding="utf-8").splitlines()
                if line.startswith("Dialogue:")
            ]
            self.assertEqual(len(events), 4)
            visible_layouts = {
                re.sub(r"\{[^}]*\}", "", event.split(",", 9)[-1])
                for event in events
            }
            self.assertEqual(len(visible_layouts), 2)
            self.assertEqual(
                sorted(Counter(
                    re.sub(r"\{[^}]*\}", "", event.split(",", 9)[-1])
                    for event in events
                ).values()),
                [2, 2],
            )
            for event in events:
                payload = event.split(",", 9)[-1]
                self.assertLessEqual(payload.count(r"\N"), 1)
                self.assertEqual(payload.count(r"{\c&H0000D7FF&}"), 1)

    def test_known_overflow_phrases_fit_the_measured_safe_width(self) -> None:
        safe_width = float(
            DEFAULT_PLAY_RES_X - 2 * CAPTION_SIDE_MARGIN - 2 * CAPTION_OUTLINE
        )
        for phrase in (
            "ESTABLISHED NEIGHBORHOODS LIKE CANYON",
            "OR THE EXTRATERRITORIAL JURISDICTION",
        ):
            group = [
                {"word": word, "start": index * 0.25, "end": index * 0.25 + 0.2}
                for index, word in enumerate(phrase.split())
            ]
            groups = _group_words(
                group,
                min_words=2,
                max_words=4,
                safe_width_px=safe_width,
            )
            for card in groups:
                font_size, line_break_at = _caption_layout(
                    card,
                    max_lines=2,
                    safe_width_px=safe_width,
                )
                words = [str(item["word"]) for item in card]
                lines = (
                    [" ".join(words)]
                    if not line_break_at
                    else [
                        " ".join(words[:line_break_at]),
                        " ".join(words[line_break_at:]),
                    ]
                )
                self.assertGreaterEqual(font_size, 80)
                self.assertLessEqual(font_size, CAPTION_FONT_SIZE)
                self.assertLessEqual(
                    max(_text_width_px(line, font_size=font_size) for line in lines),
                    safe_width + 1.0,
                )

    def test_natural_two_word_card_passes_render_qa(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "two-words.ass"
            build_ass_captions(
                [
                    {"word": "NO", "start": 0.0, "end": 0.3},
                    {"word": "WAY.", "start": 0.3, "end": 0.7},
                ],
                destination,
                min_words=2,
                max_words=4,
            )
            self.assertEqual(_validate_captions(destination), [])

    def test_numeric_fragments_never_split_across_caption_cards(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "numbers.ass"
            words = [
                {"word": "$350", "start": 1.0, "end": 1.3},
                {"word": ",000", "start": 1.3, "end": 1.6},
                {"word": "budget", "start": 1.6, "end": 1.9},
                {"word": "is", "start": 1.9, "end": 2.1},
                {"word": "different", "start": 2.1, "end": 2.5},
                {"word": "at", "start": 2.5, "end": 2.7},
                {"word": "2", "start": 2.7, "end": 2.9},
                {"word": ".39", "start": 2.9, "end": 3.1},
                {"word": "%", "start": 3.1, "end": 3.2},
            ]
            build_ass_captions(words, destination)
            text = destination.read_text(encoding="utf-8")
            visible = re.sub(r"\{[^}]*\}", "", text)
            self.assertIn("$350,000", visible)
            self.assertIn("2.39%", visible)
            self.assertNotRegex(visible, r"(?:^|\\N|\s),000(?:\s|$)")

    def test_transcript_fragments_merge_into_readable_tokens(self) -> None:
        tokens = ["$350", ",000,", "2", ".0%.", "13", "-minute", "non", "-answer"]
        words = [
            {"word": token, "start": index * 0.2, "end": index * 0.2 + 0.18}
            for index, token in enumerate(tokens)
        ]
        normalised = _normalise_words(
            words,
            clip_start_s=0.0,
            clip_end_s=None,
        )
        self.assertEqual(
            [word["word"] for word in normalised],
            ["$350,000,", "2.0%.", "13-MINUTE", "NON-ANSWER"],
        )

    def test_terminal_single_word_card_never_leaks_into_next_sentence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "terminal.ass"
            build_ass_captions(
                [
                    {"word": "GONE.", "start": 0.0, "end": 0.35},
                    {"word": "THAT", "start": 0.55, "end": 0.8},
                    {"word": "MATTERS.", "start": 0.8, "end": 1.2},
                ],
                destination,
            )
            events = [
                line
                for line in destination.read_text(encoding="utf-8").splitlines()
                if line.startswith("Dialogue:")
            ]
            visible = [
                re.sub(r"\{[^}]*\}", "", event.split(",", 9)[-1]).replace(r"\N", " ")
                for event in events
            ]
            self.assertEqual(visible[0], "GONE.")
            self.assertNotIn("GONE. THAT", visible)
            self.assertEqual(_validate_captions(destination), [])


class VisualPlanTests(unittest.TestCase):
    def test_static_plan_has_bounded_crop_track(self) -> None:
        plan = build_static_analysis(
            width=1920,
            height=1080,
            duration_s=20.0,
            mode="face_crop",
            center_x=0.98,
            center_y=0.5,
        )
        self.assertEqual(validate_visual_analysis(plan), [])
        for point in plan["crop_track"]:
            crop = point["crop"]
            self.assertLessEqual(crop["x"] + crop["width"], 1.00001)
            self.assertLessEqual(crop["y"] + crop["height"], 1.00001)

        plan["crop_track"][0]["crop"]["x"] = 1.2
        self.assertTrue(validate_visual_analysis(plan))


class GraphicsManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.asset = cls.root / "vertical.mp4"
        _make_vertical_asset(cls.asset)
        cls.asset_sha = sha256_file(cls.asset)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def _write_manifest(self, *, source_sha: str = "a" * 64) -> Path:
        manifest = self.root / "visual-replacements.json"
        manifest.write_text(
            json.dumps(
                {
                    "schema_version": GRAPHICS_MANIFEST_VERSION,
                    "source_sha256": source_sha,
                    "replacements": [
                        {
                            "id": "annual-tax",
                            "source_start_s": 2.0,
                            "source_end_s": 6.0,
                            "asset_path": self.asset.name,
                            "asset_sha256": self.asset_sha,
                            "timing_mode": "hold_last",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return manifest

    def test_manifest_is_source_bound_and_partial_clip_keeps_asset_offset(self) -> None:
        manifest_path = self._write_manifest()
        loaded = load_visual_replacements(
            manifest_path,
            expected_source_sha256="a" * 64,
            source_duration_s=10.0,
        )
        replacements = replacements_for_clip(loaded, 4.0, 10.0)
        self.assertEqual(len(replacements), 1)
        self.assertEqual(replacements[0]["clip_start_s"], 0.0)
        self.assertEqual(replacements[0]["clip_end_s"], 2.0)
        self.assertEqual(replacements[0]["asset_start_s"], 2.0)

        with self.assertRaisesRegex(ManifestError, "different source"):
            load_visual_replacements(
                manifest_path,
                expected_source_sha256="b" * 64,
                source_duration_s=10.0,
            )

    def test_manifest_rejects_asset_checksum_changes(self) -> None:
        manifest_path = self._write_manifest()
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        payload["replacements"][0]["asset_sha256"] = "f" * 64
        manifest_path.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaisesRegex(ManifestError, "checksum mismatch"):
            load_visual_replacements(
                manifest_path,
                expected_source_sha256="a" * 64,
                source_duration_s=10.0,
            )


class RenderIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.source = cls.root / "source.mp4"
        _make_source(cls.source)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def test_analysis_uses_generated_fixture_without_downloaded_model(self) -> None:
        plan = run_visual_analysis(
            self.source,
            0.0,
            10.2,
            sample_period_s=5.0,
            max_samples=4,
        )
        self.assertEqual(validate_visual_analysis(plan), [])
        self.assertIn(
            plan["analysis_backend"],
            {"opencv-haar-saliency", "center_fallback", "decode_fallback"},
        )
        self.assertTrue(plan["segments"])

    def test_render_and_fail_closed_crop_qa(self) -> None:
        output = self.root / "delivery.mp4"
        words = [
            {
                "word": f"word{index}",
                "start": index * 0.40,
                "end": index * 0.40 + 0.32,
            }
            for index in range(24)
        ]
        manifest = render_clip(
            self.source,
            output,
            0.0,
            10.2,
            words=words,
            mode="center_crop",
            metadata={"preset": "ultrafast", "crf": 32},
        )
        self.assertEqual(manifest["status"], "verified")
        self.assertEqual(manifest["version"], 3)
        self.assertRegex(manifest["input_fingerprint"], r"^[0-9a-f]{64}$")
        self.assertTrue(manifest["qa"]["passed"])
        media = manifest["qa"]["media"]
        self.assertEqual((media["width"], media["height"]), (1080, 1920))
        self.assertEqual(media["video_codec"], "h264")
        self.assertEqual(media["audio_codec"], "aac")
        self.assertEqual(media["pixel_format"], "yuv420p")
        self.assertAlmostEqual(media["fps"], 30.0, places=2)

        changed_words = [*words, {"word": "changed", "start": 9.8, "end": 10.0}]
        self.assertNotEqual(
            manifest["input_fingerprint"],
            render_input_fingerprint(
                self.source,
                0.0,
                10.2,
                changed_words,
                "center_crop",
                {"preset": "ultrafast", "crf": 32},
            ),
        )

        crop_path = Path(manifest["sidecars"]["crop_track"])
        crop = json.loads(crop_path.read_text(encoding="utf-8"))
        crop["crop_track"][0]["crop"]["x"] = 1.2
        crop_path.write_text(json.dumps(crop), encoding="utf-8")
        failed = verify_render(output, 10.2, manifest["sha256"])
        self.assertFalse(failed["passed"])
        self.assertTrue(any("crop point" in error for error in failed["errors"]))

    def test_mixed_shot_modes_render_as_one_verified_clip(self) -> None:
        output = self.root / "mixed-modes.mp4"
        words = [
            {
                "word": f"mixed{index}",
                "start": index * 0.40,
                "end": index * 0.40 + 0.32,
            }
            for index in range(24)
        ]
        plan = build_static_analysis(
            width=320,
            height=180,
            duration_s=10.2,
            mode="face_crop",
        )
        plan["segments"] = [
            {
                "start_s": 0.0,
                "end_s": 5.0,
                "mode": "face_crop",
                "shot_index": 0,
                "crop_track": plan["crop_track"],
            },
            {
                "start_s": 5.0,
                "end_s": 10.2,
                "mode": "contain",
                "shot_index": 1,
                "crop_track": plan["crop_track"],
            },
        ]
        manifest = render_clip(
            self.source,
            output,
            0.0,
            10.2,
            words=words,
            mode="auto",
            metadata={
                "preset": "ultrafast",
                "crf": 32,
                "visual_analysis": plan,
            },
        )
        self.assertEqual(manifest["status"], "verified")
        self.assertEqual(manifest["segment_count"], 2)
        self.assertTrue(manifest["qa"]["passed"])

    def test_vertical_replacement_holds_last_frame_and_preserves_source_audio(self) -> None:
        source = self.root / "replacement-source.mp4"
        blue_asset = self.root / "replacement-blue.mp4"
        green_asset = self.root / "replacement-green.mp4"
        output = self.root / "replacement-delivery.mp4"
        manifest_path = self.root / "visual-replacements.json"
        _make_color_source(source, color="red")
        _make_vertical_asset(blue_asset, color="blue", duration_s=1.0)
        _make_vertical_asset(green_asset, color="green", duration_s=1.0)
        source_sha = sha256_file(source)
        blue_sha = sha256_file(blue_asset)
        green_sha = sha256_file(green_asset)
        manifest_path.write_text(
            json.dumps(
                {
                    "schema_version": GRAPHICS_MANIFEST_VERSION,
                    "source_sha256": source_sha,
                    "replacements": [
                        {
                            "id": "blue-card",
                            "source_start_s": 2.0,
                            "source_end_s": 4.0,
                            "asset_path": blue_asset.name,
                            "asset_sha256": blue_sha,
                            "timing_mode": "hold_last",
                        },
                        {
                            "id": "green-card",
                            "source_start_s": 4.0,
                            "source_end_s": 6.0,
                            "asset_path": green_asset.name,
                            "asset_sha256": green_sha,
                            "timing_mode": "hold_last",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        loaded = load_visual_replacements(
            manifest_path,
            expected_source_sha256=source_sha,
            source_duration_s=10.4,
        )
        replacements = replacements_for_clip(loaded, 0.0, 10.2)
        words = [
            {
                "word": f"graphic{index}",
                "start": index * 0.40,
                "end": index * 0.40 + 0.32,
            }
            for index in range(24)
        ]
        metadata = {
            "preset": "ultrafast",
            "crf": 32,
            "source_sha256": source_sha,
            "visual_replacements": replacements,
        }
        rendered = render_clip(
            source,
            output,
            0.0,
            10.2,
            words=words,
            mode="center_crop",
            metadata=metadata,
        )

        self.assertEqual(rendered["status"], "verified")
        self.assertEqual(rendered["version"], 3)
        self.assertEqual(rendered["visual_replacements"]["replacement_count"], 2)
        self.assertTrue(rendered["qa"]["passed"])
        self.assertEqual(rendered["qa"]["media"]["audio_codec"], "aac")
        self.assertIsNotNone(rendered["qa"]["sidecars"]["graphics"])
        self.assertNotEqual(
            rendered["input_fingerprint"],
            render_input_fingerprint(
                source,
                0.0,
                10.2,
                words,
                "center_crop",
                {"preset": "ultrafast", "crf": 32, "source_sha256": source_sha},
            ),
        )

        before = _sample_rgb(output, 1.0)
        blue_held = _sample_rgb(output, 3.0)
        green_held = _sample_rgb(output, 5.0)
        after = _sample_rgb(output, 7.0)
        self.assertGreater(before[0], before[2] + 100)
        self.assertGreater(blue_held[2], blue_held[0] + 100)
        self.assertGreater(green_held[1], green_held[0] + 40)
        self.assertGreater(green_held[1], green_held[2] + 40)
        self.assertGreater(after[0], after[2] + 100)

        graphics_path = Path(rendered["sidecars"]["graphics"])
        graphics_plan = json.loads(graphics_path.read_text(encoding="utf-8"))
        graphics_plan["replacements"][0]["asset_sha256"] = "f" * 64
        graphics_path.write_text(json.dumps(graphics_plan), encoding="utf-8")
        failed = verify_render(
            output,
            10.2,
            rendered["sha256"],
            captions_path=rendered["sidecars"]["captions"],
            crop_track_path=rendered["sidecars"]["crop_track"],
            graphics_plan_path=graphics_path,
            checksum_path=rendered["sidecars"]["checksum"],
        )
        self.assertFalse(failed["passed"])
        self.assertTrue(
            any("asset checksum" in error for error in failed["errors"]),
            failed["errors"],
        )

    def test_short_source_audio_is_padded_to_exact_video_span(self) -> None:
        source = self.root / "short-audio-source.mp4"
        output = self.root / "short-audio-delivery.mp4"
        _make_source(source, duration_s=10.4, audio_duration_s=9.65)
        words = [
            {"word": f"pad{index}", "start": index * 0.4, "end": index * 0.4 + 0.3}
            for index in range(24)
        ]
        manifest = render_clip(
            source,
            output,
            0.0,
            10.2,
            words=words,
            mode="center_crop",
            metadata={"preset": "ultrafast", "crf": 32},
        )
        self.assertTrue(manifest["qa"]["passed"])
        self.assertAlmostEqual(manifest["qa"]["media"]["duration_s"], 10.2, delta=0.1)


if __name__ == "__main__":
    unittest.main()
