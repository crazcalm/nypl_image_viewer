from unittest import TestCase
from pathlib import Path

from nypl_image_viewer.store import (
    ItemImageStore,
    CollectionStore,
)

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
