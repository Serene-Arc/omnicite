#!/usr/bin/env python3
# coding=utf-8

import logging
import re
import sys
from typing import Optional

import click

from omnicite.source_factories.main_factory import master_source_list

logger = logging.getLogger()


def separate_specified_module(in_string: str) -> Optional[str]:
    pattern = re.compile(r"^(.*?):::")
    match = pattern.match(in_string)
    if match:
        return match.group(1)


def _setup_logging(verbosity: int):
    logger.setLevel(1)
    stream = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter("[%(asctime)s - %(name)s - %(levelname)s] - %(message)s")
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    if verbosity > 0:
        stream.setLevel(logging.DEBUG)
    else:
        stream.setLevel(logging.INFO)


@click.group()
def cli():
    pass


@cli.command("interactive")
def cli_interactive():
    pass


@cli.command("single")
def cli_single():
    pass


@click.option("--list-raw-modules", is_flag=True, default=False)
@cli.command("list-modules")
def cli_list_modules(list_raw_modules: bool):
    names = []
    if list_raw_modules:
        for val in master_source_list.values():
            names.append(f"{val.__name__.lower()} ({val.entry_type})")
    else:
        for name, val in master_source_list.items():
            names.append(f"{name} ({val.entry_type})")
    names = sorted(names)
    for n in names:
        print(n)


if __name__ == "__main__":
    cli()
