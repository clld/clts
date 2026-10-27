# Releasing clts.clld.org

```shell
git clone https://github.com/clld/clts
git clone https://github.com/cldf-clts/clts clts-data
git -C clts-data checkout v2.3.1
cd clts
pip install -e .[test]
```


1. Load the data from cldf-clts/clts:
   ```shell
   clld initdb development.ini --cldf ../clts-data/cldf-metadata.json
   ```
2. Adapt the citation on the landing page.
3. Run the tests `pytest`.
4. Deploy to server.

