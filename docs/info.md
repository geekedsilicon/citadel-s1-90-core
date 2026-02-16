# VAELIX | PROJECT CITADEL: S1-90 CORE
**Version:** 1.0.0-PROT  
**Target Silicon:** IHP 130nm SG13G2 (Tiny Tapeout 06)  
**Security Tier:** TIER 1 Authorization Proof-of-Concept  

---

## How It Works

The **S1-90 Core** is a hardware-level cryptographic "Sentinel Lock." It serves as a structural proof-of-concept for the Vaelix Sector 1 Citadel architecture. Unlike software-based authentication, the S1-90 utilizes a hardcoded logic gate mesh to verify authorization at the transistor level.

### **Architectural Overview**
1.  **Authorization Mesh:** An 8-bit comparator logic block continuously monitors the `ui_in` bus.
2.  **The Vaelix Key:** Access is granted only when the input vector matches the hardcoded key `0xB6` (`1011_0110`).
3.  **Visual Telemetry:** Upon successful authorization, the core triggers a state-change in the 7-segment display and the "Vaelix Glow" status array.
4.  **Structural Integrity:** The design uses **Citadel Primitives** (bitwise-optimized gates) and enforces `keep_hierarchy` to ensure the silicon footprint remains an exact mirror of the Verilog intent.



[Image of a logic gate symbols and truth tables]


---

## How To Test

Testing the Sentinel Lock requires the **Tiny Tapeout 06 Demo Board** or a compatible simulation environment (DigitalJS / EDA Playground).

### **1. Power On & Initialization**
* Ensure the board is powered and the project is selected.
* The 7-segment display should default to **'L'** (Locked), represented by the active-LOW hex value `0xC7`.
* All Status LEDs (UIO) should be **OFF**.

### **2. Authorization Sequence**
* **The Challenge:** Use the 8-position DIP switches (`ui_in[7:0]`) to enter the Vaelix Key.
* **The Code:** Set switches to `10110110` (Binary for 0xB6).
* **The Response:** * The 7-segment display will instantly transition to **'U'** (Unlocked/Verified), represented by hex `0xC1`.
    * The Status LED array will ignite (The **Vaelix Glow**), indicating a high-integrity connection.

### **3. Intrusion Deflection**
* Changing any single bit from the `0xB6` key will immediately revert the system to the **'L'** (Locked) state, demonstrating instantaneous logic-gate rejection.

---

## External Hardware

The S1-90 Core is engineered to interface seamlessly with standard Vaelix-cleared laboratory equipment:

* **Tiny Tapeout Demo Board:** Primary interface for manual key entry and 7-segment telemetry.
* **DIP Switches:** Used for 8-bit key injection via the `ui_in` port.
* **Common Anode 7-Segment Display:** Integrated visual output for system status (Active-LOW).
* **Vaelix Status Array:** 8-bit LED bank on the `uio_out` bus for verification feedback.
* **Xilinx PYNQ-Z2 / RFSoC 4x2:** (Pre-Silicon Development) Used for initial logic validation before IHP 130nm tape-out.



---

## Engineering Standards
* **Directive:** `` `default_nettype none `` (Enforced)
* **Frequency:** 25 MHz (Optimized for Stability)
* **Standard:** Vaelix Missionary Standard v1.2
