
import { ScannerState, BotConfig, SystemMetrics, ExecutionLog, GovernanceMode } from "../types";

export interface BackendData {
    scanners: ScannerState & { rotation: any[], correlation: any };
    bots: BotConfig[];
    health: number;
    mode: GovernanceMode;
    metrics: SystemMetrics;
    logs: ExecutionLog[];
}

class BackendService {
    private socket: WebSocket | null = null;
    private listeners: ((data: BackendData) => void)[] = [];

    connect(url: string = "ws://localhost:8000/ws") {
        this.socket = new WebSocket(url);

        this.socket.onmessage = (event) => {
            const data: BackendData = JSON.parse(event.data);
            this.listeners.forEach(l => l(data));
        };

        this.socket.onclose = () => {
            console.log("WebSocket disconnected. Retrying in 5s...");
            setTimeout(() => this.connect(url), 5000);
        };
    }

    subscribe(callback: (data: BackendData) => void) {
        this.listeners.push(callback);
        return () => {
            this.listeners = this.listeners.filter(l => l !== callback);
        };
    }
}

export const backendService = new BackendService();
