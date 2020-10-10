mkdir -p p2_results
rm -f p2_code_check.csv
for f in `ls p2_records`; do
    echo p2_records/$f
    #echo p2_records/$f > p2_results/$f.txt

    cp p2_records/$f/p2.cpp driver
    score=`python3 codestyle.py driver --silent`
    rm driver/p2.cpp
    echo $f,$score | tee -a p2_code_check.csv

    #python3 codestyle.py p2_records/$f >> p2_results/$f.txt
    #read -n1 -r -p "Press any key to continue..." key
done
