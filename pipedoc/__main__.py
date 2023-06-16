from pathlib import Path
from pycli import Application, Command, Option, Values
from pipedoc.log import log
from pipedoc.module import process_module_group
from pipedoc.docindex import render_index


class Generate(Command):
    name = "generate"
    short = "run doc generation"

    _opt_lib_groups = Option[str]("lib_groups", ["-g", "--groups"], "library groups", default="")
    _opt_lib_dir = Option[str]("lib_dir", ["-l", "--lib_dir"], "path to lib dir", default="lib")
    _opt_doc_dir = Option[str]("doc_dir", ["-d", "--doc_dir"], "path to doc dir", default="docs")
    _opt_raw_dir = Option[str]("raw_dir", ["-r", "--raw_dir"], "raw doc dir name", default="raw")
    _opt_mod_dir = Option[str]("mod_dir", ["-m", "--mod_dir"], "modules doc dir name", default="modules")
    

    def exec(self, vals: Values) -> int:
        ABS_REPO_ROOT = Path(__file__).parent.parent
        ABS_LIB_DIR = Path(ABS_REPO_ROOT, vals.get(self._opt_lib_dir))
        ABS_DOCS_DIR = Path(ABS_REPO_ROOT, vals.get(self._opt_doc_dir))
        ABS_RAW_DOC_DIR = Path(ABS_DOCS_DIR, vals.get(self._opt_raw_dir))
        ABS_MODULE_DOCS_DIR = Path(ABS_DOCS_DIR, vals.get(self._opt_mod_dir))
        ABS_DOC_INDEX_PATH = Path(ABS_DOCS_DIR, "index").with_suffix(".adoc")

        log.name = "module"
        log.info(f"updating module docs in {ABS_MODULE_DOCS_DIR}")
        groups = vals.get(self._opt_lib_groups).split(",")
        for group_name in groups:
            process_module_group(group_name, ABS_MODULE_DOCS_DIR, ABS_LIB_DIR, ABS_REPO_ROOT)
        log.name = "index"
        render_index(ABS_DOC_INDEX_PATH, ABS_RAW_DOC_DIR, ABS_MODULE_DOCS_DIR)
        return 0


if __name__ == "__main__":
    rc = Application(
        name="pipedoc",
        descr="Pipeline docstrings tool",
    ).with_commands(
        Generate()
    ).run()
    if rc != 0:
        log.critical(f"non-zero exit code: {rc}")
    exit(rc)