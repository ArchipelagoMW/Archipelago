@echo off
echo "-- Compiling objective spec"
py compile_objective_spec.py
echo "-- Compiling flagspec"
py compile_flagspec.py
echo "-- Transpiling flagset and logic cores"
py -m metapensiero.pj flagsetcore.py -o server/srcdata/flagsetcore.js
cd server
echo "-- Compiling UI spec"
copy ..\objective_data.py .
py compile_uispec.py
echo "-- Assembling JS all-in-one"
type srcdata\flagspec.js srcdata\flagsetcore.js srcdata\flagsetcorelib.js > script\flags.js
echo "-- Copying to versioned filename"
cd ..
FOR /F "usebackq delims=" %%i IN (`py -c "import version; import sys; sys.stdout.write('.'.join([str(i) for i in version.VERSION]))"`) DO set VERSION=%%i
copy server\script\flags.js server\script\flags-%VERSION%.js
