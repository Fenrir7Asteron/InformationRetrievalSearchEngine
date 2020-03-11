import os
import json

import utils.shared as shared

STORAGE_FOLDER = 'resources/'


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


def set_listing(term: str, listing: list, index_type: str, deleted=False, dirty=True):
    if index_type == 'MAIN':
        shared.main_index.update_one({'term': term}, {'$set': {'term': term, 'listing': listing}}, upsert=True)
    elif index_type == 'AUX':  # AUX stands for auxiliary
        shared.aux_index.set(term, json.dumps({'listing': listing, 'deleted': deleted, 'dirty': dirty}))
    else:
        raise ValueError("Wrong index type. Must be either `MAIN` or `AUX`.")


def get_listing(term: str, index_type: str):
    if index_type == 'MAIN':
        data = shared.main_index.find_one({'term': term})
        return data if data is not None else {'term': term, 'listing': []}
    elif index_type == 'AUX':  # AUX stands for auxiliary
        data = shared.aux_index.get(term)
        data = data if data is not None else b'{"listing": [], "deleted": false, "dirty": false}'
        return json.loads(data)
    else:
        raise ValueError("Wrong index type. Must be either `MAIN` or `AUX`.")


def append_to_listing(term: str, doc_id: int, index_type: str):
    old = get_listing(term, index_type)
    old = old['listing'] if old is not None else []
    new = old + [doc_id] if len(old) == 0 or old[-1] != doc_id else old
    set_listing(term, new, index_type)
