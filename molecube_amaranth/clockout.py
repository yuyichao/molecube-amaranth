#

from amaranth import *

from transactron import TModule, Transaction, Method, def_method

from .utils import assign_xvalue

class ClockOutController(Elaboratable):
    def __init__(self, clockoutio, *, div_width=8):
        self.clockoutio = clockoutio
        self.div_width = div_width
        self.OFF = (1 << div_width) - 1
        self.set = Method(i=[('div', div_width)])

    def elaborate(self, plat):
        m = TModule()

        counter = Signal(self.div_width)
        divider = Signal(self.div_width, init=self.OFF)
        out = Signal(1)
        m.d.comb += [self.clockoutio.o.eq(out),
                     self.clockoutio.oe.eq(1)]

        with m.If(divider == self.OFF):
            assign_xvalue(m, counter)
            m.d.sync += out.eq(0)
        with m.Elif(counter == 0):
            m.d.sync += [counter.eq(divider),
                         out.eq(~out)]
        with m.Else():
            m.d.sync += counter.eq(counter - 1)

        # The only conflict we should have is potentially trying to
        # reset while running the sequence,
        # this can be supported by simplying or-ing the input to make sure
        # the divider is OFF.
        def combiner(m, args, runs):
            div = C(0, 8)
            for i, v in enumerate(args):
                div = div | Mux(runs[i], v.div, 0)
            return {"div": div}

        @def_method(m, self.set, combiner=combiner, nonexclusive=True)
        def _(div):
            m.d.sync += [divider.eq(div),
                         counter.eq(div),
                         out.eq(0)]

        return m
