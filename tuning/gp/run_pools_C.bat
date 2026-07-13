@echo off
cd /d E:\PycharmProjects\DeepLJSP
venv\Scripts\python.exe scripts\gen_missing_pools.py --classes 15_15,20_15,20_20,30_15,30_20 --generators gp,gtmwkr --ft10 > seeds_gen_C.log 2>&1
