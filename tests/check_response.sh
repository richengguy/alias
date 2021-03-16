#!/bin/bash
set -e

if [ $# -lt 3 ]; then
    echo "Usage: $0 <shortcut> <http_code> <redirect>"
    exit 0
fi

response=$(curl -s -o /dev/null -w "%{http_code}\`%{redirect_url}" localhost:8000/$1)

parts=$(tr "\`" $'
' <<< $response)

http_code=$(sed -n '1p' <<< "$parts")
redirect=$(sed -n '2p' <<< "$parts")

if [ "$http_code" != "$2" ]; then
    echo "::error::Returned an ${http_code} code instead of a $2."
    touch error_occurred
fi

if [ "$redirect" != "$3" ]; then
    echo "::error::Returned an '${redirect}' instead of '$3'"
    touch error_occurred
fi
