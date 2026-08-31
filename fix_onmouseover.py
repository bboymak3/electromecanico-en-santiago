import os
import re

count = 0
for root, dirs, files in os.walk('./en'):
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "\\'" not in content or "lang-switcher" not in content:
            continue
        
        original = content
        
        # Fix escaped quotes in onmouseover/onmouseout
        content = content.replace(
            "onmouseover=\"this.style.background=\\'linear-gradient(135deg, #c62828, #e53935)\\'\"",
            "onmouseover=\"this.style.background='linear-gradient(135deg, #c62828, #e53935)'\""
        )
        content = content.replace(
            "onmouseout=\"this.style.background=\\'#a80000\\'\"",
            "onmouseout=\"this.style.background='#a80000'\""
        )
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1

# Also fix ES pages
for root, dirs, files in os.walk('.'):
    if root.startswith('./en'):
        continue
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "\\'" not in content or "lang-switcher" not in content:
            continue
        
        original = content
        
        content = content.replace(
            "onmouseover=\"this.style.background=\\'linear-gradient(135deg, #2d2d5e, #4a4a8a)\\'\"",
            "onmouseover=\"this.style.background='linear-gradient(135deg, #2d2d5e, #4a4a8a)'\""
        )
        content = content.replace(
            "onmouseout=\"this.style.background=\\'#1a1a2e\\'\"",
            "onmouseout=\"this.style.background='#1a1a2e'\""
        )
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1

print(f"Fixed escaped quotes in {count} files")
