from flask import Flask
import boto3
from flask import flash
import sqlite3
from flask import request
import os
from flask import send_file
import hashlib
from cryptography.fernet import Fernet
from flask import render_template
import base64
from flask import make_response
from flask import url_for
import tempfile
from flask import redirect
from sqlite3 import Error



app = Flask(__name__)

# setting up the upload file path and AWS secret key
app.config['UPLOAD_FOLDER'] = '/Users/priyankadhananjayareddy/Desktop/awsSpl/upload'
app.config['SECRET_KEY'] = 'hsouFp1YCW9nJBALsBtobahPCkgXXqrxSUixnOKv'


s3_handle = boto3.client('s3', aws_access_key_id='AKIAWLO7BZGRPNLHL2FN', aws_secret_access_key='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')
keydict = {}

# Generate encryption key
key = Fernet.generate_key()

# Initialize encryption cipher
cipher_suite = Fernet(key)

# API to create DB connection
def create_db_connection():
    conx_handle_db = None
    try:
        conx_handle_db = sqlite3.connect('file_db.sqlite')
        return conx_handle_db
    except Error as msg:
        print(msg)
    return conx_handle_db


# API to create SQLite table
def create_db_table(connection):
    create_table_command = """ CREATE TABLE IF NOT EXISTS files (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        file_name TEXT NOT NULL,
                                        file_key BLOB NOT NULL
                                    ); """
    try:
        connection_handle = connection.cursor()
        connection_handle.execute(create_table_command)
    except Error as error_msg:
        print(error_msg)

# API to encrypt data
def encrypt_data(data):
    decoded_data = data.decode('latin-1')
    return cipher_suite.encrypt(decoded_data.encode())

# API to decrypt data
def decrypt_data(decryption_data, decryption_key):
    cipher_handle = Fernet(decryption_key)
    return cipher_handle.decrypt(decryption_data).decode()

# API to upload file to AWS S3
def file_upload(file, bucket_name, encryption_key):
    s3_handle.upload_file(file, bucket_name, encryption_key)

# API to download file from AWS S3
def file_download(bucket_name, decryption_key):
    s3_handle.download_file(bucket_name, decryption_key, 'tmp')

# Landing-page route definition
@app.route('/')
def home():
    return render_template('home.html')

# Define route for file upload
method_list = ['GET', 'POST']
@app.route('/upload', methods=method_list)
def upload():
    # to handle POST method
    if request.method == 'POST':
        fle_handle = request.files['file']
        file_content = fle_handle.read()
        encrypted_content = encrypt_data(file_content)
        md5_hash = hashlib.md5(encrypted_content).hexdigest()


        # write encrypted content to a temporary file
        temp_handle = os.path.join(app.config['UPLOAD_FOLDER'], fle_handle.filename)
        fle = open(temp_handle, 'wb')
        fle.write(encrypted_content)
        file_upload(temp_handle, 'fileuploadencryption', fle_handle.filename)

        conn = create_db_connection()
        with conn:
            create_db_table(conn)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO files (file_name, file_key) VALUES (?,?)",
                           (fle_handle.filename, key))
            conn.commit()

        keydict[fle_handle.filename] = key
        os.remove(temp_handle)

        # render success message
        return render_template('success.html', key=key)
    # redirect to upload page
    return render_template('upload.html')

# Define route for file download
method_list = ['GET', 'POST']
@app.route('/download', methods=method_list)
def download():
    # handle POST request
    if request.method == 'POST':
        fle_nme_handle = request.form['file_name']
        fle_key = request.form['file_key']

        
        conx = create_db_connection()
        with conx:
            curser = conx.cursor()
            curser.execute("SELECT file_key FROM files WHERE file_name = ?", (fle_nme_handle,))
            row = curser.fetchone()
            if row and str(row[0]) == fle_key:
                key = row[0]
                file_download('fileuploadencryption', fle_nme_handle)
                with open('tmp', 'rb') as f:
                    file_content = f.read()
                    decrypted_content = decrypt_data(file_content, key)
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file_handle:
                        temp_file_handle.write(decrypted_content.encode())
                        temp_file_handle.flush()
                        temp_file_handle.seek(0)
                    flash('File downloaded successfully!', 'success')
                    redirect(url_for('download_success'))
                    response = make_response(send_file(temp_file_handle.name, as_attachment=True))
                    response.headers['Content-Disposition'] = f'attachment; filename="{fle_nme_handle}"'
                    # return the response
                    return response
            else:
                flash('Invalid file name or file key!', 'error')

    return render_template('download.html')


# Define route for success page after file download
@app.route('/downloadsuccess')
def download_success():
    return render_template('downloadsuccess.html')

# app start point
if __name__ == '__main__':
    app.run(debug=True)