import json
import re
from pathlib import Path


def write_file(data: str, dest_dir: tuple, dest_name: str) -> None:
    dir = Path(*dest_dir)
    if not dir.exists() or not dir.is_dir():
        dir.mkdir(parents=True)

    new_file = Path(dir.absolute(), dest_name)
    new_file.write_text(data)


def read_file(target_dir: tuple, target_name: str, format: str = "json") -> str | dict:
    file = Path(*target_dir, target_name)
    data = file.read_text()

    match format:
        case "json":
            data = json.loads(data)
        case _:
            raise Exception("Not implemented")

    return data


def top_down_get_directories(start_path: Path, regex_filter: str | None = None) -> list[Path]:
    results = []
    seen = set()
    for root, dirs, files in start_path.walk():
        data = {"root": root, "dirs": dirs, "files": files}
        dir_list = [root / dir_ for dir_ in dirs]

        for dir_ in dir_list:
            if regex_filter:
                if re.match(regex_filter, dir_.name):
                    results.append(dir_)
                    seen.add(str(dir_))
            else:
                if str(dir_) not in seen:
                    results.append(dir_)
                    seen.add(str(dir_))
        
    return results


def top_down_get_files(start_path: Path, regex_filter: str | None) -> list[Path]:
    results = []
    for root, dirs, files in start_path.walk():
        data = {"root": root, "dirs": dirs, "files": files}
        file_list = [root / file_ for file_ in files]

        for file_ in file_list:
            if regex_filter:
                if re.match(regex_filter, file_.name):
                    results.append(file_)
            else:
                results.append(file_)

    return results
    
