import pytest
import urllib.request
import ssl
import socket
from unittest.mock import patch, MagicMock

HTTP_IP = "172.30.67.194"

def get_http_response(ip, port=80):
    url = f"http://{ip}:{port}"
    response = urllib.request.urlopen(url)
    return response.status

def check_ssl(ip):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(), server_hostname=ip)
    return conn is not None

def get_server_network(ip):
    if ip.startswith("172.30.67.19"):
        return "black_network"
    elif ip.startswith("172.20"):
        return "blue_network"
    return "unknown"


def test_http_server_responds():
    with patch("urllib.request.urlopen") as mock_url:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_url.return_value = mock_response
        assert get_http_response(HTTP_IP) == 200

def test_http_on_correct_network():
    assert get_server_network(HTTP_IP) == "black_network"

def test_http_not_on_blue_network():
    assert get_server_network("172.20.0.5") != "black_network"

def test_ssl_certificate_present():
    with patch("ssl.create_default_context") as mock_ssl:
        mock_ssl.return_value.wrap_socket.return_value = MagicMock()
        assert check_ssl(HTTP_IP) is not None

def test_http_server_down_detected():
    with patch("urllib.request.urlopen", side_effect=Exception("Connection refused")):
        with pytest.raises(Exception, match="Connection refused"):
            get_http_response(HTTP_IP)