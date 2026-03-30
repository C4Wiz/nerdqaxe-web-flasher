[![](https://dcbadge.vercel.app/api/server/3E8ca2dkcC)](https://discord.gg/3E8ca2dkcC)

# NerdQaxe++ Web Flasher

The Nerd*axe Web Flasher is the open source tool that provides you an easy solution to flash a factory file to you device.

## Flashing process

Simply connect your device, select the model and board version and click on flash.

## Development / Run locally

You can use Docker for compiling the application and to run it locally by

```bash
# build the image
docker build . -f Dockerfile -t nerdqaxe-web-flasher

# run the container in background without hot reload
docker run --rm -d -p 3000:3000 nerdqaxe-web-flasher

# run the container in foregroud with hot reload on file changes
docker run --rm -it -p 3000:3000 -v $(pwd):/app nerdqaxe-web-flasher
```

and access it by `http://localhost:3000`
