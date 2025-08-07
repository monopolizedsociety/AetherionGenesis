# core/caps.py
import os, json, time, hmac, hashlib, base64

def _secret():
    key = os.getenv("CAPS_SECRET")
    if not key:
        # Ephemeral secret; set CAPS_SECRET in prod
        key = "dev-ephemeral-secret"
    return key.encode()

def mint(scopes, ttl_seconds=300):
    payload = {"scopes": scopes, "exp": int(time.time()) + ttl_seconds}
    body = json.dumps(payload, separators=(",",":"), sort_keys=True).encode()
    sig = hmac.new(_secret(), body, hashlib.sha256).digest()
    tok = base64.urlsafe_b64encode(body).decode().rstrip("=") + "." + base64.urlsafe_b64encode(sig).decode().rstrip("=")
    return tok

def verify(token, required_scope):
    try:
        b64_body, b64_sig = token.split(".")
        body = base64.urlsafe_b64decode(b64_body + "==")
        sig = base64.urlsafe_b64decode(b64_sig + "==")
        if not hmac.compare_digest(sig, hmac.new(_secret(), body, hashlib.sha256).digest()):
            return False, "bad_signature"
        payload = json.loads(body.decode())
        if int(time.time()) > payload.get("exp", 0):
            return False, "expired"
        scopes = payload.get("scopes", [])
        if required_scope not in scopes:
            return False, "scope_denied"
        return True, payload
    except Exception as e:
        return False, "invalid_token"
