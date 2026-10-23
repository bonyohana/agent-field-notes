pkill -f my-worker.sh
until pgrep -f job >/dev/null; do sleep 5; done
grep -o '.\{0,120\}needle.\{0,120\}' big.txt
sha256sum -c SHA256SUMS
n=$(find /var/lib/x -name '*.tmp' 2>/dev/null | wc -l)
cat >> ledger.md <<EOF
entry for `file.txt` at $H
EOF
