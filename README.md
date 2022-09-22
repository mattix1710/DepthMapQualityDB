# DepthMapQualityEstDB
Evaluation database for depth maps estimation (Django: Python)

***
TODO - before starting server (if no database file in the project)
-------------------
* <span style="color:#26867C"><b>create admin account</b></span>
    > py manage.py createsuperuser<br>
    > Username: admin<br>
    > Email address: _your_email_<br>
    > Password: _your_password_
* <span style="color:#26867C"><b>create database</b></span>
    > py manage.py migrate<br>
    > py manage.py makemigrations

***
* <span style="color:#f1c232"><b>starting a server</b></span>
    > py manage.py runserver

***
EXECUTION of BATCH files
--------------------
while calling BATCH file - current absolute path is the path that was entered in terminal<br>
i.e. 

* terminal PATH is: <em>DepthMapQualityDB/depth_grader/</em>
* BAT file PATH is: <em>DepthMapQualityDB/depth_grader/depthQualifier/src/testBatch.bat</em>

**then commands written on .bat file will be executed as on "terminal PATH"**

***
TODO - while inserting/running server
--------------------
* unpack "ffmpeg.exe" file from "ffmpeg.zip" archive
* * this file is located in **DepthMapQualityDB\depth_grader\depthQualifier\src\media_handling\\** location
* check TERMINAL path
* * BATCH files depend on the terminal path:<br>
i.e. access to **/media/** folder