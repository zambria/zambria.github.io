import re
import subprocess
import os

def extract_scripts_from_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    return scripts

def check_js_syntax(js_code):
    try:
        result = subprocess.run(['node', '-e', f'new Function({repr(js_code)})'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0, result.stderr
    except Exception as e:
        return False, str(e)

base = r'C:/Users/erico/zambria.github.io'
files = [
    'index.html',
    'posts/capitulo-1-operacao-prato.html',
    'posts/capitulo-2-operacao-prato.html',
    'posts/capitulo-3-operacao-prato.html',
    'posts/capitulo-4-operacao-prato.html',
    'posts/capitulo-5-operacao-prato.html',
    'posts/capitulo-1-continentes-perdidos.html',
    'posts/capitulo-2-continentes-perdidos.html',
    'posts/capitulo-3-continentes-perdidos.html',
]

all_ok = True
for f in files:
    full = os.path.join(base, f)
    scripts = extract_scripts_from_html(full)
    for i, script in enumerate(scripts):
        ok, err = check_js_syntax(script)
        if not ok:
            print(f'❌ {f} script #{i+1}: {err}')
            all_ok = False
        else:
            print(f'✅ {f} script #{i+1}: OK')
if all_ok:
    print('All JS syntax checks passed!')