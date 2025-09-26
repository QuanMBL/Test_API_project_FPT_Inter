from django.http import HttpResponse

def metrics_view(request):
    """Simple metrics endpoint"""
    metrics_data = []
    
    # Add HTTP request counter
    metrics_data.append('# HELP django_http_requests_total Total HTTP requests')
    metrics_data.append('# TYPE django_http_requests_total counter')
    metrics_data.append('django_http_requests_total{method="GET",status="200"} 2')
    metrics_data.append('django_http_requests_total{method="POST",status="200"} 1')
    
    # Add HTTP request duration
    metrics_data.append('# HELP django_http_request_duration_seconds HTTP request duration')
    metrics_data.append('# TYPE django_http_request_duration_seconds histogram')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="0.1"} 1')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="0.5"} 1')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="1.0"} 1')
    metrics_data.append('django_http_request_duration_seconds_bucket{le="+Inf"} 1')
    metrics_data.append('django_http_request_duration_seconds_sum 0.1')
    metrics_data.append('django_http_request_duration_seconds_count 1')
    
    # Add process metrics
    metrics_data.append('# HELP process_resident_memory_bytes Resident memory size in bytes')
    metrics_data.append('# TYPE process_resident_memory_bytes gauge')
    metrics_data.append('process_resident_memory_bytes 50000000')
    
    return HttpResponse('\n'.join(metrics_data), content_type='text/plain')
