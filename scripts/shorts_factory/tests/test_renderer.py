from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.shorts_factory.captions import build_ass_captions
from scripts.shorts_factory.qa import verify_render
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


class CaptionTests(unittest.TestCase):
    def test_karaoke_cards_are_safe_and_three_to_five_words(self) -> None:
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
            self.assertIn("MarginV", text)
            events = [line for line in text.splitlines() if line.startswith("Dialogue:")]
            self.assertGreaterEqual(len(events), 2)
            for event in events:
                payload = event.split(",", 9)[-1]
                visible = re.sub(r"\{[^}]*\}", "", payload).replace(r"\N", " ")
                count = len(visible.split())
                self.assertGreaterEqual(count, 3)
                self.assertLessEqual(count, 5)
                self.assertLessEqual(payload.count(r"\N"), 1)
            self.assertNotIn("{UNSAFE}", text)

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
        self.assertEqual(manifest["version"], 2)
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
