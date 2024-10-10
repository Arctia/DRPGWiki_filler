@REM @Author: arctia
@REM @Date:   2024-06-22
@REM @Last Modified by:   arctia
@REM Modified time: 2024-06-22

@echo off
setlocal

echo "Upload new translations"
python gst.py --refresh --update -u y

echo "Creating Frames"
cd "frame_builder"
python make_frames.py

echo Upload Images
cd ".."
python UploadImages.py

echo Uploading New characters to the wiki
python Character.py -u y -d j -i 302,304,20093,13,17,18,19,292,20001 -c r

echo Update List Tables
python CharaTable.py -u y -d j
python CharaSymbol.py -u y -d j
python CharaRelease.py -u y -d j
python CharaList.py -u y -d j
python Ampoule.py -u y -d j

echo Remove New Characters from PLibs
python MoveNewCharacters.py

endlocal