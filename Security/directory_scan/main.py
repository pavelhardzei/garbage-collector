import json
import os
import pwd
import re
import sys

from collections import namedtuple


def get_owner(path):
    return pwd.getpwuid(os.stat(path).st_uid).pw_name


def get_size(path):
    return os.stat(path).st_size


def check_elf(path):
    try:
        with open(path, 'rb') as file:
            return file.read(4) == b'\x7fELF'
    except:
        pass


def main():
    if len(sys.argv) not in (2, 3):
        print('Path(required), pattern to exclude owners(optional)')
        return

    pattern = re.compile(sys.argv[2]) if len(sys.argv) == 3 else None
    Info = namedtuple('Info', ['files', 'size'])
    users_files = {}

    for item in os.listdir(sys.argv[1]):
        path = os.path.join(sys.argv[1], item)
        if os.path.isdir(path) or not check_elf(path) or os.path.islink(path):
            continue
        
        owner = get_owner(os.path.join(sys.argv[1], item))
        if pattern is None or pattern.search(owner) is None:
            users_files.setdefault(owner, []).append(item)
    
    users_files = {k: v for k, v in sorted(users_files.items(), key=lambda x: -len(x[1]))}
    users_files = {k: Info(v, sum(get_size(os.path.join(sys.argv[1], path)) for path in v))._asdict() 
                                                                            for k, v in users_files.items()}
    print(json.dumps(users_files, indent=4))


if __name__ == '__main__':
    main()
