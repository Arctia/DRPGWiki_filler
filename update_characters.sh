echo "creating frames"
cd "res/DRPGWiki"
py make_frames.py
cd "../.."
echo "uploading Images..."
#py UploadImages.py
echo "uploading Character/s..."
py Character.py -u y -d j -i 176,223,226,229,20073 -c r
echo "uploading Secondary Tables..."
py CharaTable.py -u y -d j
py CharaSymbol.py -u y -d j
py CharaRelease.py -u y -d j