basecnf=$1
nstate=$2
basesmt2=$3
python $BOOM/script/match_def.py --mode=mark --model=$4 --cnffile=$basecnf --nstate=$nstate $basesmt2
mkdir inter
sh $BOOM/script/compose-copy.sh $basecnf.symbol.cnf inter
sh $BOOM/script/compose.sh ./declass-2.cnf inter/noninterference.cnf 0 1 inter 1
mv compose.cnf inter/noninterference_declass.cnf
