<%inherit file="../home_comp.mako"/>
<%namespace name="clts_util" file="../clts_util.mako"/>

<%def name="sidebar()">
    <div style="margin-bottom: 20px; margin-top: 20px; text-align: center">
        <img src="${req.static_url('clts:static/logo/clts2.png')}"/>
    </div>
        ${clts_util.download_info()}
</%def>

<h2>CLTS</h2>

<p class="lead">
    Cross-Linguistic Transcription Systems
</p>
<p>
    Contrary to what non-practitioners might expect, the systems of phonetic
    notation used by linguists are highly idiosyncratic. Not only do various
    linguistic subfields disagree on the specific symbols they use to denote
    the speech sounds of languages, but also in large databases of sound
    inventories considerable variation can be found. Inspired by recent
    efforts to link cross-linguistic data using reference catalogs
    - such as
    ${h.external_link('https://glottolog.org', label='Glottolog')} or
    ${h.external_link('https://concepticon.clld.org', label='Concepticon')} -
    across different resources, we present initial
    efforts to link different phonetic notation systems to a catalog of
    speech sounds. Our cross-linguistic database of phonetic transcription
    systems (CLTS) currently registers
    <a href="${req.route_url('contributions', _query=dict(sSearch_2='transcription system'))}">5 transcription systems</a>
    and links to
    <a href="${req.route_url('contributions', _query=dict(sSearch_2='transcription data'))}">22 different transcription datasets</a>,
    in addition to mapping the sounds to
    <a href="${req.route_url('contributions', _query=dict(sSearch_2='sound class system'))}">6 different sound class systems</a>.
</p>
<p>
    Cite the database as
</p>
<blockquote>
    Johann-Mattis List, Cormac Anderson, Tiago Tresoldi, & Robert Forkel.
    (2021). Cross-Linguistic Transcription Systems (Version v2.1.0).
    [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4705149
    <br>
    <a href="https://doi.org/10.5281/zenodo.4705149"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4705149.svg" alt="DOI"></a>
</blockquote>
<p>
    and the paper introducing CLTS as
</p>
<blockquote>
Anderson, Cormac, Tiago Tresoldi, Thiago C. Chacon, Anne-Maria Fehn, Mary Walworth, Robert Forkel, and Johann-Mattis List (2018): A Cross-Linguistic Database of Phonetic Transcription Systems. Yearbook of the Poznań Linguistic Meeting 4.1. 21-53. DOI: 10.2478/yplm-2018-0002 
</blockquote>
