#!/bin/sh
# Fail the job when the jdk15to18 ant build (build1-5to1-8, which does not propagate ant's exit
# status) failed, printing the compiler errors from its log first.
log="$1"
if grep -q 'BUILD FAILED' "$log"; then
  grep -n -E '\[javac\].*(error|warning: \[options\])|OutOfMemory|Exception|BUILD FAILED|xml:[0-9]+' "$log" | head -n 120
  echo "environment:"
  env | grep -i -E 'java|ant|classpath|lang|lc_' | sort
  exit 1
fi
echo "ant build OK"
