### Q&A: Assignment 1

#### 1. Write a program in python to fetch data and process
- Please find the instructions to run the program inside **readme.md** file

--------

#### 2. Explain how to package this program to run on different machines/ servers?
1. Deploy as Lambda function (Can be triggered using EventBridge or some API call, etc)
     - It is managed service, so we just need to select Runtime (Python) and for dependencies
       we need to use Lambda Layers OR Need library in zipped format in local dir of Lambda on AWS.
2. Package code using **.tar.gz** or **.zip** and copy to EC2 using scp and run it there.
   - Need to have Python and Pip install, then install dependencies (shown in Readme.md file).
3. Create a repository on GitHub, Push the code. Go to the server where you want to execute this,
    Pull the code and Execute.
   - Need to have git installed and also need to install python and dependencies using pip.
4. Write a Dockerfile, Build docker image from it. Push docker image to Dockerhub or ECR,
    then pull that docker image and run it inside EC2 or any server
   - Need to have Docker installed (Dependencies will be installed inside a container)
5. Deploy as Glue function
   - It is managed service, so we just need to select Runtime (Python or Pysprak)
6. Deploy within a cluster for distributed processing (e.g. EMR)

--------

#### 3. Explain what libraries (both standard/ external) you considered to make this program?
- Internal Modules:
  - typing - for type hints
  - os - to create folder and check if folder/file present or not, also to read ENV variables
  - json - to convert json response to python object
  - http.client.responses - to show proper http status codes in redable format
  - csv - to write dictionaries to tsv file (delimiter='\t')
  - smtplib - to send email
  - email.mime.multipart - to attach files to email
  - unittest - for unit testing
- External Libraries:
  - requests - used as http client to fetch data from Web.

--------

#### 4. Explain how to run this program.?
- Please find the instructions to run the program inside **readme.md** file

--------

#### Note: Please do not delete files present in mock_data folder