#!/usr/bin/env python3
"""
generate_challenge_v2.py

Scenario (v2):
  - Multiple internal IPs hammer auth endpoints.
  - Failure distribution: top1 > top2 > TARGET (rank #3) > others.
  - Top1 (highest failures) NEVER succeeds.
  - Target (fixed 10.10.5.23) eventually succeeds and downloads a file whose SHA256
    (real hash of generated binary) is among many other believable SHA256 downloads.
  - Several other IPs also download files (each with unique SHA256 decoys) to create noise.
  - Only target's DNS queries virustotal.com shortly AFTER its protected download.
  - Player must correlate failures → successes → downloads → DNS pivot → VirusTotal.

Generated Files:
  - flag_printer.c
  - flag_printer.exe (or placeholder if no compiler)
  - IIS_u_ex<YYMMDD>.log
  - dnsmasq_<YYYY-MM-DD>.log
  - README.txt

Flag (binary prints):
    sctf{we11_d0n3_d0_y0u_l0v3_b1u3_t34m1ng}

Usage examples:
  python generate_challenge_v2.py --date 2024-07-18
  python generate_challenge_v2.py --date 2024-07-18 --top1-fail 420 --top2-fail 330 --target-fail 250

You can re-run with different --seed to reshuffle noise while preserving structural logic.
"""

import argparse
import datetime as dt
import hashlib
import os
import random
import shutil
import subprocess
from textwrap import dedent

FLAG = "sctf{we11_d0n3_d0_y0u_l0v3_b1u3_t34m1ng}"
TARGET_IP = "10.10.5.23"  # stays fixed per your requirement

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edg/126.0.2592.87",
    "curl/7.88.1",
    "python-requests/2.31.0",
    "Windows-Update-Agent/10.0",
    "kube-probe/1.29"
]

AUTH_ENDPOINTS = ["/portal/login", "/api/auth", "/api/login"]
STATIC_PATHS = [
    "/", "/favicon.ico",
    "/assets/js/app.js", "/assets/js/runtime.js",
    "/assets/js/vendor/react.min.js", "/assets/css/main.css",
    "/assets/css/theme/dark.css", "/assets/fonts/roboto.woff2",
    "/portal/dashboard", "/portal/overview",
    "/api/ping", "/api/health", "/api/notifications", "/api/user/profile",
    "/metrics", "/health", "/content/reports/index.html",
    "/static/img/banner.png", "/static/img/icon-192.png"
]

# Candidate download paths (all will look "sensitive" enough)
DOWNLOAD_PATHS = [
    "/download/finance_q2_export.zip",
    "/download/finance_forecast.xlsx",
    "/download/hr_comp_plan.pdf",
    "/download/engineering_metrics.csv",
    "/download/budget_overview_2024.xlsx",
    "/download/devops_tooling_bundle.zip",
    "/download/security_policy.pdf",
    "/download/ops_backup_config.tar.gz"
]

DNS_COMMON = [
    "ocsp.digicert.com", "login.microsoftonline.com", "outlook.office365.com",
    "api.slack.com", "slack.com", "github.com", "api.github.com",
    "raw.githubusercontent.com", "fonts.googleapis.com", "fonts.gstatic.com",
    "cdn.jsdelivr.net", "packages.microsoft.com", "pypi.org",
    "files.pythonhosted.org", "registry.npmjs.org", "time.windows.com",
    "updates.crowdstrike.com", "agent-events.security.microsoft.com",
    "download.splunk.com", "api.segment.io", "safebrowsing.googleapis.com",
    "clients1.google.com", "clients2.google.com", "edge.microsoft.com"
]

DNS_INTERNAL = [
    "sso.corp.internal", "api.corp.internal", "metrics.corp.internal",
    "vault.corp.internal", "repo.corp.internal"
]

VT_DOMAIN = "virustotal.com"

C_SOURCE = r'''#include <stdio.h>
int main(void){
    puts("sctf{we11_d0n3_d0_y0u_l0v3_b1u3_t34m1ng}");
    return 0;
}
'''

def detect_compiler():
    for c in ["x86_64-w64-mingw32-gcc", "i686-w64-mingw32-gcc", "cl", "gcc", "clang"]:
        if shutil.which(c):
            return c
    return None

