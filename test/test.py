import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

VAELIX_KEY = 0xB6
SEG_LOCKED = 0xC7
SEG_VERIFIED = 0xC1
SEG_OFF = 0xFF
LOCKOUT_CYCLES = 100


def get_bit(value: int, bit: int) -> int:
    return (value >> bit) & 0x1


async def reset_and_enable(dut):
    dut.ena.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)
    dut.ena.value = 1
    await ClockCycles(dut.clk, 2)


@cocotb.test()
async def test_protocol_lockout_and_recovery(dut):
    cocotb.start_soon(Clock(dut.clk, 40, unit="ns").start())
    await reset_and_enable(dut)

    assert int(dut.uo_out.value) == SEG_LOCKED
    telem = int(dut.uio_out.value)
    assert get_bit(telem, 7) == 0
    assert get_bit(telem, 6) == 0

    # Trigger lockout after five bad candidates
    for attempt, value in enumerate([0x01, 0x02, 0x03, 0x04, 0x05], start=1):
        dut.ui_in.value = value
        await ClockCycles(dut.clk, 2)
        telem = int(dut.uio_out.value)
        assert int(dut.uo_out.value) == SEG_LOCKED
        assert (telem & 0xF) == attempt

    telem = int(dut.uio_out.value)
    assert get_bit(telem, 6) == 1

    # Correct key remains blocked in lockout
    dut.ui_in.value = VAELIX_KEY
    await ClockCycles(dut.clk, 2)
    telem = int(dut.uio_out.value)
    assert get_bit(telem, 6) == 1
    assert get_bit(telem, 7) == 0

    # Reset clears lockout/counters
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    telem = int(dut.uio_out.value)
    assert get_bit(telem, 6) == 0
    assert (telem & 0xF) == 0

    dut.ui_in.value = 0x55
    await ClockCycles(dut.clk, 2)
    dut.ui_in.value = VAELIX_KEY
    await ClockCycles(dut.clk, 2)
    telem = int(dut.uio_out.value)
    assert int(dut.uo_out.value) == SEG_VERIFIED
    assert get_bit(telem, 7) == 1


@cocotb.test()
async def test_lockout_auto_timeout(dut):
    cocotb.start_soon(Clock(dut.clk, 40, unit="ns").start())
    await reset_and_enable(dut)

    # Reach lockout
    for value in [0x11, 0x12, 0x13, 0x14, 0x15]:
        dut.ui_in.value = value
        await ClockCycles(dut.clk, 2)

    telem = int(dut.uio_out.value)
    assert get_bit(telem, 6) == 1

    # Wait lockout timer + margin
    await ClockCycles(dut.clk, LOCKOUT_CYCLES + 5)
    telem = int(dut.uio_out.value)
    assert get_bit(telem, 6) == 0
    assert (telem & 0xF) == 0


@cocotb.test()
async def test_exhaustive_key_acceptance(dut):
    cocotb.start_soon(Clock(dut.clk, 40, unit="ns").start())
    await reset_and_enable(dut)

    for candidate in range(256):
        # reset each iteration to avoid lockout side effects
        dut.rst_n.value = 0
        await ClockCycles(dut.clk, 1)
        dut.rst_n.value = 1
        await ClockCycles(dut.clk, 1)

        dut.ui_in.value = candidate
        await ClockCycles(dut.clk, 2)

        telem = int(dut.uio_out.value)
        if candidate == VAELIX_KEY:
            assert int(dut.uo_out.value) == SEG_VERIFIED
            assert get_bit(telem, 7) == 1
            assert get_bit(telem, 4) == 1
            assert (telem & 0xF) == 0
        else:
            assert int(dut.uo_out.value) == SEG_LOCKED
            assert get_bit(telem, 7) == 0
            assert get_bit(telem, 4) == 0
