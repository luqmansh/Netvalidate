import pytest

NETWORK_CONFIG = {
    "domain": "chairmen.lab",
    "dc1_ip": "172.30.67.3",
    "dc2_ip": "172.30.67.4",
    "dns_recursive_ip": "172.30.67.18",
    "http_ip": "172.30.67.194",
    "iscsi_target_ip": "172.30.67.130",
    "iscsi_initiator_ip": "172.30.67.131",
    "fs1_ip": "172.30.67.13",
    "fs2_ip": "172.30.67.22",
    "wac_ip": "172.30.67.24",
    "red_network": "172.30.67.1/25",
    "green_network": "172.30.67.128/26",
    "black_network": "172.30.67.192/26",
}

@pytest.fixture
def network():
    return NETWORK_CONFIG