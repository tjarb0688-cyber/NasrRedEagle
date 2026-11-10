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

      - name: Accept Android SDK Licenses
        # هذه الخطوة ضرورية لقبول تراخيص Google و Android قبل البناء
        run: |
          mkdir -p ~/.android
          echo "8933bad161af4178b1185d1a37fbf4dbfa52c9cc" > ~/.android/repositories.cfg
          
          # قبول جميع التراخيص الشائعة باستخدام أداة sdkmanager
          yes | ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager --licenses || true
          
          # إذا لم يكن ANDROID_HOME معرفًا، نستخدم المسار الافتراضي لبنوزر
          if [ ! -d "${ANDROID_HOME}" ]; then
            export ANDROID_HOME="$HOME/.buildozer/android/platform/android-sdk"
          fi
          
          # قبول التراخيص عبر الإخراج القياسي
          echo y | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses

      - name: Prepare Build Environment
        run: |
          cd ${{ github.workspace }}
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
