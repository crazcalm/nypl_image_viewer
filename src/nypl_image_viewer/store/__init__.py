from pathlib import Path

from ..filesystem import (
    top_down_get_files,
)


COLLECTION_PATH = Path(*("data", "collections"))


class ItemImageStore:
    JPG_PATTERN = "^.+\\.(jpg|jpeg)$"

    def __init__(self, parent_dir: Path) -> None:
        self.parent_dir = parent_dir

    def has(self, image_id: str) -> bool:
        result = False
        images = top_down_get_files(
            start_path=self.parent_dir, regex_filter=self.JPG_PATTERN
        )

        for image in images:
            if image.name == f"{image_id}.jpg":
                result = True
                break
        return result

    def get(self, image_id: str) -> Path | None:
        result = None
        images = top_down_get_files(
            start_path=self.parent_dir, regex_filter=self.JPG_PATTERN
        )

        for image in images:
            if image.name == f"{image_id}.jpg":
                result = image
                break
        return result

    def all(self) -> list[Path]:
        return top_down_get_files(
            start_path=self.parent_dir, regex_filter=self.JPG_PATTERN
        )


class CollectionStore:
    def __init__(self, parent_dir: Path = COLLECTION_PATH):
        self.parent_dir: Path = parent_dir

    def has(self, collection_uuid: str) -> bool:
        result = False
        for item in self.parent_dir.iterdir():
            if item.is_dir() and item.name == collection_uuid:
                result = True
                break

        return result

    def get(self, collection_uuid: str) -> ItemImageStore | None:
        result = None
        for item in self.parent_dir.iterdir():
            if item.is_dir() and item.name == collection_uuid:
                result = ItemImageStore(parent_dir=item)
                break

        return result

    def all(self) -> list[ItemImageStore]:
        results = []

        for item in self.parent_dir.iterdir():
            # 28 is a magic number, but really I just wanted a soft filter to make
            # sure that dirs with typically name lengths are not picked up.
            # ie. I only want to return the UUID named directories
            if item.is_dir() and len(item.name) > 28:
                results.append(ItemImageStore(parent_dir=item))

        return results
