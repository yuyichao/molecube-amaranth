#

from amaranth import *
from amaranth.lib import io

from transactron import TModule
from transactron.testing import TestCaseWithSimulator, SimpleTestCircuit

from molecube_amaranth.clockout import ClockOutController

import pytest

def get_clkout_test():
    m = TModule()
    port = io.SimulationPort("o", 1)
    m.submodules.buff = buff = io.Buffer("o", port)
    controller = ClockOutController(buff)
    m.submodules.circ = circ = SimpleTestCircuit(controller)

    return m, circ, port

class TestClockOut(TestCaseWithSimulator):
    def test_idle(self):
        m, circ, port = get_clkout_test()

        async def f(sim):
            assert sim.get(port.o) == 0
            for _ in range(1000):
                await sim.tick()
                assert sim.get(port.o) == 0

        with self.run_simulation(m) as sim:
            sim.add_testbench(f)

    @pytest.mark.parametrize("half_cycle", range(1, 256))
    def test_clockout(self, half_cycle):
        m, circ, port = get_clkout_test()

        async def testclock(sim):
            await circ.set.call(sim, div=half_cycle - 1)

            for _ in range(4):
                for i in range(half_cycle):
                    assert sim.get(port.o) == 0
                    await sim.tick()
                for i in range(half_cycle):
                    assert sim.get(port.o) == 1
                    await sim.tick()

            # Check to make sure that the clock will start from 0 no matter where it was

            assert sim.get(port.o) == 0
            await circ.set.call(sim, div=half_cycle - 1)

            for i in range(half_cycle):
                assert sim.get(port.o) == 0
                await sim.tick()

            assert sim.get(port.o) == 1

            await circ.set.call(sim, div=half_cycle - 1)
            for i in range(half_cycle):
                assert sim.get(port.o) == 0
                await sim.tick()
            for i in range(half_cycle):
                assert sim.get(port.o) == 1
                await sim.tick()

            await circ.set.call(sim, div=255)

            # Make sure the clock can be stopped
            for _ in range(1000):
                assert sim.get(port.o) == 0
                await sim.tick()

        with self.run_simulation(m, max_cycles=1000_000) as sim:
            sim.add_testbench(testclock)
