echo "uploading Images..."
py UploadImages.py
echo "uploading Character/s..."
py Character.py -u y -d j -i 221,222,224,20072,225 -c r
echo "uploading Secondary Tables..."
py CharaTable.py -u y -d j
py CharaSymbol.py -u y -d j
py CharaRelease.py -u y -d j