#!/usr/bin/env python3
"""Biblioteca de templates de slide — clona a geometria do MANIFESTO.
Eixo de coluna via base.css --pad-x. Headline Nofex + 1 palavra serif itálico accent.
Crankdat só no handle/swipe. 4 tipos: cover, content, quote, cta."""
import re, html

def accent(text):
    return re.sub(r"\{([^}]+)\}", lambda m: '<span class="em">%s</span>' % m.group(1), text)

def asset(path):
    """Resolve caminho de asset relativo ao HTML (que vive em slides/). 'assets/x.png' -> '../assets/x.png'.
    Caminhos já absolutos, com ../, ou http ficam intactos."""
    if not path: return path
    if path.startswith(("../", "/", "http")): return path
    return "../" + path

def footer(handle, swipe=True):
    s = '<div class="footer"><span class="handle">%s</span></div>' % html.escape(handle)
    if swipe:
        s += '<div class="swipe">arrasta &rarr;</div>'
    return s

def _num(idx, total):
    return '<div class="snum">%02d / %02d</div>' % (idx, total)

def slide(s, idx, total, meta):
    t = s["tipo"]
    if t == "cover":   return _cover(s, idx, total, meta)
    if t == "content": return _content(s, idx, total, meta)
    if t == "quote":   return _quote(s, idx, total, meta)
    if t == "cta":     return _cta(s, idx, total, meta)
    raise ValueError("tipo desconhecido: %s" % t)

def _bg(d):
    p = d.get("bg_photo")
    return ('<img class="bgphoto" src="%s"><div class="scrim"></div>' % asset(p)) if p else ""

def _content(s, idx, total, meta):
    hsize = s.get("hsize", 104)
    hero = '<div class="hero"><img class="shot" src="%s"></div>' % asset(s["hero"]) if s.get("hero") else ""
    return f"""
<div class="slide">
  <div class="ghost">{idx-1:02d}</div>
  {_num(idx,total)}
  <div style="margin-top:30px">
    <div class="kicker">{s.get('kicker','')}</div>
    <div class="headline" style="font-size:{hsize}px;">{accent(s['headline'])}</div>
    <div class="sub">{accent(s.get('sub',''))}</div>
  </div>
  <div class="spacer"></div>
  {hero}
  <div class="spacer"></div>
  {footer(meta['handle'], swipe=True)}
</div>"""

def _cover(s, idx, total, meta):
    compo = ""
    c = s.get("compo")
    if c:
        left2 = ('<img src="%s" style="position:absolute;bottom:-6px;left:-160px;width:360px;'
                 'filter:drop-shadow(0 14px 26px rgba(0,0,0,0.6));">' % asset(c["left2"])) if c.get("left2") else ""
        compo = f"""<div style="position:absolute;bottom:118px;left:0;right:0;z-index:2;display:flex;align-items:flex-end;justify-content:center;gap:30px;">
  <div style="position:relative;display:flex;align-items:flex-end;">
    <img src="{asset(c['left'])}" style="height:540px;filter:drop-shadow(0 16px 30px rgba(0,0,0,0.65));">{left2}
  </div>
  <div style="font-family:'Nofex',sans-serif;font-size:84px;color:#fff;margin-bottom:230px;filter:drop-shadow(0 4px 10px rgba(0,0,0,0.6));">&rarr;</div>
  <div style="margin-bottom:120px;display:flex;flex-direction:column;align-items:center;gap:16px;">
    <div style="width:300px;height:300px;border-radius:64px;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 20px 48px rgba(0,0,0,0.55);">
      <img src="{asset(c['right_icon'])}" style="width:210px;height:210px;"></div>
    <div style="font-family:'Inter';font-weight:700;font-size:48px;color:#fff;">{c.get('right_label','')}</div>
  </div></div>"""
    icon_top = '<img src="%s" style="width:84px;height:84px;margin:8px 0 14px;z-index:1;display:block;">' % asset(meta["icon_top"]) if meta.get("icon_top") else ""
    return f"""
<div class="slide" style="justify-content:flex-start;text-align:left;align-items:flex-start;">
  {_bg(meta)}
  <div class="snum" style="color:#cfc7bf">{idx:02d} / {total:02d}</div>
  {icon_top}
  <div class="kicker" style="margin:0 0 14px;">{s.get('kicker','')}</div>
  <div class="headline" style="font-size:{s.get('hsize',104)}px;text-align:left;">{accent(s['headline'])}</div>
  <div class="sub" style="margin:22px 0 0;max-width:26ch;text-align:left;color:#e8e0d6;">{accent(s.get('sub',''))}</div>
  {compo}
  {footer(meta['handle'], swipe=True)}
</div>"""

def _quote(s, idx, total, meta):
    return f"""
<div class="slide">
  {_num(idx,total)}
  <div style="margin-top:40px">
    <div class="kicker">{s.get('kicker','')}</div>
    <div class="headline" style="font-size:{s.get('hsize',96)}px;">{accent(s['headline'])}</div>
  </div>
  <div class="spacer"></div>
  <div class="quote">"{s['quote']}"</div>
  <div class="spacer"></div>
  <div class="sub" style="max-width:34ch;">{accent(s.get('sub',''))}</div>
  <div class="spacer"></div>
  {footer(meta['handle'], swipe=True)}
</div>"""

def _cta(s, idx, total, meta):
    icon = '<img src="%s" style="width:104px;height:104px;margin:0 auto 16px;z-index:1;display:block;">' % asset(meta["icon_top"]) if meta.get("icon_top") else ""
    bgsrc = s if s.get("bg_photo") else meta
    return f"""
<div class="slide center" style="justify-content:center;text-align:center;">
  {_bg(bgsrc)}
  <div class="snum" style="color:#cfc7bf">{idx:02d} / {total:02d}</div>
  {icon}
  <div class="cta-stack" style="text-align:center;">
    <div class="big" style="font-size:64px;color:#e8e0d6;">{s.get('headline_top','')}</div>
    <div class="big" style="font-size:120px;margin-top:8px;">Comenta</div>
    <div class="big tok" style="font-size:120px;">"{s['token']}"</div>
  </div>
  <div class="sub" style="margin:28px auto 0;max-width:30ch;text-align:center;color:#e8e0d6;">{accent(s.get('sub',''))}</div>
  <div style="font-family:'Crankdat',sans-serif;font-weight:700;font-size:48px;color:var(--accent);margin-top:20px;z-index:1;">&darr; comenta aqui embaixo</div>
  {footer(meta['handle'], swipe=False)}
</div>"""
