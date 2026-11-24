import re
import subprocess
import tempfile
import os

def extract_scripts(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    scripts = re.findall(r'<script>([\s\S]*?)</script>', content)
    return scripts

def validate_js(script_content):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(script_content)
        temp_path = f.name
    try:
        result = subprocess.run(['node', '--check', temp_path], capture_output=True, text=True, timeout=10)
        os.unlink(temp_path)
        return result.returncode == 0, result.stderr
    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        return False, str(e)

files = [
    'index.html',
    'posts/capitulo-1-operacao-prato.html',
    'posts/capitulo-2-operacao-prato.html',
    'posts/capitulo-3-operacao-prato.html',
    'posts/capitulo-4-operacao-prato.html',
    'posts/capitulo-5-operacao-prato.html',
    'posts/capitulo-6-operacao-prato.html',
    'posts/capitulo-7-operacao-prato.html',
    'posts/capitulo-8-operacao-prato.html',
    'posts/capitulo-1-continentes-perdidos.html',
    'posts/capitulo-2-continentes-perdidos.html',
    'posts/capitulo-3-continentes-perdidos.html',
]

for filepath in files:
    full_path = f'C:/Users/erico/zambria.github.io/{filepath}'
    scripts = extract_scripts(full_path)
    print(f"\n=== {filepath} ({len(scripts)} script blocks) ===")
    for i, script in enumerate(scripts):
        ok, err = validate_js(script)
        status = "OK" if ok else f"ERROR: {err}"
        print(f"  Block {i+1}: {status}")