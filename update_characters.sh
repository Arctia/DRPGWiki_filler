echo "uploading Images...\n"
py UploadImages.py
echo "uploading Character...\n"
py Character.py -u y -d j -i XXX,YYY -c r
echo "uploading Secondary Tables...\n"
py CharaTable.py -u y -d j
py CharaSymbol.py -u y -d j
py CharaRelease.py -u y -d j