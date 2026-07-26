from __future__ import annotations

import importlib
import os
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def status(ok: bool, label: str, detail: str = "") -> bool:
    mark = "OK" if ok else "WARN"
    suffix = f" - {detail}" if detail else ""
    print(f"[{mark}] {label}{suffix}")
    return ok


def check_import(module_name: str) -> bool:
    try:
        module = importlib.import_module(module_name)
    except Exception as exc:
        return status(False, f"import {module_name}", str(exc))

    version = getattr(module, "__version__", "installed")
    return status(True, f"import {module_name}", str(version))


def check_path(path: str, label: str | None = None) -> bool:
    target = ROOT / path
    return status(target.exists(), label or path, str(target))


def check_zip(path: str) -> bool:
    target = ROOT / path
    if not target.exists():
        return status(False, path, "missing")
    if not zipfile.is_zipfile(target):
        preview = target.read_text(errors="ignore")[:160].replace("\n", " ")
        return status(False, path, f"not a zip file: {preview}")
    return status(True, path, "valid zip file")


def main() -> int:
    print(f"Python: {sys.version.split()[0]}")
    print(f"Executable: {sys.executable}")
    print(f"Project: {ROOT}")
    print()

    checks = [
        check_import("torch"),
        check_import("ultralytics"),
        check_import("cv2"),
        check_import("numpy"),
        check_import("yaml"),
        check_import("dotenv"),
        check_import("roboflow"),
        check_import("kaggle"),
        check_path("data.yaml", "pretrain data.yaml"),
        check_path("train/images", "pretrain train images"),
        check_path("valid/images", "pretrain valid images"),
        check_path("test/images", "pretrain test images"),
        check_path(
            "runs/detect/onion_project/pretrain_mitosis/weights/best.pt",
            "pretrained best.pt",
        ),
        check_path(".env", ".env with ROBOFLOW_API_KEY"),
        check_zip("dataset_onion/roboflow.zip"),
    ]

    try:
        import torch

        mps_available = torch.backends.mps.is_available()
        status(mps_available, "torch MPS backend", "available" if mps_available else "CPU fallback")
    except Exception as exc:
        status(False, "torch MPS backend", str(exc))

    print()
    if all(checks):
        print("Environment is ready.")
        return 0

    print("Environment is usable, but warnings above need attention for full training.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
