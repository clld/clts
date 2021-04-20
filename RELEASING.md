# Releasing clts.clld.org

1. Load the data from cldf-clts/clts:
   ```shell
   clld initdb development.ini --cldf ../clts-data/cldf-metadata.json
   ```
2. Adapt the citation on the landing page.
3. Run the tests `pytest`.
4. Deploy to server.

