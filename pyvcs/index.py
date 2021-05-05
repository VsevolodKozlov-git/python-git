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
        while data[-1] == 0:
            data = data[:-1]
        data_end_index = len(data) - 1
        packed_data = data[:62]
        packed_name = data[62:]
        unpacked_name = packed_name.decode('ascii')
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
        while len(index_data) !=0 and index_data[0] == 0:
            index_data = index_data[1:]
        data_without_name = index_data[:62]
        name_size = int.from_bytes(data_without_name[-2:], 'big')
        full_data = index_data[:62+name_size]
        index_data = index_data[62+name_size:]
        res.append(GitIndexEntry.unpack(full_data))

    return res


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    with open(gitdir / 'index', 'wb') as index_file:
        index_file_data = 'DIRC'.encode('ascii')
        # add version
        index_file_data += b'\x00\x00\x00\x02'
        index_file_data += len(entries).to_bytes(4, 'big')
        # множество записей
        for entry in entries:
            index_file_data += entry.pack()
        sha = hashlib.sha1(index_file_data).digest()
        index_file_data += sha
        index_file.write(index_file_data)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    index_entries = read_index(gitdir)
    if details:
        for entry in index_entries:
            entry_string = f'{str(oct(entry.mode))[2:]} {entry.sha1.hex()} 0\t{entry.name}'
            print(entry_string)
    else:
        for entry in index_entries:
            print(entry.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    index_entries = []

    gitdir_relative_paths = convert_to_relative_for_gitdir(gitdir, paths)
    gitdir_relative_paths = sorted(gitdir_relative_paths)

    for path in gitdir_relative_paths:
        with open(path, 'rb') as file:
            file_data = file.read()
        file_hash = bytes.fromhex(hash_object(file_data, 'blob', True))
        file_stats = os.stat(path)
        flags = len(str(path))
        os_file_inf = os.stat(path)
        index_class_args = (int(os_file_inf.st_ctime), 0, int(os_file_inf.st_mtime),
                            0, os_file_inf.st_dev, os_file_inf.st_ino,
                            os_file_inf.st_mode, os_file_inf.st_uid, os_file_inf.st_gid,
                            os_file_inf.st_size, file_hash, flags, str(path),)
        index_entry = GitIndexEntry(*index_class_args)
        index_entries.append(index_entry)

    if write:
        write_index(gitdir, index_entries)


def convert_to_relative_for_gitdir(gitdir, paths: tp.List[pathlib.Path]):
    relative_paths = []
    for path in paths:
        absolute = path.absolute()
        relative = absolute.relative_to(os.getcwd())
        relative_paths.append(relative)
    return relative_paths