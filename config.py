from pathlib import Path

LIB_DIR = "lib"
LIB_GROUPS = ["build", "deploy"]
DOCS_DIR = "docs"
MODULES_DIR = "modules"
RAW_DOC_DIR = "raw"

ABS_REPO_ROOT = Path(__file__).parent.parent
ABS_LIB_DIR = Path(ABS_REPO_ROOT, LIB_DIR)
ABS_DOCS_DIR = Path(ABS_REPO_ROOT, DOCS_DIR)
ABS_RAW_DOC_DIR = Path(ABS_DOCS_DIR, RAW_DOC_DIR)
ABS_MODULE_DOCS_DIR = Path(ABS_DOCS_DIR, MODULES_DIR)
ABS_DOC_INDEX_PATH = Path(ABS_DOCS_DIR, "index").with_suffix(".adoc")