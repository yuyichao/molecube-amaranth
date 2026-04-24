#

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.lib.cdc import ResetSynchronizer
from amaranth_zynq.ps7 import PsZynq
from amaranth_axi import AXI32AXI, AXI2AXILite, AXILiteXBar

from molecube_amaranth.csr import Registers
from molecube_amaranth.fifo import Fifos
from molecube_amaranth.inst_runner import InstRunner
from molecube_amaranth.interface import ControlInterface
from molecube_amaranth.io import PulseIO

class TopLevel(Elaboratable):
    def __init__(self, config):
        self.config = config

    def elaborate(self, plat):
        m = Module()
        m.domains += ClockDomain('sync')
        m.submodules.ps = ps = PsZynq()
        m.submodules.regs = regs = Registers()
        m.submodules.fifos = fifos = Fifos(32)
        m.submodules.controller = controller = ControlInterface(9, regs, fifos)

        m.submodules.pulseio = pulseio = PulseIO.from_config(plat, self.config)
        m.submodules.inst_runner = inst_runner = InstRunner(
            pulseio, regs, fifos, clock_shift=self.config.CLOCK_SHIFT)

        clk = ps.get_clock_signal(0, self.config.CLOCK_HZ)
        m.d.comb += ClockSignal().eq(clk)
        reset = ps.get_reset_signal(0)
        reset_sync = ResetSynchronizer(reset, domain="sync")
        m.submodules.reset_sync = reset_sync

        axi_master = ps.MAXIGP0
        m.d.comb += ps.MAXIGP0ACLK.eq(clk)

        m.submodules.axi2axil = axi2axil = AXI2AXILite(data_width=32,
                                                       addr_width=32,
                                                       id_width=12)
        wiring.connect(m, axi_master, axi2axil.axi)

        xbar = AXILiteXBar(data_width=32, addr_width=32)
        m.submodules.xbar = xbar
        xbar.add_master(axi2axil.axilite)

        xbar.add_slave(controller.axilite.cast(m, addr_width=32),
                       0x7300_0000, 0x200)

        return m
