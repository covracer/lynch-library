set allow-duplicate-recipes

# Work around curl homebrew issue on macOS
curl_lib := if os() == "macos" {
    if path_exists("/opt/homebrew/Cellar/curl") == "true" {
        `find /opt/homebrew/Cellar/curl -maxdepth 1 -type d -name "*.*.*" | sort -V | tail -1`
    } else {
        ""
    }
} else {
    ""
}

DYLD_LIBRARY_PATH := if curl_lib != "" {
    curl_lib + "/lib:" + env_var_or_default("DYLD_LIBRARY_PATH", "")
} else {
    env_var_or_default("DYLD_LIBRARY_PATH", "")
}

import ".biobuddies/justfile"

# Uv venv and Pip Sync with --clear
ups *args:
    uv venv --clear && (uv pip sync {{args}} requirements.txt & npm clean-install & wait)

# Pre-Commit Run (defaults to modified files)
pcr *args:
    source .venv/bin/activate && pre-commit run {{args}}
