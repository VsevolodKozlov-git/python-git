import os
import pathlib
import stat
import time
import typing as tp
import binascii

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    last_dir = None
    current_dir = dirname
    content = b""
    for entry in index:
        current_name = os.path.relpath(entry.name, dirname)
        if "/" in current_name:
            left_slash = current_name.find("/")
            last_dir = current_dir
            current_dir = os.path.join(dirname, current_name[:left_slash])
            if last_dir != current_dir:
                entries_to_tree = []
                for possible_entry in index:
                    if possible_entry.name.startswith(current_dir):
                        entries_to_tree.append(possible_entry)
                inner_tree = write_tree(gitdir, entries_to_tree, current_dir)
                content += f"40000 {current_dir}\x00".encode("ascii")
                content += binascii.unhexlify(inner_tree)
        else:
            content += f"100644 {current_name}\x00".encode("ascii")
            content += entry.sha1
    tree = hash_object(content, "tree", True)
    return tree

def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    # PUT YOUR CODE HERE
    ...
