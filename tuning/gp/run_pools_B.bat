@echo off
cd /d E:\PycharmProjects\DeepLJSP
venv\Scripts\python.exe scripts\gen_missing_pools.py --classes 50_15,50_20 --generators gtmwkr > seeds_gen_B.log 2>&1
