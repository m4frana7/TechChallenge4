"""Load the precomputed search index shipped with the application."""

import gzip
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

import faiss


def load_bundled_store(bundle_path: Path, model_name: str, dimension: int):
    manifest = json.loads((bundle_path / "manifest.json").read_text())
    if manifest["model"] != model_name or manifest["dimension"] != dimension:
        raise ValueError("O índice pronto não corresponde ao modelo de embeddings configurado.")

    try:
        with tempfile.TemporaryDirectory() as scratch:
            archive = Path(scratch) / "index.gz"
            digest = hashlib.sha256()
            with archive.open("wb") as output:
                for name in manifest["parts"]:
                    if Path(name).name != name:
                        raise ValueError("Nome de parte inválido no índice pronto.")
                    with (bundle_path / name).open("rb") as source:
                        while chunk := source.read(1024 * 1024):
                            digest.update(chunk)
                            output.write(chunk)
            if digest.hexdigest() != manifest["sha256"]:
                raise ValueError("O índice pronto está incompleto ou corrompido.")
            index_path = Path(scratch) / "index.faiss"
            with gzip.open(archive, "rb") as source, index_path.open("wb") as output:
                shutil.copyfileobj(source, output)
            index = faiss.read_index(str(index_path))

        with gzip.open(bundle_path / "documents.json.gz", "rt", encoding="utf-8") as source:
            documents = json.load(source)
    except FileNotFoundError as error:
        raise ValueError("Faltam arquivos do índice pronto. Confira assets/search_index no repositório.") from error

    if index.d != dimension or index.ntotal != len(documents) or len(documents) != manifest["documents"]:
        raise ValueError("O índice pronto não corresponde aos documentos fornecidos.")
    return index, documents
