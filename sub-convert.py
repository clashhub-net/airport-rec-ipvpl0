#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订阅解析与格式转换工具
支持: Clash / V2Ray / Trojan / Shadowsocks 格式互转
"""
import sys, re, base64, json, argparse, urllib.request, ssl

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

def fetch_sub(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ClashForWindows"})
    return urllib.request.urlopen(req, timeout=30, context=CTX).read().decode("utf-8", errors="ignore")

def decode_links(text):
    links = []
    for m in re.finditer(r"https?://[A-Za-z0-9+/=_.-]+", text):
        raw = m.group()
        if raw.count("/") > 2:
            try:
                decoded = base64.b64decode(raw + "==").decode("utf-8", errors="ignore")
                if decoded.startswith(("vmess://","ss://","trojan://","vless://")):
                    links.append(decoded.strip())
                else: links.append(raw)
            except: links.append(raw)
        else: links.append(raw)
    return list(set(links))

def parse_vmess(line):
    try:
        if line.startswith("vmess://"):
            obj = json.loads(base64.b64decode(line[8:] + "==").decode("utf-8"))
            return {"name": obj.get("ps","VMess"), "type": "vmess", "server": obj.get("add"),
                    "port": int(obj.get("port", 443)), "uuid": obj.get("id"), "alterId": int(obj.get("aid", 0))}
    except: pass
    return None

def parse_ss(line):
    try:
        m = re.match(r"ss://([A-Za-z0-9+/=]+)@([^:]+):(\d+)(?:#(.+))?", line)
        if not m: return None
        decoded = base64.b64decode(m.group(1) + "==").decode("utf-8")
        method, password = decoded.split(":", 1)
        return {"name": m.group(4) or f"SS-{m.group(2)}", "type": "ss", "server": m.group(2),
                "port": int(m.group(3)), "cipher": method, "password": password}
    except: return None

def parse_trojan(line):
    try:
        m = re.match(r"trojan://([^@]+)@([^:]+):(\d+)(?:#(.+))?", line)
        if m: return {"name": m.group(4) or f"Trojan-{m.group(2)}", "type": "trojan",
                       "server": m.group(2), "port": int(m.group(3)), "password": m.group(1)}
    except: pass
    return None

def to_clash(nodes):
    lines = ["proxies:"]
    for n in nodes:
        safe = re.sub(r"[^\w\-\[\]]", "_", n.get("name","Node"))
        if n.get("type") == "ss":
            lines += [f'  - name: "{safe}"', f'    type: ss', f'    server: {n["server"]}',
                      f'    port: {n["port"]}', f'    cipher: {n["cipher"]}', f'    password: {n["password"]}']
        elif n.get("type") == "vmess":
            lines += [f'  - name: "{safe}"', f'    type: vmess', f'    server: {n["server"]}',
                      f'    port: {n["port"]}', f'    uuid: {n["uuid"]}', f'    alterId: {n.get("alterId",0)}', f'    cipher: auto']
        elif n.get("type") == "trojan":
            lines += [f'  - name: "{safe}"', f'    type: trojan', f'    server: {n["server"]}',
                      f'    port: {n["port"]}', f'    password: {n["password"]}']
    return "\n".join(lines)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="订阅解析与格式转换")
    p.add_argument("--url", help="订阅链接")
    p.add_argument("--keyword", help="关键词过滤")
    p.add_argument("--format", default="clash", choices=["clash","json"])
    args = p.parse_args()
    if not args.url: p.print_help(); return
    links = decode_links(fetch_sub(args.url))
    nodes = [n for link in links for fn in (parse_vmess, parse_ss, parse_trojan) if (n := fn(link))]
    if args.keyword:
        kw = args.keyword.lower()
        nodes = [n for n in nodes if kw in n.get("name","").lower()]
    print(to_clash(nodes))
