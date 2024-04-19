<%inherit file="home_comp.mako"/>
<%namespace name="clts_util" file="clts_util.mako"/>

<h3>Data</h3>

${clts_util.download_info()}

<div class="alert-info alert">
    <p>
        All released versions are also available at
        ${h.external_link('https://doi.org/10.5281/zenodo.3515744', label='DOI 10.5281/zenodo.3515744')}
        on ZENODO.
    </p>
    <p>
        The "raw" data is best accessed using the Python API
        <span style="font-family: monospace">pyclts</span>, described in the
        ${h.external_link('https://github.com/cldf-clts/clts/#cross-linguistic-transcription-systems', label='README.md')}.
    </p>
</div>
