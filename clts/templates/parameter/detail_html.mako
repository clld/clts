<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>

<h2>Sound <i>${ctx.description}</i></h2>

<dl>
  <dt>Grapheme</dt>
  <dd>${ctx.name}</dd>
</dl>


${request.get_datatable('values', h.models.Value, parameter=ctx).render()}


