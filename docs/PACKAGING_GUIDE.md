# Packaging and Distribution Guide — WhisperLite

This guide provides instructions for packaging WhisperLite into distributable installers for Windows, macOS, and Linux. The primary tool for this is `cargo tauri build`, which handles the bundling of the Rust core, Python engine, and frontend assets.

## 📦 Prerequisites

Before packaging, ensure you have completed the build steps outlined in the [Build and Install Guide](BUILD_INSTALL.md).

##  Packaging Command

The main command for creating all platform-specific packages is:

```bash
cd rust
cargo tauri build
```

This command will generate installers and bundles in the `rust/target/release/bundle/` directory.

## 平台特定说明

### 1. Windows

-   **Installer Type**: `.msi` (Microsoft Installer)
-   **Process**: `cargo tauri build` will produce a `.msi` file in `rust/target/release/bundle/msi/`.
-   **Configuration**: The `tauri.conf.json` file contains settings for the Windows installer, such as the application name, version, and icon.
-   **Code Signing**: For production releases, it is highly recommended to sign the `.exe` and `.msi` files with a valid code signing certificate. This can be configured in `tauri.conf.json`.

### 2. macOS

-   **Bundle Type**: `.app` (Application Bundle)
-   **Process**: The build command will generate a `.app` file in `rust/target/release/bundle/macos/`.
-   **Disk Image**: To create a distributable `.dmg` file, you can use the `app-dmg` tool or the built-in `hdiutil` command.

    ```bash
    # Example using hdiutil
    hdiutil create -volname "WhisperLite" -srcfolder "rust/target/release/bundle/macos/WhisperLite.app" -ov -format UDZO "WhisperLite.dmg"
    ```

-   **Code Signing and Notarization**: For distribution outside of the App Store, you must sign the `.app` with a Developer ID certificate and have it notarized by Apple.

### 3. Linux

-   **Package Types**: `AppImage`, `.deb` (Debian package)
-   **Process**: `cargo tauri build` will generate both an `AppImage` and a `.deb` file.
    -   **AppImage**: Located in `rust/target/release/bundle/appimage/`. This is a portable format that can run on most modern Linux distributions.
    -   **Debian Package**: Located in `rust/target/release/bundle/deb/`. This can be installed on Debian-based systems (like Ubuntu) using `dpkg` or `apt`.
-   **Configuration**: The `tauri.conf.json` file allows you to specify metadata for the `.deb` package, such as the maintainer, dependencies, and package description.

## ⚙️ Customization

The `tauri.conf.json` file is the central place for configuring the packaging process. Key settings include:

-   `package.productName`: The name of the application.
-   `package.version`: The application version.
-   `tauri.bundle.identifier`: A unique identifier for the application (e.g., `com.yourcompany.whisperlite`).
-   `tauri.bundle.icon`: A list of icon files for different platforms.
-   `tauri.bundle.windows`, `tauri.bundle.macOS`, `tauri.bundle.linux`: Platform-specific settings.

## 🚀 Distribution

Once you have built and signed your packages, you can distribute them through various channels:

-   **GitHub Releases**: Create a new release on your GitHub repository and upload the installer files.
-   **Website**: Host the installers on your project's website.
-   **Package Managers**: For Linux, you can create a repository for `apt` or `yum` to make installation easier.
