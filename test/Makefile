# ============================================================================
# VAELIX | PROJECT CITADEL — CORE VERIFICATION ENGINE
# ============================================================================
# FILE:      test/Makefile
# VERSION:   1.2.0 — Citadel Standard
# TARGET:    Tiny Tapeout 06 (IHP 130nm SG13G2)
# ENGINE:    Cocotb 2.0.1 + Icarus Verilog
# FORMAT:    FST (Fast Signal Trace) — Vaelix Efficiency Standard
#
# FIX LOG:
#   v1.2.0 — [CRITICAL] MODULE reverted fix: restored COCOTB_TEST_MODULES
#   v1.2.0 — [CRITICAL] PROJECT_SOURCES reverted fix: restored sentinel .v
#   v1.1.0 — MODULE -> COCOTB_TEST_MODULES (cocotb 2.0 migration)
#   v1.1.0 — PROJECT_SOURCES: project.v -> tt_um_vaelix_sentinel.v
#   v1.1.0 — FST waveform output enabled by default
# ============================================================================

# --- SIMULATION CONFIGURATION -----------------------------------------------
SIM           ?= icarus
FST           ?= -fst
TOPLEVEL_LANG ?= verilog
IVERILOG      ?= iverilog
VVP           ?= vvp

# --- SOURCE DEFINITIONS -----------------------------------------------------
# SRC_DIR:         Location of the Citadel structural logic.
# PROJECT_SOURCES: The Sentinel Core — must match info.yaml source_files.
SRC_DIR         = $(PWD)/../src
PROJECT_SOURCES = tt_um_vaelix_sentinel.v

# --- SIMULATION MODES -------------------------------------------------------
ifneq ($(GATES),yes)

    # MODE: RTL — Fast functional verification of the Vaelix logic intent.
    SIM_BUILD        = sim_build/rtl
    VERILOG_SOURCES += $(addprefix $(SRC_DIR)/,$(PROJECT_SOURCES))

else

    # MODE: GLS — Physical reality check against the IHP SG13G2 PDK.
    # Before running: copy hardened netlist per test/README.md Section 03-B.
    SIM_BUILD        = sim_build/gl

    COMPILE_ARGS    += -DGL_TEST
    COMPILE_ARGS    += -DFUNCTIONAL
    COMPILE_ARGS    += -DSIM

    # IHP 130nm Standard Cell Libraries (Foundry Definitions)
    VERILOG_SOURCES += $(PDK_ROOT)/ihp-sg13g2/libs.ref/sg13g2_io/verilog/sg13g2_io.v
    VERILOG_SOURCES += $(PDK_ROOT)/ihp-sg13g2/libs.ref/sg13g2_stdcell/verilog/sg13g2_stdcell.v

    # Hardened GDS netlist — injected by GitHub Actions / copied manually
    VERILOG_SOURCES += $(PWD)/gate_level_netlist.v

endif

# --- ENVIRONMENT SETUP ------------------------------------------------------
COMPILE_ARGS    += -I$(SRC_DIR)

# --- TESTBENCH INTEGRATION --------------------------------------------------
VERILOG_SOURCES += $(PWD)/tb.v
TOPLEVEL         = tb

# --- TEST MODULE (cocotb 2.0 — DO NOT revert to MODULE = test) --------------
COCOTB_TEST_MODULES = test

# --- COCOTB EXECUTION -------------------------------------------------------
include $(shell cocotb-config --makefiles)/Makefile.sim
