import importlib
import click


HELP = """
html-cluster tool
"""

SHORT_HELP = 'html-cluster tool'


@click.group(help=HELP, short_help=SHORT_HELP)
@click.version_option('1.0')
def cli():
    pass


commands = [
    'download_urls',
    # 'make_similarity_file',
    # 'generate_graph'
]


for command in commands:
    module_path = 'html_cluster.commands.' + command
    command_module = importlib.import_module(module_path)
    command_name = command.replace('_', '-')
    cli.add_command(command_module.cli, command_name)


if __name__ == '__main__':
    cli()