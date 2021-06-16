dir=$1
name=$2-$3-$4
depth=$4
python3 train_bits.py $dir/same.csv $dir/diff.csv \
  --outname=$dir/$name --symbol=$dir/symbol.txt \
--ntrees=64 --depth=$depth --nlinear=$3 --label=0

