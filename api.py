#!/usr/bin/env python3

import argparse
import requests
import json

parser = argparse.ArgumentParser(description="A simple wrapper to perform http on an API")
parser.add_argument('--url', type=str, default="localhost", help="The target api url; do not put the http://")
parser.add_argument('--https', type=bool, default=False, nargs='?', help="Whether to use https method; default: False")

subparsers = parser.add_subparsers(help='types of http methods', dest='method', required=True)

get_parser = subparsers.add_parser("get")
get_parser.add_argument('path', type=str, nargs='?', default='/', help='The path to get; do not put the full url. ex: /items')

post_parser = subparsers.add_parser("post")
post_parser.add_argument('path', type=str, help='The path to post; do not put the full url. ex: /items')
post_parser.add_argument('body', type=str, help='The body to post; should be a json string')

patch_parser = subparsers.add_parser("patch")
patch_parser.add_argument('path', type=str, help='The path to patch; do not put the full url. ex: /items/2')
patch_parser.add_argument('body', type=str, help='The body to patch; should be a json string')

put_parser = subparsers.add_parser("put")
put_parser.add_argument('path', type=str, help='The path to put; do not put the full url. ex: /items/2')
patch_parser.add_argument('body', type=str, help='The body to put; should be a json string')

delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument('path', type=str, help='The path to delete; do not put the full url. ex: /items/2')

if __name__ == '__main__':
    args = parser.parse_args()
    http = "https://" if args.https else "http://"
    if args.method == 'get':
        response = requests.get(f"{http}{args.url}{args.path}")
    elif args.method == 'post':
        response = requests.post(f"{http}{args.url}{args.path}", json=json.loads(args.body))
    elif args.method == 'patch':
        response = requests.patch(f"{http}{args.url}{args.path}", json=json.loads(args.body))
    elif args.method == 'put':
        response = requests.put(f"{http}{args.url}{args.path}", json=json.loads(args.body))
    elif args.method == 'delete':
        response = requests.delete(f"{http}{args.url}{args.path}")
    else:
        print("unsupported http method; supported methods are: get, post, patch, put, delete")
        exit(0)

    print(response.text)
