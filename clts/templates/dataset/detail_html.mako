<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    <div style="margin-bottom: 20px; margin-top: 20px; text-align: center">
        <img src="${req.static_url('clts:static/logo/clts2.png')}"/>
    </div>
    <div class="well">
        <p>
            This application serves the latest
            ${h.external_link('https://github.com/cldf/clts/releases', label='released version of the CLTS data')},
            which is curated in the GitHub repository
            ${h.external_link('https://github.com/cldf/clts', label='cldf/clts')}.
        </p>
    </div>
</%def>

<h2>CLTS</h2>

<p class="lead">
    Cross-Linguistic Transcription Systems
</p>
<p>
    Cite as
</p>
<blockquote>
    Johann-Mattis List, Cormac Anderson, Tiago Tresoldi, Simon J. Greenhill, Christoph Rzymski, & Robert Forkel.
    (2018). Cross-Linguistic Transcription Systems (Version v1.1.1).
    Max Planck Institute for the Science of Human History: Jena
    <a href="https://doi.org/10.5281/zenodo.1623511"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.1623511.svg" alt="DOI:10.5281/zenodo.1623511"></a>
</blockquote>
