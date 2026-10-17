import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).parents[1]


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExerciseContractTests(unittest.TestCase):
    def test_debug_configuration_launches_reproduction_tests(self) -> None:
        configuration = json.loads(
            (ROOT / "exercise" / ".vscode" / "launch.json").read_text()
        )

        self.assertEqual(
            configuration["configurations"][0]["name"],
            "Debug reproduction tests",
        )
        self.assertEqual(configuration["configurations"][0]["module"], "pytest")

    def test_bug_is_repeatable_and_reference_solution_passes(self) -> None:
        buggy = load_module("buggy", ROOT / "exercise" / "remove_negatives.py")
        correct = load_module(
            "correct", ROOT / "exercise_author" / "correct_remove_negatives.py"
        )
        sample = [4, -3, -2, 5]

        self.assertEqual(buggy.remove_negatives(sample.copy()), [4, -2, 5])
        self.assertEqual(buggy.remove_negatives(sample.copy()), [4, -2, 5])
        self.assertEqual(correct.remove_negatives(sample.copy()), [4, 5])

    def test_pytest_reproduces_bug_and_accepts_reference_solution(self) -> None:
        failed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=ROOT / "exercise",
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(failed.returncode, 1)
        self.assertIn("test_mixed_numbers", failed.stdout)
        self.assertIn("test_consecutive_negatives", failed.stdout)

        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            shutil.copy(
                ROOT / "exercise_author" / "correct_remove_negatives.py",
                workspace / "remove_negatives.py",
            )
            shutil.copytree(ROOT / "exercise" / "tests", workspace / "tests")
            passed = subprocess.run(
                [sys.executable, "-m", "pytest", "-q"],
                cwd=workspace,
                capture_output=True,
                check=False,
                text=True,
            )

        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)


if __name__ == "__main__":
    unittest.main()
