<%inherit file="home_comp.mako"/>

<h3>Data</h3>

<div class="alert-info alert">
    <p>
    This application serves the latest
    ${h.external_link('https://github.com/cldf/clts/releases', label='released version of the CLTS data')},
    which is curated in the GitHub repository
    ${h.external_link('https://github.com/cldf/clts', label='cldf/clts')}.
    </p>
    <p>
        All released versions are also available at
        ${h.external_link('https://doi.org/10.5281/zenodo.1617697', label='DOI 10.5281/zenodo.1617697')}
        on ZENODO.
    </p>
    <p>
        The "raw" data is best accessed using the Python API
        <span style="font-family: monospace">pyclts</span>, described in the
        ${h.external_link('https://github.com/cldf/clts/#cross-linguistic-transcription-systems', label='README.md')}.
    </p>
</div>
