import json

import click

# Read this: https://www.worthe-it.co.za/programming/2017/09/19/quick-introduction-to-graphviz.html
# python html_cluster.py generate_graph > graph.dot
# Remove the prefix directory. Generate the title as the name of the folder.
# neato -O -Tpng graph.dot
def generate_graph(similarity_file):
    edges = dict()
    hosts_used = set()

    with open(similarity_file, 'r') as json_file:
        scores = json.load(json_file)

    score_dict = {s['similarity']: (s['path1'], s['path2']) for s in scores}
    for score, paths in score_dict.items():
        host1 = paths[0]
        host2 = paths[1]
        hosts_used.add(host1)
        hosts_used.add(host2)

        # TODO: Improve this part
        # weight
        edges[host1, host2] = score / 30

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
        print('  "%s" [label="%s"]' % (host, host))

    print('}')


@click.command(short_help='Generate a Graphviz Dot file.')
@click.argument('similarity_file')
def cli(similarity_file):
    generate_graph(similarity_file)
