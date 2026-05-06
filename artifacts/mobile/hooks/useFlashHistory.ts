import AsyncStorage from "@react-native-async-storage/async-storage";
import { useCallback, useEffect, useState } from "react";

const STORAGE_KEY = "@oussama_sat_flash_history";
const MAX_RECORDS = 50;

export interface FlashRecord {
  id: string;
  fileName: string;
  fileSize?: number;
  timestamp: number;
  status: "success" | "error";
  errorMessage?: string;
  deviceInfo?: string;
  progressReached: number;
}

export function useFlashHistory() {
  const [history, setHistory] = useState<FlashRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const raw = await AsyncStorage.getItem(STORAGE_KEY);
      if (raw) setHistory(JSON.parse(raw) as FlashRecord[]);
    } catch {
      // silently ignore
    } finally {
      setLoading(false);
    }
  };

  const saveHistory = async (records: FlashRecord[]) => {
    try {
      await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(records));
    } catch {
      // silently ignore
    }
  };

  const addRecord = useCallback(
    async (record: Omit<FlashRecord, "id" | "timestamp">) => {
      const newRecord: FlashRecord = {
        ...record,
        id: `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
        timestamp: Date.now(),
      };
      const updated = [newRecord, ...history].slice(0, MAX_RECORDS);
      setHistory(updated);
      await saveHistory(updated);
      return newRecord;
    },
    [history]
  );

  const clearHistory = useCallback(async () => {
    setHistory([]);
    await AsyncStorage.removeItem(STORAGE_KEY);
  }, []);

  return { history, loading, addRecord, clearHistory };
}
