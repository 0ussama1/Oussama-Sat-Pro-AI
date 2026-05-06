import React, { useCallback, useEffect, useRef, useState } from "react";
import {
  Alert,
  Animated,
  Easing,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Feather, MaterialCommunityIcons } from "@expo/vector-icons";
import * as DocumentPicker from "expo-document-picker";
import * as Haptics from "expo-haptics";
import { useColors } from "@/hooks/useColors";
import { useFlashHistory } from "@/hooks/useFlashHistory";
import { FlashHistoryList } from "@/components/FlashHistoryList";

declare global {
  interface Navigator {
    serial?: {
      requestPort: (options?: Record<string, unknown>) => Promise<SerialPortInstance>;
      getPorts: () => Promise<SerialPortInstance[]>;
      addEventListener: (event: string, handler: EventListener) => void;
    };
  }
}

interface SerialPortInstance {
  open: (options: { baudRate: number }) => Promise<void>;
  close: () => Promise<void>;
  readable: ReadableStream | null;
  writable: WritableStream | null;
  getInfo: () => { usbVendorId?: number; usbProductId?: number };
}

interface SelectedFile {
  name: string;
  uri: string;
  size?: number;
}

type ConnectionStatus = "scanning" | "connected" | "disconnected";
type FlashStatus = "idle" | "flashing" | "success" | "error";

const CHUNK_SIZE = 1024;
const BAUD_RATE = 115200;

const supportsWebSerial =
  Platform.OS === "web" &&
  typeof navigator !== "undefined" &&
  "serial" in navigator;

