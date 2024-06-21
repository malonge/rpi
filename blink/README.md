# blink
Blink an LED light with a Raspbery Pi.

```bash
docker build -t blink .

# Control the interval length (seconds) with -s
docker run --privileged -it --rm blink python blink.py -s 0.5
```

