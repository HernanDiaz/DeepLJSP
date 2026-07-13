@echo off
cd /d E:\PycharmProjects\DeepLJSP
venv\Scripts\python.exe scripts\gen_missing_pools.py --classes 50_15,50_20 --generators gp > seeds_gen_A.log 2>&1
