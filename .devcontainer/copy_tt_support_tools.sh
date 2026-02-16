#!/bin/sh
# ==============================================================================
# VAELIX | PROJECT CITADEL — TOOLCHAIN SYNCHRONIZATION SCRIPT
# ==============================================================================
# FILE:      .devcontainer/copy_tt_support_tools.sh
# VERSION:   1.1.0 — Citadel Standard
# TARGET:    DevContainer Initialization (postStartCommand)
# PURPOSE:   Injects the Tiny Tapeout support tools into the workspace.
#
# LOGIC:
#   Checks for the 'tt' symlink specifically (not just any directory).
#   The TinyTapeout container architecture uses a symlink for 'tt/' in
#   some configurations — a directory check (-d) would incorrectly
#   overwrite a valid symlink. The symlink check (-L) is mandatory.
#
# FIX LOG:
#   v1.1.0 — [CRITICAL] Reverted -d (directory) back to -L (symlink check)
#   v1.1.0 — [MODERATE] git pull failure now warns without blocking startup
#   v1.1.0 — Normalized shebang spacing: '#! /bin/sh' -> '#!/bin/sh'
#   v1.1.0 — Added echo output for workspace initialization visibility
# ==============================================================================

# Check for symlink specifically — do NOT change -L to -d.
# See header comment for explanation of why this distinction is critical.
if [ ! -L tt ]; then
    echo "VAELIX: 'tt' symlink not detected. Initializing support tools..."

    # Copy the pre-cloned tools from the container setup directory.
    cp -R /ttsetup/tt-support-tools tt

    # Synchronize with the latest shuttle-aligned repository state.
    # Non-fatal: warn on network failure but do not block workspace startup.
    cd tt && git pull || echo "VAELIX: WARNING — git pull failed. Tools may be stale. Check network." && cd ..

    echo "VAELIX: Toolchain synchronization complete."
else
    echo "VAELIX: Toolchain symlink detected. Skipping initialization."
fi
