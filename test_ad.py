import pytest
from unittest.mock import patch, MagicMock

DOMAIN = "chairmen.lab"
DC1_IP = "172.30.67.3"
DC2_IP = "172.30.67.4"

def authenticate_user(username, password, domain):
    valid_users = {
        "admin": "password123",
        "testuser": "test456"
    }
    if valid_users.get(username) == password:
        return {"status": "authenticated", "domain": domain, "user": username}
    return {"status": "failed", "reason": "Invalid credentials"}

def get_domain_controller(domain):
    dc_map = {"chairmen.lab": DC1_IP}
    return dc_map.get(domain)

def check_dc_replication(dc1, dc2):
    if dc1 != dc2 and dc1.startswith("172.30") and dc2.startswith("172.30"):
        return {"status": "replicating", "dc1": dc1, "dc2": dc2}
    return {"status": "failed"}

def get_user_permissions(username):
    permissions = {
        "admin": ["read", "write", "execute", "manage_users"],
        "testuser": ["read"]
    }
    return permissions.get(username, [])


def test_valid_user_authenticates():
    result = authenticate_user("admin", "password123", DOMAIN)
    assert result["status"] == "authenticated"

def test_invalid_user_rejected():
    result = authenticate_user("admin", "wrongpassword", DOMAIN)
    assert result["status"] == "failed"

def test_domain_controller_found():
    assert get_domain_controller(DOMAIN) == DC1_IP

def test_unknown_domain_returns_none():
    assert get_domain_controller("unknown.lab") is None

def test_dc_replication_active():
    result = check_dc_replication(DC1_IP, DC2_IP)
    assert result["status"] == "replicating"

def test_admin_has_full_permissions():
    perms = get_user_permissions("admin")
    assert "manage_users" in perms
    assert "write" in perms

def test_regular_user_restricted():
    perms = get_user_permissions("testuser")
    assert "read" in perms
    assert "manage_users" not in perms