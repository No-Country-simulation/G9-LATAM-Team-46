# Crea venv .venv-eda y lo registra como kernel Jupyter "TechMind EDA"
# Uso (PowerShell):
#   cd C:\Team46\G9-LATAM-Team-46
#   powershell -ExecutionPolicy Bypass -File dataset\setup_kernel.ps1

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path (Join-Path $RepoRoot "dataset"))) {
    $RepoRoot = $PSScriptRoot
    if (-not (Test-Path (Join-Path $RepoRoot "dataset"))) {
        $RepoRoot = Get-Location
    }
}

Set-Location $RepoRoot
Write-Host "[ROOT] $RepoRoot"

$VenvPath = Join-Path $RepoRoot ".venv-eda"
$Py = $null
foreach ($cand in @("py -3.12", "py -3.11", "py -3.10", "python")) {
    try {
        if ($cand -like "py *") {
            $ver = Invoke-Expression "$cand -c `"import sys; print(sys.version)`"" 2>$null
        } else {
            $ver = & python -c "import sys; print(sys.version)" 2>$null
        }
        if ($LASTEXITCODE -eq 0 -or $ver) {
            $Py = $cand
            Write-Host "[PYTHON] Usando: $cand  ($ver)"
            break
        }
    } catch { }
}

if (-not $Py) {
    Write-Host "[ERROR] No se encontro Python. Instala Python 3.10+ desde python.org y marca 'Add to PATH'."
    exit 1
}

if (-not (Test-Path $VenvPath)) {
    Write-Host "[VENV] Creando $VenvPath ..."
    if ($Py -like "py *") {
        Invoke-Expression "$Py -m venv `"$VenvPath`""
    } else {
        & python -m venv $VenvPath
    }
} else {
    Write-Host "[VENV] Ya existe: $VenvPath"
}

$Pip = Join-Path $VenvPath "Scripts\pip.exe"
$PythonVenv = Join-Path $VenvPath "Scripts\python.exe"
if (-not (Test-Path $PythonVenv)) {
    Write-Host "[ERROR] No se creo el venv. Revisa permisos o antivirus."
    exit 1
}

Write-Host "[PIP] Actualizando pip..."
& $PythonVenv -m pip install --upgrade pip

$Req = Join-Path $RepoRoot "dataset\requirements-eda.txt"
Write-Host "[PIP] Instalando dependencias desde $Req ..."
& $Pip install -r $Req

Write-Host "[KERNEL] Registrando kernel 'TechMind EDA'..."
& $PythonVenv -m ipykernel install --user --name techmind-eda --display-name "Python (TechMind EDA)"

Write-Host ""
Write-Host "========================================"
Write-Host " LISTO"
Write-Host "========================================"
Write-Host "1. Abre Fase1EDA.ipynb"
Write-Host "2. Arriba a la derecha: 'Select Kernel' / 'Seleccionar kernel'"
Write-Host "3. Elige:  Python (TechMind EDA)"
Write-Host "   o el interprete:  $PythonVenv"
Write-Host "4. Si no aparece: Ctrl+Shift+P -> 'Notebook: Select Notebook Kernel' -> 'Refresh'"
Write-Host "========================================"
