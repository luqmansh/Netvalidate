import pytest
import socket
from unittest.mock import patch

DOMAIN = "chairmen.lab"
DC1_IP = "172.30.67.3"
DC2_IP = "172.30.67.4"

def resolve_domain(domain):
    return socket.gethostbyname(domain)

def check_forwarder(source_domain, target_domain):
    forwarders = {"chairmen.lab": "et.lab"}
    return forwarders.get(source_domain) == target_domain

def recursive_lookup(hostname):
    return socket.gethostbyname(hostname)


def test_dc1_resolves_domain():
    with patch("socket.gethostbyname", return_value=DC1_IP):
        assert resolve_domain(DOMAIN) == DC1_IP

def test_dc2_resolves_domain():
    with patch("socket.gethostbyname", return_value=DC2_IP):
        assert resolve_domain(DOMAIN) == DC2_IP

def test_conditional_forwarder_correct():
    assert check_forwarder("chairmen.lab", "et.lab") == True

def test_conditional_forwarder_wrong_domain():
    assert check_forwarder("chairmen.lab", "unknown.lab") == False

def test_recursive_dns_resolves_internet():
    with patch("socket.gethostbyname", return_value="8.8.8.8"):
        assert recursive_lookup("google.com") is not None

def test_dns_failure_detected():
    with patch("socket.gethostbyname", side_effect=Exception("DNS resolution failed")):
        with pytest.raises(Exception, match="DNS resolution failed"):
            resolve_domain(DOMAIN)

def test_root_hints_misconfiguration():
    with patch("socket.gethostbyname", side_effect=Exception("No root hints configured")):
        with pytest.raises(Exception):
            recursive_lookup("google.com")