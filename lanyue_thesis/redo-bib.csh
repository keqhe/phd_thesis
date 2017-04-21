#! /bin/csh -f

set file = $argv[1]

awk '{p=0} /begin/ {print $0; print ""; print "\\setlength{\\baselineskip}{0mm}"; print "\\setlength{\\partopsep}{0mm}"; print "\\setlength{\\parskip}{0mm}"; print "\\setlength{\\parsep}{0mm}"; print "\\setlength{\\listparindent}{0mm}"; print ""; p=1} (p==0) {print $0}' $file.bbl > /tmp/$file.bbl

cp -f /tmp/$file.bbl $file.bbl



