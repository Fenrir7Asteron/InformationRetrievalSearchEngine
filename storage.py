import os
import json

STORAGE_FOLDER = 'storage/'


def store_document(doc_id: int, title: str, content: bytes, mongodb) -> None:
    """Either create or update document file on disk"""
    docs = mongodb.documents
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


def set_listing(term: str, listing: list, index, index_type: str):
    if index_type == 'MAIN':
        index.update_one({'term': term}, {'$set': {'term': term, 'listing': listing}}, upsert=True)
    elif index_type == 'AUX':  # AUX stands for auxiliary
        index.set(term, json.dumps({'listing': listing}))
    else:
        raise ValueError("Wrong index type. Must be either `MAIN` or `AUX`.")


def get_listing(term: str, index, index_type: str):
    if index_type == 'MAIN':
        return index.find_one({'term': term})
    elif index_type == 'AUX':  # AUX stands for auxiliary
        return json.loads(index.get(term))
    else:
        raise ValueError("Wrong index type. Must be either `MAIN` or `AUX`.")