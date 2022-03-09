## Client side Basic Authentication proxy service

A simple service that serves as a proxy for Basic Authentication.

[![SesamCommunity CI&CD](https://github.com/sesam-community/basic-auth-proxy-service/actions/workflows/sesam-community-ci-cd.yml/badge.svg)](https://github.com/sesam-community/basic-auth-proxy-service/actions/workflows/sesam-community-ci-cd.yml)

### Environment variables:

`base_url` - the base url of the API service.

`username` - username to the API service.

`password` - password to the API service.

`log_response_data` - set this value to true to log the received data for debugging purposes, default value: false.

`stream_data` - stream response data, default value: false.

`ca_cert` - CA certificate chain

`ca_cert_file` - File name in which to store `ca_cert`, default: `/usr/local/share/ca-certificates/ca.crt`

`ca_cert_path` - where to find installed CA certificates inside the container, default: '/etc/ssl/certs'.

### Example proxy system config:

```json
{
  "_id": "basic-auth-proxy-system",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "base_url": "https://base.url.to.api/",
      "username": "username-to-api",
      "password": "$SECRET(secret-password-to-api)"
    },
    "image": "gamh/basic-auth-proxy-service:latest",
    "port": 5002
  }
}

```

### Example system using the proxy system above

```json
{
  "_id": "ifs",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "base_url": "http://basic-auth-proxy-system:5002/",
      "page_parameter": "$skip",
      "page_size_parameter": "$top",
      "use_paging": false
    },
    "image": "sesamcommunity/simple-odata:development",
    "port": 5002
  }
}
```

### Example pipe using the system above

```json
{
  "_id": "ifs-pipe",
  "type": "pipe",
  "source": {
    "system": "ifs",
    "type": "json",
    "url": "api-path"
  }
}

```

