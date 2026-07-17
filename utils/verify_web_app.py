import os
import sys
import time
import json
import urllib.request
import threading
from http.server import HTTPServer

# Ensure rogue directory is in the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from web_server import NexusHTTPHandler

TEST_PORT = 8085

def audit_html_tags():
    print("Auditing HTML5 tag structure and interactive selector IDs...")
    html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../web_app/index.html"))
    
    if not os.path.exists(html_path):
        print(f"  --> FAILED: index.html not found at {html_path}")
        return False
        
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    required_ids = [
        'chatLog', 'micBtn', 'promptInput', 'sendBtn',
        'evSlider', 'debtSlider', 'compsBody', 'cy',
        'koyfinChart', 'rrSlider', 'cdsChart', 'citationCard'
    ]
    
    for rid in required_ids:
        tag_pattern = f'id="{rid}"'
        if tag_pattern not in content:
            print(f"  --> FAILED: Interactive ID selector '{rid}' is missing in index.html")
            return False
            
    print("  --> SUCCESS: All required interactive selectors are present and valid.")
    return True

def test_http_endpoints():
    print("\nTesting HTTP endpoints delivery and JSON API contract...")
    
    # 1. Start server in a background thread
    server = HTTPServer(('127.0.0.1', TEST_PORT), NexusHTTPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Allow server a brief moment to bind port
    time.sleep(1.0)
    
    try:
        # 2. Test GET index.html
        url_index = f"http://127.0.0.1:{TEST_PORT}/"
        res_index = urllib.request.urlopen(url_index)
        assert res_index.status == 200, "Index page failed delivery"
        html_body = res_index.read().decode('utf-8')
        assert "Rogo Nexus Analyst Terminal" in html_body, "Index HTML lacks title element"
        print("  --> GET / (index.html): SUCCESS")

        # 3. Test GET styles.css
        url_css = f"http://127.0.0.1:{TEST_PORT}/styles.css"
        res_css = urllib.request.urlopen(url_css)
        assert res_css.status == 200, "CSS styles failed delivery"
        print("  --> GET /styles.css: SUCCESS")

        # 4. Test GET app.js
        url_js = f"http://127.0.0.1:{TEST_PORT}/app.js"
        res_js = urllib.request.urlopen(url_js)
        assert res_js.status == 200, "JS application failed delivery"
        print("  --> GET /app.js: SUCCESS")

        # 5. Test POST /api/chat
        url_chat = f"http://127.0.0.1:{TEST_PORT}/api/chat"
        req_data = json.dumps({"message": "Compare actual earnings consensus surprise for AIR"}).encode('utf-8')
        
        req = urllib.request.Request(
            url_chat,
            data=req_data,
            headers={'Content-Type': 'application/json'}
        )
        
        res_chat = urllib.request.urlopen(req)
        assert res_chat.status == 200, "API chat endpoint failed"
        
        chat_body = json.loads(res_chat.read().decode('utf-8'))
        assert chat_body["success"] is True, "API returned success: False"
        assert "playbook_id" in chat_body, "API payload missing playbook_id"
        assert "broker" in chat_body, "API payload missing broker"
        assert "answer_text" in chat_body, "API payload missing answer_text"
        assert "citations" in chat_body, "API payload missing citations"
        
        # Verify citation structure has expected audit parameters
        for cit in chat_body["citations"]:
            assert "citation_id" in cit, "Citation missing ID reference"
            assert "sql_locator" in cit, "Citation missing SQL audit trail reference"
            
        print("  --> POST /api/chat: SUCCESS")
        server_ok = True
        
    except Exception as e:
        print(f"  --> FAILED: Server check encountered error: {e}")
        server_ok = False
        
    finally:
        # Stop the server cleanly
        server.shutdown()
        server.server_close()
        
    return server_ok

def main():
    print("=" * 60)
    print("         NEXUS FRONTEND & HTTP SERVER VERIFICATION")
    print("=" * 60)
    
    html_ok = audit_html_tags()
    server_ok = test_http_endpoints()
    
    print("\n" + "=" * 60)
    if html_ok and server_ok:
        print("       ALL WEB APPLICATION CHECKS VERIFIED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("       VERIFICATION COMPLETED WITH ERRORS.")
        sys.exit(1)

if __name__ == "__main__":
    main()
