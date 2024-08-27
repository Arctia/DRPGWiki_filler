@REM @Author: arctia
@REM @Date:   2024-06-22
@REM @Last Modified by:   arctia
@REM Modified time: 2024-06-22

@echo off
setlocal

echo Scraping new data
cd datas
python scrape.py
cd ..

echo Refreshing translation data
python gst.py --all --refresh
echo

echo Extracting new images
cd plibs
python extract.py
python new_units.py

endlocal