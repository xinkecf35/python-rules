# Crude module to read entrypoints.txt
#
# Covers basic cases only, i.e. assumes an
# INI formatted entry_points.txt is existent

import configparser
import sys

from configparser import ConfigParser
from pathlib import Path
from string import Template

from typing import List

HELP_INFO = """
Entry Point Parser and Generator

Minimal and crude utility to parse and create entry points

Nominal reference is PyPA entry points specification:
https://packaging.python.org/en/latest/specifications/entry-points/

Usage:
entrypoint_generator [--help] [--stdout] [--write=filename] entry_points.txt


Options:
--help:     Displays this help message
--stdout:   Prints generated entry point file to standard out
--write:    writes generated entry point file to path
"""


def print_stderr(value: str):
    print(value, file=sys.stderr)


def read_entry_point_file(filename: str):
    """Attempts to read a entry_points.txt; returns a ConfigParser object"""

    potential_path = Path(filename)

    if not potential_path.exists:
        sys.stderr(f"path {filename} does not exists")
        sys.exit(2)

    entry_point_config = ConfigParser()
    if len(entry_point_config.read(potential_path)) == 0:
        print_stderr("was unable to parse entry points file as INI file")
        sys.stderr(1)

    return extract_entry_point_info(entry_point_config)

# TODO: Rethink if this is worth it given how little it does
# plus related error checking
def parse_input(parameters: List[str]):
    options = {
        "stdout": False,
        "write": None,  # Path object
    }

    for parameter in parameters:
        if parameter == "--help":
            print(HELP_INFO)
            sys.exit(0)
        elif parameter == "--stdout":
            options["stdout"] = True
        elif "--write" in parameter:
            output_path = parameter.split("=")[-1]
            options["write"] = Path(output_path)

    # get and validate the last input is valid file with entry_points config
    entry_point_info = read_entry_point_file(sys.argv[-1])

    return (options, entry_point_info)


def template_entry_point_file(module: str, entry_function: str):
    template_filepath = Path(__file__).parent / "entry_point.tmpl"
    with open(template_filepath) as template_file:
        template = Template(template_file.read())
        return template.substitute(module=module, entry_function=entry_function)


def extract_entry_point_info(entry_point_config: ConfigParser):
    """
    Extracts module and function for entry_point definition; returns as tuple of strings
    of program name, module, and function
    """
    console_scripts = entry_point_config.items("console_scripts")
    console_script = console_scripts[0]

    # Split the value assigned
    module, entry_function = console_script[1].split(":")
    return console_script[0], module, entry_function


def output_entry_point(entry_point_file: str, stdout=False, write=None):
    """Outputs generated entry point file

    TODO: reconsider this
    """
    if stdout or not write:
        print(entry_point_file)

    if write:
        with open(write, "w") as file:
            file.write(entry_point_file)


if __name__ == "__main__":
    # skipping first parameter since that's always the name of the program
    options, entry_point_info = parse_input(sys.argv[1:])

    print(options)

    # get entrypoint info and output templated entry_point file
    _, module, entry_function = entry_point_info
    entry_point_file = template_entry_point_file(module, entry_function)
    output_entry_point(entry_point_file, options["stdout"], options["write"])
