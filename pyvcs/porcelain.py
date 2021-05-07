import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object, find_all_files_from_commit_sha
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths, True)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    # делаем сам коммит
    files_in_index = read_index(gitdir)
    tree_hash = write_tree(gitdir, files_in_index)
    parent = resolve_head(gitdir)
    commit_sha = commit_tree(gitdir, tree_hash,message,parent=parent, author=author)
    update_ref(gitdir, get_ref(gitdir), commit_sha)
    return commit_sha
    # Обновляем положение головы
    # head_ref = get_ref(gitdir)
    # update_ref(gitdir, ref=head_ref, new_value=commit_hash)


def checkout(gitdir: pathlib.Path, commit_sha: str) -> None:
    '''
    :param gitdir:
    :param commit_sha: sha объекта на который мы хотим сместить голову
    :return: None
    Изменяет положение головы и удаляет все файлы и дирректрории, ненаходящиеся в измененоном
    положении HEAD. Дирректория удаляется если в она была добавлена только следующем коммите
    '''
    files_that_should_be = find_all_files_from_commit_sha(gitdir, commit_sha)



