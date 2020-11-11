import base64


def D_BASE64(origStr):
    # base64 decode should meet the padding rules
    missing_padding = 4 - len(origStr) % 4
    if missing_padding:
        origStr += '=' * missing_padding
    return origStr


str = 'eyJ0b2tlbkV4cHJpcmVBdCI6IjE2MDQ4ODY2ODc4NDEiLCJyZXF1c2VyRXhwcmlyZUF0IjoiMTYwNDg4ODQ4Nzg0MSIsInVzZXJJZCI6IjExMzU1NDI0NTY1MjY1NDg0Iiwibmlja05hbWUiOiLnv5_njrIiLCJjZW50ZXJJZCI6Ijk3ODM0ODg3MTkwNDE5NDMzNCIsImltZ0hlYWQiOiJodHRwczovL2RzczIuYmFpZHUuY29tLzZPTllzamlwMFFJWjh0eWhucS9pdC91PTI5NDQ4NTg2NTUsMzI2MDYxMTMyOCZmbT01OCIsInBob25lIjoiMTU2NzU2NzAzODMiLCJpbnRlZ3JhdGlvbkN1cnJlbnRBbW91bnQiOiI0NjUyIiwidXNlckxldmVsIjoiNSIsImxldmVsVGl0bGUiOiLpkrvnn7NPbmVPU2VyIn0='
print(len(str)%4)
temp = base64.urlsafe_b64decode(D_BASE64(str))
# 同样的，解码后的结0果是二进制，我们再转换一下
print(temp)
print('解密后的结果 --> ', eval(temp))
