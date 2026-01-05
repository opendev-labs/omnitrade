
import { GoogleGenAI } from "@google/genai";
import { ScannerState, MarketPhase, TrendState } from "../types";

let aiInstance: GoogleGenAI | null = null;

function getAI() {
  if (!aiInstance) {
    const key = process.env.API_KEY || process.env.GEMINI_API_KEY || "";
    if (!key || key === "undefined") {
      throw new Error("API Key missing");
    }
    aiInstance = new GoogleGenAI(key);
  }
  return aiInstance;
}

export async function getMarketAdvice(state: ScannerState): Promise<string> {
  try {
    const prompt = `
      Acting as a Senior Quant Trader, analyze the current market state and provide a 2-sentence tactical advice.
      Market Data:
      - Volatility: ${state.volatility}
      - Trend: ${state.trend}
      - Phase: ${state.phase}
      - Session: ${state.clock} (${state.cycle})
      - Uncertainty Level: ${state.uncertainty}
      
      Respond with specific bot recommendations based on these conditions. Keep it professional and concise.
    `;

    const ai = getAI();
    const model = ai.getGenerativeModel({ model: "gemini-1.5-flash" });
    const result = await model.generateContent(prompt);
    const response = await result.response;
    return response.text() || "Unable to retrieve AI analysis at this time.";
  } catch (error) {
    console.error("Gemini Advice Error:", error);
    return "Connection to AI Logic Engine lost. Monitoring manual telemetry.";
  }
}
