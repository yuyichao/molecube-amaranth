#

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

from transactron import TModule, Method, def_method

class Counter(wiring.Component):
    def __init__(self, width):
        super().__init__({'value': Out(width)})
        self.count = Method()
        self.clear = Method()

    def elaborate(self, plat):
        m = TModule()

        counting = Signal(1)
        clearing = Signal(1)

        with m.If(clearing):
            m.d.sync += [counting.eq(0),
                         clearing.eq(0),
                         self.value.eq(0)]
        with m.Elif(counting):
            m.d.sync += [counting.eq(0),
                         self.value.eq(self.value + 1)]

        @def_method(m, self.count, nonexclusive=True)
        def _():
            m.d.sync += counting.eq(1)

        @def_method(m, self.clear, nonexclusive=True)
        def _():
            m.d.sync += clearing.eq(1)

        return m

class Registers(Elaboratable):
    REG_WIDTH = 32
    TTL_WIDTH = 256
    CLKDIV_WIDTH = 8
    def __init__(self):
        self.ttl_hi_mask = Signal(self.TTL_WIDTH)
        self.ttl_lo_mask = Signal(self.TTL_WIDTH)
        self.ttl_out = Signal(self.TTL_WIDTH)
        self.timing_status = Signal(self.REG_WIDTH)
        self.timing_ctrl = Signal(self.REG_WIDTH)
        self.clockout_div = Signal(self.CLKDIV_WIDTH, init=255)
        self.loopback = Signal(self.REG_WIDTH)

        self.all_counters = dict(
            dbg_inst_word_count=Counter(self.REG_WIDTH),
            dbg_inst_count=Counter(self.REG_WIDTH),
            dbg_ttl_count=Counter(self.REG_WIDTH),
            dbg_dds_count=Counter(self.REG_WIDTH),
            dbg_wait_count=Counter(self.REG_WIDTH),
            dbg_clear_count=Counter(self.REG_WIDTH),
            dbg_loopback_count=Counter(self.REG_WIDTH),
            dbg_clock_count=Counter(self.REG_WIDTH),
            dbg_spi_count=Counter(self.REG_WIDTH),
            dbg_underflow_cycle=Counter(self.REG_WIDTH),
            dbg_inst_cycle=Counter(self.REG_WIDTH),
            # dbg_ttl_cycle=Counter(self.REG_WIDTH),
            # dbg_wait_cycle=Counter(self.REG_WIDTH),
            # dbg_result_overflow_count=Counter(self.REG_WIDTH),
            # dbg_result_count=Counter(self.REG_WIDTH),
            dbg_result_generated=Counter(self.REG_WIDTH),
            dbg_result_consumed=Counter(self.REG_WIDTH),
        )

        for (k, v) in self.all_counters.items():
            setattr(self, k, v)

    def elaborate(self, m):
        m = TModule()

        for (k, v) in self.all_counters.items():
            setattr(m.submodules, k, v)

        return m
