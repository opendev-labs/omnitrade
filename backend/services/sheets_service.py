import os
import json
import logging

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    GOOGLE_LIBS_AVAILABLE = True
except ImportError:
    GOOGLE_LIBS_AVAILABLE = False
    print("Warning: Google API libraries not found. Running in MOCK mode.")

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

class SheetsService:
    def __init__(self, service_account_file='service_account.json'):
        self.service = None
        self.mock_mode = True
        
        if GOOGLE_LIBS_AVAILABLE:
            if os.path.exists(service_account_file):
                try:
                    creds = Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
                    self.service = build('sheets', 'v4', credentials=creds)
                    self.mock_mode = False
                    logger.info("Connected to Google Sheets API")
                except Exception as e:
                    logger.error(f"Failed to connect to Google Sheets: {e}")
            else:
                logger.warning(f"Service account file '{service_account_file}' not found. Using MOCK mode.")
        else:
            logger.warning("Google libraries missing. Using MOCK mode.")

    def get_market_data(self, spreadsheet_id, range_name):
        if self.mock_mode:
            return self._get_mock_data(range_name)

        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            values = result.get('values', [])
            return values
        except Exception as e:
            logger.error(f"Error reading sheet: {e}")
            return self._get_mock_data(range_name)

    def _get_mock_data(self, range_name):
        # Return simulated data structure matching the expected Sheet columns
        if "MARKET_STATE" in range_name:
            return [
                ["Token", "TF", "ATR %", "BB Width", "Volatility", "Trend", "Phase", "Session", "BTC.D Bias", "Uncertainty"],
                ["BTC", "15m", "1.2", "0.05", "LOW", "UP", "ACCUMULATION", "LONDON", "NEUTRAL", "LOW"],
                ["ETH", "15m", "1.5", "0.06", "LOW", "UP", "EXPANSION", "LONDON", "BULLISH", "LOW"],
                ["SOL", "15m", "2.1", "0.08", "HIGH", "NEUTRAL", "DISTRIBUTION", "LONDON", "BEARISH", "MEDIUM"]
            ]
        elif "HEALTH_SCORE" in range_name:
            # Maybe reading a specific cell for score?
            return [["Health", "DD", "Losses", "Stress", "Uncertainty"], ["98", "0.4", "0", "0.1", "LOW"]]
        elif "CORRELATION" in range_name:
             return [["Token", "Corr"], ["ETH", "0.85"], ["SOL", "0.65"]]
        elif "BOT_PERMISSION" in range_name:
            return [
                ["Bot", "Allowed"],
                ["VWAP", "TRUE"],
                ["Breakout", "TRUE"],
                ["Trend PB", "TRUE"],
                ["Range", "FALSE"]
            ]
        return []

sheets_service = SheetsService()
