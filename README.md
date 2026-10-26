# CS-Flip-Helper

I have been heavily involved in CS2 trading and market arbitrage for a while now, manually flipping everything from operation cases to knives and gloves. Since I am studying Informatică Economică, I wanted to combine my background in market economics with my programming coursework to automate my trading strategies. 

This project is the result: a lightweight, single-page web app built to replace manual market scanning. It connects to a local Python FastAPI backend to hunt for profitable flips on CSFloat, doing all the strict math and data validation in the background so I only see actual, actionable deals.

## What it does
* **Calculates True Net Profit:** Automatically deducts the 2% CSFloat seller fee so you only see your real take-home profit.
* **Strict Filtering:** Uses Pydantic to validate inputs and instantly rejects items that don't hit your target ROI (%) or flat profit margins.
* **Clean UI:** A straightforward dark-mode dashboard written in vanilla HTML/JS that updates instantly without page reloads.

## Tech Stack
* **Backend:** Python, FastAPI, Uvicorn, Requests, Pydantic
* **Frontend:** HTML, CSS, Vanilla JavaScript (Fetch API)

## How to run it locally
1. Clone this repository to your machine.
2. Install the required Python libraries: `pip install -r requirements.txt`
3. Create a `.env` file in the root folder and add your API key: `CSFLOAT_API_KEY=your_key_here`
4. Start the backend server: `python -m uvicorn main:app --reload`
5. Double-click `index.html` to open the dashboard in your browser.

## How to get a CSFloat API Key
1. Log in to [CSFloat.com](https://csfloat.com) using your Steam account.
2. Click on your profile picture in the top right and select **Settings**.
3. Scroll down to the **Developer** section.
4. Click **Generate API Key** and copy the resulting string. Keep this secure and never share it publicly.