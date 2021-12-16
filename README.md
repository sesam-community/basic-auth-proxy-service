## Client side Basic Auth proxy service

A simple service that serves as a proxy for signing request calls to an API with a client side SSL certificate (PFX).

[![SesamCommunity CI&CD](https://github.com/sesam-community/client-ssl-certificate-proxy-service/actions/workflows/sesam-community-ci-cd.yml/badge.svg)](https://github.com/sesam-community/basic-auth-proxy-service/actions/workflows/sesam-community-ci-cd.yml)

### Environment variables:

`base_url` - the base url of the API service.

`username` - username to the API service.

`password` - password to the API service.

`log_response_data` - set this value to true to log the received data for debugging purposes, default value: false.

`stream_data` - stream response data, default value: false.


### Example system config:

```json
{
  "_id": "client-ssl-certificate-proxy-system",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "base_url": "https://base.url.to.api/",
      "username": "username-to-api",
      "password": "$SECRET(secret-password-to-api)"
    },
    "image": "sesamcommunity/basic-auth-proxy-service:latest",
    "port": 5001
  }
}

```

### Example pipe using the microservice above

```json
{
  "_id": "basic-auth-proxy-pipe",
  "type": "pipe",
  "source": {
    "is_chronological": false,
    "is_since_comparable": false,
    "supports_since": false,
    "system": "basic-auth-proxy-system",
    "type": "json",
    "url": "api-path"
  }
}

```