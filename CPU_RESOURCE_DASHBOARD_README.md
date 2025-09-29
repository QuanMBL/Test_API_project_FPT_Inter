# Comprehensive CPU & Resource Monitoring Dashboard

## 📊 Overview

This dashboard provides a comprehensive view of CPU usage, resource consumption, and performance metrics for all 4 API services in your microservices architecture.

## 🎯 Dashboard Features

### Top-Level Overview
- **CPU Usage Overview**: Real-time CPU usage across all 4 services
- **CPU Usage by Service**: Time-series graph showing CPU trends for each service
- **Memory Usage by Service**: Memory consumption patterns over time

### Detailed Service Metrics
Each service (User API, Product API, Order API, Payment API) has its own detailed metrics table showing:

#### 🔍 Service Health Metrics
- **Status**: Service availability (UP/DOWN)
- **CPU Usage**: Current CPU utilization percentage
- **Memory**: Current memory consumption in bytes
- **Request Rate**: Requests per second
- **Response Time**: Average response time in seconds
- **Error Rate**: Percentage of failed requests
- **Open FDs**: Number of open file descriptors
- **Start Time**: Service start timestamp

#### 📈 Performance Trends
- **Response Time Trends**: Historical response time patterns
- **Request Rate Trends**: Traffic patterns over time
- **Error Rate Trends**: Error rate evolution
- **Service Availability Status**: Overall system health

## 🚀 Quick Start

### Prerequisites
- Grafana running on `http://localhost:3000`
- Prometheus configured and collecting metrics
- All 4 API services running and exposing metrics

### Import Dashboard

#### Option 1: PowerShell (Windows)
```powershell
.\import-cpu-resource-dashboard.ps1
```

#### Option 2: Python Script
```bash
python k8s/monitoring/import-cpu-resource-dashboard.py
```

#### Option 3: Manual Import
1. Open Grafana at `http://localhost:3000`
2. Login with `admin` / `admin123`
3. Go to **Dashboards** → **Import**
4. Upload `monitoring/grafana/dashboards/comprehensive-cpu-resource-dashboard.json`

## 📋 Dashboard Sections

### 1. CPU Usage Overview
- **Panel**: Large stat panel showing total CPU usage across all services
- **Color Coding**: Green (<70%), Yellow (70-85%), Red (>85%)
- **Refresh Rate**: 5 seconds

### 2. CPU Usage by Service
- **Type**: Time-series graph
- **Metrics**: Individual CPU usage for each service
- **Legend**: Shows current values in table format
- **Thresholds**: Visual indicators for CPU limits

### 3. Memory Usage by Service
- **Type**: Time-series graph
- **Metrics**: Memory consumption for each service
- **Unit**: Bytes with automatic scaling
- **Thresholds**: Memory usage warnings

### 4. Detailed Service Metrics Tables
Four separate tables (one for each service) showing:

#### User API Metrics
- Service status and health indicators
- Real-time resource usage
- Performance metrics
- Error tracking

#### Product API Metrics
- Same comprehensive metrics as User API
- Service-specific performance data
- Resource utilization tracking

#### Order API Metrics
- Order processing performance
- Resource consumption patterns
- Error rate monitoring

#### Payment API Metrics
- Payment processing metrics
- Security and performance indicators
- Resource usage tracking

### 5. Performance Trends
- **Response Time Trends**: Shows latency patterns for all services
- **Request Rate Trends**: Traffic volume over time
- **Error Rate Trends**: Error patterns and trends
- **Service Availability**: Overall system health status

## 🎨 Visual Features

### Color Coding
- **Green**: Normal/Healthy status
- **Yellow**: Warning levels
- **Red**: Critical/Error conditions

### Thresholds
- **CPU Usage**: 70% (warning), 85% (critical)
- **Memory**: 100MB (warning), 200MB (critical)
- **Response Time**: 0.5s (warning), 1.0s (critical)
- **Error Rate**: 5% (warning), 10% (critical)

### Auto-refresh
- **Refresh Rate**: 5 seconds
- **Time Range**: Last 1 hour (configurable)
- **Timezone**: Browser timezone

