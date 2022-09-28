import difflib
import io
import os

import pytest
import testutils
from jinja2 import Template

securedrop_test_vars = testutils.securedrop_test_vars
testinfra_hosts = [securedrop_test_vars.app_hostname]


@pytest.mark.skip_in_prod
def test_app_iptables_rules(host):

    local = host.get_host("local://")

    # Build a dict of variables to pass to jinja for iptables comparison
    kwargs = dict(
        mon_ip=os.environ.get("MON_IP", securedrop_test_vars.mon_ip),
        default_interface=host.check_output("ip r | head -n 1 | " "awk '{ print $5 }'"),
        tor_user_id=host.check_output("id -u debian-tor"),
        time_service_user=host.check_output("id -u systemd-timesync"),
        securedrop_user_id=host.check_output("id -u www-data"),
        ssh_group_gid=host.check_output("getent group ssh | cut -d: -f3"),
        dns_server=securedrop_test_vars.dns_server,
    )

    # Required for testing under Qubes.
    if local.interface("eth0").exists:
        kwargs["ssh_ip"] = local.interface("eth0").addresses[0]

    # Build iptables scrape cmd, purge comments + counters
    iptables = r"iptables-save | sed 's/ \[[0-9]*\:[0-9]*\]//g' | egrep -v '^#'"
    environment = os.environ.get("SECUREDROP_TESTINFRA_TARGET_HOST", "staging")
    iptables_file = "{}/iptables-app-{}.j2".format(
        os.path.dirname(os.path.abspath(__file__)), environment
    )

    # template out a local iptables jinja file
    jinja_iptables = Template(io.open(iptables_file, "r").read())
    iptables_expected = jinja_iptables.render(**kwargs)

    with host.sudo():
        # Actually run the iptables scrape command
        iptables = host.check_output(iptables)
        # print diff comparison (only shows up in pytests if test fails or
        # verbosity turned way up)
        for iptablesdiff in difflib.context_diff(
            iptables_expected.split("\n"), iptables.split("\n")
        ):
            print(iptablesdiff)
        # Conduct the string comparison of the expected and actual iptables
        # ruleset
        assert iptables_expected == iptables
