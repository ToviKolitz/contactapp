#!/bin/bash

isTestsPassed=$(cat testResult.txt | grep "12 passed")
if [[ -z "$isTestsPassed" ]]; then
    echo 'failare'
    exit 1
else
    echo '=========== Unit Tests Finished with Success =============='
fi
