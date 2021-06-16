import argparse
import math
import re
import os
from IPython import embed
def main(args):
    BOOM=os.getenv('BOOM')

    tag_array_tmp=args.tag_array
    def tag_array(i,j):
        return tag_array_tmp.replace("$i","%d"%i).replace("$j","%d"%j)
    cache_observe_tmp=args.cache_observe
    prevfilename=args.file+".0"+ ".upper" if(args.use_upper_mem) else args.file+".0"
    nsets=args.nsets
    if args.all:
        skip_gap=1
    else:
        skip_gap=nsets
    def cache_observe(j):
        return cache_observe_tmp.replace("$j","%d"%j)
    def addr(j):
        return "addr_%d"%j
    f=open(args.file)
    content=f.read()
    f.close()
    addr_loc=content.find(args.secret_addr)+len(args.secret_addr)+1
    start=content.find("[",addr_loc)+1
    end=content.find("]",addr_loc)
    addr_vars=[int(i) for i in content[start:end].split()[args.secret_addr_offset:args.secret_addr_offset+args.secret_addr_len] ]
    #addr_vars=addr_vars[0:args.addr_len]
    print(addr_vars)
    for addr in range(0,1<<args.addr_len,skip_gap):
        newcontent=content
        newlines=[]
        i=newcontent.find("c "+args.secret_addr)
        start=newcontent.find("-->",i)
        end=newcontent.find("\n",i)
        line=newcontent[i:end]
        addr_var_str=" ".join([str(i) for i in addr_vars])
        newcontent=newcontent.replace(line,"c addr_%d --> [ %s ]"%(addr,addr_var_str))
        #newcontent=newcontent.replace(args.secret_addr,"addr_%d"%addr)
        newcontent=newcontent.replace(cache_observe(0),cache_observe(addr))
        newcontent=newcontent.replace("cache_observe_way_0","cache_observe_way_%d"%(addr))
        addr_val=addr
        addr_val_bin=''.join(reversed(bin(addr_val).replace("b","")))
        for offset in range(len(addr_vars)):
            if len(addr_val_bin)<=offset or addr_val_bin[offset]=='0' or offset>=args.addr_len:
                if args.use_upper_mem and offset==args.addr_len:
                        newlines.append("%d 0"%(addr_vars[offset]))
                else: 
                    newlines.append("%d 0"%(-addr_vars[offset]))
            else:
                newlines.append("%d 0"%(addr_vars[offset]))
    
        newcontent=newcontent+"\n".join(newlines)
        newfilename=args.file+".%d"%addr
        if args.use_upper_mem:
            newfilename=newfilename+".upper"
        with open(newfilename,'w') as newf:
            newf.write(newcontent)
        """
        if addr>0:    
            cmd="sh %s/script/compose.sh %s %s %d %d tmp 1"%(BOOM,newfilename,prevfilename,addr,addr+1)
            print(cmd)
            prevfilename="tmp/s%d.cnf"%(addr+1)
            simcmd="sh %s/script/simp.sh %s 1 10"%(BOOM,prevfilename)
            os.system(cmd)
            os.system(simcmd)
            prevfilename="tmp/s%d.cnf.simp"%(addr+1)
        """

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='match symbol')
    parser.add_argument('file',metavar='file',type=str,help='cnf file '
    'generated from yosys tool')
    
    parser.add_argument('--use_upper_mem',type=bool,default=False,help='#nset')
    parser.add_argument('--all',type=bool,default=False,help='#nset')
    parser.add_argument('--nsets',type=int,default=8,help='#nset')
    parser.add_argument('--nways',type=int,default=4,help='#nway')
    parser.add_argument('--addr_len',type=int,default=6,help='#addr len')
    parser.add_argument('--tag_array',type=str,default="\\top.boom_tile.dcache.meta_0.tag_array_$i[$j]",help='tag array name template')
    parser.add_argument('--cache_observe',type=str,default="cache_observe_$j",help='cache_observe tmp')
    parser.add_argument('--secret_addr',type=str,default="\\top.boom_tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.mem_0_0.ram[0]")
    parser.add_argument('--secret_addr_offset',type=int,default=52)
    parser.add_argument('--secret_addr_len',type=int,default=8)
    args=parser.parse_args()
    main(args)
