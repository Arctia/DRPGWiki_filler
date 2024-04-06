
python3 gst.py --all 
cd plibs
python3 extract.py
python3 new_units.py

cp config.json ./assets/
rm path.tar.gz
tar czfv patch.tar.gz assets/
echo "please upload patch.tar.gz to the url Arctia sent to you"

cd ..
