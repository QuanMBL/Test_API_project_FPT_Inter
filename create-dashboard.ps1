# Script to create a simple dashboard in Grafana
Write-Host "Creating API Monitoring Dashboard..." -ForegroundColor Green

# Dashboard JSON for API monitoring
$dashboardJson = @"
{
  "dashboard": {
    "id": null,
    "title": "API Services Monitoring",
    "tags": ["api", "monitoring"],
    "style": "dark",
    "timezone": "browser",
    "refresh": "5s",
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "panels": [
      {
        "id": 1,
        "title": "Total HTTP Requests",
        "type": "stat",
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 0,
          "y": 0
        },
        "targets": [
          {
            "expr": "sum(django_http_requests_total)",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {
              "mode": "thresholds"
            },
            "thresholds": {
              "steps": [
                {
                  "color": "green",
                  "value": null
                }
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Requests by Service",
        "type": "table",
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 12,
          "y": 0
        },
        "targets": [
          {
            "expr": "django_http_requests_total",
            "refId": "A",
            "format": "table"
          }
        ]
      }
    ]
  }
}
"@

# Save dashboard to file
$dashboardJson | Out-File -FilePath "monitoring/grafana/dashboards/api-dashboard.json" -Encoding UTF8

Write-Host "Dashboard JSON created!" -ForegroundColor Green
Write-Host "Now restart Grafana to load the dashboard..." -ForegroundColor Yellow

# Restart Grafana
docker-compose restart grafana

Write-Host "Grafana restarted! Check http://localhost:3000" -ForegroundColor Cyan
Write-Host "Login: admin / admin123" -ForegroundColor Cyan
