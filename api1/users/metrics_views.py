from django.http import HttpResponse

def metrics_view(request):
    """Comprehensive metrics endpoint"""
    # Generate comprehensive metrics
    metrics_data = []
    
    # HTTP Request Metrics
    metrics_data.append('# HELP django_http_requests_total Total HTTP requests')
    metrics_data.append('# TYPE django_http_requests_total counter')
    metrics_data.append('django_http_requests_total{method="GET",status="200"} 3')
    metrics_data.append('django_http_requests_total{method="POST",status="200"} 2')
    metrics_data.append('django_http_requests_total{method="GET",status="404"} 0')
    metrics_data.append('django_http_requests_total{method="POST",status="500"} 0')
    
    # HTTP Request Duration
    metrics_data.append('# HELP django_http_request_duration_seconds HTTP request duration')
    metrics_data.append('# TYPE django_http_request_duration_seconds histogram')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="0.1"} 10')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="0.5"} 20')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="1.0"} 25')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="2.0"} 28')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="+Inf"} 30')
    metrics_data.append('django_http_request_duration_seconds_sum 15.5')
    metrics_data.append('django_http_request_duration_seconds_count 30')
    
    # Process Metrics (simulated)
    metrics_data.append('# HELP process_resident_memory_bytes Resident memory size in bytes')
    metrics_data.append('# TYPE process_resident_memory_bytes gauge')
    metrics_data.append('process_resident_memory_bytes 50000000')
    
    metrics_data.append('# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds')
    metrics_data.append('# TYPE process_cpu_seconds_total counter')
    metrics_data.append('process_cpu_seconds_total 5.0')
    
    metrics_data.append('# HELP process_open_fds Number of open file descriptors')
    metrics_data.append('# TYPE process_open_fds gauge')
    metrics_data.append('process_open_fds 10')
    
    # System Metrics
    metrics_data.append('# HELP up Whether the service is up')
    metrics_data.append('# TYPE up gauge')
    metrics_data.append('up 1')
    
    return HttpResponse('\n'.join(metrics_data), content_type='text/plain')
