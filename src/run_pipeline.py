import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

SCRIPTS = [
    "src/data_generation.py",
    "src/eda.py",
    "src/optimization.py",
    "src/mapping.py",
    "src/modeling.py",
    "src/reporting.py",
]


def run_script(script_path):
    full_path = PROJECT_ROOT / script_path
    print(f"\nRunning: {script_path}")

    result = subprocess.run(
        [sys.executable, str(full_path)],
        cwd=PROJECT_ROOT,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Script failed: {script_path}")

    print(f"Finished: {script_path}")


def main():
    print("Starting full delivery route optimization pipeline...")

    for script in SCRIPTS:
        run_script(script)

    print("\nPipeline completed successfully.")
    print("All project stages were executed in sequence.")


if __name__ == "__main__":
    main()
