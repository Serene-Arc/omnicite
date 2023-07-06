#!/usr/bin/env python3
# coding=utf-8
import asyncio
import logging
import re
import sys
from pathlib import Path
from typing import Optional, Sequence, Tuple

import click
import confuse

from omnicite.formatters.bibtex_formatter import BibtexFormatter
from omnicite.source_factories.main_factory import MainFactory, master_source_list
from omnicite.sources.base_source import BaseSource

logger = logging.getLogger()


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

    logging.getLogger("asyncio").setLevel(logging.CRITICAL)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)


def separate_specified_module(in_string: str) -> Tuple[Optional[str], str]:
    pattern = re.compile(r"^(.*?):::")
    match = pattern.match(in_string)
    first_part = match.group(1) if match and match.group(1) else None
    in_string = in_string[match.end() :] if match else in_string
    in_string = re.sub(r"^[\s:]*", "", in_string)
    return first_part, in_string


def get_references(identifiers: Sequence[str], configuration: confuse.Configuration) -> Sequence[BaseSource]:
    identifiers = [separate_specified_module(i) for i in identifiers]
    unclassed_identifiers = []
    sources = []
    for c, i in identifiers:
        matched = False
        if c is not None:
            for s_class in master_source_list:
                if c.lower() == s_class.__class__.__name__:
                    sources.append(s_class(i))
                    matched = True
                    break
        if not matched:
            unclassed_identifiers.append(i)

    for i in unclassed_identifiers:
        result = MainFactory.pull_lever(i)
        if result is None:
            logger.info(f"Skipping identifier {i} as it is unsupported")
        else:
            sources.append(result(i))

    # be a good net citizen and download from each source one at a time
    bins = dict()
    for s in sources:
        if s.__class__.__name__ not in bins:
            bins[s.__class__.__name__] = []
        bins[s.__class__.__name__].append(s)

    # Set up a semaphore for each bin to limit concurrency within the bin.
    bin_semaphores = {bin_name: asyncio.Semaphore(1) for bin_name in bins}

    # Define a nested function to retrieve information for a source with the semaphore.
    async def retrieve_info_for_source(source, semaphore):
        async with semaphore:
            await source.retrieve_information(configuration)

    # Use asyncio.gather to retrieve information for all sources in each bin concurrently.
    async def perform_all_tasks():
        bin_tasks = []
        for bin_name, bin_sources in bins.items():
            bin_semaphore = bin_semaphores[bin_name]
            bin_tasks.append(
                asyncio.gather(*(retrieve_info_for_source(source, bin_semaphore) for source in bin_sources))
            )

        await asyncio.gather(*bin_tasks)

    asyncio.run(perform_all_tasks())

    return sources


def write_references(sources: Sequence[BaseSource], destination_file: Path):
    with open(destination_file, "a") as file:
        for s in sources:
            file.writelines(BibtexFormatter.convert_source(s))
            file.write("\n")


def resolve_configuration(file_path: Optional[Path]) -> confuse.Configuration:
    # TODO
    pass


@click.group()
@click.option("-", "--configuration", type=str, default=None)
@click.option("-o", "--output-file", type=str, default=None)
@click.option("-v", "--verbose", count=True, default=0)
@click.pass_context
def cli(ctx: click.Context, output_file: Optional[str], verbose: int, configuration: str):
    _setup_logging(verbose)
    ctx.ensure_object(dict)
    if output_file:
        output_file = Path(output_file).expanduser().resolve()
    if configuration:
        configuration = Path(configuration).expanduser().resolve()
        if configuration.exists() is False:
            logger.critical(f"Cannot find a configuration at {configuration} but this path was supplied")
    ctx.obj["output_file"] = output_file
    ctx.obj["configuration"] = configuration


@cli.command("interactive")
@click.pass_context
def cli_interactive(ctx: click.Context):
    output_file = ctx.obj["output_file"]
    configuration = ctx.obj["configuration"]
    print("Please type Ctrl+C to exit. Otherwise, provide a reference at the prompt.")
    while True:
        reference = input("Reference: ")
        source = get_references(
            [
                reference,
            ],
            configuration,
        )
        if output_file:
            write_references(source, output_file)
        else:
            for s in source:
                print(BibtexFormatter.convert_source(s))


@cli.command("single")
@click.argument("identifiers", nargs=-1)
@click.pass_context
def cli_single(ctx: click.Context, identifiers: Sequence[str]):
    output_file = ctx.obj["output_file"]
    configuration = ctx.obj["configuration"]
    sources = get_references(identifiers, configuration)
    if output_file:
        write_references(sources, output_file)
    else:
        for s in sources:
            print(BibtexFormatter.convert_source(s))


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
