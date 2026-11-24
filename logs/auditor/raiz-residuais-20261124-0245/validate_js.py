import re, subprocess, tempfile, os

site_root = "C:/Users/erico/zambria.github.io"
posts_dir = os.path.join(site_root, "posts")

files = ["index.html"] + sorted([f for f in os.listdir(posts_dir) if f.endswith(".html")])

issues = []
for fname in files:
    fpath = os.path.join(site_root, fname) if fname == "index.html" else os.path.join(posts_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    script_blocks = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    
    for i, script in enumerate(script_blocks):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as tmp:
            tmp.write(script)
            tmp_path = tmp.name
        
        try:
            result = subprocess.run(['node', '--check', tmp_path], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                issues.append(f'{fname}: Script block {i+1} - SYNTAX ERROR: {result.stderr.strip()}')
        except Exception as e:
            issues.append(f'{fname}: Script block {i+1} - CHECK FAILED: {e}')
        finally:
            os.unlink(tmp_path)

print(f'Total files checked: {len(files)}')
print(f'Syntax errors found: {len(issues)}')
for issue in issues:
    print(f'  - {issue}')

if not issues:
    print('All JavaScript syntax checks passed!')