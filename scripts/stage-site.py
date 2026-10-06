"""Publish website files only, excluding research, tooling and dependency files."""
from pathlib import Path
import shutil, os

root = Path(__file__).resolve().parents[1]
# Regenerate public URLs from SITE_URL at deploy time when a custom domain is configured.
if os.environ.get('SITE_URL'):
    import subprocess
    subprocess.run(['python3', str(root / 'scripts/build-pages.py')], check=True)
out = root / 'public'
shutil.rmtree(out, ignore_errors=True)
out.mkdir()
for path in root.glob('*.html'):
    shutil.copy2(path, out / path.name)
for name in ['_redirects', 'robots.txt', 'sitemap.xml', 'sw.js', 'manifest.webmanifest']:
    shutil.copy2(root / name, out / name)
for name in ['events', 'about', 'weekend', 'itineraries', 'vibes', 'standouts', 'submit', 'thanks', 'image-credits', 'saved', 'app', 'contact', 'terms', 'privacy', 'offline']:
    shutil.copytree(root / name, out / name)
for path in (root / 'assets').rglob('*'):
    if path.is_file() and path.suffix.lower() in ['.js', '.css', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.avif', '.woff', '.woff2']:
        target = out / path.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
if os.environ.get('CONTEXT') in ['branch-deploy','deploy-preview']:
    (out / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
    (out / '_headers').write_text('/*\n  X-Robots-Tag: noindex, noarchive\n')
for path in out.rglob('*'):
    if path.is_file() and path.suffix in ['.html', '.js', '.svg', '.webmanifest']:
        text = path.read_text()
        assert 'jerekeys' not in text.lower(), f'Personal account reference in {path.relative_to(out)}'
print('Staged public website without research files, source tools or dependencies')
