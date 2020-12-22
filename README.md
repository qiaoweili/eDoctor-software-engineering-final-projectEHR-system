# eDoctor-software-engineering-final-project-EHR-system

Our project is basically an EHR system which is named as E-doctor system. 

According to the definition of EHR system, EHR system is viewed as a digital vision of health records, 
and its most obvious characteristic is real-time and patient-oriented. 

Not only does the EHR system help offer detailed records of a patient’s medical inquiry history, 
but it also offers a broader overview of the patient so as to help doctors 
nd even patients himself get command of a patient's personal condition faster and much fully.

Based on this definition, our group initially separated the system into two major parts:
real-time data update and patient’s past medical record history. 

In terms of real-time data, we conducted two separate pages for doctors to write in-process diagnosis and correct detailed information for the patients, including weight, height, allergies and etc. 
In terms of past medical record history, we used another page within connection with the back-end database, and the medical records can be searched by keywords which adds large convenience to medical records.


### Main functions:
Login/ register/ logout

userinfo/ recent activities

profile change (find *Change Profile* page at top right corner, mouse hover over account)

current diagnose (only used by doctor)

Past Records (listing all past records related to the user)

### Testing
test.py/ gen.py: for account auto generation & login/logout auto test (by: Chanel & Qiaowei)

auth_test.py/data_test.py/record_test.py: unittests for each function (by: Hannah)

### Pydoc documentation
To use Pydoc module to see code documentation, set *lib* folder as source folder with the entire project.

type in: \
*python3 -m pydoc main*\
if the file is in root repository,\
else:\
*python3 -m pydoc api/auth.py*

### Contributors: 
*Edmund*: \
Front-end worker\
HTML & Layui

*Chanel & Qiaowei*:\
structure worker (Pair programming)\
mySQL->mongodb & Robot3t\
Part of basic front-end, Layui \
Js,py files conduction\
Iteration recorder \
Testing (random generation part)

*Hannah*: \
Process-check person\
Profile/ search function co-editor\
Testing(unittest part)\
Check whether we have reached our weekly goals








