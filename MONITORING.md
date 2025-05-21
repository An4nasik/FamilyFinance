# Family Finance Monitoring Setup

This project includes a complete logging and monitoring setup using:
- **Loki**: For log aggregation
- **Promtail**: For log collection from Docker containers
- **Prometheus**: For metrics collection
- **Grafana**: For visualization

## Features

- **Structured JSON Logging**: All application logs are output in JSON format
- **Request Logging**: All HTTP requests are logged with detailed information
- **Request ID Tracking**: Each request is assigned a unique ID for tracing
- **Error Handling**: Exceptions are logged with full details
- **Metrics Collection**: Application metrics are collected by Prometheus
- **Dashboard Visualization**: Logs and metrics can be visualized in Grafana

## Getting Started

1. Start the application with monitoring:
   ```
   ./start_monitoring.ps1
   ```

2. Access Grafana at http://localhost:3000 (admin/admin)

3. Create dashboards to visualize:
   - API latency and request rates
   - Error rates and types
   - Database operations
   - System metrics

## Log Queries

Example Loki queries to use in Grafana:

1. All logs from the FastAPI app:
   ```
   {container_name="fastapi_app"}
   ```

2. All error logs:
   ```
   {container_name="fastapi_app"} |= "level=\"ERROR\""
   ```

3. Logs for a specific request ID:
   ```
   {container_name="fastapi_app"} | json | request_id="your-request-id"
   ```

4. Slow requests (above 500ms):
   ```
   {container_name="fastapi_app"} | json | duration_ms > 500
   ```

## Recommended Dashboards

1. **API Overview**: Request rates, latencies, status codes
2. **Error Tracking**: Error counts, types, and details
3. **User Activity**: User login/logout, operations per user
4. **Database Performance**: Query times, connection counts
5. **System Health**: CPU, memory, disk usage

For more details on configuring Grafana and setting up alerts, refer to the Grafana documentation.
