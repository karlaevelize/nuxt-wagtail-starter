#!/usr/bin/env sh
set -e # Exit on error

# Install root CA certificate to allow HTTPS connections between services
# using self-signed *.test certificates.
echo "Trusting custom CA certificate..."
sudo cp /run/secrets/ca_cert /usr/local/share/ca-certificates/custom-ca.crt
sudo update-ca-certificates

# Make sure packages are pinned using the tilde (~) prefix
# This should prevent package.json becoming wildly out of date with package-lock.json.
npm config set save-prefix=~

# Install dependencies if one of the following is true:
# - node_modules does not exist
# - sha1sum -c ./var/package-lock.json.sha1 has a non-zero exit code because either:
#   - ./var/package-lock.json.sha1 does not exist
#   - package-lock.json has changed
if [ ! -d "node_modules" ] || ! sha1sum -c ./var/package-lock.json.sha1; then
  echo "Installing dependencies..."
  npm i
  sha1sum package-lock.json > ./var/package-lock.json.sha1
fi

# NOTE: To debug issues with the container, without starting the server,
#       run the container with the argument "debug-container".
if [ "${1}" = "debug-container" ]; then
  echo "Sleeping forever..."
  sleep infinity
fi

echo "Starting server..."
npm run dev
