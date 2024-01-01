echo "creating frames"
cd "frame_builder"
py make_frames.py
cd ".."
echo "uploading Images..."
py UploadImages.py
echo "uploading Character/s..."
py Character.py -u y -d j -i 251,250,252,253,256,254,257,255,258,259,262,263,260,264,261,60,61,136,137,20063,203,16,148,199,200,201,202,204,205,206,208,242,20012 -c r
echo "uploading Secondary Tables..."
py CharaTable.py -u y -d j
py CharaSymbol.py -u y -d j
py CharaRelease.py -u y -d j
py CharaList.py -u y -d j
cd "plibs"
py MoveNewCharacters.py