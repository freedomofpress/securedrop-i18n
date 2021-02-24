#!/usr/bin/env python

#
# Compares Tor configurations on the app server and from a backup. If
# restoring the backup would alter the server's Tor configuration,
# print a warning and exit.
#

from __future__ import print_function

import os
import re
import sys


def get_tor_versions(path):
    """
    Determine which service versions are offered in the given torrc.
    """
    service_re = re.compile(r"HiddenServiceDir\s+(?:.*)/(.*)")
    versions = set([])
    with open(path) as f:
        for line in f:
            m = service_re.match(line)
            if m:
                service = m.group(1)
                if "v3" in service:
                    versions.add(3)
                else:
                    versions.add(2)

    return versions


def strset(s):
    """
    Sort the given set and join members with "and".
    """
    return " and ".join(str(v) for v in sorted(s))


if __name__ == "__main__":
    tempdir = sys.argv[1]

    server_versions = get_tor_versions(os.path.join(tempdir, "app/etc/tor/torrc"))
    backup_versions = get_tor_versions(os.path.join(tempdir, "backup/etc/tor/torrc"))

    if server_versions == backup_versions:
        print("The Tor configuration in the backup matches the server.")
        sys.exit(0)

    if (3 in server_versions) and (3 in backup_versions):
        print("V3 services detected in backup and server - proceeding with v3-only restore")
        sys.exit(0)

    print(
        "The Tor configuration on the app server offers version {} services.".format(
            strset(server_versions)
        )
    )

    print(
        "The Tor configuration in this backup offers version {} services.".format(
            strset(backup_versions)
        )
    )

    print("\nRestoring a backup with a different Tor configuration than the server ")
    print("is currently unsupported. If you require technical assistance, please ")
    print("contact the SecureDrop team via the support portal or at ")
    print("securedrop@freedom.press.")

    sys.exit(1)
