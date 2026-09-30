$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$bin = 'C:\Program Files\PostgreSQL\17\bin'
if (-not (Test-Path "$bin\psql.exe")) { throw 'PostgreSQL 17 is not installed.' }
if (Test-Path "$root\backend\.env") { throw 'Existing .env preserved. Configure database manually.' }
$appPassword = [Guid]::NewGuid().ToString('N')
$adminPassword = [Guid]::NewGuid().ToString('N')
$jwtSecret = [Guid]::NewGuid().ToString('N') + [Guid]::NewGuid().ToString('N')
$webhookSecret = [Guid]::NewGuid().ToString('N') + [Guid]::NewGuid().ToString('N')
$seedPassword = [Guid]::NewGuid().ToString('N').Substring(0, 16)
$env:PGPASSWORD = 'LocalBootstrap_17'
& "$bin\psql.exe" -h 127.0.0.1 -U postgres -v ON_ERROR_STOP=1 -c "CREATE ROLE steel_app LOGIN PASSWORD '$appPassword' NOSUPERUSER NOCREATEDB NOCREATEROLE;"
if ($LASTEXITCODE -ne 0) { throw 'Role creation failed.' }
& "$bin\psql.exe" -h 127.0.0.1 -U postgres -v ON_ERROR_STOP=1 -c 'CREATE DATABASE steel_business OWNER steel_app;'
if ($LASTEXITCODE -ne 0) { throw 'Database creation failed.' }
& "$bin\psql.exe" -h 127.0.0.1 -U postgres -v ON_ERROR_STOP=1 -c "ALTER ROLE postgres PASSWORD '$adminPassword';"
if ($LASTEXITCODE -ne 0) { throw 'Bootstrap credential rotation failed.' }
@"
DATABASE_URL=postgresql+psycopg://steel_app:$appPassword@127.0.0.1:5432/steel_business
JWT_SECRET=$jwtSecret
WEBHOOK_SECRET=$webhookSecret
SEED_PASSWORD=$seedPassword
FRONTEND_ORIGIN=http://127.0.0.1:5173
"@ | Set-Content -LiteralPath "$root\backend\.env" -Encoding utf8
New-Item -ItemType Directory -Path "$root\runtime" -Force | Out-Null
"POSTGRES_ADMIN_PASSWORD=$adminPassword" | Set-Content -LiteralPath "$root\runtime\database-admin.env"
Remove-Item Env:\PGPASSWORD
Write-Output 'Database created; credentials stored in ignored backend/.env and runtime/database-admin.env.'
