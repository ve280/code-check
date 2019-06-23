mkdir -p p1_results
rm -f p1_code_check.csv
for f in `ls p1_records`; do
    echo p1_records/$f
    #echo p1_records/$f > p1_results/$f.txt

    score=`python3 p1/codestyle.py p1_records/$f --silent`
    echo $f,$score | tee -a p1_code_check.csv

    #python3 p1/codestyle.py p1_records/$f >> p1_results/$f.txt
    #read -n1 -r -p "Press any key to continue..." key
done
