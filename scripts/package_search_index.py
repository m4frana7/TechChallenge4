"""Package a trusted, locally generated FAISS store for application deployment.

Usage: python scripts/package_search_index.py /path/to/data/vector_store
Do not run this script on pickle files from untrusted sources.
"""
import gzip
import hashlib
import json
from pathlib import Path
import pickle
import sys
import tempfile

source = Path(sys.argv[1])
target = Path(__file__).resolve().parents[1] / 'assets' / 'search_index'
target.mkdir(parents=True, exist_ok=True)
with (source / 'documents.pkl').open('rb') as stream:
    data = pickle.load(stream)
with gzip.open(target / 'documents.json.gz', 'wt', encoding='utf-8') as stream:
    json.dump(data['documents'], stream, ensure_ascii=False, separators=(',', ':'))
parts = []
with tempfile.TemporaryFile() as archive:
    with (source / 'index.faiss').open('rb') as stream, gzip.GzipFile(fileobj=archive, mode='wb', mtime=0) as compressed:
        while chunk := stream.read(1024 * 1024):
            compressed.write(chunk)
    archive.seek(0)
    digest = hashlib.sha256()
    while chunk := archive.read(8 * 1024 * 1024):
        name = f'index.gz.part{len(parts):02d}'
        (target / name).write_bytes(chunk)
        digest.update(chunk)
        parts.append(name)
manifest = dict(version=1, model='paraphrase-multilingual-MiniLM-L12-v2',
                dimension=int(data['dimension']), documents=len(data['documents']),
                parts=parts, sha256=digest.hexdigest())
(target / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
print('Packaged', manifest['documents'], 'documents;', len(parts), 'index parts')
for path in sorted(target.iterdir()):
    print(path.name, f'{path.stat().st_size / 1024**2:.2f} MiB')
