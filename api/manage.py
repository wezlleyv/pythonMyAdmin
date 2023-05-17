#!/usr/bin/env python
import os, sys
import app


def main():
    if sys.argv[1] == "prod":
        env = "config.production"
    if sys.argv[1] == "dev":
        env = "config.development"

    try:
        os.environ.setdefault("APP_CONFIG_FILE", env)
    except:
        print("This config is not valid!")

    app.run()

if __name__ == '__main__':
    main()