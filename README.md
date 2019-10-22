# observ

Track the latest topics of interest from government sources.

## Developers

### Pre-requisites

* Python >= 3.7
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

### Get some data to start with
In the csv file 'pa_ag_2018' - which can be found in the root folder of this project - you'll find all the Palo Alto City Council agendas for 2018.
In order to add these files to your database and index them in ES, do the following:

- start a terminal with ```FLASK_APP=observ.py flask shell```
- run below commands in the shell:
  ```python
  Record.add_database()
  Record.reindex()
  ```

Now, if you try to perform a search, it will actually work.
