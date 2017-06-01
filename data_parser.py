import pickle
import csv
import time
from datetime import datetime


data = pickle.load(open('data_copy.p', 'rb'))

csv_file = open('csv_data_%s-%s_(%s).csv' % (time.localtime()[1], time.localtime()[2], time.localtime()[3]), 'w')
csv_out = csv.writer(csv_file)
csv_out.writerow(['ID', 'HOUR', 'MINUTE', 'SCORE'])

for data_tup in data:
    csv_out.writerow(data_tup)
print('Done.')