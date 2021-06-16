prefix=$1
datafile=`ls $prefix*.csv`
python3 rules2dag.py  --data=$datafile --dev_ratio=$3 --sort=$2 $prefix.rule.txt 
