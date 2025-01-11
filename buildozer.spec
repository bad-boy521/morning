[app]
title = 早安晚安
package.name = goodmorningnight
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
source.include_patterns = assets/*,screens/*,utils/*
version = 1.0

requirements = python3,kivy==2.2.1,pillow,requests,certifi,schedule

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.arch = arm64-v8a
android.accept_sdk_license = True

android.add_assets = assets/
android.add_src = screens/:utils/

orientation = portrait
fullscreen = 0
android.wakelock = True

[buildozer]
log_level = 2
warn_on_root = 0  