"""Fetch an explicitly selected public HTTPS document with a pinned connection."""

import http.client
import ipaddress
import socket
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

from .intake_files import IntakeError, MAX_BYTES


class PublicHTTPSConnection(http.client.HTTPSConnection):
    def connect(self):
        records = socket.getaddrinfo(self.host, 443, type=socket.SOCK_STREAM)
        addresses = list(dict.fromkeys(item[4][0] for item in records))
        parsed = [ipaddress.ip_address(address) for address in addresses]
        if not parsed or any(not address.is_global or address.is_multicast for address in parsed):
            raise IntakeError("The address must resolve only to public IPs.")
        # Use the resolved numeric address for TCP while retaining the original hostname for TLS.
        sock = socket.create_connection((addresses[0], 443), timeout=self.timeout)
        try:
            self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
        except BaseException:
            sock.close()
            raise


def fetch(connection, path, *, limit):
    connection.request("GET", path, headers={"User-Agent": "MToolsIntake", "Accept-Encoding": "identity"})
    response = connection.getresponse()
    if response.status != 200 or response.getheader("Content-Encoding") not in (None, "identity"):
        raise IntakeError("The selected source requires a direct, readable public response.")
    data = response.read(limit + 1)
    if len(data) > limit:
        raise IntakeError("The public source exceeds the size limit.")
    return data, response.headers.get_content_type()


def public_page(url):
    try:
        parsed = urlsplit(url)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.port not in (None, 443)
                or parsed.username is not None or parsed.password is not None or parsed.fragment):
            raise IntakeError("Use a direct public HTTPS URL.")
        if any(ord(char) <= 32 or ord(char) >= 127 for char in url) or "\\" in url:
            raise IntakeError("Use an encoded HTTPS URL.")
        path = (parsed.path or "/") + ("?" + parsed.query if parsed.query else "")
        robots = RobotFileParser()
        with_source = PublicHTTPSConnection(parsed.hostname, timeout=5)
        try:
            robot_data, _ = fetch(with_source, "/robots.txt", limit=100_000)
            robots.parse(robot_data.decode("utf-8"))
        finally:
            with_source.close()
        if not robots.can_fetch("MToolsIntake", url):
            raise IntakeError("Use an authorized upload for this source.")
        with_source = PublicHTTPSConnection(parsed.hostname, timeout=5)
        try:
            raw, mime = fetch(with_source, path, limit=MAX_BYTES)
        finally:
            with_source.close()
        if mime not in ("text/plain", "text/html"):
            raise IntakeError("Use a public HTML page or upload a supported document.")
        return raw, mime
    except (OSError, UnicodeError, ValueError, http.client.HTTPException) as exc:
        if isinstance(exc, IntakeError):
            raise
        raise IntakeError("The selected public source could not be read.") from exc
