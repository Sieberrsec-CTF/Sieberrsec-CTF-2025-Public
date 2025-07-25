Challenge Dataset (v2 – Correlation Ranking Variant)

Files:
  - IIS_u_ex240718.log
  - dnsmasq_2024-07-18.log
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
     Path: /download/finance_q2_export.zip
     Hash: bf99ca8a10434fe036bb28c701dbbdd9d42d2ae03498b4f92d19dc43b8b2df31
  6. Correlate DNS logs: only that IP queries virustotal.com after its download.
  7. Search SHA256 on VirusTotal to recover the flag (not in logs).

Key Hash (real): bf99ca8a10434fe036bb28c701dbbdd9d42d2ae03498b4f92d19dc43b8b2df31

Target success time: 2024-07-18 09:45:46
Target download time: 2024-07-18 09:45:48

Failure counts (approx):
  Top1 IP: 10.10.7.50 -> 450 failures, NO success
  Top2 IP: 10.10.5.50 -> 360 failures (some successes)
  Target IP: 10.10.5.23 -> 250 failures + 1 success + interesting download

The compiled binary prints the flag:
  sctf{we11_d0n3_d0_y0u_l0v3_b1u3_t34m1ng}

Hash Type Clue:
  Only 64-hex (SHA256) matter; 32-hex MD5-style values are optional decoys.

Deliverables (suggested to solver):
  - Ranking of top failing IPs
  - Target success timestamp
  - Download path & SHA256
  - Evidence of virustotal.com lookup
  - Final flag from VT
