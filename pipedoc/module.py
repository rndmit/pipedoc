from typing import Optional
import os
import re
from glob import glob
from pathlib import Path
from pipedoc.log import log


class ModuleBodyNotFoundErr(Exception):
    def __str__(self) -> str:
        return "file doesn't contains module body"


class ModuleOption(object):
    variable: str
    vartype: str
    descr: str
    default: str

    def __init__(self, variable: str, descr: str, default: str) -> None:
        self.variable = variable
        self.vartype = self.determine_vartype(default)
        self.descr = descr
        self.default = default

    @staticmethod
    def determine_vartype(str) -> str:
        str=str.strip()
        if len(str) == 0: return 'none'
        if re.match(r'^True$|^False$|^0$|^1$', str):
            return 'bool'
        if re.match(r'([-+]\s*)?\d+[lL]?$', str): 
            return 'int'
        if re.match(r'([-+]\s*)?[1-9][0-9]*\.?[0-9]*([Ee][+-]?[0-9]+)?$', str): 
            return 'float'
        if re.match(r'([-+]\s*)?[0-9]*\.?[0-9][0-9]*([Ee][+-]?[0-9]+)?$', str): 
            return 'float'
        return 'string' 


class PipelineModule(object):
    relpath: str
    name: str
    doc: Optional[str]
    opts: Optional[list[ModuleOption]]

    def __init__(self, repo_root: Path, path: str,  name: str, doc: Optional[str] = None, opts: Optional[list[ModuleOption]] = None) -> None:
        self.relpath = os.path.relpath(path, repo_root)
        self.name = name
        self.doc = doc
        self.opts = opts

    def __str__(self) -> str:
        content = f"""\
== {self.name}\n
`include path: {self.relpath}`\n
{self.doc}
"""
        if self.opts:
            optsdoc = "\n".join([ 
                f"|{opt.variable} |{opt.vartype} |{opt.default} |{opt.descr}"
                for opt in self.opts
            ])
            content += f"""\
=== Options
|===
|Variable |Type |Default |Description
{optsdoc}
|===
""" 
        return content + "\n"
    
    @classmethod
    def from_source(cls, repo_root: Path, path: str):
        with open(path, "r+") as source:
            content = source.readlines()
            name = cls.read_module_name(content)
            mod = PipelineModule(
                repo_root,
                path, 
                name, 
                doc=cls.read_docstrings(content),
                opts=cls.read_options(content)
            )
            return mod

    @staticmethod
    def read_module_name(content: list[str]) -> str:
        for line in content:
            if line.strip().startswith("."):
                return line.replace(":", "").strip()
        raise ModuleBodyNotFoundErr()
    
    @staticmethod
    def read_docstrings(content: list[str]) -> str:
        docstrings: str = ""
        for line in content:
            if line.startswith("---"):
                break
            if not line.strip().startswith("#"):
                continue
            docstrings += line.replace("#", "", 1).replace(" ", "", 1)
        return docstrings
    
    @staticmethod
    def read_options(content: list[str]) -> list[ModuleOption]:
        opts: list[ModuleOption] = []
        varregex = re.compile(r"^(?P<name>[A-Z0-9_]+):\s+(?P<defval>.+)$")
        for idx, line in enumerate(content):
            if not line.strip().startswith("#!opt"):
                continue
            descr = line.replace("#!opt:", "").strip()
            optvar = varregex.search(content[idx + 1].strip())
            if optvar is None:
                raise Exception(f"unable to parse option at pos {idx + 1}") 
            opts.append(ModuleOption(
                variable=optvar.group("name"),
                default=optvar.group("defval"),
                descr=descr
            ))
        return opts
    
def find_sources(pattern: Path) -> list[str]:
    sources: list[str] = []
    log.info(f"searching with pattern {pattern}")
    for file in glob(pattern.__str__(), recursive=True):
        log.info(f"processing {file}")
        sources.append(file)
    return sources


def parse(sources: list[str], repo_root: Path) -> list[PipelineModule]:
    modules: list[PipelineModule] = []
    for srcpath in sources:
        modules.append(PipelineModule.from_source(repo_root, srcpath))
    return modules


def process_module_group(name: str, outdir: Path, lib_dir: Path, repo_root: Path):
    log.info(f"processing group {name}")
    modules = parse(
        find_sources(Path(lib_dir, name, "**.yaml")),
        repo_root
    )
    outpath = Path(outdir, name).with_suffix(".adoc")
    with open(outpath, "w+t") as output:
        log.info(f"writing doc to {outpath}")
        output.write(":toc:\n:toclevels: 2\n\n")
        for mod in modules:
            output.write(mod.__str__())