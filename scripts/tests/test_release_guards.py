"""Offline negative controls for publication targeting and metadata drift."""

import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("release_metadata", ROOT / "scripts/check_release_metadata.py")
GUARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GUARD)


class ReleaseGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        for filename in (
            "TRAJECTORY_IDENTITY_PAPER.md", "CITATION.cff", ".zenodo.json",
            "scripts/check_release_metadata.py", "scripts/publish-to-zenodo.sh",
        ):
            shutil.copyfile(ROOT / filename, self.root / filename)
        self.manuscript = self.root / "TRAJECTORY_IDENTITY_PAPER.md"
        self.cff = self.root / "CITATION.cff"
        self.zenodo = self.root / ".zenodo.json"
        self.metadata = json.loads(self.zenodo.read_text())
        self.tag = self.metadata["version"]

    def rewrite_json(self, key, value):
        metadata = json.loads(self.zenodo.read_text())
        metadata[key] = value
        self.zenodo.write_text(json.dumps(metadata))

    def rewrite(self, file, old, new):
        text = file.read_text()
        self.assertIn(old, text)
        file.write_text(text.replace(old, new, 1))

    def test_current_metadata_and_tag_agree(self):
        version = json.loads(self.zenodo.read_text())["version"]
        GUARD.check(self.root, version)

    def test_title_version_date_and_abstract_drift_each_fail(self):
        originals = {p: p.read_text() for p in (self.manuscript, self.cff, self.zenodo)}
        mutations = (
            (self.manuscript, r"^# .+$", "# Another Title"),
            (self.manuscript, r"^\*\*Version:\*\* .+$", "**Version:** 9.99"),
            (self.manuscript, r"^\*\*Date:\*\* .+$", "**Date:** January 1, 1900"),
            (self.manuscript, r"^## Abstract\n\n", "## Abstract\n\nChanged abstract. "),
            (self.cff, r"^title: .+$", 'title: "Another Title"'),
            (self.cff, r"^version: .+$", 'version: "v9.99"'),
            (self.cff, r"^date-released: .+$", "date-released: 1900-01-01"),
            (self.cff, r"^abstract: >\n", "abstract: >\n  Changed abstract.\n"),
        )
        for file, pattern, new in mutations:
            with self.subTest(file=file.name, field=pattern):
                changed, count = re.subn(pattern, new, originals[file], count=1, flags=re.MULTILINE)
                self.assertEqual(count, 1)
                file.write_text(changed)
                with self.assertRaises(ValueError):
                    GUARD.check(self.root)
                file.write_text(originals[file])
        for key, value in (
            ("title", "Another Title"), ("version", "paper-v9.99"),
            ("publication_date", "1900-01-01"),
            ("description", self.metadata["description"] + "<p>Changed abstract.</p>"),
        ):
            with self.subTest(file=self.zenodo.name, field=key):
                self.rewrite_json(key, value)
                with self.assertRaises(ValueError):
                    GUARD.check(self.root)
                self.zenodo.write_text(originals[self.zenodo])

    def test_wrong_tag_concept_or_supplement_fails(self):
        with self.assertRaisesRegex(ValueError, "requested release tag"):
            GUARD.check(self.root, "paper-v9.99")
        original = self.cff.read_text()
        self.rewrite(self.cff, 'doi: "10.5281/zenodo.20098168"', 'doi: "10.5281/zenodo.19647159"')
        with self.assertRaisesRegex(ValueError, "concept DOI"):
            GUARD.check(self.root)
        self.cff.write_text(original)
        self.rewrite(self.zenodo, f"/tree/{self.tag}", "/tree/paper-v0.0-stale")
        with self.assertRaisesRegex(ValueError, "supplement"):
            GUARD.check(self.root)

    def test_missing_metadata_or_unsupported_cff_is_not_a_pass(self):
        self.rewrite(self.cff, "abstract: >", "abstract: |")
        with self.assertRaises(ValueError):
            GUARD.check(self.root)
        self.cff.unlink()
        with self.assertRaises(OSError):
            GUARD.check(self.root)

    def publish(self, override=None, response=None, tag=None, complete=False):
        # Only curl is replaced. All requests are recorded locally; the fake
        # executable has no network implementation, including on a regression.
        if shutil.which("jq") is None:
            self.fail("jq is required for the publisher's offline tests")
        bin_dir = self.root / "bin"
        bin_dir.mkdir(exist_ok=True)
        fake_curl = bin_dir / "curl"
        fake_curl.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, sys\n"
            "args = sys.argv[1:]\n"
            "method = args[args.index('-X') + 1] if '-X' in args else ('PUT' if '--upload-file' in args else 'GET')\n"
            "urls = [arg for arg in args if arg.startswith('https://')]\n"
            "body = json.loads(args[args.index('-d') + 1]) if '-d' in args else None\n"
            "with open(os.environ['CURL_LOG'], 'a') as log:\n"
            "    log.write(json.dumps({'method': method, 'urls': urls, **({'body': body} if body else {})}) + '\\n')\n"
            "if urls[0].endswith('/versions/latest'):\n"
            "    print(os.environ['FAKE_ZENODO_RESPONSE'])\n"
            "elif os.environ['FAKE_COMPLETE'] != '1':\n"
            "    sys.exit(99)\n"
            "elif '--upload-file' in args:\n"
            "    print('200')\n"
            "else:\n"
            "    print(json.dumps({'links': {'latest_draft': 'https://zenodo.invalid/api/deposit/depositions/99999', 'bucket': 'https://zenodo.invalid/api/files/offline-bucket', 'record_html': 'https://zenodo.invalid/records/99999'}, 'files': [], 'doi': '10.5281/zenodo.99999'}))\n"
            "    print('200')\n"
        )
        fake_curl.chmod(0o755)
        pdf = self.root / "paper.pdf"
        pdf.write_bytes(b"offline placeholder; never uploaded")
        log = self.root / "curl.log"
        if log.exists():
            log.unlink()
        env = os.environ.copy()
        env.pop("ZENODO_CONCEPT_RECID", None)
        env.update({
            "PATH": str(bin_dir) + os.pathsep + env["PATH"],
            "ZENODO_TOKEN": "offline-test-token",
            "ZENODO_API_BASE": "https://zenodo.invalid",
            "DRY_RUN": "0" if complete else "1",
            "FAKE_COMPLETE": "1" if complete else "0",
            "CURL_LOG": str(log),
            "FAKE_ZENODO_RESPONSE": json.dumps(response if response is not None else {
                "id": 23337710, "conceptrecid": "20098168",
                "metadata": {"version": "an-older-version"},
            }),
        })
        if override is not None:
            env["ZENODO_CONCEPT_RECID"] = override
        # A foreign cwd with conflicting metadata must not redirect this script.
        foreign_cwd = self.root / "other-project"
        foreign_cwd.mkdir(exist_ok=True)
        (foreign_cwd / ".zenodo.json").write_text('{"title":"wrong project"}')
        expected_tag = json.loads(self.zenodo.read_text())["version"]
        result = subprocess.run(
            ["bash", str(self.root / "scripts/publish-to-zenodo.sh"), tag or expected_tag, str(pdf)],
            cwd=foreign_cwd, env=env, capture_output=True, text=True, timeout=15,
        )
        calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
        return result, calls

    def test_unset_or_correct_override_reads_only_this_concept(self):
        for override in (None, "20098168"):
            with self.subTest(override=override):
                result, calls = self.publish(override)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(calls, [{
                    "method": "GET",
                    "urls": ["https://zenodo.invalid/api/records/20098168/versions/latest"],
                }])
                self.assertIn("would POST", result.stdout)

    def test_wrong_or_empty_override_fails_before_any_request(self):
        for override in ("19647159", "", "20098168/other"):
            with self.subTest(override=override):
                result, calls = self.publish(override)
                self.assertEqual(result.returncode, 64)
                self.assertIn("requires ZENODO_CONCEPT_RECID=20098168", result.stderr)
                self.assertEqual(calls, [])

    def test_missing_or_wrong_remote_target_fails_before_mutation(self):
        for response in (
            {"id": 23337710},
            {"id": 23337710, "conceptrecid": "19647159"},
            {"conceptrecid": "20098168"},
            {"id": "not-a-record", "conceptrecid": "20098168"},
            {"id": 0, "conceptrecid": "20098168"},
        ):
            with self.subTest(response=response):
                result, calls = self.publish(response=response)
                self.assertEqual(result.returncode, 70, result.stderr)
                self.assertEqual([call["method"] for call in calls], ["GET"])
                self.assertNotIn("would POST", result.stdout)

    def test_metadata_drift_or_wrong_tag_blocks_even_a_read_request(self):
        result, calls = self.publish(tag="paper-v9.99")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(calls, [])
        self.rewrite(self.cff, 'title: "', 'title: "Changed title: ')
        result, calls = self.publish()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(calls, [])

    def test_offline_publish_preserves_reviewed_metadata_from_foreign_cwd(self):
        # Use a historical date so a regression to today's date cannot pass.
        self.manuscript.write_text(re.sub(
            r"^\*\*Date:\*\* .+$", "**Date:** January 1, 1900",
            self.manuscript.read_text(), flags=re.MULTILINE,
        ))
        self.cff.write_text(re.sub(
            r"^date-released: .+$", "date-released: 1900-01-01",
            self.cff.read_text(), flags=re.MULTILINE,
        ))
        self.rewrite_json("publication_date", "1900-01-01")
        result, calls = self.publish(complete=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        payloads = [call["body"] for call in calls if "body" in call]
        self.assertEqual(payloads, [{"metadata": json.loads(self.zenodo.read_text())}])
        self.assertEqual(calls[-1]["method"], "POST")
        self.assertTrue(calls[-1]["urls"][0].endswith("/actions/publish"))


if __name__ == "__main__":
    unittest.main()
