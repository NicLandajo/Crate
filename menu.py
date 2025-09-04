import os
import nuke
import nukescripts
from PySide2 import QtWidgets, QtCore, QtGui
import subprocess
import functools
import threading
import time
import tempfile
import traceback
import shutil
import hashlib
import math

print("Crate v1.0 by Nicolas Landajo - loading...")

# Configure the asset directory
ASSET_DIR = r"L:/3D Objects"
F3D_PATH = r"C:\Users\Public\f3d_3DModelBrowser\bin\f3d.exe"

print(f"Searching Crate Asset directory: {ASSET_DIR}")
print(f"Using F3D path: {F3D_PATH}")

# Check if F3D exists
if not os.path.exists(F3D_PATH):
    print(f"❌ F3D not found at: {F3D_PATH}")
else:
    print("F3D executable found!")

class ThumbnailCache:
    """Cache for storing thumbnails with smart generation strategies"""
    def __init__(self):
        print("📸 Initializing thumbnail cache...")
        self.cache = {}
        self.failed_attempts = {}  # Track failed F3D attempts
        self.active_generations = {}  # Track ongoing generations
        
        # Use network path for shared cache across multiple computers
        self.cache_dir = r"S:\01_root\0050_pipeline\0030_software package\0050_nuke\0113_3d object browser\temp_thumbs_cache"
        
        # Fallback to local temp if network path is not available
        if not os.path.exists(self.cache_dir):
            try:
                os.makedirs(self.cache_dir, exist_ok=True)
                print(f"💾 Created network cache directory: {self.cache_dir}")
            except Exception as e:
                print(f"❌ Cannot create network cache directory: {e}")
                # Fallback to local temp directory
                self.cache_dir = os.path.join(tempfile.gettempdir(), "nuke_3d_thumbnails")
                os.makedirs(self.cache_dir, exist_ok=True)
                print(f"🔄 Using local cache directory: {self.cache_dir}")
        else:
            print(f"💾 Using network cache directory: {self.cache_dir}")
        
        # Create temp directory for network file processing (local to each machine)
        self.temp_dir = os.path.join(tempfile.gettempdir(), "nuke_3d_temp")
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Verify we can write to cache directory
        test_file = os.path.join(self.cache_dir, "test_write.tmp")
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print("✅ Cache directory is writable")
        except Exception as e:
            print(f"❌ Cache directory not writable: {e}")
            # Fallback to user's home directory if neither network nor temp is available
            self.cache_dir = os.path.expanduser("~/nuke_3d_thumbnails")
            os.makedirs(self.cache_dir, exist_ok=True)
            print(f"🔄 Using fallback cache directory: {self.cache_dir}")
    
    def get_thumbnail(self, file_path, size=128):
        """Get colored icon based on file type, or actual image preview for textures"""
        ext = os.path.splitext(file_path)[1].lower()
        texture_formats = {'.exr', '.png', '.jpg', '.jpeg', '.tga', '.tif', '.tiff', '.hdr'}
        
        # Create a UNIQUE key based on the file's full path and size
        path_hash = hashlib.md5(file_path.encode()).hexdigest()[:12]  # Create a short unique hash from the full path
        cache_key = f"{path_hash}_{size}"
        cache_file = os.path.join(self.cache_dir, f"{path_hash}_{size}.png")
        
        # Return cached thumbnail if exists in memory
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Check if a base thumbnail exists on disk (even after Nuke restart)
        # First try to find the largest available thumbnail for this file
        base_sizes = [256, 128, 100]  # Ordered from largest to smallest
        base_thumbnail = None
        base_size = None
        
        for base_size in base_sizes:
            base_cache_file = os.path.join(self.cache_dir, f"{path_hash}_{base_size}.png")
            if os.path.exists(base_cache_file) and (time.time() - os.path.getmtime(base_cache_file)) < 604800:
                try:
                    base_thumbnail = QtGui.QPixmap(base_cache_file)
                    if not base_thumbnail.isNull():
                        # Scale the base thumbnail to the requested size
                        scaled_thumbnail = base_thumbnail.scaled(size, size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                        self.cache[cache_key] = scaled_thumbnail
                        return scaled_thumbnail
                except Exception as e:
                    print(f"❌ Error loading cached thumbnail {base_cache_file}: {e}")
        
        # For image/texture files, load actual image
        if ext in texture_formats:
            try:
                pixmap = QtGui.QPixmap(file_path)
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(size, size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                    self.cache[cache_key] = pixmap
                    return pixmap
            except Exception as e:
                print(f"❌ Error loading texture {file_path}: {e}")
        
        # For 3D models, try async F3D generation (if not failed before)
        # Added .splat to the model formats list
        model_formats = {'.obj', '.fbx', '.stl', '.ply', '.gltf', '.glb', '.abc', '.usd', '.usdc', '.splat'}
        if (ext in model_formats and 
            file_path not in self.failed_attempts.get(ext, set()) and
            os.path.exists(F3D_PATH)):
            
            # Track this generation
            self.active_generations[cache_key] = True
            
            # Try to generate thumbnail in background - always generate at 256px for best scaling
            self.try_async_f3d_generation(file_path, 256, cache_key, path_hash)
            
            # Return placeholder immediately while generating
            return self.create_placeholder(ext, size, "generating...")
        
        # Final fallback - colored placeholder
        return self.create_placeholder(ext, size)
    
    def try_async_f3d_generation(self, file_path, size, cache_key, path_hash):
        """Attempt F3D thumbnail generation with better network path handling"""
        def generate_thumbnail():
            try:
                # Use our cache directory with unique hash-based filename
                # Always generate at 256px for best scaling quality
                cache_file = os.path.join(self.cache_dir, f"{path_hash}_256.png")
                
                # Skip if already exists and is recent
                if (os.path.exists(cache_file) and 
                    (time.time() - os.path.getmtime(cache_file)) < 604800):
                    pixmap = QtGui.QPixmap(cache_file)
                    if not pixmap.isNull():
                        # Cache the base size thumbnail
                        self.cache[f"{path_hash}_256"] = pixmap
                        # Remove from active generations
                        if cache_key in self.active_generations:
                            del self.active_generations[cache_key]
                        return
                
                # Handle network paths differently - copy file locally first
                if file_path.startswith(('L:/', 'L:\\', '\\\\')):
                    # Copy the file to a temporary local location for F3D to process
                    filename = os.path.basename(file_path)
                    local_temp_path = os.path.join(self.temp_dir, filename)
                    
                    # Check file size before copying (skip files larger than 500MB)
                    file_size = os.path.getsize(file_path)
                    if file_size > 500 * 1024 * 1024:  # 500MB limit
                        print(f"⚠️  Skipping large file: {filename} ({file_size/(1024*1024):.1f}MB)")
                        # Mark as failed to avoid retries
                        ext = os.path.splitext(file_path)[1].lower()
                        if ext not in self.failed_attempts:
                            self.failed_attempts[ext] = set()
                        self.failed_attempts[ext].add(file_path)
                        del self.active_generations[cache_key]
                        return
                    
                    # Copy the file
                    shutil.copy2(file_path, local_temp_path)
                    f3d_input_path = local_temp_path.replace('/', '\\')
                else:
                    # Local file, use directly
                    f3d_input_path = file_path.replace('/', '\\')
                
                # Always use local path for output
                cache_file_f3d = cache_file.replace('/', '\\')
                
                # F3D command - using compatible parameters
                cmd = [
                    F3D_PATH,
                    f3d_input_path,
                    "--output", cache_file_f3d,
                    "--no-background"
                ]
                
                print(f"🔄 Generating thumbnail: {os.path.basename(file_path)}")
                result = subprocess.run(cmd, check=True, capture_output=True, timeout=60, text=True)
                
                # Clean up temporary file if we created one
                if file_path.startswith(('L:/', 'L:\\', '\\\\')) and os.path.exists(local_temp_path):
                    os.remove(local_temp_path)
                
                if os.path.exists(cache_file):
                    time.sleep(0.5)  # Wait for file to be fully written
                    
                    # Load the generated image
                    pixmap = QtGui.QPixmap(cache_file)
                    if not pixmap.isNull():
                        # Cache the base size thumbnail
                        self.cache[f"{path_hash}_256"] = pixmap
                        print(f"✅ Thumbnail generated: {os.path.basename(file_path)}")
                    else:
                        print(f"❌ Generated thumbnail is invalid: {os.path.basename(file_path)}")
                else:
                    print(f"❌ Thumbnail file was not created: {os.path.basename(file_path)}")
                    if result.stderr:
                        print(f"   F3D stderr: {result.stderr}")
                        
            except subprocess.CalledProcessError as e:
                print(f"❌ F3D command failed for {os.path.basename(file_path)}:")
                print(f"   Error: {e}")
                if e.stderr:
                    print(f"   Stderr: {e.stderr}")
            except subprocess.TimeoutExpired:
                print(f"⏰ F3D timed out for {os.path.basename(file_path)}")
            except Exception as e:
                print(f"💥 Unexpected error generating thumbnail: {e}")
                print(f"   Traceback: {traceback.format_exc()}")
                
            # Mark this extension as failed to avoid repeated attempts
            ext = os.path.splitext(file_path)[1].lower()
            if ext not in self.failed_attempts:
                self.failed_attempts[ext] = set()
            self.failed_attempts[ext].add(file_path)
            
            # Remove from active generations
            if cache_key in self.active_generations:
                del self.active_generations[cache_key]
        
        # Start generation in background thread
        thread = threading.Thread(target=generate_thumbnail, daemon=True)
        thread.start()
    
    def create_placeholder(self, ext, size, status=""):
        """Create a colored placeholder with extension text"""
        if ext == '.abc':
            color = QtGui.QColor("#e67e22")  # Distinct color for Alembic
        elif ext in ['.obj', '.fbx']:
            color = QtGui.QColor("#e74c3c")
        elif ext in ['.stl', '.ply']:
            color = QtGui.QColor("#2ecc71")
        elif ext in ['.gltf', '.glb']:
            color = QtGui.QColor("#3498db")
        elif ext in ['.step', '.stp', '.iges', '.igs']:
            color = QtGui.QColor("#9b59b6")
        elif ext in ['.3ds', '.dae', '.usd', '.usdc']:
            color = QtGui.QColor("#f39c12")
        elif ext in ['.exr', '.png', '.jpg', '.jpeg', '.tga', '.tif', '.tiff', '.hdr']:
            color = QtGui.QColor("#f1c40f")
        else:
            color = QtGui.QColor("#95a5a6")  # Generic for rare formats
        
        pixmap = QtGui.QPixmap(size, size)
        pixmap.fill(color)
        
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtGui.QColor("white"))
        font = painter.font()
        font.setBold(True)
        font.setPointSize(max(8, min(14, size // 10)))  # Dynamic font size based on thumbnail size
        painter.setFont(font)
        
        ext_text = ext.upper().replace('.', '')
        if status:
            ext_text = f"{ext_text}\n({status})"
        
        painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, ext_text)
        painter.end()
        
        return pixmap

class ThreeDAssetBrowser(QtWidgets.QWidget):
    # Create a signal for UI updates
    update_ui_signal = QtCore.Signal()
    
    def __init__(self):
        super().__init__()
        self.thumbnail_cache = ThumbnailCache()
        self.current_path = ASSET_DIR
        self.show_textures = True
        self.thumbnail_size = 100  # Base thumbnail size
        self.zoom_level = 1.0  # Current zoom level
        self.max_cols = 4  # Default number of columns
        
        # Connect the update signal
        self.update_ui_signal.connect(self.refresh_ui)
        
        self.setup_ui()
        self.load_assets(self.current_path)
        
    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(4)
        
        # Navigation
        nav_layout = QtWidgets.QHBoxLayout()
        self.back_btn = QtWidgets.QPushButton("◀ Back")
        self.back_btn.clicked.connect(self.go_back)
        nav_layout.addWidget(self.back_btn)
        self.up_btn = QtWidgets.QPushButton("↑ Up")
        self.up_btn.clicked.connect(self.go_up)
        nav_layout.addWidget(self.up_btn)
        self.home_btn = QtWidgets.QPushButton("Home")
        self.home_btn.clicked.connect(self.go_home)
        nav_layout.addWidget(self.home_btn)
        
        self.textures_btn = QtWidgets.QPushButton("Hide Textures")
        self.textures_btn.clicked.connect(self.toggle_textures)
        self.textures_btn.setStyleSheet("QPushButton { background-color: #27ae60; color: white; }")
        nav_layout.addWidget(self.textures_btn)
        
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        nav_layout.addWidget(self.refresh_btn)
        
        # Add thumbnail regeneration button
        self.regen_thumbs_btn = QtWidgets.QPushButton("Regenerate Thumbs")
        self.regen_thumbs_btn.clicked.connect(self.regenerate_thumbnails)
        self.regen_thumbs_btn.setToolTip("Force regenerate all thumbnails")
        nav_layout.addWidget(self.regen_thumbs_btn)
        
        # Add debug button
        self.debug_btn = QtWidgets.QPushButton("Debug")
        self.debug_btn.clicked.connect(self.show_debug_info)
        self.debug_btn.setToolTip("Show debug information")
        nav_layout.addWidget(self.debug_btn)
        
        # Add F3D test button
        self.test_f3d_btn = QtWidgets.QPushButton("Test F3D")
        self.test_f3d_btn.clicked.connect(self.test_f3d_with_current_file)
        self.test_f3d_btn.setToolTip("Test F3D with a file from current directory")
        nav_layout.addWidget(self.test_f3d_btn)
        
        # Add zoom controls
        zoom_layout = QtWidgets.QHBoxLayout()
        zoom_layout.addWidget(QtWidgets.QLabel("Zoom:"))
        
        self.zoom_out_btn = QtWidgets.QPushButton("-")
        self.zoom_out_btn.setFixedWidth(30)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.zoom_out_btn.setToolTip("Zoom out (smaller thumbnails)")
        zoom_layout.addWidget(self.zoom_out_btn)
        
        self.fit_btn = QtWidgets.QPushButton("Fit")
        self.fit_btn.setFixedWidth(40)
        self.fit_btn.clicked.connect(self.fit_to_view)
        self.fit_btn.setToolTip("Fit thumbnails to view")
        zoom_layout.addWidget(self.fit_btn)
        
        self.zoom_in_btn = QtWidgets.QPushButton("+")
        self.zoom_in_btn.setFixedWidth(30)
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_in_btn.setToolTip("Zoom in (larger thumbnails)")
        zoom_layout.addWidget(self.zoom_in_btn)
        
        nav_layout.addLayout(zoom_layout)
        
        main_layout.addLayout(nav_layout)
        
        self.path_label = QtWidgets.QLabel()
        self.path_label.setWordWrap(True)
        main_layout.addWidget(self.path_label)
        
        search_layout = QtWidgets.QHBoxLayout()
        self.search_field = QtWidgets.QLineEdit()
        self.search_field.setPlaceholderText("Search assets...")
        self.search_field.textChanged.connect(self.filter_assets)
        search_layout.addWidget(self.search_field)
        main_layout.addLayout(search_layout)
        
        # Create a container for the scroll area to make it responsive
        self.scroll_container = QtWidgets.QWidget()
        scroll_container_layout = QtWidgets.QVBoxLayout(self.scroll_container)
        scroll_container_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.assets_container = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.assets_container)
        self.grid_layout.setAlignment(QtCore.Qt.AlignTop)
        self.grid_layout.setSpacing(10)  # Add some spacing between items
        self.scroll_area.setWidget(self.assets_container)
        
        scroll_container_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.scroll_container)
        
        self.status_label = QtWidgets.QLabel()
        main_layout.addWidget(self.status_label)
        
        # Set up a timer to handle resize events efficiently
        self.resize_timer = QtCore.QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.handle_resize)
        
    def resizeEvent(self, event):
        # Delay the resize handling to avoid too many updates during resizing
        self.resize_timer.start(200)  # 200ms delay
        super().resizeEvent(event)
    
    def handle_resize(self):
        """Handle window resize by recalculating the layout"""
        if self.current_path and os.path.exists(self.current_path):
            self.calculate_columns()
            self.load_assets(self.current_path)
    
    def calculate_columns(self):
        """Calculate the optimal number of columns based on available width"""
        # Get the available width (accounting for scrollbar and margins)
        available_width = self.scroll_area.width() - 30  # Account for scrollbar
        
        # Calculate how many columns we can fit
        item_width = self.thumbnail_size * self.zoom_level + 20  # Item width + margin
        self.max_cols = max(1, math.floor(available_width / item_width))
    
    def zoom_in(self):
        """Increase zoom level"""
        self.zoom_level = min(2.0, self.zoom_level + 0.2)
        self.calculate_columns()
        self.load_assets(self.current_path)
    
    def zoom_out(self):
        """Decrease zoom level"""
        self.zoom_level = max(0.4, self.zoom_level - 0.2)
        self.calculate_columns()
        self.load_assets(self.current_path)
    
    def fit_to_view(self):
        """Reset zoom to fit the view"""
        self.zoom_level = 1.0
        self.calculate_columns()
        self.load_assets(self.current_path)
    
    def refresh_ui(self):
        """Refresh the UI - called from the signal"""
        self.load_assets(self.current_path)
    
    def show_debug_info(self):
        """Show debug information"""
        debug_info = [
            f"F3D Path: {F3D_PATH}",
            f"F3D Exists: {os.path.exists(F3D_PATH)}",
            f"Cache Dir: {self.thumbnail_cache.cache_dir}",
            f"Cache Writable: {os.access(self.thumbnail_cache.cache_dir, os.W_OK)}",
            f"Temp Dir: {self.thumbnail_cache.temp_dir}",
            f"Active Generations: {len(self.thumbnail_cache.active_generations)}",
            f"Failed Attempts: {len(self.thumbnail_cache.failed_attempts)}",
            f"Current Path: {self.current_path}",
            f"Zoom Level: {self.zoom_level:.1f}",
            f"Columns: {self.max_cols}",
        ]
        
        nuke.message("Debug Information:\n\n" + "\n".join(debug_info))
    
    def test_f3d_with_current_file(self):
        """Test F3D with the first file in the current directory"""
        try:
            # Find the first 3D file in the current directory
            model_formats = {'.obj', '.fbx', '.stl', '.ply', '.gltf', '.glb', '.abc', '.splat'}
            test_file = None
            
            for item in os.listdir(self.current_path):
                item_path = os.path.join(self.current_path, item)
                if os.path.isfile(item_path):
                    ext = os.path.splitext(item)[1].lower()
                    if ext in model_formats:
                        test_file = item_path
                        break
            
            if not test_file:
                nuke.message("No 3D files found to test with F3D")
                return
            
            # Test F3D with this file
            test_output = os.path.join(self.thumbnail_cache.cache_dir, "test_output.png")
            
            # Use compatible parameters for your F3D version
            cmd = [
                F3D_PATH,
                test_file.replace('/', '\\'),
                "--output", test_output.replace('/', '\\'),
                "--no-background"
            ]
            
            print(f"🧪 Testing F3D with: {os.path.basename(test_file)}")
            print(f"   Command: {' '.join(cmd)}")
            
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=30, text=True)
                
                if os.path.exists(test_output):
                    # Load and resize to standard thumbnail size
                    pixmap = QtGui.QPixmap(test_output)
                    if not pixmap.isNull():
                        pixmap = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                        success = pixmap.save(test_output)
                        if success:
                            success_msg = f"✅ F3D test successful!\nThumbnail created: {test_output}"
                            print(success_msg)
                            
                            # Show the test result to the user
                            self.show_test_result(test_output, success_msg)
                            
                            os.remove(test_output)  # Clean up
                        else:
                            error_msg = "❌ Failed to resize test image"
                            print(error_msg)
                            nuke.message(error_msg)
                    else:
                        error_msg = "❌ Test image is invalid"
                        print(error_msg)
                        nuke.message(error_msg)
                else:
                    error_msg = f"❌ F3D test failed for {os.path.basename(test_file)}"
                    if result.stderr:
                        error_msg += f"\nF3D stderr: {result.stderr}"
                    if result.stdout:
                        error_msg += f"\nF3D stdout: {result.stdout}"
                    
                    print(error_msg)
                    nuke.message(error_msg)
                    
            except subprocess.TimeoutExpired:
                error_msg = "⏰ F3D test timed out after 30 seconds"
                print(error_msg)
                nuke.message(error_msg)
                
        except Exception as e:
            error_msg = f"💥 F3D test error: {e}"
            print(error_msg)
            nuke.message(error_msg)
    
    def show_test_result(self, image_path, message):
        """Show the test result in a dialog with the generated image"""
        try:
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("F3D Test Result")
            layout = QtWidgets.QVBoxLayout(dialog)
            
            # Add the message
            label = QtWidgets.QLabel(message)
            layout.addWidget(label)
            
            # Add the image if it exists
            if os.path.exists(image_path):
                pixmap = QtGui.QPixmap(image_path)
                if not pixmap.isNull():
                    image_label = QtWidgets.QLabel()
                    image_label.setPixmap(pixmap)
                    layout.addWidget(image_label)
            
            # Add OK button
            ok_btn = QtWidgets.QPushButton("OK")
            ok_btn.clicked.connect(dialog.accept)
            layout.addWidget(ok_btn)
            
            dialog.exec_()
        except Exception as e:
            print(f"Error showing test result: {e}")
            nuke.message(message)  # Fallback to simple message
        
    def toggle_textures(self):
        self.show_textures = not self.show_textures
        if self.show_textures:
            self.textures_btn.setText("Hide Textures")
            self.textures_btn.setStyleSheet("QPushButton { background-color: #27ae60; color: white; }")
        else:
            self.textures_btn.setText("Show Textures")
            self.textures_btn.setStyleSheet("QPushButton { background-color: #e67e22; color: white; }")
        self.refresh()
        
    def refresh(self):
        self.load_assets(self.current_path)
        self.status_label.setText("View refreshed")
    
    def regenerate_thumbnails(self):
        """Force regeneration of all thumbnails"""
        # Clear all caches and failed attempts
        self.thumbnail_cache.failed_attempts = {}
        self.thumbnail_cache.cache = {}
        self.thumbnail_cache.active_generations = {}
        
        # Clear disk cache
        for filename in os.listdir(self.thumbnail_cache.cache_dir):
            if filename.endswith('.png'):
                file_path = os.path.join(self.thumbnail_cache.cache_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        self.load_assets(self.current_path)
        self.status_label.setText("Thumbnails regenerated")
        
    def load_assets(self, path):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        self.current_path = path
        self.path_label.setText(f"Location: {os.path.basename(path)}")
        
        if not os.path.exists(path):
            self.status_label.setText("❌ Directory not found")
            return
        
        # Calculate columns based on current window size
        self.calculate_columns()
        
        try:
            # Comprehensive model formats - Added .splat to the list
            model_formats = {
                '.obj', '.fbx', '.stl', '.ply', '.dae', '.3ds', '.abc', '.usd', '.usda', '.usdc', '.usdz',
                '.gltf', '.glb', '.step', '.stp', '.iges', '.igs', '.x3d', '.wrl', '.bgeo', '.bgeo.sc',
                '.blend', '.lxo', '.c4d', '.ma', '.mb', '.ifc', '.skp', '.vrml', '.ac', '.ase', '.dxf', '.spz', '.splat'
            }
            texture_formats = {'.exr', '.png', '.jpg', '.jpeg', '.tga', '.tif', '.tiff', '.hdr'}
            
            row, col = 0, 0
            items = os.listdir(path)
            
            for item in sorted(items):
                # Ignore folders starting with dot
                if item.startswith('.'):
                    continue
                
                item_path = os.path.join(path, item).replace('\\', '/')
                
                if os.path.isdir(item_path):
                    self.add_folder_item(item, item_path, row, col)
                    col += 1
                else:
                    ext = os.path.splitext(item)[1].lower()
                    if ext in model_formats:
                        self.add_asset_item(item, item_path, row, col, "model")
                        col += 1
                    elif self.show_textures and ext in texture_formats:
                        self.add_asset_item(item, item_path, row, col, "texture")
                        col += 1
                
                if col >= self.max_cols:
                    col = 0
                    row += 1
            
            self.status_label.setText(f"Loaded {row * self.max_cols + col} items (Zoom: {self.zoom_level:.1f}x, Columns: {self.max_cols})")
            
            # Check for active generations and set up a timer to refresh when done
            if self.thumbnail_cache.active_generations:
                QtCore.QTimer.singleShot(2000, self.check_generations)
                
        except Exception as e:
            self.status_label.setText(f"Error loading assets: {str(e)}")
    
    def check_generations(self):
        """Check if any thumbnail generations are still active"""
        if self.thumbnail_cache.active_generations:
            # Still generating, check again in 2 seconds
            QtCore.QTimer.singleShot(2000, self.check_generations)
        else:
            # All generations done, refresh UI
            self.refresh()
    
    def add_folder_item(self, name, path, row, col):
        try:
            frame = QtWidgets.QFrame()
            frame.setFrameStyle(QtWidgets.QFrame.Box)
            frame_size = int(self.thumbnail_size * self.zoom_level + 50)
            frame.setFixedSize(frame_size, frame_size)
            layout = QtWidgets.QVBoxLayout(frame)
            layout.setContentsMargins(0, 0, 0, 0)  # Reduce margins for better filling
            layout.setSpacing(0)  # Remove spacing between widgets
            
            # Calculate a larger icon size to occupy more of the frame (leave ~20px for name)
            icon_size = frame_size - 20
            
            icon = self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon)
            # Generate pixmap in disabled mode for grey color
            pixmap = icon.pixmap(QtCore.QSize(icon_size, icon_size), QtGui.QIcon.Disabled)
            
            icon_label = QtWidgets.QLabel()
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(QtCore.Qt.AlignCenter)
            icon_label.setScaledContents(False)  # Preserve aspect, but since it's scaled in pixmap, it's fine
            layout.addWidget(icon_label)
            
            name_label = QtWidgets.QLabel(name)
            name_label.setAlignment(QtCore.Qt.AlignCenter)
            name_label.setWordWrap(True)
            name_label.setMaximumWidth(frame_size - 10)
            layout.addWidget(name_label)
            
            frame.mousePressEvent = lambda event: self.load_assets(path)
            self.grid_layout.addWidget(frame, row, col)
        except Exception as e:
            print(f"❌ Error adding folder item {name}: {e}")
    
    def add_asset_item(self, name, path, row, col, asset_type):
        try:
            frame = QtWidgets.QFrame()
            frame.setFrameStyle(QtWidgets.QFrame.Box)
            frame_size = int(self.thumbnail_size * self.zoom_level + 50)
            frame.setFixedSize(frame_size, frame_size)
            layout = QtWidgets.QVBoxLayout(frame)
            thumbnail_size = int(self.thumbnail_size * self.zoom_level)
            thumbnail = self.thumbnail_cache.get_thumbnail(path, thumbnail_size)
            thumbnail_label = QtWidgets.QLabel()
            thumbnail_label.setPixmap(thumbnail)
            thumbnail_label.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(thumbnail_label)
            name_label = QtWidgets.QLabel(name)
            name_label.setAlignment(QtCore.Qt.AlignCenter)
            name_label.setWordWrap(True)
            name_label.setMaximumWidth(frame_size - 10)
            layout.addWidget(name_label)
            
            if asset_type == "model":
                frame.mouseDoubleClickEvent = lambda event: self.create_readgeo_node(path)
                f3d_btn = QtWidgets.QPushButton("Open in F3D")
                f3d_btn.setFixedHeight(20)
                layout.addWidget(f3d_btn)
                f3d_btn.clicked.connect(functools.partial(self.launch_f3d, path))
            else:
                frame.mouseDoubleClickEvent = lambda event: self.create_read_node(path)
            
            self.grid_layout.addWidget(frame, row, col)
        except Exception as e:
            print(f"❌ Error adding {asset_type} item {name}: {e}")
    
    def launch_f3d(self, asset_path):
        if os.path.exists(F3D_PATH) and os.path.exists(asset_path):
            # Use the correct path format for Windows
            windows_path = asset_path.replace('/', '\\')
            subprocess.Popen([F3D_PATH, windows_path])
        else:
            nuke.message("F3D executable or asset path not found!")
    
    def create_readgeo_node(self, file_path):
        try:
            nuke_path = file_path.replace('\\', '/')
            read_geo = nuke.createNode("ReadGeo2")
            read_geo["file"].setValue(nuke_path)
            read_geo["display"].setValue("textured")
            read_geo["localizationPolicy"].setValue("on")
            read_geo["read_on_each_frame"].setValue(True)
            root_x = nuke.root().width() / 2
            root_y = nuke.root().height() / 2
            read_geo.setXYpos(int(root_x), int(root_y))
            self.status_label.setText(f"Created ReadGeo node: {os.path.basename(file_path)}")
        except Exception as e:
            self.status_label.setText(f"Error creating node: {str(e)}")
    
    def create_read_node(self, file_path):
        try:
            nuke_path = file_path.replace('\\', '/')
            read_node = nuke.createNode("Read")
            read_node["file"].setValue(nuke_path)
            root_x = nuke.root().width() / 2
            root_y = nuke.root().height() / 2
            read_node.setXYpos(int(root_x), int(root_y))
            self.status_label.setText(f"Created Read node: {os.path.basename(file_path)}")
        except Exception as e:
            self.status_label.setText(f"Error creating Read node: {str(e)}")
    
    def filter_assets(self, text):
        try:
            for i in range(self.grid_layout.count()):
                item = self.grid_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    for child in widget.findChildren(QtWidgets.QLabel):
                        if child.text() and not child.pixmap():
                            widget.setVisible(text.lower() in child.text().lower())
                            break
        except Exception as e:
            print(f"❌ Filter error: {e}")
    
    def go_back(self):
        parent = os.path.dirname(self.current_path)
        if os.path.exists(parent):
            self.load_assets(parent)
    
    def go_up(self):
        parent = os.path.dirname(self.current_path)
        if os.path.exists(parent):
            self.load_assets(parent)
    
    def go_home(self):
        self.load_assets(ASSET_DIR)
		
		
		
		
# ... (your existing ThreeDAssetBrowser class code) ...

# ADD THIS CODE RIGHT HERE, BEFORE THE PANEL REGISTRATION:

# Store the original setup_ui method
original_setup_ui = ThreeDAssetBrowser.setup_ui

# Define a new setup_ui method that adds the credit
def new_setup_ui(self):
    # Call the original setup_ui method first
    original_setup_ui(self)
    
    # Add credit label to the existing layout
    credit_layout = QtWidgets.QHBoxLayout()
    credit_layout.addStretch()  # This pushes the credit to the right
    credit_label = QtWidgets.QLabel("Crate v1.0 for Nuke by Nicolas Landajo")
    
    # Use the same font as the status label
    credit_label.setFont(self.status_label.font())
    credit_label.setStyleSheet("color: #4f4e4e;")
    
    credit_layout.addWidget(credit_label)
    self.layout().addLayout(credit_layout)

# Replace the original method with the new one
ThreeDAssetBrowser.setup_ui = new_setup_ui
		
		
		
			

# Register the panel (single click)
nukescripts.registerWidgetAsPanel(
    "ThreeDAssetBrowser",
    "Crate",
    "uk.co.studio.3d_browser_panel"
)

print("Crate registered - Ready in Pane menu!")