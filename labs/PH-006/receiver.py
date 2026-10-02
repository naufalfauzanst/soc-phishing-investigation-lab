import argparse
import json
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "received-demo.jsonl"
EXPECTED = {"username": ["user-lab"], "password": ["DEMO-NOT-A-REAL-PASSWORD"]}


class Receiver(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def reply(self, status, message):
        body = message.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/latihan":
            self.reply(404, "Alamat tidak tersedia.")
            return
        if self.headers.get_content_type() != "application/x-www-form-urlencoded":
            self.reply(415, "Gunakan formulir latihan.")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 1024:
                raise ValueError("Invalid length")
            data = parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)
        except (ValueError, UnicodeError):
            self.reply(400, "Format data tidak sesuai.")
            return
        if data != EXPECTED:
            self.reply(400, "Ditolak. Hanya data palsu bawaan yang diterima; isian tidak disimpan.")
            return
        event = {
            "case_id": "PH-006",
            "received_at_utc": datetime.now(timezone.utc).isoformat(),
            "method": "POST",
            "path": "/latihan",
            "peer_ip": self.client_address[0],
            "receiver_role": "simulated attacker; loopback only",
            "data_class": "fixed synthetic training values",
            "username": EXPECTED["username"][0],
            "password": EXPECTED["password"][0],
        }
        with EVIDENCE.open("a", encoding="utf-8") as output:
            output.write(json.dumps(event) + "\n")
        print(json.dumps(event, indent=2), flush=True)
        self.reply(200, "Data palsu berhasil diterima. Lihat terminal dan received-demo.jsonl.")


def self_test():
    before = EVIDENCE.read_bytes() if EVIDENCE.exists() else b""
    server = HTTPServer(("127.0.0.1", 0), Receiver)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    url = f"http://127.0.0.1:{server.server_port}/latihan"
    try:
        valid = urlencode({key: value[0] for key, value in EXPECTED.items()}).encode()
        request = Request(url, data=valid, headers={"Content-Type": "application/x-www-form-urlencoded"})
        with urlopen(request, timeout=5) as response:
            assert response.status == 200
        after = EVIDENCE.read_bytes()
        assert after.startswith(before)
        assert len(after[len(before):].splitlines()) == 1
        event = json.loads(after[len(before):])
        assert event["username"] == "user-lab" and event["password"] == "DEMO-NOT-A-REAL-PASSWORD"
        invalid = Request(url, data=b"username=not-demo&password=not-demo", headers={"Content-Type": "application/x-www-form-urlencoded"})
        try:
            urlopen(invalid, timeout=5)
            raise AssertionError("Unexpected input accepted")
        except HTTPError as error:
            assert error.code == 400
        assert EVIDENCE.read_bytes() == after
        result = {
            "tested_at_utc": datetime.now(timezone.utc).isoformat(),
            "transport": "Python HTTP client; not browser or Gmail",
            "bind_address": server.server_address[0],
            "test_port": server.server_port,
            "valid_demo_post": "HTTP 200; one evidence record written",
            "other_values": "HTTP 400; no evidence record written",
            "status": "passed",
        }
        (ROOT / "validation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print("Validation passed; server stopped after test.", flush=True)
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)


def main():
    parser = argparse.ArgumentParser(description="Loopback form demo; accepts fixed fake values only.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    server = HTTPServer(("127.0.0.1", 9000), Receiver)
    print("PH-006 receiver: http://127.0.0.1:9000/latihan\nOpen Invoice-Demo.pdf.html, then submit. Ctrl+C stops the server.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
