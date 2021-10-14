# FAF-191_Dining_Hall

## Build

```bash
docker image build -t dining-hall .
```

## Run

Before running dining-hall make sure to start kitchen first.

```bash
docker run -p 80:5000 --name dining-hall --link kitchen -d dining-hall
```

## Logs

```bash
docker logs -f dining-hall
```
