import subprocess

#fw = open("tmpout", "wb")
#fr = open("tmpout", "r")

p = subprocess.Popen("R", stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, bufsize = 1)
p.stdin.write(("print('Rworking')").encode())