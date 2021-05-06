import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    # PUT YOUR CODE HERE
    ...


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    ...


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    # PUT YOUR CODE HERE
    ...


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    # PUT YOUR CODE HERE
    ...


def is_detached(gitdir: pathlib.Path) -> bool:
    '''

    :param gitdir:
    :return: Сбито ли значение HEAD с ветки?
    '''
    head_path = gitdir / 'HEAD'
    with open(head_path, 'rb') as head_file:
        head_data = head_file.read()
    if head_data[:3] == b'ref':
        return False
    return True


def get_ref(gitdir: pathlib.Path) -> str:
    '''
    :param gitdir:
    :return: местоположение головы
    '''
    head_path = gitdir / 'HEAD'
    with open(head_path, 'rb') as head_file:
        head_data = head_file.read()
    if head_data[:3] == b'ref':
        head_path = head_data[5:].decode().rstrip()
        return head_path
    else:
        return head_data.hex()
