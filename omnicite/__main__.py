#!/usr/bin/env python3
# coding=utf-8

import logging
import re
import sys
from pathlib import Path
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
@click.option("-o", "--output-file", type=str, default=None)
@click.option("-v", "--verbose", count=True, default=0)
@click.pass_context
def cli(ctx: click.Context, output_file: Optional[str], verbose: int):
    _setup_logging(verbose)
    ctx.ensure_object(dict)
    ctx.obj["OUTPUT_FILE"] = output_file
    ctx.obj["VERBOSE"] = verbose


@cli.command("interactive")
@click.pass_context
def cli_interactive(ctx: click.Context):
    output_file = ctx.obj["OUTPUT_FILE"]
    verbose = ctx.obj["VERBOSE"]
    pass


@cli.command("single")
@click.pass_context
def cli_single(ctx: click.Context):
    pass


@click.argument("file", type=str)
@cli.command("input-file")
@click.pass_context
def cli_input_file(ctx: click.Context, file: str):
    file = Path(file).expanduser().resolve()


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
