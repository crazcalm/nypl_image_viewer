from .parser import (
    get_parser,
    get_env_variable,
)
from ..nypl import (
    collections,
    items,
)


ENV_API_KEY_NAME: str = "NYPL_DIGITAL_COLLECTIONS_API_KEY"


def parsed_args(env_api_key_name=ENV_API_KEY_NAME):
    api_key_default = None

    api_key = get_env_variable(env_api_key_name)
    if api_key:
        api_key_default = api_key.value

    parser = get_parser(api_key_default=api_key_default)
    return parser.parse_args()


def main():
    cli_args = parsed_args()

    match cli_args.command:
        case "collections":
            if cli_args.local:
                print("Not implemented yet")
            elif cli_args.refresh_cache:
                pag_generator = collections.get_pagination_generator(
                    api_key=cli_args.api_key
                )

                collections.create_cache(pag_generator)
            else:
                if collections.cache_exist():
                    collections.read_from_cache()
                else:
                    pag_generator = collections.get_pagination_generator(
                        api_key=cli_args.api_key
                    )
                    collections.create_cache(pag_generator)

        case "get":
            collection_uuids = getattr(cli_args, "collection-uuid")
            print("collection_uuids", collection_uuids)

            pag_generator = items.get_pagination_generator(
                api_key=cli_args.api_key, collection_uuid=collection_uuids[0]
            )
            http_client_item_details = items.get_http_client_item_details(
                api_key=cli_args.api_key
            )

            items.create_collections_item_cache(
                pag_generator=pag_generator,
                http_client_item_details=http_client_item_details,
                collection_uuid=collection_uuids[0],
            )

            """
            notes:
            - Once I have an iterator for the collection/items
              - I need to take the uuid for the item and go to the item/item_details.uuid endpoint to get the imageID and a title for the image (These should also be my cache result)

            File structure:

            collections/
              collection-uuid/
                items/
                  - cache_item list.json (only still image items -- full payload)
                  item-uuid/
                    - cache (item_details payload)
                    - image_files
   

            Once I have the imageID, can can use the below link to download the image
            http://images.nypl.org/index.php?id=1558437&t=w&download=1
            """
        case "delete":
            for collection_uuid in getattr(cli_args, "collection-uuid"):
                if not collections.collection_exist(collection_uuid):
                    print(f"Could not find collection {collection_uuid}")
                    continue
                collections.remove_collection(collection_uuid)
                    
        case _:
            raise Exception("Not implemented yet")


if __name__ == "__main__":
    """
    Correct way to run this file is
    ```
    python -m nypl_image_viewer.cli.main
    ```
    """
    main()