export default function HomeScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const { history, loading: historyLoading, addRecord, clearHistory } = useFlashHistory();

  const [selectedFile, setSelectedFile] = useState<SelectedFile | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>("scanning");
  const [portRef, setPortRef] = useState<SerialPortInstance | null>(null);
  const [flashProgress, setFlashProgress] = useState(0);
  const [flashStatus, setFlashStatus] = useState<FlashStatus>("idle");
  const [statusText, setStatusText] = useState("IA: Searching for receiver...");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const ledOpacity = useRef(new Animated.Value(1)).current;
  const pulsationAnim = useRef<Animated.CompositeAnimation | null>(null);
  const progressAnim = useRef(new Animated.Value(0)).current;
  const buttonScale = useRef(new Animated.Value(1)).current;

  const isReady = selectedFile !== null && connectionStatus === "connected" && flashStatus !== "flashing";

  useEffect(() => {
    if (connectionStatus === "connected") {
      pulsationAnim.current?.stop();
      pulsationAnim.current = Animated.loop(
        Animated.sequence([
          Animated.timing(ledOpacity, { toValue: 0.2, duration: 600, useNativeDriver: true, easing: Easing.ease }),
          Animated.timing(ledOpacity, { toValue: 1, duration: 600, useNativeDriver: true, easing: Easing.ease }),
        ])
      );
      pulsationAnim.current.start();
    } else {
      pulsationAnim.current?.stop();
      ledOpacity.setValue(1);
    }
    return () => pulsationAnim.current?.stop();
  }, [connectionStatus, ledOpacity]);

  useEffect(() => {
    Animated.timing(progressAnim, {
      toValue: flashProgress,
      duration: 200,
      useNativeDriver: false,
    }).start();
  }, [flashProgress, progressAnim]);

  const pickFile = useCallback(async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: "*/*",
        copyToCacheDirectory: true,
      });
      if (result.canceled) return;
      const asset = result.assets[0];
      if (!asset.name.endsWith(".bin")) {
        Alert.alert("Invalid File", "Please select a .bin firmware file.");
        return;
      }
      setSelectedFile({ name: asset.name, uri: asset.uri, size: asset.size });
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    } catch {
      Alert.alert("Error", "Could not open file picker.");
    }
  }, []);

  const connectDevice = useCallback(async () => {
    if (!supportsWebSerial) {
      Alert.alert(
        "USB Serial",
        "USB OTG flashing is supported on Chrome (desktop/Android) via WebSerial. On Expo Go (native), this feature requires a custom build with native serial libraries.",
        [{ text: "OK" }]
      );
      return;
    }
    try {
      const port = await navigator.serial!.requestPort();
      await port.open({ baudRate: BAUD_RATE });
      setPortRef(port);
      setConnectionStatus("connected");
      setStatusText("IA: Receiver connected");
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Connection failed";
      if (!msg.includes("No port selected")) {
        setStatusText("IA: Connection failed");
        setErrorMsg(msg);
      }
    }
  }, []);

  const disconnectDevice = useCallback(async () => {
    try {
      await portRef?.close();
    } catch {
      // ignore
    }
    setPortRef(null);
    setConnectionStatus("scanning");
    setStatusText("IA: Searching for receiver...");
    setFlashStatus("idle");
    setFlashProgress(0);
  }, [portRef]);

  const startFlash = useCallback(async () => {
    if (!isReady) return;
    setFlashStatus("flashing");
    setFlashProgress(0);
    setErrorMsg(null);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);

    try {
      if (!supportsWebSerial || !portRef?.writable) {
        // Simulate for non-web platforms
        for (let progress = 0; progress <= 100; progress += 2) {
          await new Promise<void>((resolve) => setTimeout(resolve, 60));
          setFlashProgress(progress);
          setStatusText(`Transferring: ${progress}%`);
        }
      } else {
        const response = await fetch(selectedFile!.uri);
        const buffer = await response.arrayBuffer();
        const data = new Uint8Array(buffer);
        const writer = portRef.writable.getWriter();
        const total = data.length;

        for (let i = 0; i < total; i += CHUNK_SIZE) {
          const chunk = data.slice(i, i + CHUNK_SIZE);
          await writer.write(chunk);
          const progress = Math.round(((i + chunk.length) / total) * 100);
          setFlashProgress(progress);
          setStatusText(`Transferring: ${progress}%`);
        }
        writer.releaseLock();
      }

      setFlashStatus("success");
      setFlashProgress(100);
      setStatusText("IA: Update complete ✓");
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      await addRecord({
        fileName: selectedFile!.name,
        fileSize: selectedFile!.size,
        status: "success",
        progressReached: 100,
        deviceInfo: portRef ? `USB @ ${BAUD_RATE} baud` : "Simulated",
      });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Flash failed";
      setFlashStatus("error");
      setErrorMsg(msg);
      setStatusText("IA: Flash error");
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
      await addRecord({
        fileName: selectedFile!.name,
        fileSize: selectedFile!.size,
        status: "error",
        errorMessage: msg,
        progressReached: flashProgress,
        deviceInfo: portRef ? `USB @ ${BAUD_RATE} baud` : "Simulated",
      });
    }
  }, [isReady, portRef, selectedFile, addRecord, flashProgress]);

  const resetFlash = useCallback(() => {
    setFlashStatus("idle");
    setFlashProgress(0);
    setStatusText("IA: Receiver connected");
  }, []);

  const onFlashPress = useCallback(async () => {
    if (flashStatus === "success" || flashStatus === "error") {
      resetFlash();
      return;
    }
    await startFlash();
  }, [flashStatus, resetFlash, startFlash]);

  const animateButton = useCallback(() => {
    Animated.sequence([
      Animated.timing(buttonScale, { toValue: 0.96, duration: 80, useNativeDriver: true }),
      Animated.timing(buttonScale, { toValue: 1, duration: 80, useNativeDriver: true }),
    ]).start();
  }, [buttonScale]);

  const ledColor =
    connectionStatus === "connected"
      ? "#00FF99"
      : connectionStatus === "scanning"
      ? "#555555"
      : "#FF4444";

  const progressWidth = progressAnim.interpolate({
    inputRange: [0, 100],
    outputRange: ["0%", "100%"],
  });

  const progressBarColor =
    flashStatus === "success"
      ? "#00CC66"
      : flashStatus === "error"
      ? "#CC2200"
      : "#00CC66";

  const flashButtonLabel =
    flashStatus === "flashing"
      ? "FLASHING..."
      : flashStatus === "success"
      ? "FLASH AGAIN"
      : flashStatus === "error"
      ? "RETRY"
      : "LAUNCH UPDATE";

  const flashButtonBg = isReady
    ? flashStatus === "error"
      ? "#CC2200"
      : "#005533"
    : "#1E1E1E";

  const topPad = Math.max(insets.top, Platform.OS === "web" ? 67 : 0);
  const bottomPad = Math.max(insets.bottom, Platform.OS === "web" ? 34 : 0);

  return (
    <View style={[styles.root, { backgroundColor: colors.background }]}>
      <ScrollView
        style={{ flex: 1 }}
        contentContainerStyle={[
          styles.scroll,
          { paddingTop: topPad + 20, paddingBottom: bottomPad + 20 },
        ]}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <MaterialCommunityIcons name="satellite-uplink" size={28} color={colors.primary} />
          <Text style={[styles.appTitle, { color: colors.primary }]}>OUSSAMA SAT PRO AI</Text>
        </View>

        <Text style={[styles.subtitle, { color: colors.mutedForeground }]}>
          Satellite Receiver Firmware Flasher
        </Text>

        {/* File Card */}
        <View style={[styles.card, { backgroundColor: colors.card, borderColor: colors.border }]}>
          <Text style={[styles.cardLabel, { color: colors.mutedForeground }]}>
            TARGET FIRMWARE (.bin)
          </Text>
          <Text
            style={[
              styles.fileName,
              { color: selectedFile ? colors.foreground : colors.mutedForeground },
            ]}
            numberOfLines={1}
            ellipsizeMode="middle"
          >
            {selectedFile ? selectedFile.name : "No file selected"}
          </Text>
          {selectedFile?.size !== undefined && (
            <Text style={[styles.fileSize, { color: colors.mutedForeground }]}>
              {(selectedFile.size / 1024).toFixed(1)} KB
            </Text>
          )}
        </View>

        {/* File Picker Button */}
        <Pressable
          onPress={pickFile}
          disabled={flashStatus === "flashing"}
          style={({ pressed }) => [
            styles.selectButton,
            { backgroundColor: colors.accent, opacity: pressed ? 0.85 : 1 },
          ]}
        >
          <Feather name="folder" size={18} color="#fff" />
          <Text style={styles.selectButtonText}>1. SELECT FIRMWARE FILE</Text>
        </Pressable>

        {/* Status Card */}
        <View style={[styles.statusCard, { backgroundColor: colors.card, borderColor: colors.border }]}>
          {/* LED + Status */}
          <View style={styles.statusRow}>
            <Animated.View style={{ opacity: ledOpacity }}>
              <View style={[styles.led, { backgroundColor: ledColor, shadowColor: ledColor }]} />
            </Animated.View>
            <Text style={[styles.statusText, { color: colors.foreground }]}>{statusText}</Text>
          </View>

          {/* Progress Bar */}
          <View style={[styles.progressTrack, { backgroundColor: colors.secondary }]}>
            <Animated.View
              style={[
                styles.progressFill,
                { backgroundColor: progressBarColor, width: progressWidth },
              ]}
            />
          </View>
          {flashProgress > 0 && (
            <Text style={[styles.progressPct, { color: colors.mutedForeground }]}>
              {flashProgress}%
            </Text>
          )}

          {/* Error */}
          {errorMsg && (
            <Text style={[styles.errorText, { color: colors.destructive }]} numberOfLines={2}>
              {errorMsg}
            </Text>
          )}
        </View>

        {/* Connect / Disconnect Button */}
        {connectionStatus !== "connected" ? (
          <Pressable
            onPress={connectDevice}
            style={({ pressed }) => [
              styles.connectButton,
              { backgroundColor: "#1A2E1A", borderColor: colors.primary, opacity: pressed ? 0.8 : 1 },
            ]}
          >
            <Feather name="link-2" size={18} color={colors.primary} />
            <Text style={[styles.connectButtonText, { color: colors.primary }]}>
              {connectionStatus === "scanning" ? "CONNECT USB DEVICE" : "RECONNECT DEVICE"}
            </Text>
          </Pressable>
        ) : (
          <Pressable
            onPress={disconnectDevice}
            disabled={flashStatus === "flashing"}
            style={({ pressed }) => [
              styles.connectButton,
              { backgroundColor: "#2A1A1A", borderColor: "#664444", opacity: pressed ? 0.8 : 1 },
            ]}
          >
            <Feather name="wifi-off" size={18} color="#AA5555" />
            <Text style={[styles.connectButtonText, { color: "#AA5555" }]}>DISCONNECT</Text>
          </Pressable>
        )}

        {/* Flash Button */}
        <Animated.View style={{ transform: [{ scale: buttonScale }] }}>
          <Pressable
            onPress={() => {
              animateButton();
              onFlashPress();
            }}
            disabled={!isReady && flashStatus === "idle"}
            style={[
              styles.flashButton,
              {
                backgroundColor: flashButtonBg,
                borderColor: isReady ? colors.primary : colors.border,
              },
            ]}
          >
            {flashStatus === "flashing" ? (
              <MaterialCommunityIcons name="progress-upload" size={22} color={colors.primary} />
            ) : flashStatus === "success" ? (
              <Feather name="check-circle" size={22} color={colors.primary} />
            ) : flashStatus === "error" ? (
              <Feather name="alert-circle" size={22} color="#FF5555" />
            ) : (
              <MaterialCommunityIcons name="rocket-launch" size={22} color={isReady ? colors.primary : colors.mutedForeground} />
            )}
            <Text
              style={[
                styles.flashButtonText,
                { color: isReady ? colors.primary : colors.mutedForeground },
              ]}
            >
              {flashButtonLabel}
            </Text>
          </Pressable>
        </Animated.View>

        {/* Platform Info */}
        <View style={styles.infoRow}>
          <Feather
            name={Platform.OS === "web" ? "monitor" : "smartphone"}
            size={12}
            color={colors.mutedForeground}
          />
          <Text style={[styles.infoText, { color: colors.mutedForeground }]}>
            {Platform.OS === "web"
              ? supportsWebSerial
                ? "WebSerial mode (Chrome) — real USB flashing"
                : "WebSerial not available — use Chrome for USB flashing"
              : "Native mode — USB OTG requires custom Expo build"}
          </Text>
        </View>

        {/* Flash History */}
        <FlashHistoryList
          history={history}
          loading={historyLoading}
          onClear={clearHistory}
        />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1 },
  scroll: { paddingHorizontal: 20, gap: 14 },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 10,
    marginBottom: 2,
  },
  appTitle: {
    fontSize: 20,
    fontWeight: "700",
    letterSpacing: 1.2,
    fontFamily: "Inter_700Bold",
  },
  subtitle: {
    textAlign: "center",
    fontSize: 12,
    fontFamily: "Inter_400Regular",
    marginBottom: 4,
  },
  card: {
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    gap: 6,
  },
  cardLabel: {
    fontSize: 10,
    fontFamily: "Inter_600SemiBold",
    letterSpacing: 1,
    textTransform: "uppercase",
  },
  fileName: {
    fontSize: 14,
    fontFamily: "Inter_500Medium",
  },
  fileSize: {
    fontSize: 11,
    fontFamily: "Inter_400Regular",
  },
  selectButton: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 10,
    borderRadius: 12,
    paddingVertical: 14,
    paddingHorizontal: 20,
  },
  selectButtonText: {
    color: "#fff",
    fontFamily: "Inter_700Bold",
    fontSize: 13,
    letterSpacing: 0.8,
  },
  statusCard: {
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    gap: 12,
  },
  statusRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
  },
  led: {
    width: 14,
    height: 14,
    borderRadius: 7,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.9,
    shadowRadius: 6,
    elevation: 4,
  },
  statusText: {
    fontSize: 13,
    fontFamily: "Inter_600SemiBold",
    flex: 1,
  },
  progressTrack: {
    height: 6,
    borderRadius: 3,
    overflow: "hidden",
  },
  progressFill: {
    height: "100%",
    borderRadius: 3,
  },
  progressPct: {
    fontSize: 11,
    fontFamily: "Inter_500Medium",
    textAlign: "right",
  },
  errorText: {
    fontSize: 12,
    fontFamily: "Inter_400Regular",
    marginTop: 2,
  },
  connectButton: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 10,
    borderRadius: 12,
    borderWidth: 1.5,
    paddingVertical: 13,
  },
  connectButtonText: {
    fontFamily: "Inter_700Bold",
    fontSize: 13,
    letterSpacing: 0.8,
  },
  flashButton: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 12,
    borderRadius: 14,
    borderWidth: 1.5,
    paddingVertical: 18,
  },
  flashButtonText: {
    fontFamily: "Inter_700Bold",
    fontSize: 15,
    letterSpacing: 1,
  },
  infoRow: {
    flexDirection: "row",
    alignItems: "flex-start",
    gap: 6,
    marginTop: 4,
    paddingHorizontal: 4,
  },
  infoText: {
    fontSize: 11,
    fontFamily: "Inter_400Regular",
    flex: 1,
    lineHeight: 16,
  },
});
