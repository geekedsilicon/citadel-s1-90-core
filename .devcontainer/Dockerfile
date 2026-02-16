# ==============================================================================
# VAELIX | PROJECT CITADEL — SILICON FORGE ENVIRONMENT
# ==============================================================================
# FILE:      .devcontainer/Dockerfile
# VERSION:   1.2.0 — Citadel Standard
# TARGET:    Tiny Tapeout 06 (IHP 130nm SG13G2) — ttihp26a Shuttle
# BASE:      Ubuntu 24.04 (Noble Numbat)
#
# PURPOSE:
#   Standardized ASIC development container for the S1-90 Sentinel Core.
#   Guarantees identical toolchain state across all development environments.
#   California or Berlin — same silicon, same tools, same result.
#
# TOOLCHAIN MANIFEST:
#   - Icarus Verilog       : RTL simulation engine
#   - GTKWave              : Waveform visualization
#   - Verilator            : Structural linting
#   - Verible v0.0-4023    : Verilog formatting (Vaelix alignment standard)
#   - Cocotb 2.0.1         : Python verification framework
#   - LibreLane 3.0.0.dev44: ASIC hardening flow (MANDATORY — IHP26a pin)
#   - IHP SG13G2 PDK       : 130nm foundry design kit
#
# FIX LOG:
#   v1.2.0 — [CRITICAL] TT_SUPPORT_TOOLS_BRANCH: main -> tt10 (shuttle pin)
#   v1.2.0 — [CRITICAL] chmod reverted: verible* glob -> /usr/local/bin (safe)
#   v1.2.0 — [MODERATE] apt update+install consolidated to single RUN layer
#   v1.2.0 — [MODERATE] ttsetup mkdir+clone consolidated to single RUN layer
#   v1.2.0 — [MODERATE] venv create+install consolidated to single RUN layer
#   v1.2.0 — apt -> apt-get (non-interactive Docker standard)
# ==============================================================================

ARG VARIANT=ubuntu-24.04
FROM mcr.microsoft.com/vscode/devcontainers/base:${VARIANT}

# --- ENVIRONMENT CONFIGURATION -----------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive
ENV PDK_ROOT=/home/vscode/ttsetup/pdk
ENV PDK=ihp-sg13g2

# ⚠️  SHUTTLE PIN: tt10 aligns with librelane==3.0.0.dev44 and the IHP26a shuttle.
#     DO NOT change to 'main' — main is a floating target and will break the build.
ARG TT_SUPPORT_TOOLS_BRANCH=tt10

# --- PHASE I: SYSTEM TOOLCHAIN -----------------------------------------------
# Single RUN layer prevents apt cache skew between update and install.
# --no-install-recommends keeps the image lean.
# Cleanup of apt lists reduces final image size.
RUN apt-get update && apt-get install -y --no-install-recommends \
    iverilog          \
    gtkwave           \
    python3           \
    python3-pip       \
    python3-venv      \
    python3-tk        \
    python-is-python3 \
    libcairo2         \
    verilator         \
    libpng-dev        \
    libqhull-dev      \
    curl              \
 && rm -rf /var/lib/apt/lists/*

# --- PHASE II: TINY TAPEOUT SUPPORT INFRASTRUCTURE ---------------------------
# mkdir and clone in single layer — avoids dangling empty /ttsetup layer.
RUN mkdir -p /ttsetup && \
    git clone -b ${TT_SUPPORT_TOOLS_BRANCH} \
    https://github.com/TinyTapeout/tt-support-tools \
    /ttsetup/tt-support-tools

# Inject Vaelix Python requirements and dev container helper script.
COPY test/requirements.txt              /ttsetup/test_requirements.txt
COPY .devcontainer/copy_tt_support_tools.sh /ttsetup

# --- PHASE III: PYTHON VIRTUAL ENVIRONMENT ("THE CLEAN ROOM") ----------------
# Single atomic layer: venv creation + all pip installs together.
# Installs pinned cocotb==2.0.1, pytest==8.4.2, and tt-support-tools deps.
RUN python -m venv /ttsetup/venv && \
    /ttsetup/venv/bin/pip install \
        -r /ttsetup/test_requirements.txt \
        -r /ttsetup/tt-support-tools/requirements.txt

# --- PHASE IV: STATIC ANALYSIS & FORMATTING ----------------------------------
# Verible v0.0-4023: enforces Vaelix vertical alignment and port formatting.
# chmod targets the full bin directory — glob expansion is unreliable in sh.
RUN umask 022 && \
    curl -L https://github.com/chipsalliance/verible/releases/download/v0.0-4023-gc1271a00/verible-v0.0-4023-gc1271a00-linux-static-x86_64.tar.gz | \
    tar zxf - -C /usr/local --strip-components=1 && \
    chmod 755 /usr/local/bin

# --- PHASE V: ASIC HARDENING ENGINE ------------------------------------------
# ⚠️  MANDATORY VERSION: librelane==3.0.0.dev44 is required for the IHP26a
#     shuttle. DO NOT upgrade without explicit TinyTapeout shuttle coordinator
#     approval — newer versions may break IHP SG13G2 PDK compatibility.
RUN /ttsetup/venv/bin/pip install librelane==3.0.0.dev44
