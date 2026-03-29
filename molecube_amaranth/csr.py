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

        @def_method(m, self.count)
        def _():
            m.d.sync += self.value.eq(self.value + 1)

        @def_method(m, self.clear, nonexclusive=True)
        def _():
            m.d.sync += self.value.eq(0)

        return m
