import os
import json

import click


def generate_graph(similarity_file, threshold=85):
    edges = dict()
    hosts_used = set()

    with open(similarity_file, 'r') as json_file:
        scores = json.load(json_file)

    score_dict = {s['similarity']: (s['path1'], s['path2']) for s in scores}
    for score, paths in score_dict.items():
        if score < threshold:
            continue

        host1 = paths[0]
        host2 = paths[1]
        hosts_used.add(host1)
        hosts_used.add(host2)

        edges[host1, host2] = (score - threshold) / 2

    print('graph {')
    print('  graph [overlap=scale, splines=true];')
    print('  node [shape=box, fixedsize=false, fontsize=8, margin="0.05", width="0", height="0"];')
    print()

    for k, v in edges.items():
        u1, u2 = k
        weight = v
        print('  "%s" -- "%s" [weight=%0.1f, penwidth=%0.1f]' % (u1, u2, weight, weight))

    print()

    for host in hosts_used:
        image_path = '{}.png'.format(host.replace('.html', ''))
        if os.path.exists(image_path):
            print('  "{host}" [label="{host}", image="{image_path}"]'.format(host=host, image_path=image_path)) # NOQA
        else:
            print('  "{host}" [label="{host}"]'.format(host=host))
    print('}')


# Validate Threshold
@click.command(short_help='Generate a Graphviz Dot file.')
@click.argument('similarity_file')
@click.option('--threshold', default=55)
def cli(similarity_file, threshold):
    generate_graph(similarity_file, threshold)
