# Script to start the FastAPI application with Grafana monitoring

Write-Host "Starting Family Finance application with Grafana monitoring..." -ForegroundColor Green

# Start Docker Compose
docker-compose up -d

# Check if services are running
Write-Host "`nChecking if services are up..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Display URLs
Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "Services are now accessible at:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "FastAPI Application: http://localhost:8080" -ForegroundColor Green
Write-Host "FastAPI Documentation: http://localhost:8080/docs" -ForegroundColor Green
Write-Host "Grafana Dashboard: http://localhost:3000" -ForegroundColor Green
Write-Host "  - Username: admin" -ForegroundColor Gray
Write-Host "  - Password: admin" -ForegroundColor Gray
Write-Host "Prometheus: http://localhost:9090" -ForegroundColor Green
Write-Host "Loki: http://localhost:3100" -ForegroundColor Green
Write-Host "`nTo stop the services, run: docker-compose down" -ForegroundColor Yellow
Write-Host "`nLogging Setup Complete!" -ForegroundColor Cyan
