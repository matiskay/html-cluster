# HTML Cluster

A command line tool that relies on [html-similarity](https://github.com/matiskay/html-similarity)
package to cluster html pages.

### How it works

1. Download HTML form a list of files.

```
html-cluster download-html
```

2. Create a similarity score file.

```
html-cluster make-score-similarity-file
```

3. Create the graph dot file

```
html-cluster make-graph > graph.dot
```

4. Render the image

```
neato -O -Tpng graph.dot
```