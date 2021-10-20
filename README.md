# FAF-191_Dining_Hall

## Build dining-hall ontainer

```bash
docker image build -t dining-hall .
```

## Run dining-hall container

Before running dining-hall make sure to start kitchen first.

```bash
docker run -p 80:5000 --name dining-hall --rm --net restaurant -d dining-hall
```

## Logs

```bash
docker logs -f dining-hall
```
