import click
import json
from itertools import combinations


from html_similarity import similarity
from html_cluster.settings import HTML_CLUSTER_DATA_DIRECTORY
from html_cluster.validators import validate_k
from html_cluster.utils import similarity_color


def make_similarity_file(threshold, structural_weight, similarity_file_output):
    # TODO: Identify the content-type. You are only interested in html
    import glob
    results = []

    html_paths = glob.glob('{}/*.html'.format(HTML_CLUSTER_DATA_DIRECTORY))
    for file_1, file_2 in combinations(html_paths, 2):
        print('Calculating the similarity of {} and {}'.format(file_1, file_2))
        html_1 = open(file_1).read()
        html_2 = open(file_2).read()
        # Recieve k as paramenter
        similarity_value = similarity(html_1, html_2, k=structural_weight) * 100
        # Use colors for this.
        # 0 <= similarity < 50
        # 50 <= similarity < 70
        # 70 <= similarity <= 100
        click.echo('   The similarity between them is ' + click.style('{0:.2g}%'.format(similarity_value), fg=similarity_color(similarity_value)))

        # Default 55: Recieve this as paramter.
        if similarity_value > threshold:
            results.append({
                'path1': file_1,
                'path2': file_2,
                'similarity': similarity_value
            })

    with open(similarity_file_output, 'w') as json_out:
        json.dump(results, json_out, indent=4)


# python html_cluster.py make_similarity_file --structural-weight=0.3
@click.command(help='', short_help='Create a similarity file')
@click.option('--threshold', default=55, help='', type=int)
@click.option('--structural-weight', default=0.5, help='', type=float, callback=validate_k)
@click.option('--similarity_file_output', default='similarity.json', help='')
def cli(threshold, structural_weight, similarity_file_output):
    make_similarity_file(threshold, structural_weight, similarity_file_output)
