import os
import json
import base64

import click
import requests
import htmlmin

from html_cluster.settings import (
    HTML_CLUSTER_DATA_DIRECTORY, SPLASH_URL, USER_AGENT, SPLASH_TIMEOUT, ALLOW_STATUS_CODE
)
from html_cluster.utils.common import get_file_name
from html_cluster.utils.url import FileUrlsReader

HELP = '''
'''

SHORT_HELP = 'Download html from the urls and store it in a folder.'


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
        'timeout': SPLASH_TIMEOUT,
        'images': 0,
        'url': url
    }

    return requests.get(splash_url, headers=headers, params=params)


def make_request(url, **kwargs):
    if 'splash' in kwargs and kwargs['splash']:
        if 'splash_url' in kwargs:
            return splash_request(url, kwargs['splash_url'])
        else:
            return splash_request(url, SPLASH_URL)
    return requests.get(url, headers={'user-agent': USER_AGENT})


def extract_html(url, splash, splash_url):
    is_error = False
    image = ''
    error = ''
    html = ''

    try:
        r = make_request(
            url, splash=splash, splash_url=splash_url
        )

        if 'text/html' not in r.headers['Content-Type']:
            raise Exception('The content type of url: {} is {}'.format(url, r.headers['Content-Type']))

        if r.status_code not in ALLOW_STATUS_CODE:
            raise Exception('The status code of url: {} is {}'.format(url, r.status_code))

        html = r.text

        if splash:
            json_response = json.loads(html)
            html = json_response['html']
            image = base64.b64decode(json_response['png'])
    except Exception as e:
        error = str(e)
        is_error = True

    return {
        'html': html,
        'error': error,
        'image': image
    }, is_error


def download_html(urls_file, output_directory, is_splash_request_enable=False, splash_url=SPLASH_URL):
    if not os.path.isfile(urls_file):
        click.echo('The {} file does not exits.'.format(urls_file))
        click.Context.exit(1)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    urls = FileUrlsReader(urls_file).read()
    for url in urls:
        click.echo(click.style('Downloading {}'.format(url)))
        extracted_html, error = extract_html(
            url,
            splash=is_splash_request_enable,
            splash_url=splash_url,
        )

        if not error:
            html_file_name = get_file_name(url)

            click.echo(
                click.style(
                    '  --> Saving {}/{}'.format(output_directory, html_file_name), fg='green'
                )
            )

            with open('{}/{}.html'.format(output_directory, html_file_name), 'w') as html_file:
                html_file.write(htmlmin.minify(extracted_html['html'], remove_comments=True))

            if extracted_html['image']:
                with open('{}/{}.png'.format(output_directory, html_file_name), 'wb') as png_file:
                    png_file.write(extracted_html['image'])
        else:
            click.echo(
                click.style(
                    '  --> There was a problem with url: {}, error: {}.'.format(url, extracted_html['error']), fg='red'
                )
            )


@click.command(help=HELP, short_help=SHORT_HELP)
@click.argument('urls_file')
@click.option('--output-directory', default=HTML_CLUSTER_DATA_DIRECTORY)
@click.option('--splash-enabled/--no-splash-enabled', default=False)
@click.option('--splash-url', default=SPLASH_URL)
def cli(urls_file, output_directory, splash_enabled, splash_url):
    download_html(urls_file, output_directory, splash_enabled, splash_url)
