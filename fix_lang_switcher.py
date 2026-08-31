import os
import re

# Fix the lang-switcher position on ALL pages
# The floating buttons are at top:90px with height 52px, so they end at ~142px
# Move the lang-switcher to top:150px to be safely below them
# Also raise z-index to 10002 so it's above the floating buttons (z-index: 10001)

old_pattern = r'id="lang-switcher" style="position:fixed; top:80px; right:15px; z-index:9999;'
new_value = 'id="lang-switcher" style="position:fixed; top:150px; right:15px; z-index:10002;'

count = 0
for root, dirs, files in os.walk('.'):
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_pattern in content:
            new_content = content.replace(old_pattern, new_value)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Fixed: {fpath}")

print(f"\nTotal files fixed: {count}")
