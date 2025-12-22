#!/bin/bash

URL="https://example.com"
OUTPUT_DIR="catalog"
OUTPUT_NAME="example-site"

function build_singlefile_image {
    if [[ "$(docker images -q singlefile 2> /dev/null)" == "" ]]; then
        echo "Building SingleFile Docker image..."
        docker build -t singlefile -f ./singlefile.Dockerfile .
    else
        echo "SingleFile Docker image already exists. Skipping build."
    fi
}

function build_puppeteer_screenshot_image {
    if [[ "$(docker images -q puppeteer-screenshot 2> /dev/null)" == "" ]]; then
        echo "Building Puppeteer screenshot Docker image..."
        docker build --platform linux/arm64 -t puppeteer-screenshot -f ./puppeteer-screenshot.Dockerfile .
    else
        echo "Puppeteer screenshot Docker image already exists. Skipping build."
    fi
}

function capture_html_with_singlefile {
    echo "Capturing HTML with SingleFile..."
    docker container run singlefile \
        --browser-ignore-insecure-certs \
        $URL $OUTPUT_DIR/$(date +%Y)/$OUTPUT_NAME.html
}

function capture_screenshot_with_puppeteer {
    echo "Capturing screenshot with Puppeteer..."
    docker container run --platform linux/arm64 \
        -v $(pwd)/$OUTPUT_DIR:/usr/src/app/out \
        puppeteer-screenshot \
        $URL /usr/src/app/out/$OUTPUT_NAME.png
}

$1