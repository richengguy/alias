'''Import this module to automatically load environment variables from a .flaskenv file.'''

import pathlib

try:
    import dotenv
    dotenv.load_dotenv(dotenv_path=pathlib.Path('.') / '.flaskenv')
except ImportError:
    # so nothing
    pass
