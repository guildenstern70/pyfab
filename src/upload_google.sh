#!/usr/bin/env bash
gcloud config set project fableomatic
gcloud app deploy app.yaml index.yaml --quiet

