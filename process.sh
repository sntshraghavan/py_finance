file=500_analysis.csv


sed  -i '' 's/[][]//g'  $file
sed  -i '' "s/B'//g"  $file
sed  -i '' 's/%//g'  $file
sed  -i '' "s/'//g"  $file
sed  -i '' "s/,,/,NA,/g"  $file
sed  -i '' "s/,-,/,0,/g"  $file
sed  -i '' "s/,- /,0,/g"  $file
