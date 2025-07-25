# Unzip the apk to analyse the individual files
unzip timer.apk -d unzipped

# Use cd to enter the unzipped folder
cd unzipped

# Check if the flag is hidden in plaintext in any of the unzipped files
grep -rw picoCTF .

# From the above command, the picoCTF string was found in classes3.dex

# strings classes3.dex and grep it to retreive the flag
strings -t x classes3.dex | grep picoCTF