model=spectre
nsets=$1
nways=$2
model=$3
nstate=$4
observe=observe_4
if [ $# -eq 5 ]
then
observe=$5
fi
if [ -f boom-initall.smt2 ]; then
	echo "finished yosys"
else
yosys boom.ys
fi
if [ -f test_trans.smt2.cnf ]
then
	echo "skip"
else
sh $BOOM/script/cache_observe/cleanclockreset.sh boom-initall.smt2 
sh $BOOM/script/boom-trans.sh boom-initall.smt2 test
fi
sh $BOOM/script/generate_cnf.sh $model test boom-initall.smt2 $nsets $nways $nstate
#mkdir observe
#cd observe
#sh $BOOM/script/cache_observe/observe_cmd.sh $nsets
#cd ..
mkdir s$nstate
cd s$nstate
sh $BOOM/script/cache_observe/add_cache_ob.sh $nsets $nways $model $nstate $observe
