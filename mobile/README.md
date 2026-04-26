# Eric Hsiao — 行動 App（Capacitor）

把 Hugo 網站 https://erichsiao1106.github.io 包成 iOS / Android App 上架。

---

## 架構

採「**WebView 殼 + 線上載入**」模式：App 開啟時直接載入線上網站，不 bundle 內容（fandeng 圖片就 1.2GB，無法塞進 APK）。

優點：
- APK / AAB 只有 ~3-5 MB
- Hugo 網站每次更新，App 內容自動同步，不用重發版
- PWA service worker 在 Android WebView 下仍可運作（離線快取）

---

## ⚠️ 安全：Keystore 密碼

`keystore/eric-portfolio-upload.jks` 是 App **簽名密鑰**，遺失會無法更新 App。

目前是 **placeholder 密碼** `EricChange-Me-2026!`，你**必須立刻**做以下其中一件事：

### 選項 A：保留現有 keystore，改密碼

```bash
cd mobile/keystore
"$JAVA_HOME/bin/keytool" -storepasswd -keystore eric-portfolio-upload.jks \
  -storepass 'EricChange-Me-2026!' -new '你的新強密碼'
"$JAVA_HOME/bin/keytool" -keypasswd -keystore eric-portfolio-upload.jks \
  -alias upload -storepass '你的新強密碼' \
  -keypass 'EricChange-Me-2026!' -new '你的新強密碼'
```

然後同步更新 `mobile/keystore/keystore.properties` 內的密碼。

### 選項 B：刪除重新產生

```bash
rm mobile/keystore/eric-portfolio-upload.jks
cd mobile/keystore
"$JAVA_HOME/bin/keytool" -genkeypair -v \
  -keystore eric-portfolio-upload.jks -alias upload \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -dname "CN=Eric Hsiao, OU=Personal, O=Eric Hsiao, L=Taipei, ST=Taipei, C=TW"
# (互動輸入密碼)
```

### 備份位置建議

把 `eric-portfolio-upload.jks` 和密碼一起存進 **1Password / Bitwarden**，並在另一台裝置（或 USB）放第二份備份。

---

## 開發流程

### 重 build Android Debug APK（修改網站後不用重 build，只有改 mobile/ 才要）

```bash
cd mobile/android
JAVA_HOME='C:\Program Files\Android\Android Studio\jbr' \
ANDROID_HOME='C:\Users\erich\AppData\Local\Android\Sdk' \
./gradlew assembleDebug
# 輸出：mobile/android/app/build/outputs/apk/debug/app-debug.apk
```

### 重 build Release（上架用）

```bash
cd mobile/android
JAVA_HOME='C:\Program Files\Android\Android Studio\jbr' \
ANDROID_HOME='C:\Users\erich\AppData\Local\Android\Sdk' \
./gradlew bundleRelease assembleRelease
# 輸出：
#   mobile/android/app/build/outputs/bundle/release/app-release.aab  (上 Play Store)
#   mobile/android/app/build/outputs/apk/release/app-release.apk     (側載)
```

### 改版本號（每次上架新版必做）

編輯 `mobile/android/app/build.gradle`：
```groovy
versionCode 2        // 整數，每次 +1
versionName "1.0.1"  // 給人看的版本
```

---

## 上架 Google Play Store 流程

### 1. 註冊開發者帳號（一次性）
- 網址：https://play.google.com/console/signup
- 費用：**USD $25**（一次性，永久）
- 個人帳號需驗證身份（用台灣身份證 + 信用卡）

### 2. 建立 App
- Console → Create app
- App name: `Eric Hsiao`
- Default language: Traditional Chinese (Taiwan) – zh-TW
- App or game: App
- Free or paid: Free
- 勾選 Play 規範同意項

### 3. 上傳 AAB
- 左側選單 → Test and release → Production → Create new release
- 上傳 `app-release.aab`
- Release name 預設用 versionName，可不改
- Release notes（中文）：「首發版本」之類
- **Play App Signing**：第一次會自動啟用，把你 keystore 的 key 升級成 upload key（Google 重簽用他們的 key）

### 4. 填 Store Listing（最花時間）
必填項目：
- **App icon** 512×512 PNG → 用 `static/icons/icon-512.png`
- **Feature graphic** 1024×500 PNG → 需要另做（可用 Canva / Figma）
- **截圖** 至少 2 張，1080×1920 → 用 Android emulator 或實機截
- **簡短描述** 80 字內
- **完整描述** 4000 字內
- **隱私權政策 URL**：上架必填。建議在 Hugo 加 `/privacy/` 頁面，內容說「本 App 僅顯示公開網站，不收集個資」

### 5. Content rating / Target audience / Data safety
- Content rating：問卷，作品集 App 全部選「無」即可
- Target audience：13+ 較簡單（避免 COPPA）
- Data safety：選「No data collected」（如實申報）

### 6. 送審
- 第一次審查約 **3-7 天**（個人開發者較久）
- 之後更新審查通常 **幾小時到 1 天**

---

## 重要：個人開發者新規（2024+）

Google 要求新個人開發者上架前需：
- **20 名測試者** 在 Closed testing 連續測試 14 天
- 之後才能開放 Production

如果你是首次上架，**先在 Closed testing 邀請朋友測 14 天**，再轉 Production。

---

## iOS 上架（需要 Mac）

iOS build **必須** 在 macOS + Xcode 上完成。流程：

1. 把整個 `my-portfolio/` 拷到 Mac
2. 在 Mac 上：
   ```bash
   cd mobile
   npm install
   npx cap add ios
   npx cap sync ios
   npx cap open ios   # 開啟 Xcode
   ```
3. Xcode 內：
   - Bundle Identifier 確認 `com.erichsiao.portfolio`
   - 加 Apple Developer 帳號（**USD $99 / 年**）
   - Product → Archive → Distribute App → App Store Connect

4. App Store Connect 上架：
   - https://appstoreconnect.apple.com
   - 建立 App → 上傳 build → 填 metadata → 送審
   - 審查約 **1-3 天**，比 Google 嚴格（會實際測試 App）

iOS App Icon 已在 PWA manifest 中支援，但 Capacitor iOS 需要另外塞進 `mobile/ios/App/App/Assets.xcassets/AppIcon.appiconset/`，到 Mac 上再生（用 https://appicon.co 拖 `static/images/profile.png` 進去最快）。

---

## 檔案清單

```
mobile/
├── capacitor.config.json         # App 設定（appId、server.url）
├── package.json                  # Capacitor 依賴
├── www/index.html                # Fallback 頁（網路掛掉時顯示）
├── README.md                     # 此文件
├── keystore/
│   ├── eric-portfolio-upload.jks   # ⚠️ 簽名密鑰（不入 git）
│   └── keystore.properties         # ⚠️ 密碼（不入 git）
└── android/                      # Android 原生專案
    └── app/build/outputs/
        ├── apk/release/app-release.apk    # 側載用
        └── bundle/release/app-release.aab # 上 Play Store
```
