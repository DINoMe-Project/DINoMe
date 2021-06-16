from IPython import embed
sym_var_name=[
        "mem.sram.mem.mem_ext.ram",
        "dut.tile.frontend.icache.dataArrayWay_0.dataArrayWay_0_ext.ram",
        "dut.tile.frontend.bpdpipeline.bpd.counter_table.counter_table_ext.ram"
]
def process(filename):
    with open(filename) as f:
        assign={}
        sym_vars={}
        reverse_sym_vars={}
        for line in f:
            if line.startswith('c') and "-->" in line:
                w=line.replace("]","").replace("[","").split("-->")
                name=w[0].split()[1]
                sym_vars[name]= w[1].split()
                s=sym_vars[name]
                reverse_sym_vars[name]={}
                for i in range(0,len(s)):
                    reverse_sym_vars[name][s[i]]=i
            elif not line.startswith('c') and not line.startswith('p'):
                if len(line.split())!=2:
                    continue
                var=line.split()[0]
                lit=int(var)
                var=abs(lit)
                neg= lit<0
                assign[var]=neg
        all_ranges={}
        for name in sym_vars:
            uninit=set()
            for var in sym_vars[name]:
                if abs(int(var)) in assign:
                    continue;
                uninit.add(reverse_sym_vars[name][var]);
            ranges={}
            prevvar=-2;
            L=list(uninit)
            for var in sorted(L):
                var=int(var)
                if var-prevvar==1:
                    rval= var
                else:
                    lval=var
                    rval=var
                ranges[lval]=rval
                prevvar=var
            all_ranges[name]=ranges;

            for lval in ranges:
                print(lval,ranges[lval])
    return [all_ranges,sym_vars,assign];

import argparse
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='test init file')
    parser.add_argument('file',metavar='files',type=str,help='cnf file '
    'generated from yosys tool')
    args=parser.parse_args()
    process(args.file)
