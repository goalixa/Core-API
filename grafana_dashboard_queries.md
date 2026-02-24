# Grafana Dashboard Queries for Goalixa App

This document contains useful PromQL queries for monitoring the Goalixa application.

## HTTP Request Metrics

### Request Rate
```promql
rate(goalixa_http_requests_total[5m])
```

### Request Rate by Status Code
```promql
rate(goalixa_http_requests_total[5m]) * on (status_code) group_left()
```

### Error Rate (4xx and 5xx)
```promql
sum(rate(goalixa_http_requests_total{status_code=~"4..|5.."}[5m])) / sum(rate(goalixa_http_requests_total[5m]))
```

### P95 Request Latency
```promql
histogram_quantile(0.95, sum(rate(goalixa_http_request_duration_seconds_bucket[5m])) by (le, route))
```

### Average Request Latency by Route
```promql
avg(rate(goalixa_http_request_duration_seconds_sum[5m]) / rate(goalixa_http_request_duration_seconds_count[5m])) by (route)
```

### Request Rate by Route
```promql
sum(rate(goalixa_http_requests_total[5m])) by (route)
```

## Database Metrics

### Database Query Rate
```promql
sum(rate(goalixa_db_queries_total[5m])) by (operation, table)
```

### Database Query Duration (P95)
```promql
histogram_quantile(0.95, sum(rate(goalixa_db_query_duration_seconds_bucket[5m])) by (le, operation, table))
```

### Slow Queries (>100ms)
```promql
rate(goalixa_db_query_duration_seconds_bucket{le="0.1"}[5m])
```

### Database Error Rate
```promql
sum(rate(goalixa_db_queries_total{status="error"}[5m])) / sum(rate(goalixa_db_queries_total[5m]))
```

## Authentication Metrics

### Authentication Validation Rate
```promql
sum(rate(goalixa_auth_validation_total[5m])) by (validation_type, status)
```

### Authentication Failure Rate
```promql
sum(rate(goalixa_auth_validation_total{status="failed"}[5m])) / sum(rate(goalixa_auth_validation_total[5m]))
```

### Active Sessions
```promql
goalixa_auth_active_sessions
```

## Business Logic Metrics

### Task Operations Rate
```promql
sum(rate(goalixa_task_operations_total[5m])) by (operation, status)
```

### Goal Operations Rate
```promql
sum(rate(goalixa_goal_operations_total[5m])) by (operation, status)
```

### Habit Operations Rate
```promql
sum(rate(goalixa_habit_operations_total[5m])) by (operation, status)
```

### Timer Operations Rate
```promql
sum(rate(goalixa_timer_operations_total[5m])) by (operation, status)
```

### Task Success Rate
```promql
sum(rate(goalixa_task_operations_total{status="success"}[5m])) / sum(rate(goalixa_task_operations_total[5m]))
```

## Cache Metrics

### Cache Hit Rate
```promql
sum(rate(goalixa_cache_operations_total{status="hit"}[5m])) / sum(rate(goalixa_cache_operations_total{operation="get"}[5m]))
```

### Cache Operations Rate
```promql
sum(rate(goalixa_cache_operations_total[5m])) by (operation, status)
```

### Cache Duration (P95)
```promql
histogram_quantile(0.95, sum(rate(goalixa_cache_operation_duration_seconds_bucket[5m])) by (le, operation))
```

## External Service Metrics

### External Service Request Rate
```promql
sum(rate(goalixa_external_service_requests_total[5m])) by (service, operation, status)
```

### External Service Duration (P95)
```promql
histogram_quantile(0.95, sum(rate(goalixa_external_service_duration_seconds_bucket[5m])) by (le, service))
```

### External Service Error Rate
```promql
sum(rate(goalixa_external_service_requests_total{status="error"}[5m])) / sum(rate(goalixa_external_service_requests_total[5m]))
```

## Error Metrics

### Application Error Rate
```promql
sum(rate(goalixa_errors_total[5m])) by (error_type, component)
```

### Exception Rate
```promql
sum(rate(goalixa_http_request_exceptions_total[5m])) by (exception_type)
```

## System Metrics

### Active Requests
```promql
goalixa_http_active_requests
```

### Request vs Response Size
```promql
# Average request size
avg(rate(goalixa_http_request_size_bytes_sum[5m]) / rate(goalixa_http_request_size_bytes_count[5m]))

# Average response size
avg(rate(goalixa_http_response_size_bytes_sum[5m]) / rate(goalixa_http_response_size_bytes_count[5m]))
```

## Alerts Examples

### High Error Rate Alert
```promql
sum(rate(goalixa_http_requests_total{status_code=~"5.."}[5m])) / sum(rate(goalixa_http_requests_total[5m])) > 0.05
```

### Slow Response Time Alert
```promql
histogram_quantile(0.95, sum(rate(goalixa_http_request_duration_seconds_bucket[5m])) by (le)) > 1.0
```

### High Database Error Rate Alert
```promql
sum(rate(goalixa_db_queries_total{status="error"}[5m])) / sum(rate(goalixa_db_queries_total[5m])) > 0.01
```

### Low Cache Hit Rate Alert
```promql
sum(rate(goalixa_cache_operations_total{status="hit"}[5m])) / sum(rate(goalixa_cache_operations_total{operation="get"}[5m])) < 0.8
```

### High Active Requests Alert
```promql
goalixa_http_active_requests > 100
```

## Dashboard Panels Suggestions

1. **Overview Panel**
   - Total Requests (rate)
   - Error Rate (%)
   - P95 Latency (s)
   - Active Requests

2. **Database Panel**
   - Query Rate by Operation
   - Query Duration (P95)
   - Error Rate (%)
   - Connection Pool Usage

3. **Business Logic Panel**
   - Task Operations Rate
   - Goal Operations Rate
   - Habit Operations Rate
   - Success Rate (%)

4. **Cache Panel**
   - Hit Rate (%)
   - Operations Rate
   - Cache Duration

5. **External Services Panel**
   - Request Rate by Service
   - Duration by Service (P95)
   - Error Rate by Service
