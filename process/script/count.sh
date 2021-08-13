counter=$CRYPTOSAT/build/cmsat5-count/count
cnffile=$1
nsample=$2
ntimes=$3
outdir=$4
mkdir $outdir
for xor in `seq $5 $6`
do
nohup $counter $cnffile --count_mode=iblock --num_xor_cls ${xor} \
--max_count_times=${ntimes}  --xor_ratio=0.5 --record_solution=1 \
--count_out=${xor}.count --out=$outdir --inter_mode=2 \
--nsample=${nsample} --max_sol=100 \
 --debug=0 --use_simplify=0 --max_xor_per_var=2000 \
 --one_call_timeout=100 --total_call_timeout=200 &
done
