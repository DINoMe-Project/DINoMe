module split_dataArrayWay_0_ext(
  input  [5:0]  RW0_addr,
  input         RW0_clk,
  input  [63:0] RW0_wdata,
  output [63:0] RW0_rdata,
  input         RW0_en,
  input         RW0_wmode
);
  reg [63:0] ram [0:63];
  reg [63:0] _RAND_0;
  wire [63:0] ram_RW_0_r_0_data;
  wire [5:0] ram_RW_0_r_0_addr;
  wire [63:0] ram_RW_0_w_0_data;
  wire [5:0] ram_RW_0_w_0_addr;
  wire  ram_RW_0_w_0_mask;
  wire  ram_RW_0_w_0_en;
  wire  _GEN_0;
  wire  _GEN_1;
  wire  _GEN_2;
  wire [63:0] _GEN_3;
  wire [5:0] _GEN_4;
  reg [5:0] ram_RW_0_addr_pipe_0;
  reg [31:0] _RAND_1;
  wire  _GEN_6;
  wire  ram_RW_0_addr_en;
  wire [5:0] _GEN_5;
  assign ram_RW_0_r_0_addr = ram_RW_0_addr_pipe_0;
  assign ram_RW_0_r_0_data = ram[ram_RW_0_r_0_addr];
  assign ram_RW_0_w_0_data = RW0_wdata;
  assign ram_RW_0_w_0_addr = RW0_addr;
  assign ram_RW_0_w_0_mask = 1'h1;
  assign ram_RW_0_w_0_en = RW0_en & RW0_wmode;
  assign RW0_rdata = ram_RW_0_r_0_data;
  assign _GEN_0 = RW0_en;
  assign _GEN_1 = RW0_wmode;
  assign _GEN_2 = 1'h1;
  assign _GEN_3 = RW0_wdata;
  assign _GEN_4 = RW0_addr;
  assign _GEN_6 = ~ RW0_wmode;
  assign ram_RW_0_addr_en = RW0_en & _GEN_6;
  assign _GEN_5 = RW0_addr;
`ifdef RANDOMIZE_GARBAGE_ASSIGN
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_INVALID_ASSIGN
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_REG_INIT
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_MEM_INIT
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_MEM_INIT
	integer initvar;
`endif
reg[127:0] memname;


initial begin
	_RAND_0 = {2{`RANDOM}};
`ifndef YOSYS
	for (initvar = 0; initvar < 64; initvar = initvar+1)
		ram[initvar] = _RAND_0;
`else
	$readmemh("test.hex",ram);
`endif
	_RAND_1 = {1{`RANDOM}};
	ram_RW_0_addr_pipe_0 = _RAND_1[5:0];
end
  always @(posedge RW0_clk) begin
    if(ram_RW_0_w_0_en & ram_RW_0_w_0_mask) begin
      ram[ram_RW_0_w_0_addr] <= ram_RW_0_w_0_data;
    end
    if (ram_RW_0_addr_en) begin
      ram_RW_0_addr_pipe_0 <= RW0_addr;
    end
  end
endmodule

