import gzip
import hashlib
import json

import faiss
import numpy as np
import pytest

from src.bundled_store import load_bundled_store
from src.rag_pipeline import RAGPipeline


def make_bundle(tmp_path):
    index = faiss.IndexFlatL2(2)
    index.add(np.array([[0, 0], [1, 1]], dtype='float32'))
    compressed = gzip.compress(faiss.serialize_index(index).tobytes())
    (tmp_path / 'index.gz.part00').write_bytes(compressed[:20])
    (tmp_path / 'index.gz.part01').write_bytes(compressed[20:])
    documents = [{'id': 'one'}, {'id': 'two'}]
    with gzip.open(tmp_path / 'documents.json.gz', 'wt') as stream:
        json.dump(documents, stream)
    manifest = dict(model='test-model', dimension=2, documents=2,
                    parts=['index.gz.part00', 'index.gz.part01'],
                    sha256=hashlib.sha256(compressed).hexdigest())
    (tmp_path / 'manifest.json').write_text(json.dumps(manifest))
    return documents


def test_bundle_reassembles_exact_search_index(tmp_path):
    expected = make_bundle(tmp_path)
    index, documents = load_bundled_store(tmp_path, 'test-model', 2)
    assert documents == expected
    distances, indices = index.search(np.array([[1, 1]], dtype='float32'), 1)
    assert indices[0, 0] == 1
    assert distances[0, 0] == 0


def test_corrupted_bundle_fails_without_rebuilding(tmp_path):
    make_bundle(tmp_path)
    (tmp_path / 'index.gz.part01').write_bytes(b'corrupt')
    with pytest.raises(ValueError, match='corrompido'):
        load_bundled_store(tmp_path, 'test-model', 2)


def test_bundle_rejects_incompatible_embedding_model(tmp_path):
    make_bundle(tmp_path)
    with pytest.raises(ValueError, match='modelo'):
        load_bundled_store(tmp_path, 'different-model', 2)


def test_production_bundle_skips_review_encoding(monkeypatch):
    def unexpected(*args, **kwargs):
        pytest.fail('Startup must load the bundled index, not encode the dataset')

    pipeline = RAGPipeline()
    pipeline.embeddings_gen.embedding_dimension = 384
    monkeypatch.setattr(pipeline.data_prep, 'load_data', unexpected)
    monkeypatch.setattr(pipeline.embeddings_gen, 'generate_embeddings', unexpected)
    pipeline.build_knowledge_base()
    assert pipeline.vector_store.index.ntotal == 37488
    assert len(pipeline.vector_store.documents) == 37488
    assert pipeline.vector_store.embeddings is None
