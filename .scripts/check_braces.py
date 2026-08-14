import os
import re
import sys

base = os.path.abspath(os.path.join(os.path.dirname(__file__)))
# try a few common locations for the Pedals folder
candidates = [
    os.path.join(base, 'Pedals'),
    os.path.join(base, '..', 'Pedals'),
    os.path.join(base, '..', 'pedals-vst-main', 'Pedals'),
    os.path.join(base, '..', '..', 'Pedals'),
]
root = None
for c in candidates:
    if os.path.isdir(c):
        root = os.path.abspath(c)
        break
if root is None:
    print('Could not locate Pedals folder. Tried:', candidates)
    sys.exit(2)
checks = []

for dirpath, dirnames, filenames in os.walk(root):
    # only inspect folders named 'Source' or files under a 'Source' folder
    if os.path.basename(dirpath).lower() != 'source':
        continue
    for fname in filenames:
        if not (fname.endswith('.cpp') or fname.endswith('.h')):
            continue
        path = os.path.join(dirpath, fname)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                txt = f.read()
        except Exception as e:
            checks.append((path, 'read-error', str(e)))
            continue
        open_braces = txt.count('{')
        close_braces = txt.count('}')
        if open_braces != close_braces:
            checks.append((path, 'brace-mismatch', open_braces, close_braces))
            continue
        # heuristic: #endif followed by a function/class start with no intervening '{'
        m = re.search(r'#endif\s*\n\s*([A-Za-z0-9_:*\s]+?)\s*\(', txt)
        if m:
            idx = m.start()
            prev = txt[max(0, idx-120):idx]
            if '{' not in prev and '}' not in prev:
                checks.append((path, 'endif-then-func', m.group(1).strip()))

if not checks:
    print('OK: no issues found in Pedals Source files')
else:
    for c in checks:
        print(c)