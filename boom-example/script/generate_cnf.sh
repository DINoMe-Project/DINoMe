model=$1
target=$2
basesmt2=$3
nset=$4
nway=$5
nstates=$6
#ln -s ../exp/boom_init.smt2.cnf.simp  ./
#ln -s ../exp/boom_trans.smt2.cnf.simp ./
#ln -s ../exp/boom_trans_reset.smt2.cnf.simp ./
if [ -f  ${target}_init0.smt2.cnf.autoinit ]
then
	echo "skip ${target}_init0.smt2.cnf"
else
cp ${target}_init.smt2.cnf ${target}_init0.smt2.cnf
sed -i 's/s0 --> \[[-0-9 ]*\]//g' ${target}_init0.smt2.cnf
sed -i 's/s1 --> \[[-0-9 ]*\]//g' ${target}_init0.smt2.cnf
sed -i 's/s2 -->/s0 -->/g' ${target}_init0.smt2.cnf
sh ${BOOM}/script/simplify.sh ${target}_init0.smt2.cnf 1 1
mv  ${target}_init0.smt2.cnf.simp ${target}_init0.smt2.cnf
fi
python ${BOOM}/script/match_def.py --mode=init --cnffile=${target}_init0.smt2.cnf --autoinit=1 --model=${model} ${basesmt2} --nset=${nset} --nway=${nway} 
echo "python ${BOOM}/script/match_def.py --mode=init --cnffile=${target}_init0.smt2.cnf --autoinit=1 --model=${model} ${basesmt2} --nset=${nset} --nway=${nway} "
# simplify autoinit
#sh ${BOOM}/script/simp.sh ${target}_init0.smt2.cnf.autoinit 1 1
mkdir states-cache
ln -s states-cache states
sh ${BOOM}/script/compose.sh ${target}_trans.smt2.cnf ${target}_init0.smt2.cnf.autoinit 0 ${nstates} states 1
echo "${BOOM}/script/compose.sh ${target}_trans.smt2.cnf ${target}_init0.smt2.cnf.autoinit.simp 0 ${nstates} states 1"

