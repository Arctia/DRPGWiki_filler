echo "creating frames"
cd "frame_builder"
py make_frames.py
cd ".."
echo "uploading Images..."
py UploadImages.py
echo "uploading Character/s..."
py Character.py -u y -d j -i 28,231,232 -c r
echo "uploading Secondary Tables..."
py CharaTable.py -u y -d j
py CharaSymbol.py -u y -d j
py CharaRelease.py -u y -d j
py CharaList.py -u y -d j