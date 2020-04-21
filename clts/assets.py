import pathlib

from clld.web.assets import environment

import clts


environment.append_path(
    str(pathlib.Path(clts.__file__).parent.joinpath('static')),
    url='/clts:static/')
environment.load_path = list(reversed(environment.load_path))
