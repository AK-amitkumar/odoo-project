from umalqurra.hijri_date import HijriDate
import pandas as pd
import numpy as np
from datetime import date


# df = pd.read_csv('Ksa_Emp.csv')
# exp = df['DATE OF EXPIRY']
# um = HijriDate()
c_list = []

# for x in exp:
# 	um.set_date(int(' '.join(x.split('/')[2:3])),int(' '.join(x.split('/')[1:2])),int(' '.join(x.split('/')[:1])))
# 	c_date = str(int(um.year_gr)) + "-" + str(int(um.month_gr)) + "-" + str(int(um.day_gr))
# 	c_list.append(c_date)

# dff = pd.DataFrame(c_list)
# dff.to_csv('exp.csv', sep='\t', encoding='utf-8')

	
# print (c_date)
# print (um.day_gr)
# print (um.month_gr)
# print (um.year_gr)



df = pd.read_csv('employee_imported.csv')
job_idd = df['department_id/id']

for x in job_idd:
	c_list.append("__export__.hr_department_" + str(int(filter(str.isdigit, x))))

dff = pd.DataFrame(c_list)
dff.to_csv('deprt.csv', sep='\t', encoding='utf-8')