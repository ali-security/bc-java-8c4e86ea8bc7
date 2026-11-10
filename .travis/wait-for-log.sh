#!/bin/sh
# Keep the job open until Travis has archived the test-summary line of this job's log,
# so a log fetched right after the job finishes is complete. Runs in after_script, which
# cannot change the build result. Polls every 20 s with a heartbeat line, gives up after
# $1 seconds (Travis jobs are killed at 50 min).
cap="${1:-1200}"
url="https://api.travis-ci.com/v3/job/${TRAVIS_JOB_ID}/log.txt"
marker="SEAL TEST"
marker="$marker TOTAL ("
waited=0
while [ "$waited" -lt "$cap" ]; do
  if curl -fsSL "$url" 2>/dev/null | grep -Fq "$marker"; then
    echo "log archived after ${waited}s"
    exit 0
  fi
  echo "waiting for log archive... (${waited}s)"
  sleep 20
  waited=$((waited + 20))
done
echo "log archive still incomplete after ${waited}s"
exit 0
