cnffile=$1
xor=$2
nsample=$3
dir=$4
mkdir $dir
nohup ${CRYTPSAT}/build/cmsat5-count/sampler $cnffile  --num_xor_cls ${xor} --xor_ratio=0.4 --max_sol=600 --record_solution=1 --count_out=${xor}_relax --out=$dir --nsample=${nsample} --noninter=-1 --num_cxor_cls=0 --useOtherAlt=false >  $dir/${xor}_relax$5.out &
nohup ${CRYTPSAT}/build/cmsat5-count/sampler $cnffile  --num_xor_cls ${xor} --xor_ratio=0.4 --max_sol=600 --record_solution=1 --count_out=${xor}_strict --out=$dir  --nsample=${nsample} --noninter=1 --num_cxor_cls=0 --useOtherAlt=false >  $dir/${xor}_strict$5.out &
