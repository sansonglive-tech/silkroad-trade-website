#!/usr/bin/env python3
import subprocess
import os

git_exe = r"E:\腾讯龙虾\QClaw\v0.2.29.592\resources\git\cmd\git.exe"
work = r"C:\Users\ASDCF\.qclaw\workspace"

print("Testing git connection...")
result = subprocess.run(
    [git_exe, "ls-remote", "origin", "HEAD"],
    cwd=work,
    capture_output=True,
    text=True,
    timeout=15
)
print(f"Return code: {result.returncode}")
if result.stdout:
    print(f"Stdout: {result.stdout[:200]}")
if result.stderr:
    print(f"Stderr: {result.stderr[:200]}")
