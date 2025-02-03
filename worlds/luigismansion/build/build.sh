#!/bin/bash

##
# This script takes care of bundling the apworld.
#
# Arguments:
# * $1: Can be "clean" to clean the build environment.
#
# Environment:
# * TAG:
#     A string used to tag the bundle name
#     eg: "v1.1.1" will name the bundle "luigis-mansion_apworld-v1.1.1"
#     (defaut: current date and time)
##

set -eo pipefail
shopt -s globstar

CWD="$(dirname $(realpath $0))"
REQS=("zip" "rsync" "pip")
SUPPORTED_PLATFORMS=("win_amd64" "manylinux2014_x86_64")

##
# Make sure all the required utilities are installed.
##
function pre_flight() {
    local bad="0"
    for r in ${reqs[@]}; do
        if ! command -v $r > /dev/null; then
            echo "!=> Unable to locate the '${r}' utility in \$PATH. Make sure it is installed."
            bad="1"
        fi
    done

    [ "${bad}" = "1" ] && exit 1 ||:
}

##
# Generate the `lib` folder within the target directory.
# Uses the `requirements.txt` file of the project to get every dependencies and copy them over.
# Uses `requirements.ignore` to specify which files not to copy over from within each of the requirements.
##
function get_deps() {
    local platform="$1" requirements_file="$2" to="$3" install_path="$4"
    echo "=> Bundle requirements for ${platform}"

    local install_platform_dir="${install_path}/${platform}"
    local main_platform_dir="${to}/${platform}"
    mkdir --parents ${install_platform_dir}
    mkdir --parents ${main_platform_dir}

    # Fetch the libraries binary files for the specified platform.
    echo "  -> Fetch requirements"
    pip install \
        --target ${install_platform_dir} \
        --platform ${platform} \
        --only-binary=:all: \
        --requirement ${requirements_file}

    # This is for the `.dist-info` folder, which contains the metadata of the mod.
    # We just copy over the license file into the main library folder
    declare -A dependency_exceptions
    dependency_exceptions["pillow"]="PIL"

    echo "  -> Processing metadata"
    for folder in ${install_platform_dir}/*.dist-info; do
        local dir="$(basename ${folder} | cut -d '-' -f 1)"
        if [[ -v dependency_exceptions[${dir}] ]]; then
           dir=${dependency_exceptions[${dir}]}
        fi
        local license_file=$(find ${folder} -name "LICENSE" -quit)
        cp --verbose ${license_file} "${folder}/../${dir}/" ||:
        rm --force --recursive ${folder}
    done

    # Go though each of the downloaded libraries and copy the relevant parts.
    echo "  -> Transfer requirements to bundle"
    for dependency_content in ${install_platform_dir}/*; do
        echo "    - Processing: ${dependency_content}"
        if [[ -f ${dependency_content} ]]; then
            cp ${dependency_content} ${main_platform_dir}
            continue
        fi

        # The actual code of the library.
        rsync \
            --progress \
            --recursive \
            --prune-empty-dirs \
            --exclude-from="${CWD}/requirements.ignore" \
            "${dependency_content}/" "${main_platform_dir}"
    done

    echo "  -> Cleaning"
    rm --force --recursive ${install_platform_dir}
}

##
# Create the `apworld` file used by Archipelago.
#
# Arguments:
# * $1: project root
# * $2: destination directory
##
function mk_apworld() {
    local root="$1" destdir="$2"
    echo "=> Bundling apworld"
    echo "From: ${root}"
    echo "To: ${destdir}"
    mkdir --parents "${destdir}/luigismansion"
    rsync --progress \
        --recursive \
        --prune-empty-dirs \
        --exclude-from="${CWD}/apworld.ignore" \
        "${root}/" "${destdir}/luigismansion"
    pushd "${destdir}"
    zip -9r "luigismansion.apworld" "luigismansion"
    popd

    rm --force --recursive "${destdir}/luigismansion"
}

##
# Create the final bundled archive.
#
# Arguments:
# * $1: The location from where the archive is created.
# * $2: The path of the output archive.
##
function bundle() {
    local from="$1" out="$2"
    echo "=> Finalize bundle"
    [ -f "${out}" ] && rm ${out} ||:
    pushd "${from}"
    zip -9r "${out}" "."
    popd
}

##
# Main entry point.
##
function main() {
    pre_flight

    local target_path="${CWD}/target"
    local pip_download="${CWD}/deps"
    local bundle_base="luigismansion_apworld"
    mkdir --parents ${target_path}

    case "$1" in
    # Clean the build environment.
    clean)
        find "${target_path}" \
            -depth \
            -type d \
            -name "${bundle_base}-*" \
            -exec rm --force --recursive --verbose {} \;
        ;;

    # Create the release bundle.
    *)
        local tag="${TAG:-v0.0.1}"
        local project="$(realpath ${CWD}/..)"
        local bundle="${bundle_base}-${tag}"
        local destdir="${target_path}/${bundle}"

        for platform in "${SUPPORTED_PLATFORMS[@]}"; do
            get_deps "${platform}" "${project}/requirements.txt" "${destdir}/lib" "${pip_download}"
        done
        mk_apworld "${project}" "${destdir}"
        # bundle "${destdir}" "${target_path}/${bundle}.zip"
        echo "! Bundle finalized as ${target_path}" #/${bundle}.zip"
        ;;
    esac
}
main "$@"