import re

with open('/home/maxdemarzi/.gemini/antigravity-ide/brain/87dc59a4-91a0-495a-aef7-d347d8ddfcd2/.system_generated/steps/903/content.md', 'r') as f:
    html = f.read()

# Let's find script tags
script_tags = re.findall(r'<script[^>]*src="([^"]+)"', html)
print("Scripts found:", script_tags)

# Find all links
links = re.findall(r'<a[^>]*href="([^"]+)"', html)
print("Links found:", links)
