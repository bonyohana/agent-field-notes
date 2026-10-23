#!/bin/sh
# Expect exactly one finding per bad line (FN1,FN1,FN2,FN3,FN5,FN10,FN7) and none on the good file.
set -u
D=$(cd "$(dirname "$0")" && pwd)
bad=$(python3 -I "$D/../fieldcheck.py" "$D/bad/all.sh" | sed -E 's/.*: (FN[0-9]+) .*/\1/' | sort | tr '\n' ' ')
want="FN1 FN1 FN10 FN2 FN3 FN5 FN7 "
[ "$bad" = "$want" ] || { echo "FAIL bad: got [$bad] want [$want]"; python3 -I "$D/../fieldcheck.py" "$D/bad/all.sh"; exit 1; }
python3 -I "$D/../fieldcheck.py" "$D/good/all.sh" || { echo "FAIL good: findings above"; exit 1; }
echo "PASS"
