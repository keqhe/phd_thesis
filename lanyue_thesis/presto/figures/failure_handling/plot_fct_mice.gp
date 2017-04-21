# Note you need gnuplot 4.4 for the pdfcairo terminal.

#set terminal pdfcairo font "Gill Sans,9" linewidth 4 rounded
#set terminal pdf enhanced color 'Roman,30'  linewidth 2 rounded
set terminal pdf font "Gill Sans,19" enhanced

# Line style for axes
set style line 80 lt rgb "#808080"

# Line style for grid
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

set grid back linestyle 81
#set border 3 back linestyle 80 # Remove border on top and right.  These
             # borders are useless and make it harder
             # to see plotted lines near the border.
# Also, put it in grey; no need for so much emphasis on a border.

set xtics nomirror
set ytics nomirror

#set log x
#set mxtics 10    # Makes logscale look good.

# Line styles: try to pick pleasing colors, rather
# than strictly primary colors or hard-to-see colors
# like gnuplot's default yellow.  Make the lines thick
# so they're easy to see in small plots in papers.
set style line 1 lt rgb "#A00000" lw 2 pt 1
set style line 2 lt rgb "#00A000" lw 2 pt 6
set style line 3 lt rgb "#5060D0" lw 2 pt 2
set style line 4 lt rgb "#F25900" lw 2 pt 9
set style line 5 lt rgb "#000000" lw 2 pt 14

set style line 1 lt rgb "#1b9e77" lw 10 pt 1
set style line 2 lt rgb "#d95f02" lw 10 pt 6
set style line 3 lt rgb "#7570b3" lw 10 pt 2
set style line 4 lt rgb "#e7298a" lw 10 pt 9
set style line 5 lt rgb "#636363" lw 10 pt 12

set output "failover_compare_sockperf_bijection_mice.pdf"

set ylabel "CDF" offset 2
set xlabel "Round Trip Time (milliseconds)"

set key bottom right
set xtics 0.5
#set xtics nomirror rotate by -45
#set xrange [0:10000]
#set yrange [0:10000]
#set rmargin 5

plot "bijection.symmetry.mice.latency.cdf"  using ($1/1000):2 title "Symmetry" w lp ls 1 pointinterval 100  pointsize 1.2,\
"bijection.failover.mice.latency.cdf" using ($1/1000):2 title "Failover" w lp ls 2 pointinterval 300 pointsize 1.2, \
"bijection.wcmp.mice.latency.cdf"  using ($1/1000):2 title "Weighted Multipathing" w lp ls 3 pointinterval 400 pointsize 1.2
#"OnePara_64KB_Delta55/ping.txt.cdf"  title "64K,55us" w lp ls 3 linewidth 4 pointsize 2, \
#"OnePara_64KB_Delta215/ping.txt.cdf"  title "64K,215us" w lp ls 4 linewidth 4 pointsize 2
#"ecmp_tput.cdf"  title "ecmp" w lp ls 5 linewidth 4 pointsize 2
#plot "chunk_seg.txt" using 1:2 title "" w points pointsize 1
