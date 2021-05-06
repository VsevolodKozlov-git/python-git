import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find

class ObjectsNotFound(Exception):
    pass


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f'{fmt} {len(data)}\0'.encode()
    store = header + data
    sha1 = hashlib.sha1(store).hexdigest()

    if write:
        gitdir = repo_find()
        blob_folder = gitdir.joinpath(f'objects/{sha1[:2]}')
        blob_folder.mkdir(parents=False, exist_ok=True)
        with open(blob_folder.joinpath(sha1[2:]), 'wb') as blob_file:
            zipped_store= zlib.compress(store)
            blob_file.write(zipped_store)

    return sha1


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    '''
    :return: Список хеш-кодов, имеющих начало == obj_name в дирректории gitdir
    '''
    if (len(obj_name) < 4) or (len(obj_name) > 40):
        raise ObjectsNotFound(f'Not a valid object name {obj_name}')

    found_shas = []
    object_folder = gitdir / 'objects' / obj_name[:2]
    obj_name_in_folder = obj_name[2:]
    for obj in object_folder.iterdir():
        if obj.stem[:len(obj_name_in_folder)] == obj_name_in_folder:
            found_shas.append(obj_name[:2] + obj.stem)

    if len(found_shas) == 0:
        raise ObjectsNotFound(f'Not a valid object name {obj_name}')

    return found_shas


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    raise  Exception("Не реализовано!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = gitdir / 'objects' / sha[:2] / sha[2:]
    with open(path, mode='rb') as file:
        obj_data = zlib.decompress(file.read())

    header, content = separate_obj_data(obj_data)
    fmt, content_len = separate_header(header)
    fmt = fmt.decode('ascii')

    return fmt, content


def separate_obj_data(obj_data: bytes) -> tp.Tuple[bytes, bytes]:
    sep_index = obj_data.find(b'\x00')
    header, content = separate_by_index(obj_data, sep_index)
    return header, content


def separate_header(header:bytes):
    sep_index = header.find(b' ')
    fmt, content_len = separate_by_index(header, sep_index)
    return fmt, content_len


def separate_by_index(obj_to_separate, sep_index:int):
    return obj_to_separate[:sep_index], obj_to_separate[sep_index+1:]


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find()
    shas = resolve_object(obj_name, gitdir)
    if len(shas) > 1:
        raise Exception('specify longer name')
    sha = shas[0]
    object_content_bytes = read_object(sha, gitdir)[1]
    object_content_decoded = object_content_bytes.decode('ascii')
    if pretty:
        print(object_content_decoded)




def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
