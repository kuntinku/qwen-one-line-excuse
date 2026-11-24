import http.server, json, urllib.request
LOG=open("/root/makefun/qwen-entry/system-prompt-capture.json","w")
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n=int(self.headers.get("content-length",0)); body=self.rfile.read(n)
        try:
            j=json.loads(body)
            sysm=j.get("system") or [m for m in j.get("messages",[]) if m.get("role")=="system"]
            LOG.write(json.dumps({"path":self.path,"system":sysm},ensure_ascii=False)); LOG.flush()
        except Exception: pass
        req=urllib.request.Request("https://openrouter.ai"+self.path, data=body, method="POST")
        for k,v in self.headers.items():
            if k.lower() not in ("host","content-length"): req.add_header(k,v)
        r=urllib.request.urlopen(req, timeout=120); out=r.read()
        self.send_response(r.status)
        for k,v in r.headers.items():
            if k.lower() not in ("transfer-encoding","content-length","content-encoding"): self.send_header(k,v)
        self.send_header("Content-Length",str(len(out))); self.end_headers(); self.wfile.write(out)
    def log_message(self,*a): pass
http.server.HTTPServer(("127.0.0.1",18999),H).serve_forever()
