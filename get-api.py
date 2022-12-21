#!/usr/bin/env python3

import argparse
import requests

parser = argparse.ArgumentParser(description="A simple wrapper to preform GET on the FastAPI app")

parser.add_argument('path', type=str, nargs='?', default='/', help='The path to get; do not put the full url. ex: /items')

if __name__ == '__main__':
    args = parser.parse_args()

    response = requests.get(f"http://localhost:8{args.path}")

    print(response.text)
