#!/usr/bin/python
import cgi;
import cgitb; cgitb.enable()
import webapp2


from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
from Bio.Alphabet import generic_rna

class MainPage(webapp2.RequestHandler):

	form = cgi.FieldStorage()
	targetDNA = cgi.escape(form.getfirst("targetDNA","").upper(),True)
	plasmidType = cgi.escape(form.getfirst("plasmidType",""),True)
	nt_length = cgi.escape(form.getfirst("nt_length",""),True)
	plasmidType = ''.join(plasmidType.split())
	targetDNA = ''.join(targetDNA.split())
	nt_length = ''.join(nt_length.split())
	if nt_length == "" : nt_length = 30
	if not nt_length.isdigit() : nt_length = 30
	nt_length = int(nt_length)
	nt_length = nt_length + 1
	breakLocation = targetDNA.find("*")
	breakLocation = int(breakLocation)
	topstrand5primeOverhang = ""
	topstrand3primeOverhang = "" 
	bottomstrand5primeOverhang = ""
	bottomstrand3primeOverhang = ""

	print "Content-type: text/html"
	print
	print "<html><head>"
	print ""
	print "</head><body>"
	print '<h2><i>cas9</i> DNA target spacer oligo generator</h2><form method="POST"><textarea rows="5" cols="40" name="targetDNA">'+targetDNA+'</textarea>'
	print '<br>Paste the DNA sequence area you wish to target, enter a * for the preferred location you wish to create the strand break. Note, the break will happen at the nearest NGG located upstream of the *.'
	print '<br><select name="plasmidType"><option value="Maraffini" selected>Maraffini Plasmids<option></select>'
	print '<br>Spacer size: <input name="nt_length" type="text" size="2" value="'+str(nt_length - 1)+'"> nucleotides'
	print '<input type=Submit></form>'
	print "<hr><br><pre>"
	print "nucleotides count = " +  str(len(targetDNA))
	targetDNA = targetDNA.translate(None, "*")
	PAMLocation = targetDNA.find('GG',breakLocation,len(targetDNA))
	thirtychars_before_selected_PAM = targetDNA[(PAMLocation-nt_length):PAMLocation-1]
	thirtychars_before_selected_PAM = thirtychars_before_selected_PAM
	print thirtychars_before_selected_PAM
	thirtychars_before_selected_PAM = Seq(thirtychars_before_selected_PAM, generic_dna)
	print thirtychars_before_selected_PAM.complement() + "   <--- Complement<br>Reverse Complement --->" +thirtychars_before_selected_PAM.reverse_complement()
	print "<table><tr><th><br>Oligos to synthesize:</th></tr>"
	if plasmidType == "Maraffini": topstrand5primeOverhang = "AAAC"; topstrand3primeOverhang="G"; bottomstrand5primeOverhang = "AAAAC"; bottomstrand3primeOverhang = "";
	print "<tr><td>5'- "+topstrand5primeOverhang+thirtychars_before_selected_PAM+topstrand3primeOverhang+" -3'</td></tr><tr/><tr/>"
	print "<tr><td><i><font color=#888888>3'- </font><font color=#CCCCCC>&nbsp;&nbsp;&nbsp;&nbsp;</font><font color=#888888>"+bottomstrand3primeOverhang+thirtychars_before_selected_PAM.complement()+bottomstrand5primeOverhang[::-1]+" - 5'</font></i></td></tr>" 
	print "<tr><td>5'- "+bottomstrand5primeOverhang+thirtychars_before_selected_PAM.reverse_complement()+bottomstrand3primeOverhang+" -3'</td></tr></table>"
	print "<br></pre><br></body></html>"

app = webapp2.WSGIApplication([('/helloworld', MainPage)],
				debug=True)