import sys
import os
import csv
import polib
import glob

csv_metadata = 'metadata.csv'
csv_translation = 'translation.csv'
my_encodeing = 'utf_8_sig'
my_po_name = 'export.po'

def po2csv():
    for name in glob.glob('data/po/*/*.po'):
        po = polib.pofile(name)
        path = 'data/csv/{}/'.format(po.metadata['Language'])
        os.makedirs(path, exist_ok=True)
        # メタデータ
        with open(path + csv_metadata, 'w', newline='', encoding=my_encodeing) as csvfile:
            writer = csv.writer(csvfile)
            for row in po.metadata:
                print("{}:{}".format(row, po.metadata[row]))
                writer.writerow([row, po.metadata[row]])
        # 翻訳データ
        with open(path + csv_translation, 'w', newline='', encoding=my_encodeing) as csvfile:
            writer = csv.writer(csvfile)
            for entry in po:
                writer.writerow([entry.msgctxt ,entry.msgid, entry.msgstr])

def csv2po():
    for name in glob.glob('data/csv/*/'):
        po = polib.POFile()
        dict = {}
        # メタデータ
        with open(name + csv_metadata, 'r', encoding=my_encodeing) as metadata:
            reader = csv.reader(metadata)
            dict = {rows[0]:rows[1] for rows in reader}
        po.metadata = dict
        # 翻訳データ
        with open(name + csv_translation, 'r', encoding=my_encodeing) as translation:
            reader = csv.reader(translation)
            for row in reader:
                entry = polib.POEntry(msgctxt=row[0], msgid=row[1], msgstr=row[2])
                po.append(entry)
        
        path = 'data/export/{}/'.format(po.metadata['Language'])
        os.makedirs(path, exist_ok=True)
        os.chmod(path, mode=0o755)
        #poファイル書き出し
        po.save(path + my_po_name)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} <po2csv|csv2po>'.format(sys.argv[0]))
        sys.exit(1)
    if sys.argv[1] == 'po2csv':
        po2csv()
    elif sys.argv[1] == 'csv2po':
        csv2po()