import subprocess
from flask import Flask, render_template, request
from csv import writer, reader
from shutil import copyfile, copytree, rmtree
import os
from binascii import hexlify


app = Flask(__name__)

admin_key = "sctf{c5v_sh0u1dNt_hv_Tru5t3d_y4}"

ctf_cats = {"pwn":"Pwn","web":"Web Exploitation","crypto":"Cryptography","forens":"Forenics","rev":"Reverse Engineering","osint":"Osint","misc":"Misc"}
award_cats = {"best":"Best category - Where more x challs?","worst":"Worst Category - Should be removed","easiest": "Easiest Category - Too EZ","hardest":"Hardest Category - Git gud"}
votes = {}

# set up vote count
for award_cat in award_cats.keys():
    votes[award_cat]= [1]*7

def analyse_vote(filename):
    # read the vote 
    with open(filename,'r') as f:
        rows = list(reader(f))
        vote = rows[3]

    # delete the submission form
    if os.path.exists(filename):
        os.remove(filename)
        
    # add the vote to the count if the vote is verified
    if vote[2] == admin_key:
        try:   
            votes[vote[1]][list(ctf_cats.keys()).index(vote[0])] += 1
            log = "Thank you! Your vote has been counted."
        except:
            log = "Sorry! An error occurred in your vote."
    else:
        log = "Sorry! An error occurred in your vote."
    
    return log


@app.route('/',methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # get the user's vote
        ctf_cat = request.form.get("ctf_cat")
        award_cat = request.form.get("award_cat")
        ctf_cat.replace(',','')
        award_cat.replace(',','')

        # create a new submission sheet
        id = hexlify(os.urandom(24)).decode()
        filename = "submissions/submissions-" + id + ".csv"
        copyfile("submissions/submissions.csv",filename)

        # populate with the user's vote
        with open(filename, 'a') as f:
            writer_obj = writer(f)
            writer_obj.writerow([ctf_cat,award_cat,"NIL"])
            f.close()
        
        # verify the vote
        copytree('/home/ctf/.config/libreoffice/4/user', '/tmp/user-'+id+'/user')
        subprocess.Popen(['libreoffice', '--headless', '-env:UserInstallation=file:///tmp/user-'+id,'--infilter="Text - txt - csv (StarCalc):44,34,0,1,,0,,,,,,,true,,true"',filename,'macro:///Standard.Module1.Main'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).communicate()
        rmtree('/tmp/user-'+id)

        # read and analyse the vote
        log = analyse_vote(filename)

        # render results
        return render_template('index.html',award_cats=award_cats,ctf_cats=ctf_cats,log=log)
    
    return render_template('index.html',award_cats=award_cats,ctf_cats=ctf_cats)


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0',threaded=True)
