echo "creating frames"
cd "frame_builder"
python3 make_frames.py
cd ".."
echo "uploading Images..."
python3 UploadImages.py
echo "uploading Character/s..."
python3 Character.py -u y -d j -i 1,2 -c r
echo "uploading Secondary Tables..."
python3 CharaTable.py -u y -d j
python3 CharaSymbol.py -u y -d j
python3 CharaRelease.py -u y -d j
python3 CharaList.py -u y -d j
cd "plibs"
python3 MoveNewCharacters.py