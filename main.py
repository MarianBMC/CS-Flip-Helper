import time
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import requests

load_dotenv() 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanSettings(BaseModel):
    items: List[str]
    min_roi: float
    min_profit: float

def scan_target_items(settings: ScanSettings):
    api_key = os.getenv("CSFLOAT_API_KEY")  
    url = "https://csfloat.com/api/v1/listings"
    
    headers = {"Authorization": api_key}
    deals = []
    
    if not api_key:
        print("ERROR: CSFLOAT_API_KEY not found in .env file")
        return
    print("\n--- NEW SCAN INITIATED ---")

    for raw_name in settings.items:
        name = raw_name.strip()
        if not name:
            continue

        print(f"Checking item: '{name}'")

        params = {
            "market_hash_name": name,
            "limit": 1,
            "sort_by": "lowest_price",
            "type": "buy_now"
        }

        response = requests.get(url, params=params, headers=headers)
        print(f"API Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                listing = data[0]
                buy_price = listing["price"] / 100
                market_price = listing.get("reference", {}).get("base_price", 0) / 100
                
                print(f"Found listing: Buy=${buy_price:.2f} | Ref=${market_price:.2f}")

                if market_price == 0:
                    print("-> Skipped: No reference market price available.")
                    continue

                csfloat_fee = 0.02
                net_revenue = market_price * (1 - csfloat_fee)
                profit = net_revenue - buy_price
                margin = (profit / buy_price) * 100 if buy_price > 0 else 0

                print(f"-> Math: Net Profit=${profit:.2f}, Margin={margin:.1f}%")

                if margin >= settings.min_roi or profit >= settings.min_profit:
                    print("-> ✅ DEAL ACCEPTED! Sending to website.")
                    deals.append({
                        "item": name,
                        "buy_price": round(buy_price, 2),
                        "market_value": round(market_price, 2),
                        "profit": round(profit, 2),
                        "roi": round(margin, 1)
                    })
                else:
                    print("-> ❌ DEAL REJECTED: ROI or Profit too low based on your settings.")
            else:
                print("-> Skipped: No listings found for this exact item name on CSFloat.")
        else:
            print(f"-> API Error Response: {response.text}")
            
        time.sleep(1) # Pause for 1 second so CSFloat block 

    print("--- SCAN COMPLETE ---\n")
    return deals

@app.post("/api/deals")
def get_deals(settings: ScanSettings):
    results = scan_target_items(settings)
    return {"status": "success", "deals": results}