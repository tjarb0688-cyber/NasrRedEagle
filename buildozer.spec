[app]

# (str) Title of your application
title = Nasr Red Eagle

# (str) Package name
package.name = nasrredeagle

# (str) Package domain (needed for android/ios packaging)
package.domain = org.nasrredeagle

# (str) Source code where the main app live
source.dir = .

# (list) Application requirements
requirements = python3,kivy

# (str) Supported Android API level to use.
android.api = 33

# (str) Minimum Android SDK version to use
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Version code
version.code = 1

# (str) Version string
version = 1.0

# (str) Build tools version
android.build_tools_version = 34.0.0

[buildozer]

# (int) Log level (0=error only, 1=info, 2=debug)
log_level = 2

# (str) Path to build artifact storage
bin_dir = bin

# (str) Path to cache directory
cache_dir = .buildozer
