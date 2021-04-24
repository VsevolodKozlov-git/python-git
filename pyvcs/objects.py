import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f'{fmt} {len(data)}\0'
    store = header + data.decode()
    sha1 = hashlib.sha1(store.encode()).hexdigest()

    if write:
        gitdir = repo_find()
        blob_folder = gitdir.joinpath(f'objects/{sha1[:2]}')
        blob_folder.mkdir(parents=False, exist_ok=True)
        with open(blob_folder.joinpath(sha1[2:]), 'wb') as blob_file:
            zipped_store= zlib.compress(store.encode())
            blob_file.write(zipped_store)

    return sha1
    
        
def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    # PUT YOUR CODE HERE
    ...
DDlo

def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    ...


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
