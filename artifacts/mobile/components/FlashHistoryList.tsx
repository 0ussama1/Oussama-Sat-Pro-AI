import { Feather } from "@expo/vector-icons";
import React, { useState } from "react";
import {
  Alert,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useColors } from "@/hooks/useColors";
import type { FlashRecord } from "@/hooks/useFlashHistory";

interface Props {
  history: FlashRecord[];
  loading: boolean;
  onClear: () => void;
}

function formatDate(ts: number): string {
  const d = new Date(ts);
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

function formatTime(ts: number): string {
  const d = new Date(ts);
  return d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
}

function formatSize(bytes?: number): string {
  if (!bytes) return "";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

function RecordRow({ record }: { record: FlashRecord }) {
  const colors = useColors();
  const isSuccess = record.status === "success";

  return (
    <View style={[styles.row, { backgroundColor: colors.card, borderColor: colors.border }]}>
      <View style={[styles.statusDot, { backgroundColor: isSuccess ? "#00CC66" : "#CC2200" }]} />
      <View style={styles.rowContent}>
        <Text
          style={[styles.rowFileName, { color: colors.foreground }]}
          numberOfLines={1}
          ellipsizeMode="middle"
        >
          {record.fileName}
        </Text>
        <View style={styles.rowMeta}>
          {record.fileSize !== undefined && (
            <Text style={[styles.metaTag, { color: colors.mutedForeground }]}>
              {formatSize(record.fileSize)}
            </Text>
          )}
          {record.deviceInfo && (
            <Text style={[styles.metaTag, { color: colors.mutedForeground }]}>
              {record.deviceInfo}
            </Text>
          )}
          {!isSuccess && record.errorMessage && (
            <Text style={[styles.metaTag, { color: "#CC4444" }]} numberOfLines={1}>
              {record.errorMessage}
            </Text>
          )}
        </View>
      </View>
      <View style={styles.rowRight}>
        <Text style={[styles.rowDate, { color: colors.mutedForeground }]}>
          {formatDate(record.timestamp)}
        </Text>
        <Text style={[styles.rowTime, { color: colors.mutedForeground }]}>
          {formatTime(record.timestamp)}
        </Text>
        <Text style={[styles.rowStatus, { color: isSuccess ? "#00CC66" : "#CC4444" }]}>
          {isSuccess ? "✓ OK" : "✗ ERR"}
        </Text>
      </View>
    </View>
  );
}

export function FlashHistoryList({ history, loading, onClear }: Props) {
  const colors = useColors();
  const [expanded, setExpanded] = useState(true);

  const handleClear = () => {
    Alert.alert(
      "Clear History",
      "Remove all flash history records?",
      [
        { text: "Cancel", style: "cancel" },
        { text: "Clear", style: "destructive", onPress: onClear },
      ]
    );
  };

  return (
    <View style={[styles.container, { borderColor: colors.border }]}>
      {/* Header */}
      <Pressable
        onPress={() => setExpanded((e) => !e)}
        style={styles.header}
      >
        <View style={styles.headerLeft}>
          <Feather name="clock" size={14} color={colors.primary} />
          <Text style={[styles.headerTitle, { color: colors.foreground }]}>
            Flash History
          </Text>
          {history.length > 0 && (
            <View style={[styles.badge, { backgroundColor: colors.secondary }]}>
              <Text style={[styles.badgeText, { color: colors.mutedForeground }]}>
                {history.length}
              </Text>
            </View>
          )}
        </View>
        <View style={styles.headerRight}>
          {history.length > 0 && expanded && (
            <Pressable onPress={handleClear} style={styles.clearBtn} hitSlop={8}>
              <Feather name="trash-2" size={13} color="#CC4444" />
            </Pressable>
          )}
          <Feather
            name={expanded ? "chevron-up" : "chevron-down"}
            size={16}
            color={colors.mutedForeground}
          />
        </View>
      </Pressable>

      {expanded && (
        <View>
          {loading ? (
            <Text style={[styles.emptyText, { color: colors.mutedForeground }]}>Loading...</Text>
          ) : history.length === 0 ? (
            <Text style={[styles.emptyText, { color: colors.mutedForeground }]}>
              No flashes yet — complete a firmware update to see it here.
            </Text>
          ) : (
            <View style={styles.list}>
              {history.map((record) => (
                <RecordRow key={record.id} record={record} />
              ))}
            </View>
          )}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    borderRadius: 14,
    borderWidth: 1,
    overflow: "hidden",
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    paddingVertical: 13,
  },
  headerLeft: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  headerTitle: {
    fontSize: 13,
    fontFamily: "Inter_600SemiBold",
  },
  badge: {
    borderRadius: 10,
    paddingHorizontal: 7,
    paddingVertical: 2,
  },
  badgeText: {
    fontSize: 11,
    fontFamily: "Inter_600SemiBold",
  },
  headerRight: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },
  clearBtn: {
    padding: 2,
  },
  emptyText: {
    fontSize: 12,
    fontFamily: "Inter_400Regular",
    textAlign: "center",
    paddingHorizontal: 20,
    paddingBottom: 16,
    lineHeight: 18,
  },
  list: {
    gap: 1,
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    paddingHorizontal: 14,
    paddingVertical: 11,
    borderTopWidth: 1,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    flexShrink: 0,
  },
  rowContent: {
    flex: 1,
    gap: 3,
    minWidth: 0,
  },
  rowFileName: {
    fontSize: 12,
    fontFamily: "Inter_500Medium",
  },
  rowMeta: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 6,
  },
  metaTag: {
    fontSize: 10,
    fontFamily: "Inter_400Regular",
  },
  rowRight: {
    alignItems: "flex-end",
    gap: 2,
    flexShrink: 0,
  },
  rowDate: {
    fontSize: 10,
    fontFamily: "Inter_400Regular",
  },
  rowTime: {
    fontSize: 10,
    fontFamily: "Inter_400Regular",
  },
  rowStatus: {
    fontSize: 11,
    fontFamily: "Inter_600SemiBold",
  },
});
