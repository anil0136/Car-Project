import os
import re

def resolve_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to match the Git conflict markers and keep the HEAD part.
    # The pattern matches:
    # 1. <<<<<<< HEAD (and optional newline)
    # 2. Capture group 1: everything up to =======
    # 3. ======= (and optional newline)
    # 4. everything up to >>>>>>> [commit hash]
    # 5. >>>>>>> [commit hash] (and optional newline)
    
    pattern = re.compile(r'<<<<<<< HEAD\r?\n(.*?)\r?\n=======\r?\n.*?\r?\n>>>>>>> [a-f0-9]+\r?\n?', re.DOTALL)
    
    new_content, count = pattern.subn(r'\1\n', content)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Resolved {count} conflicts in {filepath}")

def main():
    templates_dir = r'c:\Users\ASUS\Project\Car\templates'
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                resolve_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
