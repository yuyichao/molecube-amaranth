#

from molecube_amaranth.toplevel import TopLevel
from amaranth_zynq.platform import ZC702Platform
from transactron import TransactronContextElaboratable

def build_zc702(config, do_build=True, build_dir="build"):
    top = TopLevel(config)
    core = TransactronContextElaboratable(top)
    plat = ZC702Platform()
    plan = plat.build(core, do_build=do_build, build_dir=build_dir)
    if not do_build:
        plan.extract(build_dir)
