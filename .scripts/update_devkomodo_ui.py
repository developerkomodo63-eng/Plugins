import os
import re

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
modified = []
for dirpath, dirnames, filenames in os.walk(root):
    for fname in filenames:
        if fname == 'DevKomodoUI.h':
            path = os.path.join(dirpath, fname)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                txt = f.read()
            orig = txt
            changed = False
            # insert prettifyID if missing
            if 'prettifyID' not in txt:
                # find end of upper() function
                m = re.search(r"static\s+juce::String\s+upper\s*\([^\)]*\)\s*\{[^\}]*\}", txt, flags=re.S)
                if m:
                    insert_at = m.end()
                    prettify = '''\n\n    static juce::String prettifyID (const juce::String& id)\n    {\n        juce::String s = id;\n        s = s.replaceCharacter ('_', ' ').replaceCharacter ('-', ' ');\n        juce::StringArray parts;\n        parts.addTokens (s, " ", "");\n        for (int i = 0; i < parts.size(); ++i)\n        {\n            auto p = parts[i].trim();\n            if (p.isEmpty())\n                continue;\n            p = p.toLowerCase();\n            if (p.length() > 0)\n                p = p.substring (0, 1).toUpperCase() + p.substring (1);\n            parts.set (i, p);\n        }\n        return parts.joinIntoString (' ');\n    }\n'''
                    txt = txt[:insert_at] + prettify + txt[insert_at:]
                    changed = True
            # add presetBox tooltip if missing
            if 'presetBox.setTooltip' not in txt:
                # find the presetBox.onChange block end ("};") after "presetBox.onChange"
                m2 = re.search(r"presetBox\.onChange\s*=\s*\[this\][\s\S]*?;\s*\}", txt)
                if m2:
                    # place tooltip right after that block
                    insert_at2 = m2.end()
                    txt = txt[:insert_at2] + "\n        presetBox.setTooltip (\"Select a factory preset or MANUAL\");\n" + txt[insert_at2:]
                    changed = True
            if changed and txt != orig:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(txt)
                modified.append(path)

print('Modified files:')
for p in modified:
    print(p)
print('Total modified:', len(modified))
