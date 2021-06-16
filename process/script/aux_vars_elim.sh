maxres=10000
if [ $! -gt 2 ]
then
	maxres=$3
fi
python $BOOM/script/aux_vars_elim.py $1.e$2 --maxres=$maxres
index=$2
index=$((index+1))
mv $1.e$2.e $1.e$index
sh $BOOM/script/coprocess.sh $1.e$index
mv $1.e$index.simp $1.e$index
