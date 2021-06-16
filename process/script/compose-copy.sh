cycle=2
if [ $# -eq 3 ] 
then 
	cycle=$3
fi
mkdir $2
nohup $CRYPTSAT/build/cmsat5-compose/compose --compose_mode=copy --keepsymbol=1  --cycles=$cycle  --memoutmult=5000 --composedfile=noninterference.cnf  --simplify_interval=1  $1 simp.cnf --out=$2 --compsvar=10000000 --compslimit=5000 --mult=4 --preschedule="renumber"  > $1.out &
