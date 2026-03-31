import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

VAELIX_KEY = 0xB6
SEG_LOCKED = 0xC7
SEG_VERIFIED = 0xC1
SEG_OFF = 0xFF


def get_bit(value: int, bit: int) -> int:
    return (value >> bit) & 0x1


@cocotb.test()
async def test_sentinel_saas_bridge_protocol(dut):
    cocotb.start_soon(Clock(dut.clk, 40, unit="ns").start())

    dut.ena.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    assert int(dut.uo_out.value) == SEG_OFF

    dut.ena.value = 1
    await ClockCycles(dut.clk, 2)

    assert int(dut.uo_out.value) == SEG_LOCKED
    telem = int(dut.uio_out.value)
    assert get_bit(telem, 7) == 0
    assert get_bit(telem, 6) == 0
    assert (telem & 0xF) == 0

    event_start = get_bit(telem, 5)

    bad_values = [0x01, 0x02, 0x03, 0x04, 0x05]
    for attempt, value in enumerate(bad_values, start=1):
        dut.ui_in.value = value
        await ClockCycles(dut.clk, 2)
        telem = int(dut.uio_out.value)
        assert int(dut.uo_out.value) == SEG_LOCKED
        assert get_bit(telem, 7) == 0
        assert get_bit(telem, 4) == 0
        if attempt < 5:
            assert get_bit(telem, 6) == 0
        assert (telem & 0xF) == attempt

    telem = int(dut.uio_out.value)
    assert get_bit(telem, 6) == 1

    # Correct key while lockout active remains blocked
    dut.ui_in.value = VAELIX_KEY
    await ClockCycles(dut.clk, 2)
    telem = int(dut.uio_out.value)
    assert get_bit(telem, 6) == 1
    assert get_bit(telem, 7) == 0

    # Clear via reset pulse
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    telem = int(dut.uio_out.value)
    assert get_bit(telem, 6) == 0
    assert (telem & 0xF) == 0

    # change away and back to key to generate submission event for valid key
    dut.ui_in.value = 0x55
    await ClockCycles(dut.clk, 2)
    dut.ui_in.value = VAELIX_KEY
    await ClockCycles(dut.clk, 2)

    telem = int(dut.uio_out.value)
    assert int(dut.uo_out.value) == SEG_VERIFIED
    assert get_bit(telem, 7) == 1
    assert get_bit(telem, 4) == 1
    assert get_bit(telem, 5) != event_start
