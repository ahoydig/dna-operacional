import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import templates

def test_accent():
    assert '<span class="em">Hormozi</span>' in templates.accent("Clone o {Hormozi}")
    assert templates.accent("sem") == "sem"

def test_asset_prefixa_dotdot():
    assert templates.asset("assets/x.png") == "../assets/x.png"
    assert templates.asset("../assets/x.png") == "../assets/x.png"
    assert templates.asset("http://a/x.png") == "http://a/x.png"

def test_footer_swipe():
    assert "swipe" in templates.footer("@x", True)
    assert "swipe" not in templates.footer("@x", False)
    assert "@x" in templates.footer("@x")

def test_content_tem_tudo():
    s={"tipo":"content","kicker":"Passo 1","headline":"Crie um {projeto}","sub":"x","hero":"assets/t.png"}
    o=templates.slide(s,2,7,{"handle":"@f"})
    assert "Passo 1" in o and '<span class="em">projeto</span>' in o
    assert "../assets/t.png" in o and "02 / 07" in o and "@f" in o

def test_cover_compo_e_bg():
    s={"tipo":"cover","kicker":"K","headline":"H {a}","sub":"s {b}",
       "compo":{"left":"assets/p.png","right_icon":"assets/i.png","right_label":"Claude"}}
    o=templates.slide(s,1,7,{"handle":"@f","bg_photo":"assets/bg.png","icon_top":"assets/i.png"})
    assert "../assets/bg.png" in o and "bgphoto" in o
    assert "../assets/p.png" in o and "Claude" in o

def test_cta_token_sem_swipe():
    s={"tipo":"cta","headline_top":"Quer?","token":"HORMOZI","sub":"m {x}"}
    o=templates.slide(s,7,7,{"handle":"@f"})
    assert "HORMOZI" in o and "cta-stack" in o and "swipe" not in o

def test_quote():
    s={"tipo":"quote","kicker":"K","headline":"H {x}","quote":"frase","sub":"s"}
    o=templates.slide(s,6,7,{"handle":"@f"})
    assert "frase" in o and "quote" in o
