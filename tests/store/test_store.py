from unittest import TestCase
from pathlib import Path

from nypl_image_viewer.store import (
    ItemImageStore,
    CollectionStore,
    Image,
)


class TestImage(TestCase):
    def setUp(self) -> None:
        self.image_path_1 = Path(*("tests", "fixtures", "collections", "5a9b7c30-c5ec-012f-32f8-58d385a7bc34", "items", "5b4ce4a0-c5ec-012f-52ab-58d385a7bc34", "images", "1557745", "1557745.jpg"))

    def test_path(self) -> None:
        image = Image(path=self.image_path_1)
        self.assertEqual(self.image_path_1, image.path)

    def test_title(self) -> None:
        # TODO
        import pdb
        pdb.set_trace()
        
        pass

class TestItemImageStore(TestCase):
    def setUp(self) -> None:
        self.parent_dir = parent_dir=Path(*("tests", "fixtures", "collections", "5a9b7c30-c5ec-012f-32f8-58d385a7bc34"))
        self.store = ItemImageStore(parent_dir=self.parent_dir)
    
    def test_has(self) -> None:
        self.assertTrue(self.store.has("1557745"))
        self.assertFalse(self.store.has("not found"))

    def test_all_with_duplicate_images(self) -> None:
        expected = ['1557745.jpg', '1557745.jpg', '1557746.jpg', '1557746.jpg', '1557747.jpg', '1557747.jpg', '1557748.jpg', '1557748.jpg', '1557749.jpg', '1557749.jpg', '1557820.jpg', '1557820.jpg', '1557821.jpg', '1557821.jpg', '1557822.jpg', '1557822.jpg', '1557823.jpg', '1557823.jpg', '1557824.jpg', '1557824.jpg']
        results = self.store.all(remove_duplicate_images=False)
        results = [item.path.name for item in results]
        results.sort()

        self.assertListEqual(results, expected)

    def test_all_no_duplicate_images(self) -> None:
        expected = ['1557745.jpg', '1557746.jpg', '1557747.jpg', '1557748.jpg', '1557749.jpg', '1557820.jpg', '1557821.jpg', '1557822.jpg', '1557823.jpg', '1557824.jpg']
        results = self.store.all()
        results = [item.path.name for item in results]
        results.sort()

        self.assertListEqual(results, expected)
        

class TestCollectionStore(TestCase):
    def setUp(self):
        self.new_york_collection_uuid = "5a9b7c30-c5ec-012f-32f8-58d385a7bc34"
        self.uuid_not_found = "448488484884884884"
        self.store = CollectionStore(parent_dir=Path(*("tests", "fixtures", "collections")))

    def test_has(self):
        self.assertTrue(self.store.has(self.new_york_collection_uuid))
        self.assertFalse(self.store.has(self.uuid_not_found))

    def test_get_not_found(self):
        self.assertIsNone(self.store.get(self.uuid_not_found))

    def test_get(self):
        result = self.store.get(self.new_york_collection_uuid)
        self.assertEqual(result.parent_dir.name, self.new_york_collection_uuid)

    def test_all(self):
        expected = [
            '5a9b7c30-c5ec-012f-32f8-58d385a7bc34',
            '86003f40-594a-0132-b4bd-58d385a7bbd0',
            'e2a46770-c605-012f-e823-58d385a7bc34',
            'f8965280-9050-0132-d187-58d385a7bbd0',
        ]
        
        results = self.store.all()
        parent_dirs = [item.parent_dir.name for item in results]
        parent_dirs.sort()

        self.assertListEqual(parent_dirs, expected)
