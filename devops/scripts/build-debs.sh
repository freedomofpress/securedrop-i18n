#!/bin/bash
# shellcheck disable=SC2209
#
# Wrapper around debian build logic to bootstrap virtualenv

set -e
set -o pipefail

. ./devops/scripts/boot-strap-venv.sh

virtualenv_bootstrap

RUN_TESTS="${1:-test}"
TARGET_PLATFORM="${2:-focal}"
SCENARIO_NAME="builder-${TARGET_PLATFORM}"

case "$RUN_TESTS" in
    notest)
        molecule_action=converge
        ;;
    test)
        molecule_action=test
        ;;
esac

case "$SD_DEBUG_BUILD_DEBS" in
    [yY][eE][sS])
        DEBUG="--debug"
        ;;
    *)
        DEBUG=""
        ;;
esac

molecule ${DEBUG} "${molecule_action}" -s "${SCENARIO_NAME}"
