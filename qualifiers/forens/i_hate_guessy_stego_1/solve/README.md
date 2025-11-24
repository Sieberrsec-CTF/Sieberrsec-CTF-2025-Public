# i hate guessy stego 1 &mdash; Author's Writeup

## Solution

Whenever you run `binwalk` (the old Python-based version, anyway &mdash; the new Rust-based version seems to work differently) on a PNG, you'll see "Zlib compressed data" (unless the PNG isn't compressed). 99.99% of the time, it's a red herring. This time, though, I've decided to basically use the PNG as a compressed archive. Or something. You're welcome.

See `solve.py` for a solution script.

Honestly though, `binwalk` (the one on Aperi'Solve) suffices for this one.