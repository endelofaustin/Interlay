[app]
title = Interlay
package.name = Interlay
package.domain = endelinterprises
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,md,txt,xml
source.include_patterns = SBLGNT/*,SBLGNT/data/sblgnt/text/*,SBLGNT/data/sblgnt/xml/*
source.exclude_dirs = venv,tests,previous_versions
version = 0.1
requirements = python3==3.11.2,kivy,certifi,charset-normalizer,distlib,docutils,filelock,idna,Kivy-Garden,kivymd,pexpect,pillow,platformdirs,ptyprocess,Pygments,requests,sh,urllib3,plyer
icon.filename = greek_bible_icon.png
orientation = portrait
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.minapi = 21
android.api = 31
android.ndk = 25b
android.ndk_path = ~/.buildozer/android/platform/android-ndk-r25b

[buildozer]
log_level = 2
warn_on_root = 1

