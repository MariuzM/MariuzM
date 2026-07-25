import json
import os
import re
import urllib.request

token = os.environ["GH_TOKEN"]

def stars(repo):
    req = urllib.request.Request(
        f"https://api.github.com/repos/MariuzM/{repo}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req) as res:
        return json.load(res)["stargazers_count"]

def fmt(n):
    if n >= 1000:
        return f"{n / 1000:.1f}".rstrip("0").rstrip(".") + "k"
    return str(n)

with open("README.md") as f:
    lines = f.read().splitlines(keepends=True)

out = []
for line in lines:
    m = re.search(r'<a href="https://github\.com/MariuzM/([^"]+)">', line)
    if m:
        line = re.sub(
            r"(</picture>&nbsp;)[^&<]*(&nbsp;)",
            lambda s: s.group(1) + fmt(stars(m.group(1))) + s.group(2),
            line,
        )
    out.append(line)

with open("README.md", "w") as f:
    f.write("".join(out))
