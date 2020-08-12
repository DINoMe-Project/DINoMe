filename=$1
cp $filename $filename.init
sed -i "s/ \\\top.boom_tile.dcache.random/ attack_\\\top.boom_tile.dcache.random/g" $filename.init
cp $filename.init $filename.final

sed -i "s/ \\\top.boom_tile.dcache.meta/ ob_\\\top.boom_tile.dcache.meta/g" $filename.final
sed -i "s/cache_observe/final_cache_observe/g" $filename.final
