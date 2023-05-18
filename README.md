# secure_cloud_storage
# PROBLEM STATEMENT:
In the current era, there is an exponentially growing volume of sensitive data that individuals and 
organizations need to store and access remotely. Many current cloud storage solutions do not 
possess sufficient security measures to guarantee data confidentiality and integrity, which results 
in users being exposed to risks such as cyber-attacks, data breaches, and unauthorized access. To 
solve this problem, we are proposing a project to design and implement a secure cloud storage 
system that provides users with the ability to upload and download files in a user-friendly manner 
while ensuring data confidentiality and integrity. This system utilizes advanced security techniques 
such as encryption, access control, and authentication to guarantee that only authorized individuals 
can access files and that files are not altered or corrupted during transfer. With the successful 
implementation of this system, users can confidently upload and download files from anywhere, 
at any time, with the assurance that their data is being protected and only accessible by authorized 
personnel.
# DESIGN:
The system has the following components,
o Web application
o Cloud storage service
o Database
The interactions between the components are illustrated in the following diagram,
Figure 1: System Design
It has the following functionalities,
• File Upload:
When a user uploads a file to the system,
o The file will be encrypted using the Fernet algorithm. It uses the same key for 
encryption and decryption, hence it is a symmetric encryption algorithm.
o The encrypted file will be uploaded to AWS S3, where it will be stored securely.
• File Download:
When a user wants to download a file,
o The user will enter the file name and encryption key.
o Post authentication, the file will be downloaded from AWS S3 and decrypted using 
the encryption key.
o The user will be able to view the original contents of the file.
• Access Control:
To manage access control, the system will store a mapping record of each file and its 
encryption key in an SQLite database. 
• Security:
The system will use encryption and access control to ensure data confidentiality and data 
integrity.
o Fernet encryption algorithm
o Authentication to assure that only authorized users has system access.
o Access control to guarantee that only authorized individuals have access to the files.
• User Interface
The system has a user-friendly interface through which the users can easily upload and 
download files securely. It includes the following features:
o A file upload form that allows users to select files to upload.
o A file download form that allows users to search for and download files.
# IMPLEMENTATION:
The project is implemented using Flask, which is a Python web framework. It also utilizes Amazon 
S3, a cloud service for file storage and SQLite, a lightweight database. The system employs the 
Fernet encryption algorithm, a secure symmetric encryption algorithm, to encrypt files during the 
storage process. The algorithm ensures that only authorized users can download the files. The file 
transfers to and from Amazon S3 are handled securely by the boto3 module of the AWS SDK. The 
information about uploaded files, including the file name and encryption key, is stored in a SQLite 
database. It is a lightweight, file-based database which is easy to maintain, making it ideal for this 
type of system. Overall, the amalgamation of these tools creates a secure and user-friendly 
mechanism to access and store the user files. 
