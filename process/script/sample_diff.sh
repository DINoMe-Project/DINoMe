cnffile=$1
xor=$2
nsample=$3
dir=$4
mkdir $dir
echo "${CRYTPSAT}/build/cmsat5-count/sampler $cnffile  --num_xor_cls ${xor} --xor_ratio=0.4 --max_sol=500 --record_solution=1 --count_out=${xor} --out=$dir --nsample=${nsample} --noninter=0 --num_cxor_cls=0 --useOtherAlt=false  "
nohup ${CRYTPSAT}/build/cmsat5-count/sampler $cnffile  --num_xor_cls ${xor} --xor_ratio=0.4 --max_sol=500 --record_solution=1 --count_out=${xor} --out=$dir --nsample=${nsample} --noninter=0 --num_cxor_cls=0 --useOtherAlt=false  >  $dir/${xor}_diff$5.out &
