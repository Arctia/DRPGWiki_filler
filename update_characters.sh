echo "creating frames"
cd "frame_builder"
python3 make_frames.py
cd ".."
echo "uploading Images..."
python3 UploadImages.py
echo "uploading Character/s..."
python3 Character.py -u y -d j -i 276,20085,278,20084,29,138,242,160,20047,130,181,191,20041,20064,20049,99,100,158,159,20050,20066 -c r
echo "uploading Secondary Tables..."
python3 CharaTable.py -u y -d j
python3 CharaSymbol.py -u y -d j
python3 CharaRelease.py -u y -d j
python3 CharaList.py -u y -d j
cd "plibs"
# python3 MoveNewCharacters.py