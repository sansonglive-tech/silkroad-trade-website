import re

path = r'C:\Users\ASDCF\.qclaw\workspace\update_wb_training_with_images.js'

with open(path, encoding='utf-8') as f:
    lines = f.readlines()

to_remove = set()

for i, line in enumerate(lines):
    if '...screenshot(' in line:
        to_remove.add(i)
        # Remove the next line if it's spacer()
        if i + 1 < len(lines) and lines[i + 1].strip() == 'spacer(),':
            to_remove.add(i + 1)

print(f"Removing {len(to_remove)} lines: {sorted(to_remove)}")

new_lines = [line for i, line in enumerate(lines) if i not in to_remove]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Done.")
