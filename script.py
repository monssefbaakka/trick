
import os
import shutil

# Replace org.trcky.trick with org.trcky.trick
OLD_DOT = "org.trcky.trick"
NEW_DOT = "org.trcky"
OLD_SLASH = "org/trcky/trick"
NEW_SLASH = "org/trcky"
OLD_COM = "net.discdd"
NEW_COM = "org.trcky"

base_dir = r"c:\Users\Monssef\trick"

# Files to skip
skip_dirs = {".git", ".gradle", "build", "target", ".idea", "node_modules", "gradle"}
skip_exts = {".jar", ".so", ".class", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".pack", ".idx"}

# 1. First find all files and do string replacement
for root, dirs, files in os.walk(base_dir):
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    for file in files:
        if file.endswith(tuple(skip_exts)): continue
        file_path = os.path.join(root, file)
        
        # skip script itself
        if "script.py" in file_path: continue
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if OLD_DOT in content or OLD_SLASH in content or OLD_COM in content:
                # We replace org.trcky.trick -> org.trcky
                new_content = content.replace(OLD_DOT, NEW_DOT).replace("net.discdd", "org.trcky").replace(OLD_SLASH, NEW_SLASH)
                with open(file_path, "w", encoding="utf-8", newline="") as f:
                    f.write(new_content)
                print(f"Updated content: {file_path}")
        except Exception as e:
            print(f"Could not read {file_path}: {e}")

# 2. Rename directories: org/trcky/trick -> org/trcky
# Actually we need a more methodical approach since we are replacing 3 levels with 2 levels.
# We will find any folder named "trick" whose parent is "discdd", whose parent is "net"
import pathlib

for p in sorted(pathlib.Path(base_dir).rglob("*"), reverse=True):
    if p.is_dir() and p.name == "trick" and p.parent.name == "discdd" and p.parent.parent.name == "net":
        # Check if org/trcky/trick is currently holding files
        # We need to move the contents of org/trcky/trick to a new location org/trcky
        net_dir = p.parent.parent
        parent_of_net = net_dir.parent
        
        new_dir = parent_of_net / "org" / "trcky"
        new_dir.mkdir(parents=True, exist_ok=True)
        
        # move contents of track to trcky
        for item in p.iterdir():
            shutil.move(str(item), str(new_dir / item.name))
        
        # now remove org/trcky/trick if empty
        try:
            p.rmdir()
            p.parent.rmdir()
            net_dir.rmdir()
        except:
            pass
        print(f"Moved directory {p} to {new_dir}")
        continue

