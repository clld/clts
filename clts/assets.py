from clldutils.path import Path
from clld.web.assets import environment

import clts


environment.append_path(
    Path(clts.__file__).parent.joinpath('static').as_posix(),
    url='/clts:static/')
environment.load_path = list(reversed(environment.load_path))
