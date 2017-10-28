import click
import glob
import json
from itertools import combinations

from html_similarity import similarity
from html_cluster.settings import HTML_CLUSTER_DATA_DIRECTORY
from html_cluster.validators import validate_k
from html_cluster.utils.common import similarity_color


def make_score_similarity_file(structural_weight, similarity_file_output):
    results = []

    html_paths = glob.glob('{}/*.html'.format(HTML_CLUSTER_DATA_DIRECTORY))

    for file_path_1, file_path_2 in combinations(html_paths, 2):
        # TODO: Remove the data directory
        print('Calculating the similarity of {} and {}'.format(file_path_1, file_path_2))
        with open(file_path_1) as file_1, open(file_path_2) as file_2:
            html_1 = file_1.read()
            html_2 = file_2.read()

            similarity_score = similarity(html_1, html_2, k=structural_weight) * 100
            click.echo(
                '   The similarity between them is ' + click.style('{0:.2g}%'.format(
                    similarity_score), fg=similarity_color(similarity_score)
                )
            )
            results.append({
                'path1': file_path_1,
                'path2': file_path_2,
                'similarity': similarity_score
            })

    with open(similarity_file_output, 'w') as json_out:
        json.dump(results, json_out, indent=4)


@click.command(help='', short_help='Create a similarity file')
@click.option('--structural-weight', default=0.5, help='', type=float, callback=validate_k)
@click.option('--similarity_file_output', default='similarity_score.json', help='')
def cli(structural_weight, similarity_file_output):
    make_score_similarity_file(structural_weight, similarity_file_output)
