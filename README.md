# Publishing Gateway

To run install poetry and execute:

    $ poetry run publishing-gw

## Example usage

```sh
curl -i -X PUT -H "Authorization: Token token=34170cc4-0a3d-11e6-823b-6c400891b752" -F 'meta={
    "recording":{
      "language":"deu",
      "mime_type": "text/vtt"
    }
  };type=application/json' -F file=@37C3_\ Feierliche\ Eröffnung.vtt \
  http://localhost:5005/api/37c3/events/fddf9aa7-4952-497e-b706-2e802deef3cc/file
```
