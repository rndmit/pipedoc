from pathlib import Path
from config import *
from log import log
from module import process_module_group
from docindex import render_index


def main():
    log.name = "module"
    log.info(f"updating module docs in {ABS_MODULE_DOCS_DIR}")
    for group_name in LIB_GROUPS:
        process_module_group(group_name, ABS_MODULE_DOCS_DIR)
    log.name = "index"
    render_index(ABS_DOC_INDEX_PATH, ABS_RAW_DOC_DIR, ABS_MODULE_DOCS_DIR)

if __name__ == "__main__":
    main()