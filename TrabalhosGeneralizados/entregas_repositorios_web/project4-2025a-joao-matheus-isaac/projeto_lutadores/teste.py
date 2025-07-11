import os

with open("imports.txt", "w", encoding="utf-8") as out_file:
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.strip().startswith("import ") or line.strip().startswith("from "):
                            out_file.write(line)