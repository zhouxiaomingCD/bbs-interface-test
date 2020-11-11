import requests

accesskey = 'eyJhbGciOiJIUzI1NiJ9.eyJ0b2tlbkV4cHJpcmVBdCI6IjE2MDQ1NDc2NDQ1MzQiLCJyZXF1c2VyRXhwcmlyZUF0IjoiMTYwNDU0OTQ0NDUzNCIsInVzZXJJZCI6IjExNjEzODg3NDI1NDA3MjczIiwibmlja05hbWUiOiLmooHlh6Toi7EiLCJjZW50ZXJJZCI6IjIxNDA5MTg4ODI5Nzc1Njg5MiIsImltZ0hlYWQiOiJodHRwczovL2RzczIuYmFpZHUuY29tLzZPTllzamlwMFFJWjh0eWhucS9pdC91PTI5NDQ4NTg2NTUsMzI2MDYxMTMyOCZmbT01OCIsInBob25lIjoiMTMzMjc4ODc4MTgiLCJpbnRlZ3JhdGlvbkN1cnJlbnRBbW91bnQiOiI0NTA2IiwidXNlckxldmVsIjoiNSIsImxldmVsVGl0bGUiOiLpkrvnn7NPbmVPU2VyIn0.3voMHW9ceJmz8flbCjIaB7lOixjtE7Up_rxsX4dbFmY'

headers = {
    "accesskey": accesskey
}
url = "https://test.os.cmiotcd.com:28443/forum/consumer/api/collection/post/addCollection"
data = {
    'operation': 1, 'postId': 46242154850570240, 'topicId': '0'
}
res = requests.post(url=url, json=data, headers=headers)
print(res.json())
