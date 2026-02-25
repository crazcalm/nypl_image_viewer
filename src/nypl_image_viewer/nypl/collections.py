from datetime import datetime
import json
from typing import cast

from python_stuff.http.client import (
    HttpClient,
    Pagination,
)

from ..filesystem import (
    write_file,
    read_file,
    file_exist,
)


CACHE_DEST_DIR: tuple = ("data", "collections")
CACHE_DEST_NAME: str = "list_cache.json"


def get_pagination_generator(api_key: str, per_page: int = 500):
    headers = {}
    headers["authorization"] = f'Token token="{api_key}"'
    my_client = HttpClient(
        base_uri="https://api.repo.nypl.org/api/v2/",
        headers=headers,
        params=[("per_page", str(per_page)), ("publicDomainOnly", "true")],
    )

    pag = Pagination(
        http_client=my_client,
        page_url_param="page",
        stop_condition_func=lambda x: (
            len(x["nyplAPI"]["response"]["collection"]) < per_page
        ),
    )
    return pag.iter(endpoint="collections")


def print_collection_data(data: dict, format_type: str = "print") -> None:
    # TODO: I want two types: print and json (enums)

    match format_type:
        case "print":
            print(f"{data['uuid']} -- {data['title']}")

        case _:
            print("Don't know this type format...")


def create_cache(
    pag_generator,
    dest_dir: tuple = ("data", "collections"),
    dest_name: str = "list_cache.json",
    output_format_type: str = "print",
):
    cache = {}
    cache["metadata"] = {"crawl_date": str(datetime.today())}
    cache["results"] = []  # type: ignore[assignment]
    for json_data in pag_generator:
        for collection in json_data["nyplAPI"]["response"]["collection"]:
            cache["results"].append(collection)  # type: ignore[attr-defined]

            print_collection_data(collection)

    # TODO: write to file destination
    json_str = json.dumps(cache)

    write_file(data=json_str, dest_dir=dest_dir, dest_name=dest_name)


def read_from_cache(
    target_dir: tuple = CACHE_DEST_DIR,
    target_name: str = CACHE_DEST_NAME,
    output_format_type: str = "print",
) -> None:
    data = read_file(target_dir=target_dir, target_name=target_name)
    data = cast(dict, data)
    for collection in data["results"]:
        print_collection_data(collection)


def cache_exist(
    target_dir: tuple = CACHE_DEST_DIR,
    target_name: str = CACHE_DEST_NAME,
) -> bool:
    return file_exist(target=(*target_dir, target_name))
