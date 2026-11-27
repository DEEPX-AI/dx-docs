---
title: DxMsgBroker
description: Reference for the dxmsgbroker sink element, which publishes message payloads to MQTT or Kafka.
---

# DxMsgBroker

`dxmsgbroker` is a sink that publishes the payloads from [DxMsgConv](dxmsgconv.md) to an MQTT or Kafka broker. Place it right after `dxmsgconv`.

## Example

```text
... ! dxmsgconv config-file-path=dx_stream/configs/msgconv_config.json ! queue ! \
  dxmsgbroker broker-name=kafka conn-info=localhost:9092 topic=test
```

A full command is on [DxMsgConv](dxmsgconv.md#example).

## Behavior

* `broker-name`, `conn-info` and `topic` are checked when the element starts. If `broker-name` is not `mqtt` or `kafka`, or `conn-info` or `topic` is empty, the element posts an error and does not start. Set all three.
* When the broker is not connected or a publish fails, the message is dropped with a warning. After 10 failures in a row the element posts an error and the pipeline stops. A successful publish resets the count.
* One interface serves both brokers, so you switch between MQTT and Kafka by changing `broker-name` and `conn-info` only.
* Accepts single stream and multi stream caps; it only reads payload metadata.
* Needs `libmosquitto` (MQTT) and `librdkafka` (Kafka); `install.sh` installs both.

## Broker configuration file

`config` points to an optional file for authentication and TLS. MQTT (`dx_stream/configs/broker_mqtt.cfg`):

```ini
username = user
password = 1234
# client-id = dx_stream_client
tls_enable = 1
tls_insecure = 1
tls_cafile = /etc/mosquitto/ca_certificates/ca.crt
tls_capath = /etc/mosquitto/ca_certificates
tls_certfile = /etc/mosquitto/certs/client.crt
tls_keyfile = /etc/mosquitto/certs/client.key
```

Kafka (`dx_stream/configs/broker_kafka.cfg`) takes librdkafka settings in a `[kafka]` section:

```ini
[kafka]
message.max.bytes=10485760
#security.protocol=ssl
#ssl.ca.location=<path to CA certificate file>
#ssl.certificate.location=<path to client certificate file>
#ssl.key.location=<path to client key file>
#ssl.key.password=KEY_PASSWORD
```

See [Secure brokers](../pipelines.md#secure-brokers-with-tls) for a full TLS setup.

## Pads

| Pad | Caps |
|---|---|
| sink | `video/x-raw`; `application/x-dxvideoraw` |

## Properties

| Name | Type | Default | Description |
|---|---|---|---|
| `broker-name` | string | `"mqtt"` | `mqtt` or `kafka`. Set it explicitly. |
| `conn-info` | string | none | Broker address as `host:port`. Required. |
| `topic` | string | none | Topic to publish to. Required. |
| `config` | string | none | Optional broker configuration file. |

## Next steps

* [Message broker pipelines](../pipelines.md#message-broker)
* [Broker troubleshooting](../debugging.md#message-broker-problems)
