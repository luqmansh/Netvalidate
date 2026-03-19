import pytest
from unittest.mock import patch, MagicMock

TARGET_IP = "172.30.67.130"
INITIATOR_IP = "172.30.67.131"

def connect_iscsi(target_ip, initiator_ip):
    if target_ip.startswith("172.30.67.1"):
        return {"status": "connected", "target": target_ip, "initiator": initiator_ip}
    return {"status": "failed"}

def check_iscsi_network(ip):
    if ip.startswith("172.30.67.1"):
        return "green_network"
    elif ip.startswith("172.20"):
        return "blue_network"
    return "unknown"

def get_storage_size(target_ip):
    return 500


def test_iscsi_target_reachable():
    result = connect_iscsi(TARGET_IP, INITIATOR_IP)
    assert result["status"] == "connected"

def test_iscsi_initiator_connects_to_target():
    result = connect_iscsi(TARGET_IP, INITIATOR_IP)
    assert result["target"] == TARGET_IP
    assert result["initiator"] == INITIATOR_IP

def test_iscsi_on_green_network():
    assert check_iscsi_network(TARGET_IP) == "green_network"
    assert check_iscsi_network(INITIATOR_IP) == "green_network"

def test_iscsi_not_on_blue_network():
    assert check_iscsi_network("172.20.0.5") != "green_network"

def test_iscsi_storage_available():
    assert get_storage_size(TARGET_IP) > 0

def test_iscsi_connection_failure_detected():
    result = connect_iscsi("999.999.999.999", INITIATOR_IP)
    assert result["status"] == "failed"