import os
import argparse
from argparse import ArgumentParser
from typing import NamedTuple


class EnvironmentVariable(NamedTuple):
    name: str
    value: str


def get_env_variable(name: str) -> EnvironmentVariable | None:
    result = EnvironmentVariable(name, os.environ.get(name, default=""))

    if not result.value:
        return None
    return result


def add_collection_subcommand(parent: argparse._SubParsersAction) -> None:
    parser = parent.add_parser("collections")
    parser.add_argument("--local", action="store_true")
    parser.add_argument("--refresh-cache", action="store_true", dest="refresh_cache")


def add_view_subcommand(parent: argparse._SubParsersAction) -> None:
    parser = parent.add_parser("view")
    parser.add_argument("collection-uuid", nargs="+")


def add_get_subcommand(parent: argparse._SubParsersAction) -> None:
    parser = parent.add_parser("get")
    parser.add_argument("collection-uuid", nargs="+")


def add_delete_subcommand(parent: argparse._SubParsersAction) -> None:
    parser = parent.add_parser("delete")
    parser.add_argument("collection-uuid", nargs="+")


def get_parser(api_key_default: str | None = None) -> ArgumentParser:
    parser = ArgumentParser()
    if api_key_default:
        parser.add_argument("--api-key", help="api key", default=api_key_default)
    else:
        parser.add_argument("--api-key", help="api key", required=True)
    subparsers = parser.add_subparsers(help="subparsers help", dest="command")

    # add subparsers
    add_collection_subcommand(subparsers)
    add_view_subcommand(subparsers)
    add_get_subcommand(subparsers)
    add_delete_subcommand(subparsers)

    return parser


if __name__ == "__main__":
    # local testing
    parser = get_parser()
    parser.parse_args()
