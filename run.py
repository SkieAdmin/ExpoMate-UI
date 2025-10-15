import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import asyncio
import subprocess
import threading
import os
import json
from datetime import datetime
from pathlib import Path
import shutil
import webbrowser
import platform


class ExpoMateBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("ExpoMate - Android APK Builder")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Colors - Dark and Orange theme (Elegant)
        self.bg_color = "#0f0f0f"
        self.fg_color = "#ffffff"
        self.orange_color = "#ff8c00"
        self.orange_hover = "#ffaa33"
        self.dark_gray = "#1a1a1a"
        self.light_gray = "#2d2d2d"
        self.accent_color = "#ff6b35"

        self.root.configure(bg=self.bg_color)

        # Variables
        self.expo_folder = tk.StringVar()
        self.build_type = tk.StringVar(value="release")  # debug or release
        self.is_prebuild_done = False
        self.log_dir = Path("log")
        self.log_dir.mkdir(exist_ok=True)
        self.current_log_file = None

        # Setup UI
        self.setup_ui()

        # Initialize log file
        self.init_log_file()

    def init_log_file(self):
        """Initialize log file with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_log_file = self.log_dir / f"log_data_{timestamp}.txt"
        self.log_message(f"=== ExpoMate - Log Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

    def setup_ui(self):
        """Setup the elegant user interface"""
        # Header Frame with gradient effect simulation
        header_frame = tk.Frame(self.root, bg=self.dark_gray, height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)

        # Title with elegant styling
        title_label = tk.Label(
            header_frame,
            text="⚡ ExpoMate",
            font=("Segoe UI", 32, "bold"),
            bg=self.dark_gray,
            fg=self.orange_color
        )
        title_label.pack(pady=(20, 0))

        subtitle_label = tk.Label(
            header_frame,
            text="Android APK Builder • Powered by Expo",
            font=("Segoe UI", 11),
            bg=self.dark_gray,
            fg="#888888"
        )
        subtitle_label.pack(pady=(0, 10))

        # Menu bar (About button in top right)
        menu_frame = tk.Frame(header_frame, bg=self.dark_gray)
        menu_frame.place(relx=1.0, rely=0, anchor="ne", x=-10, y=10)

        about_btn = tk.Button(
            menu_frame,
            text="ℹ About",
            command=self.show_about,
            bg=self.light_gray,
            fg=self.fg_color,
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            borderwidth=0
        )
        about_btn.pack()
        self._bind_hover_effect(about_btn, self.light_gray, self.orange_color)

        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Folder selection card
        folder_card = tk.Frame(main_frame, bg=self.dark_gray, bd=0)
        folder_card.pack(fill=tk.X, pady=(0, 20))

        folder_inner = tk.Frame(folder_card, bg=self.dark_gray)
        folder_inner.pack(fill=tk.X, padx=20, pady=15)

        folder_label = tk.Label(
            folder_inner,
            text="📁 Expo Project Folder",
            font=("Segoe UI", 12, "bold"),
            bg=self.dark_gray,
            fg=self.orange_color
        )
        folder_label.pack(anchor=tk.W, pady=(0, 8))

        folder_select_frame = tk.Frame(folder_inner, bg=self.dark_gray)
        folder_select_frame.pack(fill=tk.X)

        self.folder_entry = tk.Entry(
            folder_select_frame,
            textvariable=self.expo_folder,
            font=("Segoe UI", 10),
            bg=self.light_gray,
            fg=self.fg_color,
            insertbackground=self.orange_color,
            relief=tk.FLAT,
            state="readonly",
            readonlybackground=self.light_gray
        )
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))

        browse_btn = tk.Button(
            folder_select_frame,
            text="Browse",
            command=self.browse_folder,
            bg=self.orange_color,
            fg="#000000",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=25,
            pady=8,
            cursor="hand2",
            borderwidth=0
        )
        browse_btn.pack(side=tk.LEFT)
        self._bind_hover_effect(browse_btn, self.orange_color, self.orange_hover)

        # Build Type Selection Card
        build_card = tk.Frame(main_frame, bg=self.dark_gray, bd=0)
        build_card.pack(fill=tk.X, pady=(0, 20))

        build_inner = tk.Frame(build_card, bg=self.dark_gray)
        build_inner.pack(fill=tk.X, padx=20, pady=15)

        build_label = tk.Label(
            build_inner,
            text="⚙️ Build Configuration",
            font=("Segoe UI", 12, "bold"),
            bg=self.dark_gray,
            fg=self.orange_color
        )
        build_label.pack(anchor=tk.W, pady=(0, 10))

        build_type_frame = tk.Frame(build_inner, bg=self.dark_gray)
        build_type_frame.pack(fill=tk.X)

        # Custom styled radio buttons
        self.release_radio = tk.Radiobutton(
            build_type_frame,
            text="Release Build (Production)",
            variable=self.build_type,
            value="release",
            font=("Segoe UI", 10),
            bg=self.dark_gray,
            fg=self.fg_color,
            selectcolor=self.light_gray,
            activebackground=self.dark_gray,
            activeforeground=self.orange_color,
            cursor="hand2",
            bd=0,
            highlightthickness=0
        )
        self.release_radio.pack(side=tk.LEFT, padx=(0, 30))

        self.debug_radio = tk.Radiobutton(
            build_type_frame,
            text="Debug Build (Development)",
            variable=self.build_type,
            value="debug",
            font=("Segoe UI", 10),
            bg=self.dark_gray,
            fg=self.fg_color,
            selectcolor=self.light_gray,
            activebackground=self.dark_gray,
            activeforeground=self.orange_color,
            cursor="hand2",
            bd=0,
            highlightthickness=0
        )
        self.debug_radio.pack(side=tk.LEFT)

        # Action Buttons Card
        actions_card = tk.Frame(main_frame, bg=self.dark_gray, bd=0)
        actions_card.pack(fill=tk.X, pady=(0, 20))

        actions_inner = tk.Frame(actions_card, bg=self.dark_gray)
        actions_inner.pack(fill=tk.X, padx=20, pady=15)

        buttons_frame = tk.Frame(actions_inner, bg=self.dark_gray)
        buttons_frame.pack()

        self.prebuild_btn = tk.Button(
            buttons_frame,
            text="🔧 Run Prebuild",
            command=self.run_prebuild,
            bg=self.orange_color,
            fg="#000000",
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            padx=35,
            pady=12,
            cursor="hand2",
            state=tk.DISABLED,
            borderwidth=0
        )
        self.prebuild_btn.pack(side=tk.LEFT, padx=(0, 15))
        self._bind_hover_effect(self.prebuild_btn, self.orange_color, self.orange_hover)

        self.clean_btn = tk.Button(
            buttons_frame,
            text="🧹 Clean",
            command=self.run_clean,
            bg=self.light_gray,
            fg=self.fg_color,
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            padx=35,
            pady=12,
            cursor="hand2",
            state=tk.DISABLED,
            borderwidth=0
        )
        self.clean_btn.pack(side=tk.LEFT, padx=(0, 15))
        self._bind_hover_effect(self.clean_btn, self.light_gray, self.accent_color)

        self.compile_btn = tk.Button(
            buttons_frame,
            text="🚀 Compile APK",
            command=self.run_compile,
            bg=self.light_gray,
            fg=self.fg_color,
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            padx=35,
            pady=12,
            cursor="hand2",
            state=tk.DISABLED,
            borderwidth=0
        )
        self.compile_btn.pack(side=tk.LEFT)
        self._bind_hover_effect(self.compile_btn, self.light_gray, self.accent_color)

        # Progress bar with elegant styling
        progress_frame = tk.Frame(main_frame, bg=self.bg_color)
        progress_frame.pack(fill=tk.X, pady=(0, 20))

        self.progress = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(fill=tk.X)

        # Style progress bar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "TProgressbar",
            troughcolor=self.dark_gray,
            background=self.orange_color,
            bordercolor=self.bg_color,
            darkcolor=self.orange_color,
            lightcolor=self.orange_color,
            thickness=8
        )

        # Log box card with elegant design
        log_card = tk.Frame(main_frame, bg=self.dark_gray, bd=0)
        log_card.pack(fill=tk.BOTH, expand=True)

        log_inner = tk.Frame(log_card, bg=self.dark_gray)
        log_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        log_header = tk.Frame(log_inner, bg=self.dark_gray)
        log_header.pack(fill=tk.X, pady=(0, 10))

        log_label = tk.Label(
            log_header,
            text="📝 Build Log",
            font=("Segoe UI", 12, "bold"),
            bg=self.dark_gray,
            fg=self.orange_color
        )
        log_label.pack(side=tk.LEFT)

        clear_log_btn = tk.Button(
            log_header,
            text="Clear",
            command=self.clear_log,
            bg=self.light_gray,
            fg=self.fg_color,
            font=("Segoe UI", 8),
            relief=tk.FLAT,
            padx=12,
            pady=3,
            cursor="hand2",
            borderwidth=0
        )
        clear_log_btn.pack(side=tk.RIGHT)
        self._bind_hover_effect(clear_log_btn, self.light_gray, self.accent_color)

        self.log_box = scrolledtext.ScrolledText(
            log_inner,
            font=("Consolas", 9),
            bg=self.light_gray,
            fg="#e0e0e0",
            insertbackground=self.orange_color,
            relief=tk.FLAT,
            wrap=tk.WORD,
            state=tk.DISABLED,
            padx=10,
            pady=10
        )
        self.log_box.pack(fill=tk.BOTH, expand=True)

        # Configure scrollbar
        self.log_box.vbar.config(
            bg=self.dark_gray,
            troughcolor=self.dark_gray,
            activebackground=self.orange_color
        )

        # Footer
        footer_label = tk.Label(
            self.root,
            text="Made with ❤️ by Panda-Pelican Development LLC",
            font=("Segoe UI", 8),
            bg=self.bg_color,
            fg="#555555"
        )
        footer_label.pack(side=tk.BOTTOM, pady=(0, 10))

    def _bind_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            if button['state'] != tk.DISABLED:
                button.config(bg=hover_color)

        def on_leave(e):
            if button['state'] != tk.DISABLED:
                button.config(bg=normal_color)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def clear_log(self):
        """Clear the log box"""
        self.log_box.config(state=tk.NORMAL)
        self.log_box.delete(1.0, tk.END)
        self.log_box.config(state=tk.DISABLED)

    def show_about(self):
        """Show elegant About dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About ExpoMate")
        about_window.geometry("500x450")
        about_window.resizable(False, False)
        about_window.configure(bg=self.bg_color)
        about_window.transient(self.root)
        about_window.grab_set()

        # Center the window
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (about_window.winfo_screenheight() // 2) - (450 // 2)
        about_window.geometry(f"500x450+{x}+{y}")

        # Header
        header = tk.Frame(about_window, bg=self.dark_gray, height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="⚡ ExpoMate",
            font=("Segoe UI", 28, "bold"),
            bg=self.dark_gray,
            fg=self.orange_color
        )
        title.pack(pady=(20, 5))

        version = tk.Label(
            header,
            text="Version 1.1.0",
            font=("Segoe UI", 10),
            bg=self.dark_gray,
            fg="#888888"
        )
        version.pack()

        # Content
        content = tk.Frame(about_window, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Developer info with elegant spacing
        dev_label = tk.Label(
            content,
            text="Developed by",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg="#888888"
        )
        dev_label.pack(pady=(10, 5))

        name_label = tk.Label(
            content,
            text="SkieHackerYT",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        name_label.pack(pady=(0, 5))

        company_label = tk.Label(
            content,
            text="Panda-Pelican Development LLC",
            font=("Segoe UI", 12),
            bg=self.bg_color,
            fg=self.orange_color
        )
        company_label.pack(pady=(0, 20))

        # Separator
        separator = tk.Frame(content, bg=self.dark_gray, height=2)
        separator.pack(fill=tk.X, pady=15)

        # Links with fancy buttons
        links_label = tk.Label(
            content,
            text="Connect & Support",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        links_label.pack(pady=(10, 15))

        # Donate button
        donate_btn = tk.Button(
            content,
            text="💝 Donate via PayPal",
            command=lambda: webbrowser.open("https://www.paypal.com/paypalme/skiehackeryt"),
            bg=self.orange_color,
            fg="#000000",
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            borderwidth=0
        )
        donate_btn.pack(pady=5)
        self._bind_hover_effect(donate_btn, self.orange_color, self.orange_hover)

        # GitHub button
        github_btn = tk.Button(
            content,
            text="🌟 View GitHub",
            command=lambda: webbrowser.open("https://github.com/SkieAdmin"),
            bg=self.light_gray,
            fg=self.fg_color,
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            borderwidth=0
        )
        github_btn.pack(pady=5)
        self._bind_hover_effect(github_btn, self.light_gray, self.accent_color)

        # Close button
        close_btn = tk.Button(
            content,
            text="Close",
            command=about_window.destroy,
            bg=self.dark_gray,
            fg=self.fg_color,
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            borderwidth=0
        )
        close_btn.pack(pady=(20, 0))
        self._bind_hover_effect(close_btn, self.dark_gray, self.light_gray)

    def browse_folder(self):
        """Browse and select Expo project folder"""
        folder = filedialog.askdirectory(title="Select Expo Project Folder")
        if folder:
            self.expo_folder.set(folder)
            self.log_message(f"Selected folder: {folder}\n")
            self.check_dependencies()

    def check_dependencies(self):
        """Check for required dependencies in the selected folder"""
        folder = self.expo_folder.get()
        if not folder:
            return

        self.log_message("Checking dependencies...\n")

        # Check for package.json
        package_json = Path(folder) / "package.json"
        if not package_json.exists():
            self.log_message("[ERROR] package.json not found. Not a valid Node.js project.\n")
            messagebox.showerror("Error", "package.json not found in the selected folder.")
            return

        # Check package.json for expo
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
                dependencies = package_data.get('dependencies', {})
                dev_dependencies = package_data.get('devDependencies', {})

                has_expo = 'expo' in dependencies or 'expo' in dev_dependencies

                if has_expo:
                    self.log_message("[OK] Expo found in package.json\n")
                else:
                    self.log_message("[WARNING] Expo not found in package.json dependencies\n")

        except Exception as e:
            self.log_message(f"[ERROR] Failed to read package.json: {str(e)}\n")
            return

        # Check for node_modules
        node_modules = Path(folder) / "node_modules"
        if not node_modules.exists():
            self.log_message("[WARNING] node_modules not found. You may need to run 'npm install' first.\n")
        else:
            self.log_message("[OK] node_modules directory found\n")

        # Check if Node.js/npm/npx is available
        if not self.check_nodejs():
            return

        self.log_message("[SUCCESS] All basic checks passed!\n")
        self.prebuild_btn.config(state=tk.NORMAL, bg=self.orange_color)
        self.clean_btn.config(state=tk.NORMAL, bg=self.light_gray)

    def check_nodejs(self):
        """Check if Node.js and npx are installed, offer to help install if missing"""
        # Try multiple common Node.js commands
        nodejs_found = False
        npm_found = False
        npx_found = False

        # On Windows, use shell=True to properly resolve PATH
        use_shell = (os.name == 'nt')

        # Check Node.js
        for node_cmd in ["node", "nodejs"]:
            try:
                result = subprocess.run(
                    [node_cmd, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    shell=use_shell
                )
                if result.returncode == 0:
                    nodejs_found = True
                    self.log_message(f"[OK] Node.js is available (version: {result.stdout.strip()})\n")
                    break
            except (FileNotFoundError, Exception) as e:
                continue

        # Check npm
        try:
            result = subprocess.run(
                ["npm", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=use_shell
            )
            if result.returncode == 0:
                npm_found = True
                self.log_message(f"[OK] npm is available (version: {result.stdout.strip()})\n")
        except (FileNotFoundError, Exception):
            pass

        # Check npx
        try:
            result = subprocess.run(
                ["npx", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=use_shell
            )
            if result.returncode == 0:
                npx_found = True
                self.log_message(f"[OK] npx is available (version: {result.stdout.strip()})\n")
        except (FileNotFoundError, Exception):
            pass

        # If all found, return success
        if nodejs_found and npm_found and npx_found:
            return True

        # If not found, offer help
        missing = []
        if not nodejs_found:
            missing.append("Node.js")
        if not npm_found:
            missing.append("npm")
        if not npx_found:
            missing.append("npx")

        self.log_message(f"[ERROR] Missing required tools: {', '.join(missing)}\n")

        # Show dialog with installation options
        response = messagebox.askyesno(
            "Node.js Not Found",
            f"Node.js/npm/npx is required but not found.\n\n"
            f"Missing: {', '.join(missing)}\n\n"
            f"Would you like to open the Node.js download page?\n\n"
            f"After installation, please restart this application.",
            icon='warning'
        )

        if response:
            self.log_message("[INFO] Opening Node.js download page...\n")
            nodejs_url = "https://nodejs.org/en/download/"
            try:
                webbrowser.open(nodejs_url)
                self.log_message(f"[INFO] Opened: {nodejs_url}\n")
                self.log_message("[INFO] Please download and install Node.js, then restart this application.\n")
            except Exception as e:
                self.log_message(f"[ERROR] Failed to open browser: {str(e)}\n")
                self.log_message(f"[INFO] Please manually visit: {nodejs_url}\n")
        else:
            self.log_message("[INFO] User declined to download Node.js.\n")
            self.log_message("[INFO] You can manually install Node.js from: https://nodejs.org/\n")

        return False

    def log_message(self, message):
        """Add message to log box and save to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"

        # Update log box
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, formatted_message)
        self.log_box.see(tk.END)
        self.log_box.config(state=tk.DISABLED)

        # Save to file
        if self.current_log_file:
            try:
                with open(self.current_log_file, 'a', encoding='utf-8') as f:
                    f.write(formatted_message)
            except Exception as e:
                print(f"Failed to write to log file: {e}")

    def run_prebuild(self):
        """Run npx expo prebuild in a separate thread"""
        self.prebuild_btn.config(state=tk.DISABLED)
        self.compile_btn.config(state=tk.DISABLED)
        self.progress.start(10)

        self.log_message("Starting Expo prebuild...\n")

        # Run in separate thread to avoid blocking UI
        thread = threading.Thread(target=self._run_prebuild_async, daemon=True)
        thread.start()

    def _run_prebuild_async(self):
        """Async function to run prebuild command"""
        folder = self.expo_folder.get()

        try:
            # Run npx expo prebuild
            # Use shell=True on Windows to properly resolve npx from PATH
            process = subprocess.Popen(
                ["npx", "expo", "prebuild"],
                cwd=folder,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                shell=(os.name == 'nt')
            )

            # Read output in real-time
            for line in process.stdout:
                self.root.after(0, self.log_message, line)

            process.wait()

            if process.returncode == 0:
                # Create local.properties after successful prebuild
                self.root.after(0, self._create_local_properties)
                self.root.after(0, self._prebuild_success)
            else:
                self.root.after(0, self._prebuild_failed)

        except Exception as e:
            error_msg = f"[ERROR] Prebuild failed: {str(e)}\n"
            self.root.after(0, self.log_message, error_msg)
            self.root.after(0, self._prebuild_failed)

    def _create_local_properties(self):
        """Create local.properties file with Android SDK path"""
        folder = self.expo_folder.get()
        android_folder = Path(folder) / "android"

        if not android_folder.exists():
            self.log_message("[WARNING] Android folder not found, skipping local.properties creation.\n")
            return

        try:
            # Get the current username
            username = os.getenv('USERNAME') or os.getenv('USER') or 'admin'

            # Construct the SDK path based on OS
            if os.name == 'nt':  # Windows
                sdk_path = f"C:\\\\Users\\\\{username}\\\\AppData\\\\Local\\\\Android\\\\Sdk"
            else:  # Linux/Mac
                sdk_path = f"/Users/{username}/Library/Android/sdk"

            # Create local.properties file
            local_properties_path = android_folder / "local.properties"
            with open(local_properties_path, 'w', encoding='utf-8') as f:
                f.write(f"sdk.dir={sdk_path}\n")

            self.log_message(f"[SUCCESS] Created local.properties with SDK path: {sdk_path}\n")

        except Exception as e:
            self.log_message(f"[WARNING] Failed to create local.properties: {str(e)}\n")

    def _prebuild_success(self):
        """Handle successful prebuild"""
        self.progress.stop()
        self.is_prebuild_done = True
        self.log_message("\n[SUCCESS] Prebuild completed successfully!\n")
        self.log_message("You can now compile the project.\n")

        # Show success popup
        messagebox.showinfo("Success", "Successfully Prebuild, You can now compile it")

        # Enable compile button
        self.compile_btn.config(state=tk.NORMAL, bg=self.orange_color)
        self.prebuild_btn.config(state=tk.NORMAL)

    def _prebuild_failed(self):
        """Handle failed prebuild"""
        self.progress.stop()
        self.log_message("\n[ERROR] Prebuild failed. Check the log for details.\n")
        messagebox.showerror("Error", "Prebuild failed. Check the log for details.")
        self.prebuild_btn.config(state=tk.NORMAL)

    def run_clean(self):
        """Run Gradle clean task"""
        if not self.is_prebuild_done:
            messagebox.showwarning("Warning", "Please run prebuild first!")
            return

        self.clean_btn.config(state=tk.DISABLED)
        self.compile_btn.config(state=tk.DISABLED)
        self.prebuild_btn.config(state=tk.DISABLED)

        self.log_message("\nRunning Gradle clean...\n")

        # Run in separate thread
        thread = threading.Thread(target=self._run_clean_async, daemon=True)
        thread.start()

    def _run_clean_async(self):
        """Async function to run clean task"""
        folder = self.expo_folder.get()
        android_folder = Path(folder) / "android"

        if not android_folder.exists():
            error_msg = "[ERROR] Android folder not found. Did prebuild complete successfully?\n"
            self.root.after(0, self.log_message, error_msg)
            self.root.after(0, self._clean_complete)
            return

        try:
            # Check if gradlew exists
            gradlew = android_folder / "gradlew.bat" if os.name == 'nt' else android_folder / "gradlew"

            if not gradlew.exists():
                error_msg = "[ERROR] Gradle wrapper not found in android folder.\n"
                self.root.after(0, self.log_message, error_msg)
                self.root.after(0, self._clean_complete)
                return

            self.root.after(0, self.log_message, f"Running clean in visible terminal window...\n")
            self.root.after(0, self.log_message, f"Command: {str(gradlew)} clean\n")

            # On Windows, show CMD window
            if os.name == 'nt':
                batch_file = android_folder / "temp_clean.bat"
                marker_file = android_folder / ".clean_running"

                # Create marker file
                with open(marker_file, 'w') as f:
                    f.write("cleaning")

                batch_content = f'''@echo off
title ExpoMate - Cleaning Build
echo ========================================
echo ExpoMate - Gradle Clean
echo ========================================
echo.
cd /d "{android_folder}"
call "{gradlew}" clean
set CLEAN_EXIT_CODE=%ERRORLEVEL%
echo.
echo ========================================
if %CLEAN_EXIT_CODE% EQU 0 (
    echo CLEAN SUCCESSFUL!
    echo ========================================
    echo.
    del "{marker_file}" 2>nul
    echo Closing window in 2 seconds...
    timeout /t 2 /nobreak >nul
    del "{batch_file}" 2>nul
    exit 0
) else (
    echo CLEAN FAILED!
    echo Exit Code: %CLEAN_EXIT_CODE%
    echo ========================================
    echo.
    del "{marker_file}" 2>nul
    echo Press any key to close this window...
    pause >nul
    del "{batch_file}" 2>nul
    exit %CLEAN_EXIT_CODE%
)
'''
                with open(batch_file, 'w') as f:
                    f.write(batch_content)

                # Run the batch file in a new CMD window
                subprocess.Popen(
                    ['cmd', '/c', 'start', 'cmd', '/k', str(batch_file)],
                    cwd=str(android_folder),
                    shell=True
                )

                import time
                time.sleep(1)
                self.root.after(0, self.log_message, "Clean running in terminal window...\n")

                # Monitor for marker file deletion (means it completed)
                max_wait = 30  # 30 seconds max
                elapsed = 0
                while elapsed < max_wait and marker_file.exists():
                    time.sleep(1)
                    elapsed += 1

                # Clean up files if still exist
                for file in [marker_file, batch_file]:
                    if file.exists():
                        try:
                            file.unlink()
                        except Exception:
                            pass

                self.root.after(0, self.log_message, "[SUCCESS] Clean completed!\n")
                self.root.after(0, self._clean_complete)

            else:
                # On macOS/Linux
                terminal_opened = False

                # Try macOS Terminal first (most common on Mac)
                if platform.system() == 'Darwin':  # macOS
                    try:
                        # Use AppleScript to open Terminal on macOS
                        applescript = f'''
                        tell application "Terminal"
                            do script "cd '{android_folder}' && '{gradlew}' clean && echo 'CLEAN SUCCESSFUL! Closing in 2 seconds...' && sleep 2 && exit"
                            activate
                        end tell
                        '''
                        subprocess.Popen(['osascript', '-e', applescript])
                        terminal_opened = True
                        self.root.after(0, self.log_message, "Clean running in Terminal window (macOS)...\n")
                    except Exception as e:
                        self.root.after(0, self.log_message, f"[WARNING] Failed to open Terminal: {str(e)}\n")

                # Try Linux terminals
                if not terminal_opened:
                    terminal_commands = [
                        ['gnome-terminal', '--', 'bash', '-c', f'cd "{android_folder}" && "{gradlew}" clean && echo "CLEAN SUCCESSFUL! Closing in 2 seconds..." && sleep 2'],
                        ['xterm', '-e', f'cd "{android_folder}" && "{gradlew}" clean && echo "CLEAN SUCCESSFUL! Closing in 2 seconds..." && sleep 2'],
                        ['konsole', '-e', f'cd "{android_folder}" && "{gradlew}" clean && echo "CLEAN SUCCESSFUL! Closing in 2 seconds..." && sleep 2'],
                    ]

                    for cmd in terminal_commands:
                        try:
                            subprocess.Popen(cmd)
                            terminal_opened = True
                            self.root.after(0, self.log_message, "Clean running in terminal window...\n")
                            break
                        except FileNotFoundError:
                            continue

                import time
                time.sleep(5)
                self.root.after(0, self.log_message, "[SUCCESS] Clean completed!\n")
                self.root.after(0, self._clean_complete)

        except Exception as e:
            error_msg = f"[ERROR] Clean failed: {str(e)}\n"
            self.root.after(0, self.log_message, error_msg)
            self.root.after(0, self._clean_complete)

    def _clean_complete(self):
        """Re-enable buttons after clean"""
        self.clean_btn.config(state=tk.NORMAL)
        self.compile_btn.config(state=tk.NORMAL)
        self.prebuild_btn.config(state=tk.NORMAL)

    def run_compile(self):
        """Run Android compilation"""
        if not self.is_prebuild_done:
            messagebox.showwarning("Warning", "Please run prebuild first!")
            return

        self.compile_btn.config(state=tk.DISABLED)
        self.prebuild_btn.config(state=tk.DISABLED)
        self.clean_btn.config(state=tk.DISABLED)
        self.progress.start(10)

        build_type = self.build_type.get()
        self.log_message(f"\nStarting Android compilation ({build_type} build)...\n")

        # Run in separate thread
        thread = threading.Thread(target=self._run_compile_async, daemon=True)
        thread.start()

    def _run_compile_async(self):
        """Async function to run compilation"""
        folder = self.expo_folder.get()
        android_folder = Path(folder) / "android"
        build_type = self.build_type.get()

        # Determine gradle task
        gradle_task = "assembleRelease" if build_type == "release" else "assembleDebug"

        if not android_folder.exists():
            error_msg = "[ERROR] Android folder not found. Did prebuild complete successfully?\n"
            self.root.after(0, self.log_message, error_msg)
            self.root.after(0, self._compile_failed)
            return

        try:
            # Check if gradlew exists
            gradlew = android_folder / "gradlew.bat" if os.name == 'nt' else android_folder / "gradlew"

            if not gradlew.exists():
                error_msg = "[ERROR] Gradle wrapper not found in android folder.\n"
                self.root.after(0, self.log_message, error_msg)
                self.root.after(0, self._compile_failed)
                return

            self.root.after(0, self.log_message, f"Running Gradle build in visible terminal window...\n")
            self.root.after(0, self.log_message, f"Command: {str(gradlew)} {gradle_task}\n")

            # On Windows, show CMD window with the build process
            if os.name == 'nt':
                batch_file = android_folder / "temp_build.bat"
                marker_file = android_folder / ".build_running"
                success_marker = android_folder / ".build_success"

                # Create marker file
                with open(marker_file, 'w') as f:
                    f.write("building")

                batch_content = f'''@echo off
title ExpoMate - Building APK
echo ========================================
echo ExpoMate - Android APK Build Process
echo ========================================
echo Build Type: {build_type.upper()}
echo ========================================
echo.
cd /d "{android_folder}"
call "{gradlew}" {gradle_task}
set BUILD_EXIT_CODE=%ERRORLEVEL%
echo.
echo ========================================
if %BUILD_EXIT_CODE% EQU 0 (
    echo BUILD SUCCESSFUL!
    echo APK Location: app\\build\\outputs\\apk\\{build_type}
    echo ========================================
    echo.
    echo. > "{success_marker}"
    del "{marker_file}" 2>nul
    echo Closing window in 3 seconds...
    timeout /t 3 /nobreak >nul
    del "{batch_file}" 2>nul
    exit 0
) else (
    echo BUILD FAILED!
    echo Exit Code: %BUILD_EXIT_CODE%
    echo Check the error messages above.
    echo ========================================
    echo.
    del "{marker_file}" 2>nul
    echo Press any key to close this window...
    pause >nul
    del "{batch_file}" 2>nul
    exit %BUILD_EXIT_CODE%
)
'''
                with open(batch_file, 'w') as f:
                    f.write(batch_content)

                # Run the batch file in a new visible CMD window
                subprocess.Popen(
                    ['cmd', '/c', 'start', 'cmd', '/k', str(batch_file)],
                    cwd=str(android_folder),
                    shell=True
                )

                import time
                time.sleep(1)
                self.root.after(0, self.log_message, "Build running in terminal window. Monitoring progress...\n")

                # Monitor for marker file deletion (means it completed)
                max_wait = 600  # Maximum 10 minutes
                elapsed = 0
                while elapsed < max_wait and marker_file.exists():
                    time.sleep(2)
                    elapsed += 2

                    # Log progress every 30 seconds
                    if elapsed % 30 == 0:
                        self.root.after(0, self.log_message, f"Build still in progress... ({elapsed}s elapsed)\n")

                # Check if it was successful
                if success_marker.exists():
                    apk_path = android_folder / "app" / "build" / "outputs" / "apk" / build_type
                    self.root.after(0, self.log_message, "\n[SUCCESS] Build completed successfully!\n")

                    # Clean up marker files
                    for file in [marker_file, batch_file, success_marker]:
                        if file.exists():
                            try:
                                file.unlink()
                            except Exception:
                                pass

                    self.root.after(0, self._compile_success, str(apk_path))
                elif not marker_file.exists():
                    # Build finished but failed
                    self.root.after(0, self.log_message, "\n[ERROR] Build failed.\n")

                    # Clean up files
                    for file in [marker_file, batch_file, success_marker]:
                        if file.exists():
                            try:
                                file.unlink()
                            except Exception:
                                pass

                    self.root.after(0, self._compile_failed)
                else:
                    # Timeout
                    self.root.after(0, self.log_message, "\n[WARNING] Build monitoring timeout.\n")

                    # Clean up files
                    for file in [marker_file, batch_file, success_marker]:
                        if file.exists():
                            try:
                                file.unlink()
                            except Exception:
                                pass

                    self.root.after(0, self._compile_failed)

            else:
                # On macOS/Linux, open a terminal window
                terminal_opened = False

                # Try macOS Terminal first (most common on Mac)
                if platform.system() == 'Darwin':  # macOS
                    try:
                        # Use AppleScript to open Terminal on macOS
                        applescript = f'''
                        tell application "Terminal"
                            do script "cd '{android_folder}' && '{gradlew}' {gradle_task} && echo 'BUILD SUCCESSFUL! Closing in 3 seconds...' && sleep 3 && exit"
                            activate
                        end tell
                        '''
                        subprocess.Popen(['osascript', '-e', applescript])
                        terminal_opened = True
                        self.root.after(0, self.log_message, "Build running in Terminal window (macOS)...\n")
                    except Exception as e:
                        self.root.after(0, self.log_message, f"[WARNING] Failed to open Terminal: {str(e)}\n")

                # Try Linux terminals
                if not terminal_opened:
                    terminal_commands = [
                        ['gnome-terminal', '--', 'bash', '-c', f'cd "{android_folder}" && "{gradlew}" {gradle_task} && echo "BUILD SUCCESSFUL! Closing in 3 seconds..." && sleep 3'],
                        ['xterm', '-e', f'cd "{android_folder}" && "{gradlew}" {gradle_task} && echo "BUILD SUCCESSFUL! Closing in 3 seconds..." && sleep 3'],
                        ['konsole', '-e', f'cd "{android_folder}" && "{gradlew}" {gradle_task} && echo "BUILD SUCCESSFUL! Closing in 3 seconds..." && sleep 3'],
                    ]

                    for cmd in terminal_commands:
                        try:
                            subprocess.Popen(cmd)
                            terminal_opened = True
                            self.root.after(0, self.log_message, "Build running in terminal window...\n")
                            break
                        except FileNotFoundError:
                            continue

                if not terminal_opened:
                    self.root.after(0, self.log_message, "[WARNING] Could not open terminal. Running in background...\n")
                    # Fallback to background execution
                    process = subprocess.Popen(
                        [str(gradlew), gradle_task],
                        cwd=str(android_folder),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1,
                        universal_newlines=True
                    )

                    for line in process.stdout:
                        self.root.after(0, self.log_message, line)

                    process.wait()

                    if process.returncode == 0:
                        apk_path = android_folder / "app" / "build" / "outputs" / "apk" / build_type
                        self.root.after(0, self._compile_success, str(apk_path))
                    else:
                        self.root.after(0, self._compile_failed)
                else:
                    # Monitor for completion
                    self._monitor_build_completion(android_folder, None, build_type)

        except Exception as e:
            error_msg = f"[ERROR] Compilation failed: {str(e)}\n"
            self.root.after(0, self.log_message, error_msg)
            self.root.after(0, self._compile_failed)

    def _monitor_build_completion(self, android_folder, batch_file, build_type):
        """Monitor the build process for completion"""
        import time
        apk_path = android_folder / "app" / "build" / "outputs" / "apk" / build_type

        max_wait = 600  # Maximum 10 minutes
        elapsed = 0

        while elapsed < max_wait:
            time.sleep(2)
            elapsed += 2

            # Check if APK was generated (build successful)
            if apk_path.exists() and any(apk_path.glob("*.apk")):
                self.root.after(0, self.log_message, "\n[SUCCESS] APK file detected! Build completed successfully.\n")

                # Clean up batch file if it exists
                if batch_file and batch_file.exists():
                    try:
                        time.sleep(3)  # Wait for auto-close
                        if batch_file.exists():
                            batch_file.unlink()
                    except Exception:
                        pass

                self.root.after(0, self._compile_success, str(apk_path))
                return

            # Log progress every 30 seconds
            if elapsed % 30 == 0:
                self.root.after(0, self.log_message, f"Build still in progress... ({elapsed}s elapsed)\n")

        # Timeout - assume failure
        self.root.after(0, self.log_message, "\n[WARNING] Build monitoring timeout. Check the terminal window for status.\n")

        # Clean up batch file
        if batch_file and batch_file.exists():
            try:
                batch_file.unlink()
            except Exception:
                pass

        self.root.after(0, self._compile_failed)

    def _compile_success(self, output_path):
        """Handle successful compilation"""
        self.progress.stop()
        self.log_message(f"\n[SUCCESS] Compilation completed successfully!\n")
        self.log_message(f"APK output location: {output_path}\n")

        # Show success message
        messagebox.showinfo("Success", f"Compilation completed successfully!\n\nOpening output folder...")

        # Open output folder
        if os.path.exists(output_path):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(output_path)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.Popen(['open', output_path])
                else:  # Linux
                    subprocess.Popen(['xdg-open', output_path])
                self.log_message("Opened output folder.\n")
            except Exception as e:
                self.log_message(f"[ERROR] Failed to open output folder: {str(e)}\n")
        else:
            self.log_message(f"[WARNING] Output folder not found: {output_path}\n")

        # Re-enable buttons
        self.compile_btn.config(state=tk.NORMAL)
        self.prebuild_btn.config(state=tk.NORMAL)
        self.clean_btn.config(state=tk.NORMAL)

    def _compile_failed(self):
        """Handle failed compilation"""
        self.progress.stop()
        self.log_message("\n[ERROR] Compilation failed. Check the log for details.\n")
        messagebox.showerror("Error", "Compilation failed. Check the log for details.")
        self.compile_btn.config(state=tk.NORMAL)
        self.prebuild_btn.config(state=tk.NORMAL)
        self.clean_btn.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    app = ExpoMateBuilder(root)
    root.mainloop()


if __name__ == "__main__":
    main()
