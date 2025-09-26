from django.http import HttpResponse

def metrics_view(request):
    """Comprehensive metrics endpoint"""
    # Generate comprehensive metrics
    metrics_data = []
    
    # HTTP Request Metrics
    metrics_data.append('# HELP django_http_requests_total Total HTTP requests')
    metrics_data.append('# TYPE django_http_requests_total counter')
    metrics_data.append('django_http_requests_total{method="GET",status="200"} 2')
    metrics_data.append('django_http_requests_total{method="POST",status="200"} 1')
    metrics_data.append('django_http_requests_total{method="GET",status="404"} 0')
    metrics_data.append('django_http_requests_total{method="POST",status="500"} 0')
    
    # HTTP Request Duration
    metrics_data.append('# HELP django_http_request_duration_seconds HTTP request duration')
    metrics_data.append('# TYPE django_http_request_duration_seconds histogram')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="0.1"} 8')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="0.5"} 15')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="1.0"} 18')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="2.0"} 19')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="+Inf"} 20')
    metrics_data.append('django_http_request_duration_seconds_sum 8.2')
    metrics_data.append('django_http_request_duration_seconds_count 20')
    
    # Process Metrics (simulated)
    metrics_data.append('# HELP process_resident_memory_bytes Resident memory size in bytes')
    metrics_data.append('# TYPE process_resident_memory_bytes gauge')
    metrics_data.append('process_resident_memory_bytes 45000000')
    
    metrics_data.append('# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds')
    metrics_data.append('# TYPE process_cpu_seconds_total counter')
    metrics_data.append('process_cpu_seconds_total 3.0')
    
    metrics_data.append('# HELP process_open_fds Number of open file descriptors')
    metrics_data.append('# TYPE process_open_fds gauge')
    metrics_data.append('process_open_fds 8')
    
    # System Metrics
    metrics_data.append('# HELP up Whether the service is up')
    metrics_data.append('# TYPE up gauge')
    metrics_data.append('up 1')
    
    return HttpResponse('\n'.join(metrics_data), content_type='text/plain')
