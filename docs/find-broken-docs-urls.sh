#!/bin/bash
set -e
set -u
set -o pipefail


all_known_urls_tmpfile="$(mktemp)"
broken_urls_tmpfile="$(mktemp)"

# Only search ReST files, otherwise the built assets in HTML format will be
# searched as well, provided duplicates. Writing to a 
find docs -type f -iname '*.rst' -exec \
    grep -s --no-filename -I -rP --color=never -o \
    $'https?:[^\s\'\"`>]*' {} + | sort -u > "${all_known_urls_tmpfile}"

# Count up the URLs we found, for informative output.
known_url_count="$(wc --lines "${all_known_urls_tmpfile}" | perl -lanE 'print $F[0]')"
echo "Found ${known_url_count} URLs, attempting to load..."

# Iterate over list of probably-URLs and record which ones return non-200.
while read url ; do
    curl --connect-timeout 5 --head --fail --silent "${url}" > /dev/null \
        || echo "FAILED: ${url}" >> "${broken_urls_tmpfile}"
done < "${all_known_urls_tmpfile}"

# Count up the broken URLs we found, for informative output.
broken_url_count="$(wc --lines "${broken_urls_tmpfile}" | perl -lanE 'print $F[0]')"
echo "The following ${broken_url_count} URLs in the SecureDrop document appear to be broken:"
cat "${broken_urls_tmpfile}"
