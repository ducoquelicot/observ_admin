# Observ

Track the latest topics of interest from government sources.

## Developers

### Pre-requisites

* Python >= 3.6
* [Elasticsearch 7.x](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)

### Install

```
git clone
cd observ_admin
pipenv install
flask db upgrade
```

### Run

* Start elasticsearch (varies depending on your setup). For example,
  ```
  cd /path/to/elasticsearch-7.0.1
  ./bin/elasticsearch
  ```
* Start flask
  ```
  cd observ_admin
  pipenv shell
  flask run
  ```
