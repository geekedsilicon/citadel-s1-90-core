# ============================================================================
# VAELIX | PROJECT CITADEL — INTERROGATION SCRIPT
# ============================================================================
# FILE:      test/test.py
# VERSION:   1.1.0 — Citadel Standard
# TARGET:    Tiny Tapeout 06 (IHP 130nm SG13G2)
# ENGINE:    Cocotb 2.0.1 (Python Verification Framework)
# PURPOSE:   Brute-Force Verification of the S1-90 Sentinel Lock Logic.
#
# FIX LOG:
#   v1.1.0 — [CRITICAL] Phase II assertions: raw value -> int() cast (cocotb 2.0)
#   v1.1.0 — [CRITICAL] Debrief log count corrected: 255 -> 256 vectors total
#   v1.1.0 — [MODERATE] ClockCycles -> Timer(1ns) propagation guard on comb. logic
#   v1.1.0 — Clock comment updated: explicitly states 25MHz
# ============================================================================

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

# --- CITADEL CONSTANTS ------------------------------------------------------
# THE VAELIX KEY: 0xB6 (1011_0110)
VAELIX_KEY = 0xB6

# TELEMETRY STATES — Active LOW / Common Anode 7-Segment
# 'L' (Locked)   : Segments F, E, D ON         -> 0xC7
# 'U' (Verified) : Segments F, E, D, C, B ON   -> 0xC1
# OFF            : All Segments OFF             -> 0xFF
SEG_LOCKED   = 0xC7
SEG_VERIFIED = 0xC1
SEG_OFF      = 0xFF

# STATUS ARRAY STATES — Active HIGH
GLOW_ON  = 0xFF
GLOW_OFF = 0x00


@cocotb.test()
async def test_sentinel_logic(dut):
    """
    THE INTERROGATION:
    Iterates through all 256 possible 8-bit input vectors to verify
    ONLY the Vaelix Key (0xB6) triggers the Authorized state.
    All 255 remaining vectors must be rejected without exception.
    """

    dut._log.info("-------------------------------------------------------")
    dut._log.info("VAELIX SENTINEL | STARTING INTERROGATION PROTOCOL")
    dut._log.info("-------------------------------------------------------")

    # ------------------------------------------------------------------
    # 1. CLOCK INITIALIZATION
    # ------------------------------------------------------------------
    # 40ns period = 25MHz. Stability target per Vaelix Missionary Std.
    # Clock is driven for simulation timeline stability even though the
    # Sentinel core is purely combinational logic.
    clock = Clock(dut.clk, 40, unit="ns")
    cocotb.start_soon(clock.start())

    # ------------------------------------------------------------------
    # 2. SYSTEM RESET & ENABLE
    # ------------------------------------------------------------------
    dut._log.info("[SETUP] Initializing power and reset vectors...")
    dut.ena.value   = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 5)   # Stabilization hold
    dut.rst_n.value = 1
    dut._log.info("[SETUP] System active. ena=1, rst_n=1.")

    # ------------------------------------------------------------------
    # 3. PHASE I — BRUTE FORCE ATTACK (0x00 to 0xFF)
    # ------------------------------------------------------------------
    dut._log.info("[PHASE I] Executing 8-bit brute force attack (0x00-0xFF)...")

    for i in range(256):
        dut.ui_in.value = i

        # Timer propagation guard — combinational logic settles after
        # propagation delay, not a clock edge. 1ns is sufficient for
        # Icarus with the 40ns clock period.
        await Timer(1, units="ns")

        # Capture outputs with explicit int() cast (cocotb 2.0 safe)
        telemetry = int(dut.uo_out.value)
        status    = int(dut.uio_out.value)

        if i == VAELIX_KEY:
            # AUTHORIZED VECTOR — must unlock
            dut._log.info(
                f"  [KEY] VECTOR 0x{i:02X} -> "
                f"7SEG=0x{telemetry:02X} GLOW=0x{status:02X} | AUTHORIZED"
            )
            assert telemetry == SEG_VERIFIED, (
                f"CRITICAL FAILURE: Key 0xB6 did not unlock! "
                f"Expected 0x{SEG_VERIFIED:02X}, got 0x{telemetry:02X}"
            )
            assert status == GLOW_ON, (
                f"CRITICAL FAILURE: Vaelix Glow failed on Key! "
                f"Expected 0x{GLOW_ON:02X}, got 0x{status:02X}"
            )

        else:
            # INTRUSION VECTOR — must be rejected
            assert telemetry == SEG_LOCKED, (
                f"SECURITY BREACH: Vector 0x{i:02X} bypassed the lock! "
                f"Expected 0x{SEG_LOCKED:02X}, got 0x{telemetry:02X}"
            )
            assert status == GLOW_OFF, (
                f"SECURITY BREACH: Vector 0x{i:02X} triggered Status Array! "
                f"Expected 0x{GLOW_OFF:02X}, got 0x{status:02X}"
            )

    dut._log.info(
        "[PHASE I] Brute force complete. "
        "256 vectors tested. 255 intrusion attempts deflected."
    )

    # ------------------------------------------------------------------
    # 4. PHASE II — POWER-DOWN SECURITY CHECK
    # ------------------------------------------------------------------
    dut._log.info("[PHASE II] Verifying power-down security (ena=0)...")

    dut.ui_in.value = VAELIX_KEY    # Present valid key
    dut.ena.value   = 0             # Cut power

    await Timer(1, units="ns")      # Propagation guard

    # Explicit int() cast — required for reliable comparison in cocotb 2.0
    assert int(dut.uo_out.value) == SEG_OFF, (
        f"FAILURE: Display active during power-down! "
        f"Expected 0x{SEG_OFF:02X}, got 0x{int(dut.uo_out.value):02X}"
    )
    assert int(dut.uio_out.value) == GLOW_OFF, (
        f"FAILURE: Status array active during power-down! "
        f"Expected 0x{GLOW_OFF:02X}, got 0x{int(dut.uio_out.value):02X}"
    )

    dut._log.info("[PHASE II] Power-down security confirmed. All outputs silent.")

    # ------------------------------------------------------------------
    # 5. PHASE III — POWER RESTORE + RE-AUTHORIZATION CHECK
    # ------------------------------------------------------------------
    dut._log.info("[PHASE III] Verifying re-authorization after power restore...")

    dut.ena.value = 1               # Restore power
    await Timer(1, units="ns")      # Propagation guard

    assert int(dut.uo_out.value) == SEG_VERIFIED, (
        f"FAILURE: Re-authorization failed after power restore! "
        f"Expected 0x{SEG_VERIFIED:02X}, got 0x{int(dut.uo_out.value):02X}"
    )
    assert int(dut.uio_out.value) == GLOW_ON, (
        f"FAILURE: Glow did not restore after power-on! "
        f"Expected 0x{GLOW_ON:02X}, got 0x{int(dut.uio_out.value):02X}"
    )

    dut._log.info("[PHASE III] Re-authorization confirmed.")

    # ------------------------------------------------------------------
    # 6. MISSION DEBRIEF
    # ------------------------------------------------------------------
    dut._log.info("-------------------------------------------------------")
    dut._log.info("VAELIX SENTINEL | INTERROGATION SUCCESSFUL")
    dut._log.info("  256 vectors tested | 255 intrusions deflected")
    dut._log.info("  Power-down and power-restore sequences verified")
    dut._log.info("  S1-90 Core cleared for tape-out")
    dut._log.info("-------------------------------------------------------")
