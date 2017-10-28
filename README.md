# HTML Cluster

[![Build Status](https://travis-ci.org/matiskay/html-cluster.svg?branch=master)](https://travis-ci.org/matiskay/html-cluster)

A command line tool to cluster html pages based on structural and style similarity.

## Install

The quick way:

```
pip install html-cluster
```

## How it works

1. Download HTML form a list of files.

```
html-cluster download-html urls.txt
```

2. Create a similarity score file.

```
html-cluster make-score-similarity-file --structural-weight=0.3
```

3. Create the graph dot file

```
html-cluster make-graph > graph.dot
```

4. Render the image

```
neato -O -Tpng graph.dot
```

## Examples of the images generated by the script

### Example 1

![Example 1](assets/example-1.jpg)

### Example 2

![Example 2](assets/example-2.jpg)
