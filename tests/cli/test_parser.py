import os
import unittest
from unittest import TestCase
from typing import NamedTuple, ClassVar, cast

from nypl_image_viewer.cli.parser import (
    EnvironmentVariable,
    get_env_variable,
    get_parser,
)


class TestGetParser(TestCase):
    def test_with_api_default(self) -> None:
        class Case(NamedTuple):
            default: str | None
            expected_api_key: str
            command: list[str]

        cases = [
            Case("default_api_key", "default_api_key", []),
            Case(None, "api_key", ["--api-key", "api_key"]),
            Case("default_api_key", "api_key", ["--api-key", "api_key"]),
        ]

        for case_num, case in enumerate(cases, start=1):
            with self.subTest(f"case({case_num}): {case}"):
                parser = get_parser(case.default)
                result = parser.parse_args(case.command)

                self.assertEqual(result.api_key, case.expected_api_key)

    def test_no_api_key(self) -> None:
        parser = get_parser()

        with self.assertRaises(SystemExit):
            parser.parse_args([])


class TestGetEnvVariable(TestCase):
    test_env: ClassVar[str]
    test_env_value: ClassVar[str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_env = "TestGetEnvVariable"
        cls.test_env_value = "Yep, we testing"

        os.environ[cls.test_env] = cls.test_env_value

    @classmethod
    def tearDownClass(cls) -> None:
        del os.environ[cls.test_env]

    def test_found_env_value(self) -> None:
        result = get_env_variable(self.test_env)
        result = cast(EnvironmentVariable, result)

        self.assertEqual(result.value, self.test_env_value)

    def test_cant_find_env_value(self) -> None:
        result = get_env_variable("UnknownEnvironmentVariable")
        self.assertIsNone(result)


class TestEnvironmentVariable(TestCase):
    def test_basic(self) -> None:
        name = "test_name"
        value = "test_value"

        data = EnvironmentVariable(name, value)
        self.assertEqual(data.name, name)
        self.assertEqual(data.value, value)


if __name__ == "__main__":
    unittest.main()
