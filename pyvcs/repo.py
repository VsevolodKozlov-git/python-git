import os
import pathlib
import typing as tp


class RepositoryNotFound(Exception):
    pass


def convert_to_path_if_needed(workdir):
    if type(workdir) == str:
        workdir = pathlib.Path(workdir)
    return pathlib.Path(workdir)


def get_git_folder_name():
    try:
        git_folder_name = os.environ["GIT_DIR"]
    except KeyError:
        git_folder_name = '.git'
    return git_folder_name


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    workdir = convert_to_path_if_needed(workdir)

    ready_repo_parent = find_ready_repo_in_parents(workdir)
    ready_repo_in_workdir = find_ready_repo_in_workdir(workdir)
    if ready_repo_in_workdir is not None:
        return ready_repo_in_workdir
    if ready_repo_parent is not None:
        return ready_repo_parent
    else:
        raise RepositoryNotFound('Not a git repository')


def find_ready_repo_in_parents(workdir):
    git_folder_name = get_git_folder_name()
    parts_of_workdir_path = workdir.absolute().parts
    for i in range(len(parts_of_workdir_path)):
        if parts_of_workdir_path[i] == git_folder_name:
            repo_path_tuple = parts_of_workdir_path[:i + 1]
            repo_path_string = os.path.join(*repo_path_tuple)
            return pathlib.Path(repo_path_string)
    return None


def find_ready_repo_in_workdir(workdir):
    git_folder_name = get_git_folder_name()
    all_in_workdir = workdir.glob('*')
    if any(map(lambda x: x.name == git_folder_name and x.is_dir(), all_in_workdir)):
        return workdir.joinpath(git_folder_name)


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    workdir = convert_to_path_if_needed(workdir)

    if workdir.is_file():
        filename = workdir.name
        raise Exception(f"{filename} is not a directory")

    git_folder_name = get_git_folder_name()
    git_path = workdir.joinpath(git_folder_name)
    git_path.mkdir(exist_ok=True, parents=True)

    dirs_to_create = ['refs/heads', 'refs/tags', 'objects']
    for directory in dirs_to_create:
        new_dir_path = git_path.joinpath(directory)
        new_dir_path.mkdir(parents=True, exist_ok=True)

    file_names_to_write = ['HEAD', 'config', 'description']
    strings_to_write_in_file = ['ref: refs/heads/master\n',
                                "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n",
                                'Unnamed pyvcs repository.\n']

    for file_name, string_to_write in zip(file_names_to_write, strings_to_write_in_file):
        with open(git_path.joinpath(file_name), 'w') as file:
            print(string_to_write, end='', sep='', file=file)

    return git_path


if __name__ == '__main__':
    pass
