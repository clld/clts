<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${ctx.sound_type} feature - ${ctx.feature}: ${ctx.value}</%block>

<h2>${ctx.sound_type} feature - ${ctx.feature}: ${ctx.value}</h2>

<h3>${len(ctx.sounds)} Sounds</h3>

<table class="table table-nonfluid table-condensed">
    <thead>
    <tr><th>Grapheme</th><th>Name</th></tr>
    </thead>
    <tbody>
    % for sound in ctx.sounds:
    <tr>
        <td>${sound.name}</td>
        <td>${h.link(req, sound, label=sound.description)}</td>
    </tr>
    % endfor
    </tbody>
</table>