nstate=60
basecnf=s${nstate}.cnf
basesmt2=boom-initall.smt2
symbol_cnf=$basecnf.symbol.cnf 
observe_cnf=observe_counter.smt2.cnf.simp
i=$1
model=$2
python $BOOM/script/generate_cache_observe.py observe_counter.smt2 --nset=$i --nway=$((32/i)) --model=$model
sh $BOOM/script/stp_tocnf.sh observe_counter.smt2
sh $BOOM/script/boom-trans.sh boom-initall.smt2 cache
sh $BOOM/script/generate_cnf.sh $model cache boom-initall.smt2 $i $((32/i)) $nstate
sleep 6
#sh $BOOM/script/compose.sh cache_trans.smt2.cnf cache_init.smt2.cnf.autoinit.simp 0 60 states 1
sleep 10
mkdir s$nstate

cp states/$basecnf s$nstate/
cd s$nstate
python $BOOM/script/match_def.py --mode=mark --model=$model --cnffile=$basecnf --nstate=$((nstate+1)) ../$basesmt2 --nset=$i --nway=$((32/i)) 

cp ../$observe_cnf ./
outcnf=$symbol_cnf.observe
sh $BOOM/script/compose-observe.sh $observe_cnf $symbol_cnf
# now you can use inter/noninterference.cnf to count






