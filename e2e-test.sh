#!/bin/bash


status=$(curl -s -o /dev/null -I -w "%{http_code}" http://localhost:5000)

if [[ "$status" == 200 ]]; then
    echo '=========== E2E Test Finish with Success =============='
else
    echo 'failare'
    exit 1
fi
