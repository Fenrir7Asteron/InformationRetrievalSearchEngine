import os
import json

STORAGE_FOLDER = 'storage/'


def store_document(doc_id: int, title: str, content: bytes) -> None:
    """Either create or update document file on disk"""
    if not os.path.exists(STORAGE_FOLDER):
        os.mkdir(STORAGE_FOLDER)
    with open(STORAGE_FOLDER + str(doc_id), 'w') as doc_file:
        json.dump({
            'title': title,
            'content': content
        }, doc_file)


def get_document(doc_id: int) -> dict:
    with open(STORAGE_FOLDER + str(doc_id), 'r') as doc_file:
        return json.load(doc_file)


def get_documents(doc_ids: list) -> list:
    res = []
    for doc_id in doc_ids:
        res.append(get_document(doc_id))
    return res
