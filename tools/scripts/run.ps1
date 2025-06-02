Write-Host '🛑 remove service'
docker compose down -v

Write-Host '🔨 build service'
docker compose build

Write-Host '✅ run service'
docker compose run -d
