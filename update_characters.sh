python3 gst.py --refresh --update -u y
echo "creating frames"
cd "frame_builder"
python3 make_frames.py
cd ".."
echo "uploading Images..."
python3 UploadImages.py
echo "uploading Character/s..."
# 301,298,299,6,7,234,236,20017,75,188,241,242
python3 Character.py -u y -d j -i 302,304,20093,13,17,18,19,20001 -c r
echo "uploading Secondary Tables..."
python3 CharaTable.py -u y -d j
python3 CharaSymbol.py -u y -d j
python3 CharaRelease.py -u y -d j
python3 CharaList.py -u y -d j
python3 Ampoule.py -u y -d j
cd "plibs"
python3 MoveNewCharacters.py