import re
import subprocess
import os

def extract_js_from_html(filepath):
    """Extract JavaScript from <script> tags in HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all <script>...</script> blocks (not external scripts with src)
    script_blocks = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', content, re.DOTALL)
    return script_blocks

def validate_js(js_code, filename):
    """Validate JS syntax using node --check"""
    # Write JS to a temp file
    temp_file = f"C:/Users/erico/AppData/Local/Temp/temp_check_{os.path.basename(filename)}.js"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    try:
        result = subprocess.run(['node', '--check', temp_file], capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stderr
    except Exception as e:
        return False, str(e)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

# Check all HTML files
base = "C:/Users/erico/zambria.github.io"
files_to_check = [
    "index.html",
    "posts/capitulo-1-operacao-prato.html",
    "posts/capitulo-2-operacao-prato.html",
    "posts/capitulo-3-operacao-prato.html",
    "posts/capitulo-4-operacao-prato.html",
    "posts/capitulo-5-operacao-prato.html",
    "posts/capitulo-6-operacao-prato.html",
    "posts/capitulo-7-operacao-prato.html",
    "posts/capitulo-8-operacao-prato.html",
    "posts/capitulo-1-continentes-perdidos.html",
    "posts/capitulo-2-continentes-perdidos.html",
    "posts/capitulo-3-continentes-perdidos.html",
]

all_ok = True
for filepath in files_to_check:
    full_path = os.path.join(base, filepath)
    scripts = extract_js_from_html(full_path)
    print(f"\n=== {filepath} ({len(scripts)} script blocks) ===")
    for i, script in enumerate(scripts):
        ok, err = validate_js(script, filepath)
        if ok:
            print(f"  Script block {i+1}: OK")
        else:
            print(f"  Script block {i+1}: ERROR: {err.strip()}")
            all_ok = False

print(f"\n{'='*50}")
print(f"Overall: {'ALL JS SYNTAX OK' if all_ok else 'ERRORS FOUND'}")