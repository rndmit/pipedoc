from os.path import relpath, basename, splitext
from string import Template
from pathlib import Path
from glob import glob
from pipedoc.log import log


INDEX_TPL = Template("""\
:toc:

== Module docs

$links

$includes
""")

def raw_includes(dir: Path) -> str:
    includes: str = ""
    pattern = Path(dir, "**.adoc")
    log.info(f"searching with pattern {pattern}")
    for file in sorted(glob(pattern.__str__(), recursive=True)):
        includes += f"include::{relpath(file, dir.parent)}[]\n\n"
        log.info(f"added include of {file}")
    return includes


def group_links(dir: Path) -> str:
    links: str = ""
    pattern = Path(dir, "**.adoc")
    log.info(f"searching with pattern {pattern}")
    for file in sorted(glob(pattern.__str__(), recursive=True)):
        path = relpath(file, dir.parent)
        links += f"* link:{path}[{splitext(basename(path))[0]}]\n\n"
        log.info(f"added link to {file}")
    return links


def render_index(path: Path, raw_doc_dir: Path, module_doc_dir: Path):
    with open(path, "w+") as output:
        log.info(f"updating index {path}")
        output.write(INDEX_TPL.substitute({
            "includes": raw_includes(raw_doc_dir),
            "links": group_links(module_doc_dir)
        }))