import json
import sys
from pathlib import Path

def ipynb_to_py(ipynb_file):
    ipynb_path = Path(ipynb_file)
    py_file = ipynb_path.with_suffix(".py")

    with ipynb_path.open("r", encoding="utf-8") as f:
        notebook = json.load(f)

    lines = []
    for cell in notebook["cells"]:
        if cell["cell_type"] == "markdown":
            for line in cell["source"]:
                lines.append("# " + line.rstrip())
            lines.append("")  # blank line
        elif cell["cell_type"] == "code":
            for line in cell["source"]:
                lines.append(line.rstrip())
            lines.append("")  # blank line

    py_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Converted {ipynb_file} → {py_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ipynb_to_py.py notebook.ipynb")
        sys.exit(1)
    ipynb_to_py(sys.argv[1])
 