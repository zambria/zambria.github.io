import re
import subprocess
import tempfile
import os

def check_scripts_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    errors = []
    for i, script in enumerate(scripts):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as tmp:
            tmp.write(script)
            tmp_path = tmp.name
        try:
            result = subprocess.run(['node', '--check', tmp_path], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                errors.append(f'Script block {i+1}: {result.stderr.strip()}')
        finally:
            os.unlink(tmp_path)
    return errors

files = ['index.html'] + [f'posts/{f}' for f in os.listdir('posts') if f.endswith('.html')]
all_errors = {}
for f in files:
    errs = check_scripts_in_file(f)
    if errs:
        all_errors[f] = errs

if all_errors:
    for f, errs in all_errors.items():
        print(f'{f}:')
        for e in errs:
            print(f'  {e}')
else:
    print('All JavaScript syntax checks passed!')