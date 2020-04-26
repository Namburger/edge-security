#!/bin/bash
set -e

function info {
  echo -e "\033[0;32m${1}\033[0m"  # green
}
function warn {
  echo -e "\033[0;33m${1}\033[0m"  # yellow
}
function error {
  echo -e "\033[0;31m${1}\033[0m"  # red
}

warn "Attempting to get the correct CPU Arch and python version:"
readonly ARCH="$(uname -m)"
info "ARCH: ${ARCH}"

PYTHON=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
info "PYTHON VERSION: ${PYTHON}"
if [[ -z "$PYTHON" ]]
then
  error "No Python3, please install..."
fi
PYTHON=$(python3 -c 'import platform; major, minor, _= platform.python_version_tuple(); print(major+minor)')
tflite_runtime=https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp${PYTHON}-cp${PYTHON}m-linux_${ARCH}.whl

info "Installing dependencies..."
pip_pkgs=("Flask==1.0.2 ${tflite_runtime}")
for pkg in $pip_pkgs; do
  info "Installing pip package: $pkg"
  python3 -m pip install $pkg --user
done

apt_pkgs=("python3-opencv=3.2.0+dfsg-6")
for pkg in $apt_pkgs; do
  info "Installing pip package: $pkg"
  sudo apt install $pkg
done
