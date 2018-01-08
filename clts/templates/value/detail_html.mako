<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "values" %>

<h2>Grapheme «${ctx.grapheme}» (<i>${ctx.name}</i>) in Dataset <i>${ctx.transcription_data}</i></h2>

<dl>
  <dt>Grapheme</dt>
  <dd>${ctx.grapheme}</dd>
  % if ctx.url:
    <dt>URL</dt>
    <dd><a target="_blank" href="${ctx.url}">LINK</a></dd>
  % endif
  % if ctx.frequency:
    <dt>Frequency</dt>
    <dd>${ctx.frequency}</dd>
  % endif
</dl>
