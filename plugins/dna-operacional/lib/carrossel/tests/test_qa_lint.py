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

def test_headline_pequena_flagada():
    # headline < 76px (inline) deve disparar HEADLINE_TOO_SMALL — headline tem que dominar
    import os
    p = os.path.join(FIX, "_tmp_small.html")
    open(p, "w").write(
        '<style>:root{--bg:#16213E;--text:#FFFFFF;--accent:#E94560;}'
        '.slide{background:var(--bg);color:var(--text);}.body{font-size:24px;}</style>'
        '<div class="slide"><div class="headline" style="font-size:50px;">T <span class="em">x</span></div>'
        '<div class="body">y</div>'
        '<div class="screenshot-frame"><img src="x.png"></div></div>')
    result = run_lint("_tmp_small.html")
    os.remove(p)
    assert "HEADLINE_TOO_SMALL" in [v["code"] for v in result["violations"]]

def test_headline_grande_inline_ok():
    # headline 104px (o que o design aprovado usa) NÃO deve disparar (escala rígida foi removida)
    import os
    p = os.path.join(FIX, "_tmp_big.html")
    open(p, "w").write(
        '<style>:root{--bg:#16213E;--text:#FFFFFF;--accent:#E94560;}'
        '.slide{background:var(--bg);color:var(--text);}.body{font-size:24px;}</style>'
        '<div class="slide"><div class="headline" style="font-size:104px;">T <span class="em">x</span></div>'
        '<div class="body">y</div>'
        '<div class="screenshot-frame"><img src="x.png"></div></div>')
    result = run_lint("_tmp_big.html")
    os.remove(p)
    codes = [v["code"] for v in result["violations"]]
    assert "HEADLINE_TOO_SMALL" not in codes and "FONT_OFF_SCALE" not in codes

def test_headline_sem_accent_flagado():
    p = os.path.join(FIX, "_tmp_noacc.html")
    open(p,"w").write('<style>:root{--bg:#16213E;--ink:#FFF;--accent:#E94560;}'
      '.slide{background:var(--bg);color:var(--ink);}.body{font-size:24px;}.headline{font-size:76px;}</style>'
      '<div class="slide"><div class="headline">SEM ACCENT</div><div class="body">x</div>'
      '<div class="screenshot-frame"><img src="x"></div></div>')
    r=run_lint("_tmp_noacc.html"); os.remove(p)
    assert "HEADLINE_NO_ACCENT" in [v["code"] for v in r["violations"]]

def test_headline_com_accent_ok():
    p = os.path.join(FIX, "_tmp_acc.html")
    open(p,"w").write('<style>:root{--bg:#16213E;--ink:#FFF;--accent:#E94560;}'
      '.slide{background:var(--bg);color:var(--ink);}.body{font-size:24px;}.headline{font-size:76px;}</style>'
      '<div class="slide"><div class="headline">COM <span class="em">accent</span></div>'
      '<div class="body">x</div><div class="screenshot-frame"><img src="x"></div></div>')
    r=run_lint("_tmp_acc.html"); os.remove(p)
    assert "HEADLINE_NO_ACCENT" not in [v["code"] for v in r["violations"]]

def test_contraste_le_base_css_linkado():
    """Prova do achado adversarial: qa_lint deve ler o CSS de um <link href=...css>, não só <style>.
    Antes era inerte (HTML real linka base.css externo)."""
    import os, tempfile, shutil
    d = tempfile.mkdtemp()
    try:
        open(os.path.join(d,"bad.css"),"w").write(
            ":root{--bg:#cccccc;--text:#dddddd;--accent:#eeeeee;}")
        open(os.path.join(d,"s.html"),"w").write(
            '<!DOCTYPE html><html><head><link rel="stylesheet" href="bad.css"></head>'
            '<body><div class="slide"><div class="headline" style="font-size:104px;">H <span class="em">x</span></div>'
            '<div class="body">y</div></div></body></html>')
        import subprocess, sys, json as J
        out = subprocess.run([sys.executable, os.path.join(HERE,"..","qa_lint.py"),
                              os.path.join(d,"s.html"), "--json"], capture_output=True, text=True)
        codes = [v["code"] for v in J.loads(out.stdout)["violations"]]
        assert "CONTRAST_INK_BG" in codes, "contraste do base.css linkado não foi lido (lint inerte)"
    finally:
        shutil.rmtree(d)
