#generate boom.ys using base.ys
tile={    
#        "dcache_auto_out_a_ready":1,
#        "dcache_auto_out_a_valid":1,
#        "dcache_auto_out_a_bits_opcode":3,
#        "dcache_auto_out_a_bits_size":3,
#        "dcache_auto_out_a_bits_address":32,
#        "dcache_auto_out_a_bits_data":128,
#        "dcache_auto_out_b_ready":1,
#        "dcache_auto_out_b_valid":1,
#        "dcache_auto_out_b_bits_address":32,
#        "dcache_auto_out_c_ready":1,
#        "dcache_auto_out_c_valid":1,
#        "dcache_auto_out_c_bits_address":32,
#        "dcache_auto_out_c_bits_data":128,
#        "dcache_auto_out_d_ready":1,
#        "dcache_auto_out_d_valid":1,
#        "dcache_auto_out_d_bits_data":128,
        "dcache_io_cpu_req_bits_addr":40,
        "dcache_io_cpu_req_bits_tag":7,
#        "dcache_io_cpu_s1_data_data":64,
#        "dcache_io_cpu_resp_bits_addr":40,
#        "dcache_io_cpu_resp_bits_tag":7,
#        "dcache_io_cpu_resp_bits_data":64,
#        "dcache_io_cpu_resp_bits_data_raw":64,
#        "dcache_io_cpu_resp_bits_store_data":64,
#        "core_io_ifu_flush_pc":40,
#        "core_io_ifu_com_fetch_pc":40,
        "core_io_ifu_fetchpacket_bits_uops_0_inst":32,
#        "core_io_ifu_fetchpacket_bits_uops_0_pc":40,
#        "core_io_ifu_br_unit_target":40,
#        "core_io_ifu_br_unit_btb_update_bits_pc":40,
#        "core_io_ifu_br_unit_btb_update_bits_target":40,
#        "core_io_ifu_get_pc_fetch_pc":40
        }
frontend={}
#{"s2_pc":40}
HS=[[frontend,{}],[tile,frontend]]
alls=tile.copy()
alls.update(frontend)
HS=HS+[[{},alls],[{},alls]]
print (HS)
H=[["BoomFrontend",'frontend'],["BoomTile","tile"],["ExampleBoomSystem","dut"],["TestHarness",""]]
import sys
infile='base.ys'
if len(sys.argv)>1:
    infile=sys.argv[1]

def write2ys(filename):
    f=open(infile,'r')
    r=f.read();
    state=""
    module=H[0]
    submodule=""
    i=-1
    for module in H:
        i=i+1
        all_S=HS[i]
        state=state+"cd "+module[0]+"\n"
        S=all_S[0]
        for name in S:
            state=state+"expose "+name+"\n"
            state=state+"rename "+name+" my_"+name+"\n"
        S=all_S[1]
        for name in S:
            state=state+"add -output my_"+ name+" "+str(S[name])+"\n"
            state=state+"connect -port "+submodule+" my_"+ name+" my_"+name+"\n"
        submodule=module[1]
        state=state+"cd ..\n"
    print(state)
    r=r.replace("#myExposure",state)
    f.close()
    f=open(filename,'w+')
    f.write(r)
    f.close()

write2ys(infile.replace("base","boom"))
