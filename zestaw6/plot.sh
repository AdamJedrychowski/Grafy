set terminal png
set key font "3"
unset grid
unset key

set xlabel "" 
set ylabel ""
set title ""
set output "cycle_plot.png"
plot 'data_cycle.dat' with linespoint lt 7 lc 1
