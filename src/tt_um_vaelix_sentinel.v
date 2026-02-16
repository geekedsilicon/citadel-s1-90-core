/*
 * ============================================================================
 * VAELIX | PROJECT CITADEL: S1-90 CORE
 * ============================================================================
 * COPYRIGHT:  (c) 2026 Vaelix Systems Engineering
 * SPDX-License-Identifier: Apache-2.0
 * FILE:       src/tt_um_vaelix_sentinel.v
 * TARGET:     Tiny Tapeout 06 (IHP 130nm SG13G2)
 * MODULE:     tt_um_vaelix_sentinel
 * STANDARD:   Vaelix Missionary Standard v1.2
 *
 * DESCRIPTION:
 * Primary structural logic for the S1-90 "Sentinel Lock."
 * Implements an 8-bit cryptographic authorization gate (Key: 0xB6)
 * with Active-LOW 7-segment telemetry for the TT06 Demo Board.
 *
 * FIX LOG:
 *   v1.1.0 — [CRITICAL] Added (* keep_hierarchy *) per Vaelix Standard
 *   v1.1.0 — [MODERATE] Wire constants migrated to localparam
 *   v1.1.0 — Segment encodings verified against TT06 Active-LOW pinout
 * ============================================================================
 */

`default_nettype none

(* keep_hierarchy *)
module tt_um_vaelix_sentinel (
    input  wire [7:0] ui_in,    // Dedicated inputs  — Authorization Key (DIP Switches)
    output wire [7:0] uo_out,   // Dedicated outputs — 7-Segment Display  (Active LOW)
    input  wire [7:0] uio_in,   // IOs: Input path   — Unused
    output wire [7:0] uio_out,  // IOs: Output path  — Status Array ("Vaelix Glow")
    output wire [7:0] uio_oe,   // IOs: Enable path  — Directional Control
    input  wire       ena,      // Power Enable      — Always 1 when active
    input  wire       clk,      // System Clock      — Unused (Combinational)
    input  wire       rst_n     // System Reset      — Unused (Combinational)
);

    /* -----------------------------------------------------------------------
     * 0. CITADEL CONSTANTS
     * -----------------------------------------------------------------------
     * Elaboration-time constants — zero silicon cost.
     * Verified against TT06 Active-LOW (Common Anode) pinout.
     *   uo[0]=SEG_A, uo[1]=SEG_B, ..., uo[7]=SEG_DP
     */
    localparam [7:0] VAELIX_KEY    = 8'hB6;  // 1011_0110

    localparam [7:0] SEG_LOCKED    = 8'hC7;  // 'L': segments f,e,d ON
    localparam [7:0] SEG_VERIFIED  = 8'hC1;  // 'U': segments f,e,d,c,b ON
    localparam [7:0] SEG_OFF       = 8'hFF;  // All segments OFF

    /* -----------------------------------------------------------------------
     * 1. AUTHORIZATION LOGIC
     * -----------------------------------------------------------------------
     * Hardcoded bitwise comparison for instantaneous verification.
     * No clock required — combinational gate mesh.
     */
    wire auth_gate_state;
    assign auth_gate_state = (ui_in == VAELIX_KEY);

    /* -----------------------------------------------------------------------
     * 2. VISUAL TELEMETRY (7-SEGMENT / ACTIVE LOW)
     * -----------------------------------------------------------------------
     * ena=0 → Display OFF  (board unpowered / project deselected)
     * ena=1, locked   → Display 'L'
     * ena=1, verified → Display 'U'
     */
    assign uo_out = ena ? (auth_gate_state ? SEG_VERIFIED : SEG_LOCKED)
                        : SEG_OFF;

    /* -----------------------------------------------------------------------
     * 3. STATUS ARRAY ("VAELIX GLOW")
     * -----------------------------------------------------------------------
     * Authorized → All 8 LEDs HIGH (0xFF) — Vaelix Glow active
     * Locked     → All 8 LEDs LOW  (0x00) — Silent
     * All UIO pins set to OUTPUT mode unconditionally.
     */
    assign uio_out = (ena & auth_gate_state) ? 8'hFF : 8'h00;
    assign uio_oe  = 8'hFF;

    /* -----------------------------------------------------------------------
     * 4. UNUSED SIGNAL TERMINATION
     * -----------------------------------------------------------------------
     * Bitwise reduction suppresses synthesis warnings without creating nets.
     */
    wire _unused_ok = &{uio_in, clk, rst_n, 1'b0};

endmodule
