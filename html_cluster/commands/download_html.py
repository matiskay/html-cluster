import os
import json
import base64

import click
import requests
from html_cluster.settings import HTML_CLUSTER_DATA_DIRECTORY, SPLASH_URL, USER_AGENT
from html_cluster.utils import file_name, is_html_page_from_string

# TODO: Add default user-agent

# This must be the default. The user should add the file name he wants
# The name of the directory should depend on the name of the file.


# Increase the timeout to 30 seconds
# This should be down in the splash requests and the splash server.
def splash_request(url, splash_url):
    splash_url = splash_url.rstrip('/') + '/render.json'
    headers = {
        'content-type': 'application/json',
        'user-agent': USER_AGENT
    }
    params = {
        'html': 1,
        'png': 1,
        'width': 400,
        'height': 300,
        'timeout': 10,
        'images': 0,
        'url': url
    }

    return requests.get(splash_url, headers=headers, params=params)



# Check if the url is a valid url.
# TODO: Display stats about the download
# Get splash support using docker so we can store the
# id:
# url:
# image:
# Additional information:
# TODO: Splash support: https://github.com/TeamHG-Memex/page-compare/blob/master/scrape.py
# Avoid urls by extension
def download_html(urls_file, output_directory, is_splash_request_enable=False, splash_url=SPLASH_URL):
    if not os.path.isfile(urls_file):
        click.echo('The {} file does not exits.'.format(urls_file))
        click.Context.exit(1)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(urls_file, 'r') as f:
        lines = f.readlines()

        total_of_lines = len(lines)

        for index, line in enumerate(lines):
            url = line.replace('\n', '').strip()
            url = url.strip()
            if not url:
                continue

            click.echo(
                click.style(
                    'Downloading {} ({}/{})'.format(url, index + 1, total_of_lines), blink=True, bold=True
                )
            )
            try:
                # The idea here is to create a client which handle this.
                # Create the same interface. A dict with the information.
                if is_splash_request_enable:
                    r = splash_request(url, SPLASH_URL)
                else:
                    r = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
                html = r.text

                if r.status_code == requests.codes.ok:
                    html_file_name = file_name(url, html)
                    click.echo(
                        click.style(
                            '  --> Saving {}'.format(html_file_name), fg='green'
                        )
                    )

                    if is_splash_request_enable:
                        json_response = json.loads(r.text)
                        html = json_response['html']

                    if is_html_page_from_string(html):
                        with open('{}/{}.html'.format(output_directory, html_file_name), 'w') as html_file:
                            html_file.write(html)

                        if is_splash_request_enable:
                            with open('{}/{}.png'.format(output_directory, html_file_name), 'wb') as png_file:
                                png_file.write(base64.b64decode(json_response['png']))

                    else:
                        click.echo(
                            click.style('  --> The url {} is not an html file'.format(url), fg='red')
                        )
                else:
                    click.echo(
                        click.style(
                            '  --> The {} return a bad status code ({}).'.format(url, r.status_code), fg='red'
                        )
                    )
            except Exception as e:
                print('   --> Oh noes! {}'.format(e))

# TODO: Add splash support.
HELP = '''
'''

SHORT_HELP = 'Download the html from the urls and store it in a folder.'

@click.command(help=HELP, short_help=SHORT_HELP)
@click.argument('urls_file')
@click.option('--output-directory', default=HTML_CLUSTER_DATA_DIRECTORY)
@click.option('--splash-enabled/--no-splash-enabled', default=False)
@click.option('--splash-url', default=SPLASH_URL)
# @click.option('--splash-enabled/--no-splash-enabled', default=False, help='Enable Splash')
# @click.option('--splash-url', default=SPLASH_URL)
# def cli(urls_file, output_directory, splash_enabled, splash_url):
def cli(urls_file, output_directory, splash_enabled, splash_url):
    # download_html(urls_file, output_directory, is_splash_request_enable, splash_url)
    download_html(urls_file, output_directory, splash_enabled, splash_url)
