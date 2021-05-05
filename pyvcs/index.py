import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from string import  ascii_letters, punctuation, digits
from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        data_to_pack = (self.ctime_s, self.ctime_n, self.mtime_s,
                       self.mtime_n, self.dev, self.ino,
                       self.mode, self.uid, self.gid,
                       self.size, self.sha1, self.flags,)
        encoded_name = self.name.encode('ascii')
        packed_data = struct.pack("!LLLLLLLLLL20sH", *data_to_pack) + encoded_name
        while len(packed_data) % 8 != 0:
            packed_data += b'\x00'
        return packed_data

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        while not data[-1]:
            data = data[:-1]
        data_end_index = len(data) - 1

        while chr(data[data_end_index]) in (ascii_letters + punctuation + digits):
            data_end_index -= 1
        packed_name = data[data_end_index+1:]
        unpacked_name = packed_name.decode('ascii')

        packed_data = data[:data_end_index+1]
        unpacked_data = list(struct.unpack("!LLLLLLLLLL20sH", packed_data)) + [unpacked_name]

        return GitIndexEntry(*unpacked_data)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    index_path = gitdir / 'index'
    if not index_path.is_file():
        return []

    res = []
    with open(index_path, 'rb') as index_file:
        index_data = index_file.read()
    index_entries = struct.unpack('!i', index_data[8:12])[0]

    index_data = index_data[12:]

    for i in range(index_entries):
        pass
        while len(index_data) !=0 and index_data[0] == 0:
            index_data = index_data[1:]
        data_without_name = index_data[:62]
        name_size = int.from_bytes(data_without_name[-2:], 'big')
        full_data = index_data[:62+name_size]
        index_data = index_data[62+name_size:]
        res.append(GitIndexEntry.unpack(full_data))

    return res


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # PUT YOUR CODE HERE
    ...


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    ...


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...
