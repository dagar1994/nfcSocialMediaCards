import requests
import subprocess

def commandExecute(command):
        process = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = process.communicate()
        SUCCESS_OUTPUT=stdout
        ERROR_OUTPUT=stderr
        EXIT_CODE=process.returncode
        PROCESS_ID=process.pid
        return (SUCCESS_OUTPUT,ERROR_OUTPUT,EXIT_CODE,PROCESS_ID)


size = "150x150"
color = "ffdc7d"
url = "http://127.0.0.1:5000/youtube/ctyt2/admin"
request = requests.get("https://api.qrserver.com/v1/create-qr-code/?size=" + size + "&data=" + url + "&color=" + color)
request.content

with open("qr.png","w") as f:
	f.write(request.content)

commandExecute("convert qr.png -fuzz 20% -transparent white qr.png")
