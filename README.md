![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/fpga/badge.svg)

# VAELIX | PROJECT CITADEL
## S1-90 "ATOMIC" SILICON PROTOTYPE
**"The Luxury of Silence. The Certainty of Logic."**

---

## 01 | THE MISSION
**Project Citadel** is the computational foundation of the Vaelix ecosystem. The **S1-90 Core** represents our transition from high-fidelity FPGA prototyping on **Xilinx RFSoC 4x2** and **PYNQ-Z2** platforms to custom, mission-critical ASIC hardware. 

This repository contains the hardened structural Verilog for the **Sentinel Lock**—a cryptographic hardware authorization gate engineered for the **IHP 130nm SG13G2** process (Tiny Tapeout 06 / IHP26a Shuttle).



---

## 02 | ARCHITECTURAL STANDARDS
At Vaelix, we do not settle for "functional." We demand **Symmetry and Resilience**. All assets within this repository adhere to the **Vaelix Missionary Standard v1.2**:

* **Logic Primitives:** Engineered using bitwise-accurate Citadel Primitives to ensure transistor-level predictability.
* **Integrity:** `keep_hierarchy` enforcement prevents synthesis flattening, preserving our structural intellectual property.
* **Verification:** Zero-defect net declaration via `` `default_nettype none ``.
* **Performance:** Clocked at a stable **25MHz** to prioritize authorization certainty over hazardous raw speed.

---

## 03 | THE SENTINEL PROTOCOL
The S1-90 Core implements the **Sentinel Lock**, an 8-bit hardware-level security gate.

* **Verification:** Transistor-gate comparison against the Vaelix Key: `0xB6`.
* **Telemetry:** Real-time system status via an Active-LOW 7-segment interface.
* **Persistence:** Structured telemetry on `uio_out` enables deterministic SaaS bridge ingestion.



[Image of logic gate symbols and truth tables]


---

## 04 | REPOSITORY STRUCTURE
* [`src/`](src/): Hardened Verilog source and IHP-optimized synthesis configurations.
* [`docs/`](docs/info.md): Detailed operational theory and hardware-level "Manual of Arms."
* [`test/`](test/): Rigorous testbenches for intrusion deflection and logic verification.

---

## 05 | THE VAELIX PIPELINE
The GDSII files in this repository are automatically hardened using the **LibreLane** ASIC flow. Every commit triggers a full suite of LVS (Layout vs. Schematic) and DRC (Design Rule Checks) to ensure that the silicon arriving from the German fab is as perfect as the logic that birthed it.

### **TECHNICAL SPECIFICATIONS**
| Parameter | Specification |
| :--- | :--- |
| **Process Node** | IHP 130nm SG13G2 |
| **Die Area** | 1x1 Tile (167x108 µm) |
| **Logic Density** | 65% (Fortified) |
| **Target Power** | Optimized for VX-1 Telemetry Modules |

---


## 06 | SAAS BRIDGE PROTOCOL
The hardware now exposes an explicit command/telemetry contract for an external MCU that
relays state to the Vaelix SaaS platform:

* `ui_in[7:0]`: candidate key byte (any value change is a submission event)
* `uio_out[7]`: authorized flag
* `uio_out[6]`: lockout flag
* `uio_out[5]`: event toggle bit
* `uio_out[4]`: last command result
* `uio_out[3:0]`: failed-attempt counter
* `rst_n` pulse: clears lockout / resets bridge session

Reference bridge firmware and JSON payload formatter live in [`firmware/`](firmware/).

---

## 07 | FIRMWARE READINESS
A reference firmware package is now included in [`firmware/`](firmware/) for MCU-side
bridge integration. It provides HAL hooks to drive candidate bytes/reset pulses, read telemetry bits,
and format deterministic JSON payloads suitable for direct SaaS ingest pipelines.

## 08 | CONTACT & CUSTODY
**VAELIX SYSTEMS** *The Louis Vuitton of Defense and Deep Tech.*



---
© 2026 Vaelix Systems Engineering. All Rights Reserved. TIER 1 Clearance Required for Full Schematic Access.
