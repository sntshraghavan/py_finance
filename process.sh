#install by the following 
# python3  -m pip install yahoofinancials

file=500_analysis.csv
#rm stock_dfs/*

python3 get_500list.py   ## download historic data 
python3 append_Q_stats.py  ##calculate  
#
##sed  -i '' 's/[][]//g'  $file
#sed  -i '' "s/B,/,/g"  $file
#sed  -i '' 's/%//g'  $file
#sed  -i '' "s/'//g"  $file
#sed  -i '' "s/,,/,NA,/g"  $file
#sed  -i '' "s/,-,/,0,/g"  $file
#sed  -i '' "s/,- /,0,/g"  $file
#
#python3 brain.py
