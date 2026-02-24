from datetime import datetime
import json

from python_stuff.http.client import (
    HttpClient,
    Pagination,
)

from ..filesystem import (
    write_file,
)
from .images import download_image


def get_pagination_generator(api_key: str, collection_uuid: str, per_page: int = 500):
    """
    collections/uuid/items endpoint
    """
    headers = {}
    headers["authorization"] = f'Token token="{api_key}"'
    my_client = HttpClient(
        base_uri=f"https://api.repo.nypl.org/api/v2/collections/{collection_uuid}",
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
    return pag.iter(endpoint="items")


def print_item_data(
    data: dict,
    collection_uuid: str,
    item_uuid: str,
    title: str | None = None,
    format_type: str = "print",
) -> None:
    print(
        f"collection: {collection_uuid}, item: {item_uuid}, title: {title}, data: {data}"
    )


def get_http_client_item_details(api_key: str, per_page: int = 500):
    headers = {}
    headers["authorization"] = f'Token token="{api_key}"'
    my_client = HttpClient(
        base_uri="https://api.repo.nypl.org/api/v2/items/item_details/",
        headers=headers,
        params=[("per_page", str(per_page)), ("publicDomainOnly", "true")],
    )
    return my_client


def create_collections_item_cache(
    pag_generator,
    http_client_item_details: HttpClient,
    collection_uuid: str,
    dest_parent_dir: tuple = ("data", "collections"),
    dest_name: str = "collections_items_cache.json",
) -> None:
    cache = {}
    cache["metadata"] = {"crawl_date": str(datetime.today())}
    cache["results"] = []  # type: ignore[assignment]

    for json_data in pag_generator:
        # Check if results exist:
        if json_data["nyplAPI"]["response"].get("numItems") in (None, "0"):
            continue
        
        for item in json_data["nyplAPI"]["response"]["collection"]:
            if item.get("mods", {}).get("typeOfResource") != "still image":
                continue

            pag_item_details = Pagination(
                http_client=http_client_item_details,
                page_url_param="page",
                stop_condition_func=lambda x: (
                    len(x["nyplAPI"]["response"]["imm_captures"]["capture"]) < 500
                ),  # Figure out how to pass this value
            )
            for item_json in pag_item_details.iter(endpoint=item["uuid"]):
                cache["results"].append(item_json)  # type: ignore[attr-defined]

                for capture_json in item_json["nyplAPI"]["response"]["imm_captures"][
                    "capture"
                ]:
                    """
                    Around here, I should:
                    - create data/collections/c-uuid/items/i-uuid/image/image-id/image_file
                    """
                    image_id = capture_json.get("imageID", {}).get("$")

                    if not image_id:
                        continue
                    capture_dir = (
                        *dest_parent_dir,
                        collection_uuid,
                        "items",
                        item["uuid"],
                        "images",
                        image_id,
                    )
                    write_file(
                        data=json.dumps(capture_json),
                        dest_dir=capture_dir,
                        dest_name="capture_cache.json",
                    )

                    download_image(image_id=image_id, dest=(*capture_dir, f"{image_id}.jpg"))

                    print_item_data(
                        data=capture_json,
                        collection_uuid=collection_uuid,
                        item_uuid=item["uuid"],
                        title=item_json["nyplAPI"]["response"]["mods"]["titleInfo"][
                            "title"
                        ].get("$"),
                    )

    json_str = json.dumps(cache)
    write_file(
        data=json_str, dest_dir=(*dest_parent_dir, collection_uuid), dest_name=dest_name
    )
