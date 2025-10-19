import re, pathlib, datetime

def extract_summary(log_path:str)->str:
    p = pathlib.Path(log_path)
    if not p.exists():
        return "No log found."
    txt = p.read_text(encoding="utf-8")
    # crude metrics
    total = len(re.findall(r":: (PASSED|FAILED|ERROR|SKIPPED)", txt))
    passed = len(re.findall(r":: PASSED", txt))
    failed = len(re.findall(r":: FAILED", txt))
    errors = len(re.findall(r":: ERROR", txt))
    return f"Time: {datetime.datetime.now().isoformat()}\nTotal: {total}, Passed: {passed}, Failed: {failed}, Errors: {errors}\nTail:\n" + txt[-800:]
