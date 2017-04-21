# Make this OS specific

switch (uname)
    case Darwin
       # Redoing figure captions for OSDI figures. OSDI figures have slightly different formats
      sed -i '' 's/\(\\\\contentsline {figure}.*\){.*bf \(.*}\).*fontsize.*.fontsize.*\({[0-9]*}{figure.*}\)/\1{\2}}\3/' dissertation.lof
      # Redoing figure captions for other figures.
      sed -i '' 's/\(\\\\contentsline {figure}.*\){.*bf \(.*}\).*fontsize.*\({[0-9]*}{figure.*}\)/\1{\2}}\3/' dissertation.lof
      # Redoing table cpations. Slightly different for OSDI.
      sed -i ''  's/\(\\\\contentsline {table}.*\){.*bf \(.*}\).*fontsize.*\({[0-9]*}{table.*}\)/\1{\2}}\3/' dissertation.lof
      sed -i '' 's/\(\\\\contentsline {table}.*\){.*spaces \(.*}\).*fontsize.*\({[0-9]*}{table.*}\)/\1{\2}}\3/' dissertation.lof
     # removing empty lines after the first
     sed -i '' '2,${;/^.*addvspace.*$/d;}' dissertation.lof
     tail dissertation.lof
   case Linux
       # Redoing figure captions for OSDI figures. OSDI figures have slightly different formats
      sed -i 's/\(\\\\contentsline {figure}.*\){.*bf \(.*}\).*fontsize.*.fontsize.*\({[0-9]*}{figure.*}\)/\1{\2}}\3/' dissertation.lof
      # Redoing figure captions for other figures.
      sed -i 's/\(\\\\contentsline {figure}.*\){.*bf \(.*}\).*fontsize.*\({[0-9]*}{figure.*}\)/\1{\2}}\3/' dissertation.lof
      # Redoing table cpations. Slightly different for OSDI.
      sed -i 's/\(\\\\contentsline {table}.*\){.*bf \(.*}\).*fontsize.*\({[0-9]*}{table.*}\)/\1{\2}}\3/' dissertation.lof
      sed -i 's/\(\\\\contentsline {table}.*\){.*spaces \(.*}\).*fontsize.*\({[0-9]*}{table.*}\)/\1{\2}}\3/' dissertation.lof
     # removing empty lines after the first
     sed -i '2,${;/^.*addvspace.*$/d;}' dissertation.lof
     tail dissertation.lof
end
