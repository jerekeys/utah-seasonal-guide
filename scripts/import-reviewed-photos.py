"""Build the reviewed image package; reject a changed subject or failed download."""
import concurrent.futures, hashlib, io, json, pathlib, time, urllib.request
from PIL import Image, ImageOps
ROOT = pathlib.Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'assets/reviewed-photo-manifest.json').read_text())
def dhash(image):
    values = list(image.convert('L').resize((9, 8)).getdata())
    return sum((values[y*9+x] > values[y*9+x+1]) << (y*8+x) for y in range(8) for x in range(8))
def build(item):
    destination = ROOT / item['destination']
    if not destination.resolve().is_relative_to((ROOT / 'assets/photos').resolve()):
        raise ValueError('Image destination is outside the photo directory')
    if destination.exists():
        image = Image.open(destination)
        image.verify()
        image = Image.open(destination)
        if (dhash(image) ^ int(item['reviewHash'], 16)).bit_count() > 10:
            raise ValueError('Existing asset differs from the reviewed subject')
        return item['destination']
    for attempt in range(3):
        try:
            request = urllib.request.Request(item['url'], headers={'User-Agent': 'Mozilla/5.0 (UtahSeasonalGuide editorial photo package)'})
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read(25_000_000)
            image = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert('RGB')
            if min(image.size) < 300 or max(image.size) < 650:
                raise ValueError('Source no longer meets the reviewed dimensions')
            distance = (dhash(image) ^ int(item['reviewHash'], 16)).bit_count()
            if distance > 10:
                raise ValueError(f'Source differs from the reviewed subject ({distance}/64)')
            image.thumbnail((1600, 1600))
            destination.parent.mkdir(parents=True, exist_ok=True)
            image.save(destination, 'WEBP', quality=84)
            return item['destination']
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    pending = {pool.submit(build, item): item for item in manifest['items']}
    failures = []
    for future in concurrent.futures.as_completed(pending):
        item = pending[future]
        try:
            print('Built', future.result(), flush=True)
        except Exception as error:
            failures.append({'destination': item['destination'], 'error': str(error)})
    if failures:
        print(json.dumps(failures, indent=2))
        raise SystemExit('Photo package incomplete; development will not be updated')
print('Complete reviewed package:', len(manifest['items']), 'assets')
