
import os, requests
class SportsKeyClient:
    def __init__(self, base_url=None, api_key=None):
        self.base_url=base_url or os.getenv("SPORTSKEY_BASE_URL","")
        self.api_key=api_key or os.getenv("SPORTSKEY_API_KEY","")
        if not self.base_url: raise RuntimeError("SPORTSKEY_BASE_URL not set")
        if not self.api_key: raise RuntimeError("SPORTSKEY_API_KEY not set")
    def _h(self): return {"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"}
    def get_availability(self, resource_id, date_from, date_to):
        r=requests.get(f"{self.base_url}/availability",headers=self._h(),
                       params={"resource_id":resource_id,"date_from":date_from,"date_to":date_to},timeout=20)
        r.raise_for_status(); return r.json()
