# alias - Simplified Link Shortner

'alias' is a simple, Flask-based link shortening system.  Unlike a more generic
link shortener, like [bitly](https://bitly.com/), 'alias' is a direct mapping
between an alias and it's full link.  E.g., `https://links.example.com/search`
redirects to `https://www.google.com`.

## Running

### Locally

'alias' uses [conda](https://docs.conda.io/en/latest/) for environment
management.  First, install the necessary dependencies:

```shell
$ conda env create
$ conda activate alias
$ pip install -e .
```

Next, create a `.flaskenv` file with the following contents:

```
FLASK_APP=alias:create_app
FLASK_ENV=development
```

'alias' can be managed via the command line.  Once installed,

```shell
$ alias-app init
$ alias-app add search https://www.google.com
```

will initialize the application database and a 'search' shortcut to
https://www.google.com.

Run the development server with

```shell
$ flask run
```

Finally, all of the tests can be run with

```shell
$ tox
```

### Docker

There are two ways to run the Docker build.  First is manually using the
Dockerfile in the `deployment/` folder.  Build the image and run it via

```shell
$ docker build -t alias-app -f deployment/Dockerfile.alias .
$ docker run -p "8000:8000" alias-app
```

This will create a new container and bind the internal port 8000 to the external
port 8000.

The other way is via `docker-compose`. This includes a
[Caddy 2](https://caddyserver.com/) reverse proxy that runs in front of the
"alias" container.  Building it and starting it is

```shell
$ docker-compose build
$ docker-compose up
```

Everything can be cleaned up with

```shell
$ docker-compose down --rmi all -v
```
