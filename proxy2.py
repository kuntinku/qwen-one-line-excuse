import http.server, json, urllib.request, os
CAP="/root/makefun/qwen-entry/capture-body.json"
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n=int(self.headers.get("content-length",0)); body=self.rfile.read(n)
        if not os.path.exists(CAP) or os.path.getsize(CAP)<100000:
            if n>50000:
                open(CAP,"wb").write(body)
        req=urllib.request.Request("https://openrouter.ai"+self.path, data=body, method="POST")
        for k,v in self.headers.items():
            if k.lower() not in ("host","content-length"): req.add_header(k,v)
        r=urllib.request.urlopen(req, timeout=120); out=r.read()
        self.send_response(r.status)
        for k,v in r.headers.items():
            if k.lower() not in ("transfer-encoding","content-length","content-encoding"): self.send_header(k,v)
        self.send_header("Content-Length",str(len(out))); self.end_headers(); self.wfile.write(out)
    def log_message(self,*a): pass
http.server.HTTPServer(("127.0.0.1",18998),H).serve_forever()
