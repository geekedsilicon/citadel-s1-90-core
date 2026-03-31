/*
 * ============================================================================
 * VAELIX | PROJECT CITADEL: S1-90 CORE
 * ============================================================================
 * COPYRIGHT:  (c) 2026 Vaelix Systems Engineering
 * SPDX-License-Identifier: Apache-2.0
 * FILE:       src/tt_um_vaelix_sentinel.v
 * TARGET:     Tiny Tapeout 06 (IHP 130nm SG13G2)
 * MODULE:     tt_um_vaelix_sentinel
 * STANDARD:   Vaelix Missionary Standard v1.3
 *
 * DESCRIPTION:
 * Stateful Sentinel Lock with explicit command/telemetry signaling so an
 * external host MCU can bridge device state to the Vaelix SaaS platform.
 *
 * INPUT STRATEGY
 *   Candidate bytes are sampled from ui_in; each ui_in change is treated as a
 *   new submission event. Lockout clear occurs via rst_n assertion.
 *
 * TELEMETRY OUTPUTS (uio_out)
 *   uio_out[7] = AUTHORIZED
 *   uio_out[6] = LOCKOUT
 *   uio_out[5] = EVENT_TOGGLE   (toggles each submission event)
 *   uio_out[4] = LAST_RESULT    (1=last submit accepted)
 *   uio_out[3:0] = FAILED_ATTEMPTS (saturating counter nibble)
 * ============================================================================
 */

`default_nettype none

(* keep_hierarchy *)
module tt_um_vaelix_sentinel (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    localparam [7:0] VAELIX_KEY      = 8'hB6;
    localparam [7:0] SEG_LOCKED      = 8'hC7;
    localparam [7:0] SEG_VERIFIED    = 8'hC1;
    localparam [7:0] SEG_OFF         = 8'hFF;

    localparam [3:0] MAX_FAILED      = 4'd5;
    localparam [7:0] LOCKOUT_CYCLES  = 8'd100;

    reg        auth_state;
    reg        lockout_state;
    reg        event_toggle;
    reg        last_result;
    reg [3:0]  failed_attempts;
    reg [7:0]  lockout_timer;
    reg [7:0]  last_candidate;

    wire key_match = (ui_in == VAELIX_KEY);
    wire submission_event = (ui_in != last_candidate);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            auth_state      <= 1'b0;
            lockout_state   <= 1'b0;
            event_toggle    <= 1'b0;
            last_result     <= 1'b0;
            failed_attempts <= 4'd0;
            lockout_timer   <= 8'd0;
            last_candidate  <= 8'd00;
        end else if (!ena) begin
            auth_state      <= 1'b0;
            lockout_state   <= 1'b0;
            event_toggle    <= 1'b0;
            last_result     <= 1'b0;
            failed_attempts <= 4'd0;
            lockout_timer   <= 8'd0;
            last_candidate  <= 8'd00;
        end else begin
            if (lockout_state) begin
                if (lockout_timer != 8'd0) begin
                    lockout_timer <= lockout_timer - 8'd1;
                end else begin
                    lockout_state   <= 1'b0;
                    failed_attempts <= 4'd0;
                end
                auth_state  <= 1'b0;
                last_result <= 1'b0;
            end else if (submission_event) begin
                event_toggle   <= ~event_toggle;
                last_candidate <= ui_in;

                if (key_match) begin
                    auth_state      <= 1'b1;
                    last_result     <= 1'b1;
                    failed_attempts <= 4'd0;
                end else begin
                    auth_state  <= 1'b0;
                    last_result <= 1'b0;

                    if (failed_attempts < 4'hF) begin
                        failed_attempts <= failed_attempts + 4'd1;
                    end

                    if ((failed_attempts + 4'd1) >= MAX_FAILED) begin
                        lockout_state <= 1'b1;
                        lockout_timer <= LOCKOUT_CYCLES;
                    end
                end
            end
        end
    end

    assign uo_out = ena ? (auth_state ? SEG_VERIFIED : SEG_LOCKED) : SEG_OFF;

    assign uio_out[7]   = auth_state;
    assign uio_out[6]   = lockout_state;
    assign uio_out[5]   = event_toggle;
    assign uio_out[4]   = last_result;
    assign uio_out[3:0] = failed_attempts;
    assign uio_oe       = 8'hFF;

    wire _unused_ok = &{uio_in, 1'b0};

endmodule
