#!/usr/bin/env python
import os, sys
from api import app


def main():
    if sys.argv[1] == "prod":
        env = "api.config.production"
    if sys.argv[1] == "dev":
        env = "api.config.development"

    try:
        os.environ.setdefault("APP_CONFIG_FILE", env)
    except:
        print("This config is not valid!")

    app.run()

if __name__ == '__main__':
    main()