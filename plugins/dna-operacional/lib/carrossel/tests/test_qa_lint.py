import subprocess, sys, os, json
HERE = os.path.dirname(__file__)
LINT = os.path.join(HERE, "..", "qa_lint.py")
FIX = os.path.join(HERE, "fixtures")

def run_lint(fixture):
    out = subprocess.run(
        [sys.executable, LINT, os.path.join(FIX, fixture), "--json"],
        capture_output=True, text=True,
    )
    return json.loads(out.stdout)

def test_low_contrast_is_flagged():
    result = run_lint("slide_low_contrast.html")
    codes = [v["code"] for v in result["violations"]]
    assert "CONTRAST_INK_BG" in codes

def test_ok_slide_has_no_violations():
    result = run_lint("slide_ok.html")
    assert result["violations"] == []
