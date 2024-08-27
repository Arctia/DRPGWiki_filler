
cd datas
python3 scrape.py
cd ..

python3 gst.py --all --refresh
echo
cd plibs
python3 extract.py
python3 new_units.py

cp config.json ./assets/
rm patch.tar.gz
echo "compressing new assets"
tar czf patch.tar.gz assets/
echo "please upload patch.tar.gz to Arctia if something is goin wrong"
echo "now open result.xlxs in translation_sheet and copy the new/modded" "columns to the online spreadsheet"
cd ..
