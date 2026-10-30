# Releasing clts.clld.org

```shell
git clone https://github.com/clld/clts
git clone --branch v2.3.1 --depth 1 https://github.com/cldf-clts/clts clts-data
cd clts
pip install -e .[test]
```

Load the data from cldf-clts/clts:
```shell
clld initdb development.ini --cldf ../clts-data/cldf-metadata.json
```
Adapt the citation on the landing page.
Run the tests `pytest`.
```shell
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO --compress gzip:9 clts > clts.sql.gz
```

