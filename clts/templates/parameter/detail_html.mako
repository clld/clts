<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>

<%def name="sidebar()">
    <div class="well">
        <dl>
            <dt>Grapheme</dt>
            <dd>${ctx.name}</dd>
            <dt>Unicode</dt>
            <dd>${ctx.unicode}</dd>
            <dt>Category</dt>
            <dd>${ctx.description.split()[-1]}</dd>
            <dt>Features</dt>
            <dd>
                <ol class="unstyled">
                    % for f in ctx.features:
                        <li>${h.link(req, f, label='{}: {}'.format(f.feature, f.value))}</li>
                    % endfor
                </ol>
            </dd>
        </dl>
    </div>
</%def>

<h2>Sound <i>${ctx.description}</i></h2>

% if ctx.id == 'NA':
    <div class="alert alert-info">
        This marker is provided to support linking "unknown" sounds (i.e. sounds that can not be mapped to
        a sound in the BIPA transcription system) to CLTS.
    </div>
% else:
    ${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
% endif


