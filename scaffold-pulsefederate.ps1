# =====================================================================
# scaffold-pulsefederate.ps1
# Creates the complete PulseFederate monorepo in one shot.
# Run from the parent directory where you want the project folder.
# =====================================================================

$ErrorActionPreference = "Stop"
$root = "federated-population-health"

# ---------- Helper: write a file, creating parent dirs as needed ----------
function Write-File {
    param([string]$Path, [string]$Content)
    $full = Join-Path $root $Path
    $dir  = Split-Path $full -Parent
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    [System.IO.File]::WriteAllText($full, $Content, [System.Text.UTF8Encoding]::new($false))
    Write-Host "  + $Path" -ForegroundColor DarkGray
}

# ---------- 1. Create every directory up front ----------
$dirs = @(
    "backend/app/api", "backend/app/domain", "backend/app/ml", "backend/app/services",
    "backend/tests",
    "frontend/src/app/admin", "frontend/src/app/hospital",
    "frontend/src/components", "frontend/src/lib",
    "clients",
    "data/synthetic", "data/partitions",
    "docker", "k8s", "monitoring", "docs", "tests", "scripts"
)
foreach ($d in $dirs) {
    New-Item -ItemType Directory -Force -Path (Join-Path $root $d) | Out-Null
}

Write-Host "`n=== ROOT ===" -ForegroundColor Cyan

# ---------- 2. Root files ----------
Write-File "README.md" @'
# Federated Population Health Platform
...
MIT
'@


## Quick Start

python scripts/generate_synthetic_data.py
docker compose -f docker/docker-compose.yml up --build