## 🔧 Configuration

### Prometheus Queries Used
```promql
# CPU Usage
rate(process_cpu_seconds_total{job="service-name"}[5m]) * 100

# Memory Usage
process_resident_memory_bytes{job="service-name"}

# Request Rate
rate(django_http_requests_total{job="service-name"}[5m])

# Response Time
avg(django_http_request_duration_seconds_sum{job="service-name"} / django_http_request_duration_seconds_count{job="service-name"})

# Error Rate
sum(rate(django_http_requests_total{job="service-name",status=~"4..|5.."}[5m])) / sum(rate(django_http_requests_total{job="service-name"}[5m])) * 100
```

### Service Names
- `user-api`
- `product-api`
- `order-api`
- `payment-api`

## 📊 Metrics Explained

### CPU Usage
- **What it measures**: CPU time consumed by each service
- **Unit**: Percentage of CPU cores
- **Calculation**: Rate of CPU seconds over 5-minute window

### Memory Usage
- **What it measures**: Resident memory (RAM) used by each service
- **Unit**: Bytes (automatically scaled to MB/GB)
- **Source**: Process resident memory bytes

### Request Rate
- **What it measures**: HTTP requests per second
- **Unit**: Requests per second (reqps)
- **Calculation**: Rate of HTTP requests over 5-minute window

### Response Time
- **What it measures**: Average time to process HTTP requests
- **Unit**: Seconds
- **Calculation**: Sum of durations divided by request count

### Error Rate
- **What it measures**: Percentage of HTTP 4xx and 5xx responses
- **Unit**: Percentage
- **Calculation**: Error requests / Total requests * 100

## 🚨 Alerting Recommendations

### CPU Alerts
- **Warning**: CPU > 70% for 5 minutes
- **Critical**: CPU > 85% for 2 minutes

### Memory Alerts
- **Warning**: Memory > 100MB for 5 minutes
- **Critical**: Memory > 200MB for 2 minutes

### Response Time Alerts
- **Warning**: Response time > 0.5s for 5 minutes
- **Critical**: Response time > 1.0s for 2 minutes

### Error Rate Alerts
- **Warning**: Error rate > 5% for 5 minutes
- **Critical**: Error rate > 10% for 2 minutes

## 🔍 Troubleshooting

### Common Issues

#### No Data Showing
1. Check if Prometheus is running
2. Verify service metrics endpoints are accessible
3. Check Prometheus configuration for service discovery

#### Dashboard Not Loading
1. Verify Grafana is running on port 3000
2. Check authentication credentials
3. Ensure dashboard JSON is valid

#### Missing Metrics
1. Verify services are exposing metrics on `/metrics` endpoint
2. Check Prometheus targets are UP
3. Verify metric names match the queries

### Debug Steps
1. Check Prometheus targets: `http://localhost:9090/targets`
2. Verify metrics: `http://localhost:9090/graph`
3. Check Grafana data sources: `http://localhost:3000/datasources`

## 📈 Performance Optimization

### Dashboard Performance
- **Refresh Rate**: 5 seconds (adjust based on needs)
- **Time Range**: 1 hour (extend for historical analysis)
- **Query Optimization**: Use appropriate time ranges

### Resource Usage
- **CPU**: Monitor dashboard CPU usage
- **Memory**: Check Grafana memory consumption
- **Network**: Monitor data transfer rates

## 🔄 Maintenance

### Regular Tasks
1. **Weekly**: Review dashboard performance
2. **Monthly**: Update thresholds based on usage patterns
3. **Quarterly**: Review and optimize queries

### Updates
- Dashboard version: 1.0
- Compatible with Grafana 8.0+
- Requires Prometheus metrics

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all prerequisites are met
3. Review Prometheus and Grafana logs
4. Test individual metric queries

---

**Dashboard Version**: 1.0  
**Last Updated**: $(Get-Date -Format "yyyy-MM-dd")  
**Compatible With**: Grafana 8.0+, Prometheus 2.0+
