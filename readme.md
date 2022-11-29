### Assignment 1 Solution:

###### Maintainer: Ganesh Patil

### 1. Environment:
- Program Created using Python- 3.10
- Install the dependencies using **requirements.txt** using below command:
````
$ pip install -r requirements.txt
````
- Export Gmail credentials as ENV variables and use below name:
  - EMAIL_ID - for sender email
  - EMAIL_APP_PASSWORD - for sender password
  
- **Gmail does not accept username and password now**
- We Need to create Application specific password from gmail settings. 
  then only we will be able to send email.
- Create App Password for using Gmail SMTP service
- Please check following sites for reference:
  - https://support.google.com/accounts/answer/6010255?hl=en
  - https://support.google.com/accounts/answer/185833

--------

### 2. Execution:
For executing the program run below command:
````
$ python main.py
````
- Execution sequence:
  1. Fetching the data from dummyjson site
  2. Asking user how to sort data (by **title** or **price**)
  3. Sorting the data after user enter his choice
  4. Saving the sorted data in local
  5. Asking user whether to share data via email 
     1. If Yes then share file via email
     2. If No then print the path of file in local

- Sample execution 1:
  ````
  $ python main.py  
  How do you want to sort the data? 'TITLE' Or 'PRICE'? title
  Do you want to share file via email? (YES/NO): yes
  File is shared via email
  ````
- Sample execution 2:
  ````
  $ python main.py
  How do you want to sort the data? 'TITLE' Or 'PRICE'? price
  Do you want to share file via email? (YES/NO): no
  Result file is stored on below path:
  C:\Users\Ganesh_Patil\Desktop\results\products.txt
  ````
--------

### 3. Testcases:
Run below command for running test cases: 
````
$ python -m unittest discover
````

--------

#### Note: Please do not delete mock_objects folder