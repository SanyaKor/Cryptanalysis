import nbformat
import re
import importlib.metadata


EXCLUDED_LIBS = {
    'basis_reduction_2d',
    'LLL',
    'NTRU'
}

IMPORT_RE = re.compile(r'^\s*(?:import|from)\s+([a-zA-Z_][\w]*)')

FILES_TO_SCAN = [
    "LLL.ipynb",
    "NTRU.ipynb",
    "Exercises.ipynb",
    "basis_reduction_2d.ipynb",
    "requirements.py"
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
    all_code = "\n".join(cell.source for cell in nb.cells if cell.cell_type == 'code')
    return extract_imports_from_code(all_code)

def scan_py_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return extract_imports_from_code(f.read())


all_imports = set()
for file in FILES_TO_SCAN:
    if file.endswith(".ipynb"):
        all_imports.update(scan_notebook(file))
    elif file.endswith(".py"):
        all_imports.update(scan_py_file(file))


req_lines = []
for lib in sorted(all_imports):
    try:
        version = importlib.metadata.version(lib)
        req_lines.append(f"{lib}=={version}")
    except importlib.metadata.PackageNotFoundError:
        req_lines.append(lib)  # без версии


with open("requirements.txt", "w") as f:
    f.write("\n".join(req_lines) + "\n")

print("✅ requirements.txt created from explicit file list:")
for line in req_lines:
    print(" -", line)