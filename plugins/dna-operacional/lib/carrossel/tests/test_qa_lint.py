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

def test_tiny_body_is_flagged():
    result = run_lint("slide_tiny_body.html")
    codes = [v["code"] for v in result["violations"]]
    assert "BODY_TOO_SMALL" in codes

def test_contain_bg_is_flagged():
    result = run_lint("slide_contain_bg.html")
    codes = [v["code"] for v in result["violations"]]
    assert "OBJECTFIT_CONTAIN_BG" in codes

def test_offscale_font_is_flagged():
    # font-size fora da escala modular (ex: 50px) deve ser pego
    import os
    p = os.path.join(FIX, "_tmp_offscale.html")
    open(p, "w").write(
        '<style>:root{--bg:#16213E;--ink:#FFFFFF;--accent:#E94560;}'
        '.slide{background:var(--bg);color:var(--ink);}'
        '.headline{font-size:50px;}.body{font-size:24px;}</style>'
        '<div class="slide"><div class="headline">T</div>'
        '<div class="body">x</div>'
        '<div class="screenshot-frame"><img src="x.png"></div></div>')
    result = run_lint("_tmp_offscale.html")
    os.remove(p)
    codes = [v["code"] for v in result["violations"]]
    assert "FONT_OFF_SCALE" in codes
