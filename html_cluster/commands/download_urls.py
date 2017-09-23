import os

import click
import requests
from html_cluster.settings import HTML_CLUSTER_DATA_DIRECTORY
from html_cluster.utils import file_name

# This must be the default. The user should add the file name he wants
# The name of the directory should depend on the name of the file.



# TODO: Check if the resource is a html page. :D
# TODO: Display stats about the download
# Get splash support using docker so we can store the
# id:
# url:
# image:
# Additional information:
def download_urls(urls_file, output_directory):
    if not os.path.isfile(urls_file):
        click.echo('The {} does not exits.'.format(urls_file))
        click.Context.exit(1)

    if not os.path.exists(output_directory):
        os.makedirs('html_cluster_data')

    with open(urls_file, 'r') as f:
        lines = f.readlines()

        total_of_lines = len(lines)

        for index, line in enumerate(lines):
            url = line.replace('\n', '').strip()
            url = url.strip()
            if not url:
                # Print empty url
                continue

            click.echo(
                click.style(
                    'Downloading {} ({}/{})'.format(url, index + 1, total_of_lines), blink=True, bold=True
                )
            )
            try:
                r = requests.get(url)
                html = r.text

                if r.status_code == requests.codes.ok:
                    html_file_name = '{}/{}.html'.format(output_directory, file_name(url, html))
                    click.echo(
                        click.style(
                            '  --> Saving {}'.format(html_file_name), fg='green'
                        )
                    )

                    with open(html_file_name, 'w') as html_file:
                        html_file.write(html)
                else:
                    click.echo(
                        click.style(
                            '  --> The {} return a bad status code ({}).'.format(url, r.status_code), fg='red'
                        )
                    )
            except Exception as e:
                print('   --> Oh noes! {}'.format(e))


@click.command()
@click.argument('urls_file')
def cli(urls_file):
    download_urls(urls_file, HTML_CLUSTER_DATA_DIRECTORY)
