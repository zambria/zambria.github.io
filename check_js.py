import re
import subprocess
import os

def extract_js_from_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    inline_scripts = []
    for script in scripts:
        script = script.strip()
        if script and not script.startswith('//'):
            inline_scripts.append(script)
    return inline_scripts

base_dir = r'C:\Users\erico\zambria.github.io'
posts_dir = os.path.join(base_dir, 'posts')
files = ['index.html'] + [f'posts/{f}' for f in os.listdir(posts_dir) if f.endswith('.html')]

all_ok = True
for filepath in files:
    full_path = os.path.join(base_dir, filepath)
    scripts = extract_js_from_html(full_path)
    for i, script in enumerate(scripts):
        temp_file = os.path.join(os.environ.get('TEMP', 'C:\tmp'), f'check_js_{os.path.basename(filepath)}_{i}.js')
        with open(temp_file, 'w') as f:
            f.write(script)
        result = subprocess.run(['node', '--check', temp_file], capture_output=True, text=True)
        if result.returncode != 0:
            print(f'ERROR in {filepath} (script #{i+1}):')
            print(result.stderr)
            all_ok = False
        else:
            print(f'OK: {filepath} (script #{i+1})')
        os.remove(temp_file)

if all_ok:
    print('All JavaScript syntax checks passed!')
else:
    print('Some JavaScript syntax errors found!')
