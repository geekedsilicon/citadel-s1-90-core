# VAELIX | PROJECT CITADEL — VERIFICATION PROTOCOL
**"Trust, but Verify. Then Verify Again."**

**Version:** 1.1.0  
**Engine:** Cocotb 2.0.1 + Icarus Verilog  
**Target:** S1-90 Sentinel Lock (IHP 130nm SG13G2)

This directory contains the automated test harness for the **S1-90 "Sentinel 
Lock"**. It drives the Device Under Test (DUT) through a rigorous suite of 
authorization vectors and intrusion deflection scenarios before any silicon 
is committed to the German fab.

---

## 01 | THE INTERROGATION PROTOCOL

Two distinct verification layers are executed before tape-out:

**Layer 1 — RTL Simulation (Functional)**
- **Objective:** Verify the Verilog logic intent: `ui_in == 0xB6` → Unlock.
- **Engine:** Icarus Verilog + Cocotb 2.0.1
- **Speed:** Near-instantaneous.

**Layer 2 — Gate-Level Simulation (Physical)**
- **Objective:** Verify the hardened GDSII netlist against the IHP 130nm PDK.
  Confirms physical AND/OR/DFF gates behave correctly under timing constraints.
- **Engine:** Icarus Verilog + IHP SG13G2 Standard Cell Library.

---

## 02 | ENVIRONMENT SETUP

### File Manifest
| File | Purpose |
| :--- | :--- |
| `Makefile` | Simulation control — targets `tt_um_vaelix_sentinel.v` |
| `tb.v` | Verilog testbench — instantiates `tt_um_vaelix_sentinel` |
| `test.py` | Cocotb Python test vectors — authorization + intrusion cases |
| `requirements.txt` | Pinned Python dependencies |
| `tb.gtkw` | Pre-configured GTKWave signal layout |

### Prerequisites
```sh
# 1. Install Icarus Verilog
sudo apt-get install -y iverilog

# 2. Install pinned Python dependencies (DO NOT use bare 'pip install cocotb')
pip install -r requirements.txt
```

Current pinned versions: `cocotb==2.0.1`, `pytest==8.4.2`

---

## 03 | EXECUTION COMMANDS

### A. RTL Simulation — Logic Verification

Verifies the structural Verilog intent against all authorization vectors:
```sh
make -B
```

### B. Gate-Level Simulation — Physical Verification

Step 1 — Harden the design via the GDS GitHub Action, then copy the netlist:
```sh
# LibreLane output path after GDS action completes:
cp ../runs/tt_um_vaelix_sentinel/results/final/verilog/gl/tt_um_vaelix_sentinel.v \
   gate_level_netlist.v
```

Step 2 — Run GLS:
```sh
make -B GATES=yes
```

### C. Waveform Format Override (VCD instead of FST)

FST is the default (more efficient). To force VCD output:
```sh
make -B FST=
```

This generates `tb.vcd` instead of `tb.fst`.

---

## 04 | WAVEFORM ANALYSIS

### GTKWave (with pre-configured Citadel signal layout)
```sh
gtkwave tb.fst tb.gtkw
```

### Surfer
```sh
surfer tb.fst
```

The `tb.gtkw` file pre-loads the complete Sentinel signal set:
`ena`, `clk`, `rst_n`, `ui_in[7:0]`, `uio_in[7:0]`, `uio_oe[7:0]`,
`uio_out[7:0]`, `uo_out[7:0]`

---

## 05 | EXPECTED SENTINEL RESPONSES

| `ui_in` Input | `uo_out` (7-Seg) | `uio_out` (Glow) | State |
| :--- | :--- | :--- | :--- |
| `0xB6` (`1011_0110`) | `0xC1` ('U') | `0xFF` (All ON) | ✅ AUTHORIZED |
| Any other value | `0xC7` ('L') | `0x00` (All OFF) | 🔒 LOCKED |
| `ena = 0` | `0xFF` (Blank) | `0x00` (All OFF) | ⚫ OFFLINE |

---

## 06 | INTRUSION DEFLECTION MATRIX

A compliant Sentinel must reject all single-bit deviations from `0xB6`:

| Attack Vector | Expected `uo_out` | Expected `uio_out` |
| :--- | :--- | :--- |
| `0xB7` (bit 0 flip) | `0xC7` | `0x00` |
| `0xB4` (bit 1 flip) | `0xC7` | `0x00` |
| `0xB2` (bit 2 flip) | `0xC7` | `0x00` |
| `0xFE` (bit 0 only) | `0xC7` | `0x00` |
| `0x00` (all LOW) | `0xC7` | `0x00` |
| `0xFF` (all HIGH) | `0xC7` | `0x00` |

---

## 07 | FAILURE TRIAGE

| Symptom | Probable Cause |
| :--- | :--- |
| `ModuleNotFoundError: cocotb` | Run `pip install -r requirements.txt` |
| `module tt_um_vaelix_sentinel not found` | Check `tb.v` instantiation name |
| `file not found: tt_um_vaelix_sentinel.v` | Check `PROJECT_SOURCES` in `Makefile` |
| `gate_level_netlist.v` missing on GLS run | Copy netlist per Section 03-B above |
| Tests pass but `uo_out` values wrong | Verify Active-LOW encoding in `test.py` |

---

*Vaelix Missionary Standard v1.2 — Zero-Defect Verification Enforced*
