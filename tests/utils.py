#

class DDSChecker:
    @staticmethod
    async def idle(sim, port, n=10):
        for _ in range(n):
            assert sim.get(port.addr.o) == 0
            assert sim.get(port.data.oe) == (1 << 16) - 1
            assert sim.get(port.data.o) == 0
            assert sim.get(port.ctrl.o) == 0b011
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == (1 << 11) - 1
            await sim.tick()

    @staticmethod
    async def set1(sim, csr, port, *, id, addr1, data1):
        t_adsu = sim.get(csr.dds_write_adsu) + 1
        t_wrlow = sim.get(csr.dds_write_wrlow) + 1
        t_adhd = sim.get(csr.dds_write_adhd) + 1
        t_fuddl = sim.get(csr.dds_write_fuddl) + 1
        t_fudhd = sim.get(csr.dds_write_fudhd) + 1

        cs = ((1 << 11) - 1) ^ (1 << id)

        for _ in range(t_adsu):
            assert sim.get(port.addr.o) == addr1
            assert sim.get(port.data.oe) == (1 << 16) - 1
            assert sim.get(port.data.o) == data1
            assert sim.get(port.ctrl.o) == 0b011
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

        for _ in range(t_wrlow):
            assert sim.get(port.addr.o) == addr1
            assert sim.get(port.data.oe) == (1 << 16) - 1
            assert sim.get(port.data.o) == data1
            assert sim.get(port.ctrl.o) == 0b010
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

        for _ in range(t_fuddl):
            assert sim.get(port.addr.o) == addr1
            assert sim.get(port.data.oe) == (1 << 16) - 1
            assert sim.get(port.data.o) == data1
            assert sim.get(port.ctrl.o) == 0b011
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

        for _ in range(t_fudhd):
            assert sim.get(port.addr.o) == addr1
            assert sim.get(port.data.oe) == (1 << 16) - 1
            assert sim.get(port.data.o) == data1
            assert sim.get(port.ctrl.o) == 0b011
            assert sim.get(port.fud.o) == 1
            assert sim.get(port.cs.o) == cs
            await sim.tick()

    @staticmethod
    async def set2(sim, csr, port, *, id, addr1, data1, addr2, data2):
        t_adsu = sim.get(csr.dds_write_adsu) + 1
        t_wrlow = sim.get(csr.dds_write_wrlow) + 1
        t_adhd = sim.get(csr.dds_write_adhd) + 1
        t_fuddl = sim.get(csr.dds_write_fuddl) + 1
        t_fudhd = sim.get(csr.dds_write_fudhd) + 1

        cs = ((1 << 11) - 1) ^ (1 << id)

        for _ in range(t_adsu):
            assert sim.get(port.addr.o) == addr1
            assert sim.get(port.data.oe) == (1 << 16) - 1
            assert sim.get(port.data.o) == data1
            assert sim.get(port.ctrl.o) == 0b011
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

        for _ in range(t_wrlow):
            assert sim.get(port.addr.o) == addr1
            assert sim.get(port.data.oe) == (1 << 16) - 1
            assert sim.get(port.data.o) == data1
            assert sim.get(port.ctrl.o) == 0b010
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

        for _ in range(t_adhd):
            assert sim.get(port.addr.o) == addr1
            assert sim.get(port.data.oe) == (1 << 16) - 1
            assert sim.get(port.data.o) == data1
            assert sim.get(port.ctrl.o) == 0b011
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

        for _ in range(t_adsu):
            assert sim.get(port.addr.o) == addr2
            assert sim.get(port.data.oe) == (1 << 16) - 1
            assert sim.get(port.data.o) == data2
            assert sim.get(port.ctrl.o) == 0b011
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

        for _ in range(t_wrlow):
            assert sim.get(port.addr.o) == addr2
            assert sim.get(port.data.oe) == (1 << 16) - 1
            assert sim.get(port.data.o) == data2
            assert sim.get(port.ctrl.o) == 0b010
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

        for _ in range(t_fuddl):
            assert sim.get(port.addr.o) == addr2
            assert sim.get(port.data.oe) == (1 << 16) - 1
            assert sim.get(port.data.o) == data2
            assert sim.get(port.ctrl.o) == 0b011
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

        for _ in range(t_fudhd):
            assert sim.get(port.addr.o) == addr2
            assert sim.get(port.data.oe) == (1 << 16) - 1
            assert sim.get(port.data.o) == data2
            assert sim.get(port.ctrl.o) == 0b011
            assert sim.get(port.fud.o) == 1
            assert sim.get(port.cs.o) == cs
            await sim.tick()

    @staticmethod
    async def reset(sim, csr, port, *, id):
        rshd = sim.get(csr.dds_reset_rshd)

        cs = ((1 << 11) - 1) ^ (1 << id)

        for _ in range(rshd + 1):
            assert sim.get(port.addr.o) == 0
            assert sim.get(port.data.oe) == (1 << 16) - 1
            assert sim.get(port.data.o) == 0
            assert sim.get(port.ctrl.o) == 0b111
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

    @staticmethod
    async def get1(sim, csr, port, *, id, addr, data):
        asu = sim.get(csr.dds_read_asu)
        rdhoz = sim.get(csr.dds_read_rdhoz)

        cs = ((1 << 11) - 1) ^ (1 << id)

        sim.set(port.data.i, data)

        for _ in range(asu + 1):
            assert sim.get(port.addr.o) == addr
            assert sim.get(port.data.oe) == 0
            assert sim.get(port.data.o) == 0
            assert sim.get(port.ctrl.o) == 0b001
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

        for _ in range(rdhoz + 1):
            assert sim.get(port.addr.o) == 0
            assert sim.get(port.data.oe) == 0
            assert sim.get(port.data.o) == 0
            assert sim.get(port.ctrl.o) == 0b011
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

    @staticmethod
    async def get2(sim, csr, port, *, id, addr, data):
        asu = sim.get(csr.dds_read_asu)
        rdl = sim.get(csr.dds_read_rdl)
        rdhoz = sim.get(csr.dds_read_rdhoz)

        cs = ((1 << 11) - 1) ^ (1 << id)

        sim.set(port.data.i, data >> 16)

        for _ in range(asu + 1):
            assert sim.get(port.addr.o) == addr + 2
            assert sim.get(port.data.oe) == 0
            assert sim.get(port.data.o) == 0
            assert sim.get(port.ctrl.o) == 0b001
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

        if rdl != 0:
            for _ in range(rdl + 1):
                assert sim.get(port.addr.o) == addr
                assert sim.get(port.data.oe) == 0
                assert sim.get(port.data.o) == 0
                assert sim.get(port.ctrl.o) == 0b011
                assert sim.get(port.fud.o) == 0
                assert sim.get(port.cs.o) == cs
                await sim.tick()

        sim.set(port.data.i, data & 0xffff)

        for _ in range(asu + 1):
            assert sim.get(port.addr.o) == addr
            assert sim.get(port.data.oe) == 0
            assert sim.get(port.data.o) == 0
            assert sim.get(port.ctrl.o) == 0b001
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()

        for _ in range(rdhoz + 1):
            assert sim.get(port.addr.o) == 0
            assert sim.get(port.data.oe) == 0
            assert sim.get(port.data.o) == 0
            assert sim.get(port.ctrl.o) == 0b011
            assert sim.get(port.fud.o) == 0
            assert sim.get(port.cs.o) == cs
            await sim.tick()
