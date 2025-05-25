import nbformat
import re
import importlib.metadata
import os

EXCLUDED_LIBS = {
    "lattice_methods",
    "tests",
    "os",
    "re",
    "importlib"
}

IMPORT_RE = re.compile(r'^\s*(?:import|from)\s+([a-zA-Z_][\w]*)')

# 🔽 Укажи папки и файлы, которые надо просканировать
SCAN_PATHS = [
    "../lattice_methods/",
    "../notebooks/",
    "../tools/requirements.py"
]

def extract_imports_from_code(source):
    imports = set()
    for line in source.splitlines():
        match = IMPORT_RE.match(line)
        if match:
            lib = match.group(1)
            if lib and not lib.startswith((".", "_")) and lib not in EXCLUDED_LIBS:
                imports.add(lib)
    return imports

def scan_notebook(path):
    nb = nbformat.read(path, as_version=4)
    code = "\n".join(cell.source for cell in nb.cells if cell.cell_type == 'code')
    return extract_imports_from_code(code)

def scan_py_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return extract_imports_from_code(f.read())

def walk_paths(paths):
    all_imports = set()
    for path in paths:
        path = os.path.abspath(path)
        if os.path.isfile(path):
            if path.endswith(".ipynb"):
                all_imports.update(scan_notebook(path))
            elif path.endswith(".py"):
                all_imports.update(scan_py_file(path))
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    full = os.path.join(root, file)
                    if file.endswith(".ipynb"):
                        all_imports.update(scan_notebook(full))
                    elif file.endswith(".py"):
                        all_imports.update(scan_py_file(full))
    return all_imports


all_imports = walk_paths(SCAN_PATHS)

req_lines = []
for lib in sorted(all_imports):
    try:
        version = importlib.metadata.version(lib)
        req_lines.append(f"{lib}=={version}")
    except importlib.metadata.PackageNotFoundError:
        req_lines.append(lib)  # просто имя без версии

with open("../requirements.txt", "w") as f:
    f.write("\n".join(req_lines) + "\n")

print("✅ requirements.txt generated:")
for line in req_lines:
    print(" -", line)