def compile_binary(src, out):
    comp = detect_compiler()
    if not comp:
        return False, "No compiler"
    try:
        if comp == "cl":
            subprocess.check_call(["cl", "/nologo", src, "/Fe" + out],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.check_call([comp, src, "-O2", "-s", "-o", out],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True, comp
    except subprocess.CalledProcessError as e:
        return False, f"Compilation failed: {e}"

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def random_sha256():
    return hashlib.sha256(os.urandom(48)).hexdigest()

def random_md5():
    return hashlib.md5(os.urandom(32)).hexdigest()

def generate_iis_log(
    outfile,
    date,
    server_ip,
    top1_ip,
    top2_ip,
    target_fail,
    top1_fail,
    top2_fail,
    other_fail_range,
    normal_success_count,
    download_count_other_sha256,
    include_md5_decoys,
    real_sha256,
    target_download_path,
    seed
):
    """
    Build IIS log with ranking: top1_fail > top2_fail > target_fail.
    - top1_ip: highest failures, NO success
    - top2_ip: second highest, may have some successes
    - target (fixed TARGET_IP): third, has success + real protected download
    - Many other IPs: fewer failures & successes + decoy downloads with SHA256 (and optional MD5)
    """
    random.seed(seed)
    lines = []
    header = dedent(f"""\
    #Software: Microsoft Internet Information Services 10.0
    #Version: 1.0
    #Date: {date.strftime('%Y-%m-%d')} 00:00:00
    #Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) sc-status sc-substatus sc-win32-status time-taken x-filehash
    """).strip()
    lines.append(header)

    base_ts = dt.datetime.combine(date, dt.time(9, 0, 0))
    cur = base_ts

    def add_line(ts, method, path, query, username, cip, status, sub, win32, ttime, ua, xhash="-"):
        lines.append(f"{ts.date()} {ts.time()} {server_ip} {method} {path} {query or '-'} 443 "
                     f"{username or '-'} {cip} \"{ua}\" {status} {sub} {win32} {ttime} {xhash}")

    def bump(lo=1, hi=3):
        nonlocal cur
        cur += dt.timedelta(seconds=random.randint(lo, hi))

    # Build IP pool (excluding already designated ones)
    other_ips = [
        "10.10.5.10", "10.10.5.11", "10.10.5.12",
        "10.10.5.30", "10.10.5.31", "10.10.5.40",
        "10.10.5.45", "10.10.5.55", "10.10.5.60",
        "10.10.6.14", "10.10.6.21"
    ]
    for ip in [top1_ip, top2_ip, TARGET_IP]:
        if ip in other_ips:
            other_ips.remove(ip)

    # 1. Ambient normal traffic (successes + static)
    for _ in range(250):
        ip = random.choice(other_ips + [top2_ip])
        path = random.choice(STATIC_PATHS)
        ua = random.choice(USER_AGENTS)
        status_choice = random.random()
        if status_choice < 0.85:
            st = 200; sub=0; win=0
        elif status_choice < 0.9:
            st = 304; sub=0; win=0
        elif status_choice < 0.95:
            st = 404; sub=0; win=2
        else:
            st = 500; sub=0; win=64
        add_line(cur, "GET", path, None, None, ip, st, sub, win, random.randint(5,110), ua)
        bump()

    # Function to spray failures
    def spray_failures(ip, count):
        nonlocal cur
        for _ in range(count):
            ep = random.choice(AUTH_ENDPOINTS)
            method = random.choice(["POST","POST","GET"])
            ua = random.choice(USER_AGENTS)
            add_line(cur, method, ep, None, None, ip, 401, 2, 5, random.randint(40,90), ua)
            bump()

    # 2. Failures for top1, top2, target (in interleaved waves)
    # Interleave waves to look realistic (session-based)
    waves = 5
    top1_per_wave = top1_fail // waves
    top2_per_wave = top2_fail // waves
    target_per_wave = target_fail // waves

    remaining_top1 = top1_fail
    remaining_top2 = top2_fail
    remaining_target = target_fail

    for w in range(waves):
        c1 = top1_per_wave if w < waves-1 else remaining_top1
        c2 = top2_per_wave if w < waves-1 else remaining_top2
        c3 = target_per_wave if w < waves-1 else remaining_target

        spray_failures(top1_ip, c1); remaining_top1 -= c1
        # Insert some normal successes in between
        for _ in range(normal_success_count//waves):
            ip = random.choice(other_ips)
            method = "POST"
            ep = random.choice(AUTH_ENDPOINTS)
            ua = random.choice(USER_AGENTS)
            username = f"user{random.randint(100,199)}"
            add_line(cur, method, ep, None, username, ip, 200, 0, 0, random.randint(60,140), ua)
            bump()

        spray_failures(top2_ip, c2); remaining_top2 -= c2

        # Add some top2 successes (OPTIONAL noise)
        for _ in range(random.randint(1,3)):
            ep = random.choice(AUTH_ENDPOINTS)
            ua = random.choice(USER_AGENTS)
            add_line(cur, "POST", ep, None, f"user_top2_{random.randint(1,5)}", top2_ip, 200, 0, 0, random.randint(70,120), ua)
            bump()

        spray_failures(TARGET_IP, c3); remaining_target -= c3

        # Sprinkle some unrelated successful logins
        for _ in range(random.randint(3,7)):
            ip = random.choice(other_ips)
            ua = random.choice(USER_AGENTS)
            ep = random.choice(AUTH_ENDPOINTS)
            add_line(cur, "POST", ep, None, f"user{random.randint(200,299)}", ip, 200, 0, 0, random.randint(55,130), ua)
            bump()

    # 3. TARGET success (only after its failures complete)
    ua_t = random.choice(USER_AGENTS)
    success_ep = random.choice(AUTH_ENDPOINTS)
    add_line(cur, "POST", success_ep, None, "finance_reader", TARGET_IP, 200, 0, 0, random.randint(80,150), ua_t)
    t_target_success = cur
    bump(2,4)

    # 4. TARGET real download with real SHA256
    add_line(cur, "GET", target_download_path, "ver=3.4", "finance_reader", TARGET_IP,
             200, 0, 0, random.randint(250,700), ua_t, real_sha256)
    t_target_download = cur
    bump()

    # 5. Multiple OTHER SHA256 downloads (decoys)
    # Build a pool of decoy SHA256 (distinct)
    decoy_sha256 = {real_sha256}
    while len(decoy_sha256) < download_count_other_sha256 + 1:
        decoy_sha256.add(random_sha256())
    decoy_sha256.remove(real_sha256)
    decoy_sha256 = list(decoy_sha256)

    # Assign decoy downloads to mixture of IPs (including maybe target once more to muddy)
    decoy_paths = [p for p in DOWNLOAD_PATHS if p != target_download_path]
    for h in decoy_sha256:
        ip = random.choice([top2_ip] + other_ips)
        path = random.choice(decoy_paths)
        ua = random.choice(USER_AGENTS)
        user = f"user{random.randint(300,399)}" if ip != TARGET_IP else "finance_reader"
        add_line(cur, "GET", path, None, user, ip, 200, 0, 0, random.randint(120,650), ua, h)
        bump()

    # 6. Optional MD5 decoys (short hashes)
    if include_md5_decoys:
        for _ in range(5):
            ip = random.choice(other_ips)
            path = random.choice(decoy_paths)
            add_line(cur, "GET", path, None, f"user{random.randint(400,499)}", ip, 200, 0, 0,
                     random.randint(90,300), random.choice(USER_AGENTS), random_md5())
            bump()

    # 7. Post-download browsing for target
    post_paths = ["/portal/dashboard", "/api/user/profile", "/portal/overview", "/api/notifications"]
    for _ in range(6):
        p = random.choice(post_paths)
        add_line(cur, "GET", p, None, "finance_reader", TARGET_IP, 200, 0, 0,
                 random.randint(40,120), ua_t)
        bump()

    # 8. More ambient noise after
    for _ in range(120):
        ip = random.choice(other_ips + [top2_ip])
        p = random.choice(STATIC_PATHS)
        ua = random.choice(USER_AGENTS)
        status_roll = random.random()
        if status_roll < 0.9:
            st=200; sub=0; win=0
        elif status_roll < 0.93:
            st=304; sub=0; win=0
        elif status_roll < 0.97:
            st=404; sub=0; win=2
        else:
            st=500; sub=0; win=64
        add_line(cur, "GET", p, None, None, ip, st, sub, win, random.randint(5,130), ua)
        bump()

    with open(outfile, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return {
        "target_success": t_target_success,
        "target_download": t_target_download
    }

def generate_dnsmasq(
    outfile,
    date,
    target_download_time,
    top1_ip,
    top2_ip,
    extra_ip_list,
    seed
):
    random.seed(seed)
    lines = []
    dns_host = "dns01"
    pid = 742

    def emit(ts, text):
        lines.append(f"{ts.strftime('%b')} {ts.day:02d} {ts.strftime('%H:%M:%S')} {dns_host} dnsmasq[{pid}]: {text}")

    # Time window
    start = target_download_time - dt.timedelta(minutes=10)
    end   = target_download_time + dt.timedelta(minutes=10)

    # Function to generate queries for a host (NO virustotal)
    def host_queries(ip, base_ts):
        t = base_ts
        domains = random.sample(DNS_COMMON + DNS_INTERNAL, k=random.randint(8,14))
        for d in domains:
            recs = ["A"] + (["AAAA"] if random.random() < 0.35 else [])
            for r in recs:
                emit(t, f"query[{r}] {d} from {ip}")
            emit(t, f"forwarded {d} to 1.1.1.1")
            emit(t, f"reply {d} is 203.0.113.{random.randint(1,254)}")
            t += dt.timedelta(seconds=random.randint(2,10))

    # Generate for top1, top2, others BEFORE and AFTER (no VT)
    all_noise_ips = [top1_ip, top2_ip] + extra_ip_list
    for ip in all_noise_ips:
        base_ts = start + dt.timedelta(seconds=random.randint(0, 300))
        host_queries(ip, base_ts)

    # Target normal queries after download
    t_target = target_download_time + dt.timedelta(seconds=20)
    host_queries(TARGET_IP, t_target)

    # Virustotal pivot (ONLY target) a bit later
    vt_time = t_target + dt.timedelta(seconds=random.randint(60,120))
    emit(vt_time, f"query[A] {VT_DOMAIN} from {TARGET_IP}")
    emit(vt_time, f"query[AAAA] {VT_DOMAIN} from {TARGET_IP}")
    emit(vt_time, f"forwarded {VT_DOMAIN} to 1.1.1.1")
    emit(vt_time, f"reply {VT_DOMAIN} is 104.16.132.{random.randint(10,200)}")

    lines.sort()
    with open(outfile, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def write_readme(path, date, real_hash, target_download_path,
                 top1_ip, top2_ip, target_success_time, target_download_time,
                 top1_fail, top2_fail, target_fail):
    content = dedent(f"""
    Challenge Dataset (v2 – Correlation Ranking Variant)

    Files:
      - IIS_u_ex{date.strftime('%y%m%d')}.log
      - dnsmasq_{date.strftime('%Y-%m-%d')}.log
      - flag_printer.c
      - flag_printer.exe (placeholder if no compiler)
      - README.txt

    INTENDED SOLVE STEPS:
      1. Count failed auth (401) attempts by client IP (c-ip). Rank them.
         - Highest failure count: IP A (no successful auth at all).
         - Second: IP B (some successes, benign downloads).
         - THIRD: 10.10.5.23 (TARGET) – has failures then success.
      2. Observe many successful logins across many IPs (normal app usage).
      3. Ignore top1 (never succeeds). Investigate successful IPs below it.
      4. Extract all file download lines with 64-hex SHA256 hashes (many decoys).
      5. Identify which SHA256 belongs to the file downloaded by 10.10.5.23 RIGHT after its first success:
         Path: {target_download_path}
         Hash: {real_hash}
      6. Correlate DNS logs: only that IP queries virustotal.com after its download.
      7. Search SHA256 on VirusTotal to recover the flag (not in logs).

    Key Hash (real): {real_hash}

    Target success time: {target_success_time}
    Target download time: {target_download_time}

    Failure counts (approx):
      Top1 IP: {top1_ip} -> {top1_fail} failures, NO success
      Top2 IP: {top2_ip} -> {top2_fail} failures (some successes)
      Target IP: 10.10.5.23 -> {target_fail} failures + 1 success + interesting download

    The compiled binary prints the flag:
      sctf{{we11_d0n3_d0_y0u_l0v3_b1u3_t34m1ng}}

    Hash Type Clue:
      Only 64-hex (SHA256) matter; 32-hex MD5-style values are optional decoys.

    Deliverables (suggested to solver):
      - Ranking of top failing IPs
      - Target success timestamp
      - Download path & SHA256
      - Evidence of virustotal.com lookup
      - Final flag from VT
    """).strip()
    with open(path, "w", encoding="utf-8") as f:
        f.write(content + "\n")

def main():
    ap = argparse.ArgumentParser(description="Generate v2 correlation challenge with target ranked 3rd by failures.")
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")
    ap.add_argument("--server-ip", default="192.0.2.80")
    ap.add_argument("--top1-ip", default="10.10.7.50", help="Highest failing IP (no success)")
    ap.add_argument("--top2-ip", default="10.10.5.50", help="Second highest failing IP")
    ap.add_argument("--top1-fail", type=int, default=420)
    ap.add_argument("--top2-fail", type=int, default=330)
    ap.add_argument("--target-fail", type=int, default=250)
    ap.add_argument("--other-fail-min", type=int, default=15)
    ap.add_argument("--other-fail-max", type=int, default=60)
    ap.add_argument("--normal-success-per-wave", type=int, default=14,
                    help="Baseline successful auth noise per wave (higher => more realism)")
    ap.add_argument("--other-sha256-downloads", type=int, default=9,
                    help="Number of SHA256 decoy downloads (besides real)")
    ap.add_argument("--no-md5-decoys", action="store_true",
                    help="Disable 32-hex MD5 decoy hashes")
    ap.add_argument("--seed", type=int, default=123456)
    ap.add_argument("--exe-name", default="flag_printer.exe")
    args = ap.parse_args()

    if args.date:
        date = dt.datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        date = dt.date.today()

    random.seed(args.seed)

    # 1. Write C source
    with open("flag_printer.c", "w", encoding="utf-8") as f:
        f.write(C_SOURCE)

    # 2. Compile
    ok, info = compile_binary("flag_printer.c", args.exe_name)
    if not ok:
        with open(args.exe_name, "wb") as f:
            f.write(b"PLACEHOLDER_BINARY_" + FLAG.encode())
        print(f"[!] {info}; using placeholder binary.")
    else:
        print(f"[+] Compiled with {info}: {args.exe_name}")

    # 3. Real SHA256
    real_hash = sha256_file(args.exe_name)
    print(f"[+] Real binary SHA256: {real_hash}")

    # 4. Pick target download path (first path in list for determinism)
    target_download_path = DOWNLOAD_PATHS[0]

    # 5. Generate IIS log
    iis_name = f"IIS_u_ex{date.strftime('%y%m%d')}.log"
    meta = generate_iis_log(
        iis_name,
        date,
        args.server_ip,
        args.top1_ip,
        args.top2_ip,
        target_fail=args.target_fail,
        top1_fail=args.top1_fail,
        top2_fail=args.top2_fail,
        other_fail_range=(args.other_fail_min, args.other_fail_max),
        normal_success_count=args.normal_success_per_wave,
        download_count_other_sha256=args.other_sha256_downloads,
        include_md5_decoys=not args.no_md5_decoys,
        real_sha256=real_hash,
        target_download_path=target_download_path,
        seed=args.seed ^ 0xABCDEF
    )
    print(f"[+] IIS log: {iis_name}")

    # 6. Generate DNS log (virustotal only for target)
    dns_name = f"dnsmasq_{date.strftime('%Y-%m-%d')}.log"
    extra_ips_for_dns = [
        "10.10.5.10","10.10.5.11","10.10.5.12","10.10.5.30",
        "10.10.5.31","10.10.5.40","10.10.5.45","10.10.5.55",
        "10.10.5.60","10.10.6.14","10.10.6.21"
    ]
    generate_dnsmasq(
        dns_name,
        date,
        meta["target_download"],
        args.top1_ip,
        args.top2_ip,
        extra_ips_for_dns,
        seed=args.seed ^ 0x13579
    )
    print(f"[+] DNS log: {dns_name}")

    # 7. README
    write_readme(
        "README.txt",
        date,
        real_hash,
        target_download_path,
        args.top1_ip,
        args.top2_ip,
        meta["target_success"],
        meta["target_download"],
        args.top1_fail,
        args.top2_fail,
        args.target_fail
    )
    print("[+] README.txt written")

    print("\n== SUMMARY ==")
    print(f"Target IP (rank #3 by failures): {TARGET_IP} (failures={args.target_fail})")
    print(f"Top1 IP (no success): {args.top1_ip} (failures={args.top1_fail})")
    print(f"Top2 IP: {args.top2_ip} (failures={args.top2_fail})")
    print(f"Real SHA256 (target download): {real_hash}")
    print("Files generated:", args.exe_name, iis_name, dns_name, "flag_printer.c", "README.txt")
    print("Done. Upload the file / hash to VirusTotal and put the flag there.")
    
if __name__ == "__main__":
    main()
