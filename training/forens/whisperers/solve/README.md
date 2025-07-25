1. Open the file in Wireshark
2. Notice that there are two HTTP packets:
   - The first one is a request to the server
   - The second one is the response from the server
3. The response contains the flag in the body of the packet. Double-click on the response (`244 HTTP/1.1 200 OK`), and view the `Line-based text data`, and you should see the flag.