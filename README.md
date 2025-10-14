# ⚡ ExpoMate - Android APK Builder

A professional, elegant Python GUI application for building Android APK files from Expo projects with ease.

![Version](https://img.shields.io/badge/version-1.0.0-orange)
![Python](https://img.shields.io/badge/python-3.6+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📋 Description

**ExpoMate** is a powerful yet simple-to-use desktop application that streamlines the process of building Android APK files from Expo projects. With its modern dark and orange-themed interface, ExpoMate provides an intuitive workflow for developers to prebuild, clean, and compile their Expo applications into production-ready Android APKs.

### ✨ Key Features

- **🎨 Modern UI** - Elegant dark theme with orange accents
- **🔧 Automated Prebuild** - Run `expo prebuild` with a single click
- **🧹 Build Cleanup** - Clean build artifacts before compilation
- **🚀 One-Click Compilation** - Build release or debug APKs effortlessly
- **📝 Real-Time Logging** - Monitor build progress with live log output
- **💾 Auto-Save Logs** - All logs automatically saved with timestamps
- **🎯 Progress Tracking** - Visual progress bar and status updates
- **📂 Auto-Open Output** - Automatically opens APK output folder on success
- **⚙️ Build Configuration** - Choose between Release or Debug builds
- **🪟 Visible Terminal** - View detailed build process in CMD window

## 🎯 Requirements

Before using ExpoMate, ensure you have the following installed:

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| **Android Studio** | Latest | Android SDK and build tools |
| **Java SDK** | 21+ | Java Development Kit for Android builds |
| **Node.js** | Latest | JavaScript runtime for Expo CLI |
| **Python** | 3.6+ | To run ExpoMate application |

### Installation Links

- [Android Studio](https://developer.android.com/studio) - Download and install Android Studio
- [Java SDK 21](https://www.oracle.com/java/technologies/downloads/) - Download Java Development Kit
- [Node.js](https://nodejs.org/) - Download the latest LTS version
- [Python](https://www.python.org/downloads/) - Download Python 3.6 or higher

## 🚀 Getting Started

### Installation

1. **Clone or download** this repository to your local machine

2. **Ensure all requirements** are installed (see Requirements section above)

3. **Navigate** to the project directory:
   ```bash
   cd "Android APK Generator"
   ```

4. **Run ExpoMate**:
   ```bash
   python run.py
   ```

### First Time Setup

1. Launch ExpoMate by running `python run.py`
2. The application will automatically detect if Node.js/npm/npx is installed
3. If any dependencies are missing, ExpoMate will guide you to install them

## 📖 How to Use

### Step 1: Select Your Expo Project

1. Click the **Browse** button
2. Navigate to your Expo project folder
3. Select the folder containing your `package.json` file
4. ExpoMate will automatically check for dependencies

### Step 2: Run Prebuild

1. Click **🔧 Run Prebuild** button
2. Wait for the prebuild process to complete
3. A success message will appear when finished

### Step 3: Choose Build Type (Optional)

Select your desired build configuration:
- **Release Build (Production)** - Optimized APK for distribution
- **Debug Build (Development)** - APK with debugging enabled

### Step 4: Clean Build (Optional)

Click **🧹 Clean** button to remove old build artifacts before compilation. This ensures a fresh build.

### Step 5: Compile APK

1. Click **🚀 Compile APK** button
2. A CMD window will open showing the build process
3. Monitor progress in both the CMD window and ExpoMate log
4. On success, the output folder will automatically open
5. Your APK will be located in: `android/app/build/outputs/apk/[release or debug]/`

## 📂 Log Files

All build logs are automatically saved in the `log/` directory with timestamps:
```
log/log_data_YYYYMMDD_HHMMSS.txt
```

This allows you to review past builds and troubleshoot any issues.

## 🎨 Interface Overview

### Main Window

- **Header** - Application title and About button
- **Folder Selection** - Browse and select your Expo project
- **Build Configuration** - Choose between Release or Debug build
- **Action Buttons** - Prebuild, Clean, and Compile controls
- **Progress Bar** - Visual indication of ongoing operations
- **Build Log** - Real-time output and status messages

### Features in Detail

#### 🔧 Run Prebuild
Executes `npx expo prebuild` to generate native Android project files. This step is required before compilation.

#### 🧹 Clean
Runs `gradlew clean` to remove build cache and artifacts. Opens a CMD window showing the clean process. Auto-closes on success (2 seconds).

#### 🚀 Compile APK
Runs Gradle build to generate the APK. Opens a CMD window showing detailed build output. Auto-closes on success (3 seconds), stays open on failure for error review.

## ⚙️ Build Types

### Release Build
- Optimized for production
- Smaller APK size
- ProGuard/R8 optimization enabled
- Suitable for distribution

### Debug Build
- Includes debugging symbols
- Faster build time
- Easier to debug
- Suitable for development and testing

## 🛠️ Troubleshooting

### Node.js Not Found

If ExpoMate reports that Node.js is not found:
1. Click **Yes** when prompted to open the download page
2. Install Node.js from the official website
3. Restart ExpoMate

### Build Failed

If compilation fails:
1. Check the CMD window for detailed error messages
2. Review the log file in the `log/` directory
3. Ensure all requirements are properly installed
4. Try running **🧹 Clean** before compiling again

### Gradle Issues

If you encounter Gradle-related errors:
1. Ensure Android Studio is properly installed
2. Verify ANDROID_HOME environment variable is set
3. Check that Java SDK 21 is installed
4. Run Android Studio once to complete SDK setup

## 📄 About

### Developer

**ExpoMate** is developed by:

**Kerneil Rommel S. Gocotano**
*Panda-Pelican Development LLC*

### Credits

Created by: **SkieHacker**

### Support

If you find ExpoMate useful, consider supporting the development:
- 💝 [Donate via PayPal](https://www.paypal.com/paypalme/skiehackeryt)
- 🌟 [View on GitHub](https://github.com/SkieAdmin)

## 🔄 Version History

### Version 1.0.0
- Initial release
- Expo prebuild support
- Gradle clean functionality
- Release and Debug build options
- Real-time logging with auto-save
- Auto-open output folder
- Visible terminal windows with auto-close
- Elegant dark and orange UI theme

## 📜 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---

**Made with ❤️ by Panda-Pelican Development LLC**

*ExpoMate - Build Android APKs with ease!*
