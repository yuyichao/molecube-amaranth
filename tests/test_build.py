#

from molecube_amaranth.build import build_zc702
from molecube_amaranth.config import Config

import tempfile

def test_build():
    with tempfile.TemporaryDirectory() as d:
        build_zc702(Config(), do_build=False, build_dir=d)
