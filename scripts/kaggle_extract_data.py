import os
from pathlib import Path

script_dir = Path(__file__).resolve().parent
project_dir = script_dir.parent
os.environ.setdefault("KAGGLE_CONFIG_DIR", str(script_dir))

import kaggle

kaggle.api.authenticate()

raw_dir = project_dir / "data" / "raw"
raw_dir.mkdir(parents=True, exist_ok=True)
kaggle.api.dataset_download_files(
	"bwandowando/dpwh-flood-control-projects",
	path=str(raw_dir),
	unzip=True,
)
print(f"Dataset downloaded and extracted to {raw_dir}")