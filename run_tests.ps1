# Automated Test Runner for Member M4 (HW06 EShop API Testing)
# Usage: powershell -ExecutionPolicy Bypass -File .\run_tests.ps1

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  EShop API Automated Test Pipeline — Member M4 (23120228)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Reset & Seed SQLite Database
Write-Host "`n[Step 1/4] Resetting & Seeding Database..." -ForegroundColor Yellow
node .\backend\database.js

# 2. Start Backend Server
Write-Host "`n[Step 2/4] Starting Backend Server (http://localhost:3000)..." -ForegroundColor Yellow
$serverProcess = Start-Process -FilePath "node" -ArgumentList "backend\server.js" -PassThru
Start-Sleep -Seconds 2

# Verify server is listening
try {
    $res = Invoke-WebRequest -Uri "http://localhost:3000/api/categories" -UseBasicParsing -TimeoutSec 3
    Write-Host "Backend Server started successfully (PID: $($serverProcess.Id))." -ForegroundColor Green
} catch {
    Write-Host "Failed to connect to Backend Server." -ForegroundColor Red
    if ($serverProcess) { Stop-Process -Id $serverProcess.Id -Force }
    exit 1
}

# 3. Resolve Paths & Newman
Write-Host "`n[Step 3/4] Running Newman Test Suite with X-Student-Id: 23120228..." -ForegroundColor Yellow

$collectionPath = Join-Path $PSScriptRoot "postman\m4_eshop_collection.json"
$envPath = Join-Path $PSScriptRoot "postman\eshop_environment.json"
$reportPath = Join-Path $PSScriptRoot "report\newman_report.html"
$jsonPath = Join-Path $PSScriptRoot "report\newman_results.json"

try {
    if (Get-Command newman.cmd -ErrorAction SilentlyContinue) {
        & newman.cmd run "$collectionPath" -e "$envPath" -r "cli,htmlextra,json" --reporter-htmlextra-export "$reportPath" --reporter-json-export "$jsonPath" --suppress-exit-code
    } elseif (Get-Command newman -ErrorAction SilentlyContinue) {
        & newman run "$collectionPath" -e "$envPath" -r "cli,htmlextra,json" --reporter-htmlextra-export "$reportPath" --reporter-json-export "$jsonPath" --suppress-exit-code
    } else {
        & npx.cmd newman run "$collectionPath" -e "$envPath" -r "cli,htmlextra,json" --reporter-htmlextra-export "$reportPath" --reporter-json-export "$jsonPath" --suppress-exit-code
    }
} catch {
    Write-Host "Newman execution error: $_" -ForegroundColor Red
} finally {
    # Clean up server process
    Write-Host "Shutting down background server (PID: $($serverProcess.Id))..." -ForegroundColor Gray
    Stop-Process -Id $serverProcess.Id -Force -ErrorAction SilentlyContinue
}

# 4. Generate Detailed Markdown Analysis
Write-Host "`n[Step 4/4] Generating Detailed Failure & Bug Analysis Markdown..." -ForegroundColor Yellow
python .agents\skills\api-test-generator\scripts\parse_results.py

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  Test Execution Complete!" -ForegroundColor Green
Write-Host "  1. HTML Report:              .\report\newman_report.html" -ForegroundColor Green
Write-Host "  2. Detailed Markdown Report: .\report\test_execution_detailed.md" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
