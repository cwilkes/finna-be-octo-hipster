import sys
import os
import argparse
import click


@click.command()
@click.argument('directory', default='.', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--port_new', type=click.INT, default=12000)
@click.option('--port_processed', type=click.INT, default=12001)
def run_server(directory, port_new, port_processed):
    print directory, port_new, port_processed
