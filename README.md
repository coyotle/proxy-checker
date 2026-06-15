# proxy-checker

Lightweight proxy health checker microservice for [Gatus](https://github.com/TwinProduction/gatus), [Uptime Kuma](https://github.com/louislam/uptime-kuma), and similar monitoring systems.

Monitors SOCKS and HTTP proxies via simple HTTP requests — useful both for checking proxy availability and for verifying connectivity to hosts behind a proxy.

## How it works

`proxy-checker` exposes an HTTP endpoint. Your monitoring system polls it with a proxy URL as a query parameter. The service attempts to reach a target URL through that proxy and returns `200` on success or `503` on failure.

## Endpoints

| Endpoint      | Description              |
| ------------- | ------------------------ |
| `GET /`       | Service health check     |
| `GET /health` | Proxy connectivity check |

### `/health` parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `proxy` | ✓ | — | Proxy URL, e.g. `socks5://host:port` or `http://host:port`. Authentication is supported: `http://user:pass@host:port` |
| `check_url` | | `https://ifconfig.me/ip` | URL to fetch through the proxy |
| `timeout` | | `5.0` | Request timeout in seconds |


### Response

**Success (`200`):**

```json
{
  "status": "ok",
  "proxy": "socks5://192.168.0.2:1080",
  "check_url": "https://ifconfig.me/ip",
  "timeout": 5.0,
  "response": "1.2.3.4"
}
```

**Failure (`503`):** plain text error message from the exception.

## Usage

### Docker Compose

```yaml
services:
  proxy-checker:
    image: ghcr.io/coyotle/proxy-checker:latest
    restart: unless-stopped
```

Or build locally:

```yaml
services:
  proxy-checker:
    build: /path-to-sources
    restart: unless-stopped
```

### Gatus

```yaml
endpoints:
  - name: proxy
    group: proxies
    url: "http://proxy-checker:8000/health?proxy=socks5://192.168.0.2:1080"
    interval: 5m
    conditions:
      - "[STATUS] == 200"

  # Custom target URL and timeout
  - name: host-behind-proxy
    group: proxies
    url: "http://proxy-checker:8000/health?proxy=socks5://192.168.0.2:1080&check_url=https://example.com&timeout=10"
    interval: 5m
    conditions:
      - "[STATUS] == 200"
```

### Uptime Kuma

Add an **HTTP(s)** monitor with URL:

```
http://proxy-checker:8000/health?proxy=socks5://192.168.0.2:1080
```

Expected status code: `200`.

## Use cases

- **Proxy availability** — check that a SOCKS5/HTTP proxy is up and accepting connections
- **End-to-end connectivity** — verify that a host behind a proxy is reachable by setting `check_url` to an internal service
- **Exit IP monitoring** — use default `check_url=https://ifconfig.me/ip` to confirm the expected exit IP address

## License

MIT
