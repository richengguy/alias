#!/bin/bash
set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <http_code> <redirect>"
    exit 0
fi

response=$(curl -s -o /dev/null -w "%{http_code}\`%{redirect_url}" localhost:8000/search)

parts=$(tr "\`" $'
' <<< $response)

http_code=$(sed -n '1p' <<< "$parts")
redirect=$(sed -n '2p' <<< "$parts")

if [ "$http_code" != "$1" ]; then
    echo "::error::Returned an ${http_code} code instead of a 301."
fi

if [ "$redirect" != "$2" ]; then
    echo "::error::Returned an '${redirect}' instead of '$2'"
fi
