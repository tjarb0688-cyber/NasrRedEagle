name: Build Android APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y python3-pip build-essential git python3-dev ffmpeg zlib1g-dev libzip-dev liblzma-dev openjdk-17-jdk-headless

      - name: Install Python dependencies
        run: |
          pip install --upgrade pip
          pip install buildozer cython
          pip install kivy[kde] 

      - name: Download and Accept Android SDK Licenses
        run: |
          # تثبيت أدوات سطر الأوامر الخاصة بـ Android
          export ANDROID_HOME="$HOME/.buildozer/android/platform/android-sdk"
          
          # إنشاء المجلدات الأساسية
          mkdir -p "$ANDROID_HOME/cmdline-tools"
          cd "$ANDROID_HOME/cmdline-tools"
          
          # تنزيل أحدث إصدار من cmdline-tools
          wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O cmdtools.zip
          unzip -q cmdtools.zip -d temp_unzip
          mv temp_unzip/cmdline-tools latest
          rm -rf temp_unzip cmdtools.zip
          
          # قبول جميع التراخيص
          yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses > /dev/null 2>&1 || true

      - name: Install Required SDK Packages
        run: |
          export ANDROID_HOME="$HOME/.buildozer/android/platform/android-sdk"
          
          # تثبيت الحزم الأساسية التي تسبب عادة مشاكل التراخيص
          $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager "platforms;android-33" "build-tools;34.0.0" "platform-tools"
          
          # التأكد من وجود AIDL
          $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager "build-tools;34.0.0"

      - name: Clean Old State
        run: |
          rm -rf .buildozer bin

      - name: Prepare Build Environment
        run: |
          cd ${{ github.workspace }}
          # الآن buildozer سيجد الأدوات موجودة وسيبدأ في تهيئة البيئة
          buildozer android debug prepare

      - name: Build APK
        run: |
          cd ${{ github.workspace }}
          buildozer android debug

      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: NasrRedEagle-APK
          path: bin/*.apk
