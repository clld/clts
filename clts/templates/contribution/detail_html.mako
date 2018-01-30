<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<%def name="sidebar()">
    <div class="well">
        <h3>Sources</h3>
        ${h.linked_references(req, ctx)|n}
    </div>
</%def>

<h2>${ctx.datatype.value.capitalize()} <i>${ctx.name}</i></h2>

<div class="alert-success alert">
    ${u.markdown(ctx.description)|n}
</div>

${util.data()}

<% dt = request.get_datatable('values', h.models.Value, contribution=ctx) %>
% if dt:
<div>
    ${dt.render()}
</div>
% endif
