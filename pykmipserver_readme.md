README -- how to run PyKmip server


Generally speaking, you need to generate your own server and client certificates and then set the configuration options in the server.conf and pykmip.conf configuration files to point to those certificate files. 

To run the PyKmip server, we need to do four steps.
1. Generate a file named server.conf in the directory /etc/pykmip
As for the content, you should follow the template below. And please note that the pykmip.conf in the folder kmip is out-of-dated already, you can just ignore that file. 

[server]
hostname=127.0.0.1 
port=5696
certificate_path=/etc/rootca/intermediate/certs/server_certificate.pem
key_path=/etc/rootca/intermediate/private/server_key.pem
ca_path=/etc/rootca/certs/ca.cert.pem
auth_suite=Basic
policy_path=None

2. Generate your own CA, certificate and private key with openssl
For the "certificate_path","key_path" and "ca_path" you need to generate your own PEM files first and modify the path. 
First, you should generate a self-signed CA certificate along with its private key. You can then use this CA certificate to generate a server certificate (and its private key) and a client certificate (and its private key). 

* If you are an experienced developer, the link below supplies some commands you may need
https://www.sslshopper.com/article-most-common-openssl-commands.html
* If you are unfamiliar with this process, the link below is highly-recommend. 
Note that you should create the root pair firstly, then create the intermediate pair, and sign server certificate. https://jamielinux.com/docs/openssl-certificate-authority/create-the-root-pair.html

3. Execute #python bin/run_server.py
4. To test whether the server is running, you can try commands below.
* ps -ef | grep run_server.py  # see if "run_server.py" appears in the current process list
* netstat -an | grep 5696  # see if any processes are bound to port 5696
If those commands print anything, then it's the server is running.
