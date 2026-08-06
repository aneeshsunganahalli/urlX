#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Initialize variable for no-cache flag
NO_CACHE=""

# Parse command line flags
for arg in "$@"; do
  case $arg in
  --no-cache)
    NO_CACHE="--no-cache"
    shift
    ;;
  *)
    # Unknown option
    ;;
  esac
done

echo "==> Stopping existing containers..."
docker compose down

echo "==> Building server service ${NO_CACHE:+(with --no-cache)}..."
docker compose build $NO_CACHE server

echo "==> Starting containers in detached mode..."
docker compose up -d

echo "==> Done!"
