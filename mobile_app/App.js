import { StatusBar } from "expo-status-bar";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  ActivityIndicator,
  BackHandler,
  Platform,
  Pressable,
  SafeAreaView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { WebView } from "react-native-webview";

const DEFAULT_WEB_URL_ANDROID = "http://10.0.2.2:3000";
const DEFAULT_WEB_URL_IOS = "http://localhost:3000";

const APP_WEB_URL = (
  Platform.OS === "android"
    ? process.env.EXPO_PUBLIC_WEB_URL_ANDROID ||
      process.env.EXPO_PUBLIC_WEB_URL ||
      DEFAULT_WEB_URL_ANDROID
    : process.env.EXPO_PUBLIC_WEB_URL_IOS ||
      process.env.EXPO_PUBLIC_WEB_URL ||
      DEFAULT_WEB_URL_IOS
).trim();

function getAllowedOrigin(url) {
  try {
    const parsed = new URL(url);
    return `${parsed.protocol}//${parsed.host}`;
  } catch {
    return null;
  }
}

export default function App() {
  const webViewRef = useRef(null);
  const [canGoBack, setCanGoBack] = useState(false);
  const [loadError, setLoadError] = useState("");
  const [reloadKey, setReloadKey] = useState(0);

  const allowedOrigin = useMemo(() => getAllowedOrigin(APP_WEB_URL), []);
  const originWhitelist = useMemo(() => ["http://*", "https://*", "about:blank"], []);

  useEffect(() => {
    if (Platform.OS !== "android") {
      return undefined;
    }

    const subscription = BackHandler.addEventListener("hardwareBackPress", () => {
      if (canGoBack && webViewRef.current) {
        webViewRef.current.goBack();
        return true;
      }
      return false;
    });

    return () => subscription.remove();
  }, [canGoBack]);

  const handleShouldStartLoad = useCallback(
    (request) => {
      const { url } = request;
      if (!url || url.startsWith("about:blank")) {
        return true;
      }

      // Внутри WebView разрешаем обычные web-ссылки
      if (url.startsWith("http://") || url.startsWith("https://")) {
        return true;
      }

      // Невеб-схемы блокируем, чтобы приложение не выбрасывало в Safari
      return false;
    },
    []
  );

  const forceReload = useCallback(() => {
    setLoadError("");
    setReloadKey((value) => value + 1);
  }, []);

  if (!allowedOrigin) {
    return (
      <SafeAreaView style={styles.safe}>
        <View style={styles.center}>
          <Text style={styles.title}>Некорректный URL для WebView</Text>
          <Text style={styles.text}>Проверь `.env` в папке `mobile_app`.</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safe}>
      <StatusBar style="dark" />
      {loadError ? (
        <View style={styles.center}>
          <Text style={styles.title}>Нет соединения с сайтом</Text>
          <Text style={styles.text}>{loadError}</Text>
          <Pressable style={styles.button} onPress={forceReload}>
            <Text style={styles.buttonText}>Повторить</Text>
          </Pressable>
        </View>
      ) : (
        <WebView
          key={reloadKey}
          ref={webViewRef}
          source={{ uri: APP_WEB_URL }}
          startInLoadingState
          renderLoading={() => (
            <View style={styles.loader}>
              <ActivityIndicator size="large" color="#0f766e" />
              <Text style={styles.text}>Загружаем IT School...</Text>
            </View>
          )}
          onError={({ nativeEvent }) => setLoadError(nativeEvent.description || "Network error")}
          onHttpError={({ nativeEvent }) =>
            setLoadError(`HTTP ${nativeEvent.statusCode}: ${nativeEvent.description}`)
          }
          onNavigationStateChange={(state) => setCanGoBack(state.canGoBack)}
          onShouldStartLoadWithRequest={handleShouldStartLoad}
          pullToRefreshEnabled
          allowsBackForwardNavigationGestures
          javaScriptEnabled
          domStorageEnabled
          sharedCookiesEnabled
          thirdPartyCookiesEnabled
          originWhitelist={originWhitelist}
          setSupportMultipleWindows={false}
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: "#ffffff",
  },
  loader: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    gap: 12,
    backgroundColor: "#ffffff",
  },
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 20,
    backgroundColor: "#ffffff",
  },
  title: {
    fontSize: 18,
    fontWeight: "700",
    marginBottom: 10,
    textAlign: "center",
  },
  text: {
    fontSize: 14,
    color: "#374151",
    textAlign: "center",
    marginBottom: 12,
  },
  button: {
    marginTop: 4,
    backgroundColor: "#0f766e",
    borderRadius: 10,
    paddingHorizontal: 18,
    paddingVertical: 10,
  },
  buttonText: {
    color: "#ffffff",
    fontWeight: "600",
  },
});
