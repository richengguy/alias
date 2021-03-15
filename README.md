# alias - Simplified Link Shortner

'alias' is a simple, Flask-based link shortening system.  Unlike a more generic
link shortener, like [bitly](https://bitly.com/), 'alias' is a direct mapping
between an alias and it's full link.  E.g., `https://links.example.com/search`
redirects to `https://www.google.com`.

## Running

### Locally for Development

'alias' uses [conda](https://docs.conda.io/en/latest/) for environment
management.  First, install the necessary dependencies:

```shell
$ conda env create
$ conda activate alias
$ pip install -e .
```

Create a `.flaskenv` file with the following contents:

```
FLASK_APP=alias:create_app
FLASK_ENV=development
```

Run the development server with

```shell
$ flask run
```
