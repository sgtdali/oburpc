"""Ducray TR sitesinde ürün/seri bağlantılarını keşfeder (tools.py'nin nazik, önbellekli get'ini kullanır)."""
import re, sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "staging"))
import tools  # noqa: E402

BASE = "https://www.ducray.com"


def paths(html):
    html = html.replace("\\u002F", "/").replace("\\/", "/")
    return sorted(set(re.findall(r"/tr-tr/[pf]/[A-Za-z0-9_\-/%.]+", html)))


if __name__ == "__main__":
    out = {}
    for u in sys.argv[1:]:
        r = tools.fs.get(u if u.startswith("http") else BASE + u)
        html = r if isinstance(r, str) else getattr(r, "text", str(r))
        ps = paths(html)
        out[u] = ps
        print(u, len(html), len(ps))
        for p in ps:
            print("  ", p)
