# Codex Notes

## Environment

- Use the local virtual environment at `.venv` when it exists.
- If a fresh environment is needed, run:

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

- Validate the setup with:

```bash
.venv/bin/python scripts/check_environment.py
```

## Project Commands

- Pretrain YOLO on the mitosis dataset:

```bash
.venv/bin/python train_pretrain.py
```

- Fine-tune on the onion dataset:

```bash
.venv/bin/python train_finetunning.py
```

- Run inference on a test image:

```bash
.venv/bin/python pretest.py
```

## Notes

- Keep `.env` private. Use `.env.example` as the template for `ROBOFLOW_API_KEY`.
- Large model weights, datasets, and training outputs are intentionally ignored by Git.
- The checked-in code expects the pretrained weight at `runs/detect/onion_project/pretrain_mitosis/weights/best.pt`.
