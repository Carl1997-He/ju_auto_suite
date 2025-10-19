import subprocess, os, pathlib, datetime

ROOT = pathlib.Path(__file__).parent.resolve()
LOG_DIR = ROOT / "feishu_notifier" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOG_DIR / "pytest_run.log"

modules = ["airdrop_api", "jugame_reward_check"]

def run_pytest(module):
    print(f"==> Running pytest in {module}")
    proc = subprocess.run(
        ["pytest", "-q", "--disable-warnings", "-rA", module + "/tests"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=ROOT
    )
    return proc.stdout, proc.returncode

def main():
    with open(log_file, "a", encoding="utf-8") as lf:
        lf.write(f"\n==== PYTEST RUN @ {datetime.datetime.now().isoformat()} ====")
        rc_total = 0
        for m in modules:
            out, rc = run_pytest(m)
            lf.write(f"\n## Module: {m}\n")
            lf.write(out)
            rc_total |= rc
        lf.write("\n==== END RUN ====\n")
    print(f"Logs written to: {log_file}")
    if rc_total != 0:
        print("Some tests failed. Check the log for details.")
    else:
        print("All tests passed.")

if __name__ == "__main__":
    main()
