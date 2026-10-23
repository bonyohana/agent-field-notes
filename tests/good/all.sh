kill "$(cat worker.pid)"
START=$(date +%s)
until [ -e done ] || [ $(( $(date +%s) - START )) -gt 130 ]; do sleep 3; done
grep -o 'needle.\{0,40\}' big.txt
sha256sum -c SHA256SUMS || exit 1
n=$(sudo find /var/lib/x -name '*.tmp' | wc -l)
cat >> ledger.md <<'EOF'
entry for `file.txt`
EOF
tr a b <<<"word"
# pkill -f in a comment is fine
pgrep -u svc -f "[.]venv/bin/app" >/dev/null
i=0
until ready; do i=$((i+1)); [ "$i" -lt 10 ] || exit 1; sleep 2; done
cat > doc.md <<EOF
literal \`code\` stays text
EOF
pgrep -u otheruser -f worker >/dev/null
