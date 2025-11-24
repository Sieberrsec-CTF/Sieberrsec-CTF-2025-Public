#!/usr/bin/env python3
import io, tarfile, base64, stat, gzip, time

buf = io.BytesIO()

# write a gzip-compressed tar stream:  mode='w:gz'
with tarfile.open(fileobj=buf, mode='w:gz') as t:
    info        = tarfile.TarInfo('x')      # path inside the sandbox
    info.type   = tarfile.FIFOTYPE          # make it a named pipe
    info.mode   = 0o600                     # permissions (not important)
    info.mtime  = int(time.time())          # keep tar happy
    t.addfile(info)                         # no payload is written

tar_gz_b64 = base64.b64encode(buf.getvalue()).decode()
print(tar_gz_b64)

print(len(tar_gz_b64))

with open('fifo.tar', 'wb') as f:
    f.write(buf.getvalue())