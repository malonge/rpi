# blink
Blink an LED light with a Raspbery Pi.

```bash
docker build -t blink .

# Control the interval length (seconds) with -s
docker run --privileged -it --rm blink python blink.py -s 0.5
```

> Controlling the [GPIO in a container](https://stackoverflow.com/questions/78011212/controlling-gpio-from-a-docker-container-in-raspberry-pi-5) on a Raspberry Pi 5
