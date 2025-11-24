# i hate guessy stego 0 &mdash; Author's Writeup

## Solution

This challenge hints at DNS-based data exfiltration. This is a technique often employed by malware to bypass network restrictions, largely because DNS traffic is rarely filtered in typical network environments. A closer inspection of the provided capture file in Wireshark reveals an unusually high volume of DNS requests, many of which are directed at suspicious subdomains of `dnslog.cn`.

This behaviour is characteristic of tools or malware that exfiltrate data via DNS queries, particularly when using services like DNSLog &mdash; a popular DNS logging platform commonly used in penetration testing.

As each leftmost subdomain of `dnslog.cn` consists of two characters, one can reasonably suspect that they represent hex-encoded ASCII character codes. By extracting and decoding these subdomains, the flag is revealed.

See `solve.py` for a solution script.

## References

- https://www.akamai.com/glossary/what-is-dns-data-exfiltration