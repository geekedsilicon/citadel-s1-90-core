/*
 * ============================================================================
 * VAELIX | PROJECT CITADEL — INTERROGATION HARNESS
 * ============================================================================
 * FILE:      test/tb.v
 * VERSION:   1.1.0 — Citadel Standard
 * TARGET:    Tiny Tapeout 06 (IHP 130nm SG13G2)
 * MODULE:    tb (Testbench Wrapper)
 * PURPOSE:   Instantiates the Sentinel Core for Cocotb verification.
 * FORMAT:    FST (Fast Signal Trace)
 *
 * FIX LOG:
 *   v1.1.0 — [CRITICAL] tt_um_example -> tt_um_vaelix_sentinel
 *   v1.1.0 — [CRITICAL] uo_out port connection restored (was absent)
 *   v1.1.0 — Signal comments updated to Sentinel Protocol nomenclature
 * ============================================================================
 */

`default_nettype none
`timescale 1ns / 1ps

module tb ();

  /* -----------------------------------------------------------------------
   * 1. TELEMETRY RECORDING
   * -----------------------------------------------------------------------
   * Dumps all simulation signals to tb.fst.
   * View with: gtkwave tb.fst tb.gtkw  OR  surfer tb.fst
   */
  initial begin
    $dumpfile("tb.fst");
    $dumpvars(0, tb);
    #1;
  end

  /* -----------------------------------------------------------------------
   * 2. SIGNAL DEFINITIONS
   * -----------------------------------------------------------------------
   * Registers driven by Cocotb test.py.
   * Wires monitored and asserted by Cocotb test.py.
   */
  reg        clk;       // System Clock
  reg        rst_n;     // System Reset     (active LOW)
  reg        ena;       // Power Enable     (always 1 when active)

  reg  [7:0] ui_in;     // Authorization Key input    (DIP switches)
  reg  [7:0] uio_in;    // Bidirectional IO input      (unused)

  wire [7:0] uo_out;    // 7-Segment Telemetry output  (Active LOW)
  wire [7:0] uio_out;   // Status Array output         ("Vaelix Glow")
  wire [7:0] uio_oe;    // IO Direction Control        (all OUTPUT)

  /* -----------------------------------------------------------------------
   * 3. DUT INSTANTIATION — S1-90 SENTINEL CORE
   * -----------------------------------------------------------------------
   * All ports explicitly connected. default_nettype none enforces
   * that any missing connection is a compile error, not a silent bug.
   */
  tt_um_vaelix_sentinel user_project (
      .ui_in   (ui_in),    // Authorization Key (target: 0xB6)
      .uo_out  (uo_out),   // 7-Segment display (Active LOW)
      .uio_in  (uio_in),   // Unused IO input
      .uio_out (uio_out),  // Status "Glow" array
      .uio_oe  (uio_oe),   // IO enable vector
      .ena     (ena),      // Power enable
      .clk     (clk),      // System clock
      .rst_n   (rst_n)     // System reset (active LOW)
  );

endmodule
