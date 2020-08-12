module split_itag_array_ext(
  input  [2:0]  RW0_addr,
  input         RW0_clk,
  input  [23:0] RW0_wdata,
  output [23:0] RW0_rdata,
  input         RW0_en,
  input         RW0_wmode,
  input         RW0_wmask
);
  reg [23:0] ram [0:7];
  reg [31:0] _RAND_0;
  wire [23:0] ram_RW_0_r_0_data;
  wire [2:0] ram_RW_0_r_0_addr;
  wire [23:0] ram_RW_0_w_0_data;
  wire [2:0] ram_RW_0_w_0_addr;
  wire  ram_RW_0_w_0_mask;
  wire  ram_RW_0_w_0_en;
  wire  _GEN_0;
  wire  _GEN_1;
  wire  _GEN_2;
  wire [23:0] _GEN_3;
  wire [2:0] _GEN_4;
  reg [2:0] ram_RW_0_addr_pipe_0;
  reg [31:0] _RAND_1;
  wire  _GEN_6;
  wire  ram_RW_0_addr_en;
  wire [2:0] _GEN_5;
  assign ram_RW_0_r_0_addr = ram_RW_0_addr_pipe_0;
  assign ram_RW_0_r_0_data = ram[ram_RW_0_r_0_addr];
  assign ram_RW_0_w_0_data = RW0_wdata;
  assign ram_RW_0_w_0_addr = RW0_addr;
  assign ram_RW_0_w_0_mask = RW0_wmask;
  assign ram_RW_0_w_0_en = RW0_en & RW0_wmode;
  assign RW0_rdata = ram_RW_0_r_0_data;
  assign _GEN_0 = RW0_en;
  assign _GEN_1 = RW0_wmode;
  assign _GEN_2 = RW0_wmask;
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
`ifndef RANDOM
`define RANDOM $random
`endif
`ifdef RANDOMIZE_MEM_INIT
  integer initvar;
`endif
initial begin
  `ifdef RANDOMIZE
    `ifdef INIT_RANDOM
      `INIT_RANDOM
    `endif
    `ifndef VERILATOR
      `ifdef RANDOMIZE_DELAY
        #`RANDOMIZE_DELAY begin end
      `else
        #0.002 begin end
      `endif
    `endif
  _RAND_0 = {1{`RANDOM}};

  `ifdef RANDOMIZE_MEM_INIT
  for (initvar = 0; initvar < 8; initvar = initvar+1)
  `ifdef YOSYS
    ram[initvar] = {3'b01,22'b0};
  `else
    ram[initvar] = _RAND_0[23:0];
`endif
  `endif // RANDOMIZE_MEM_INIT
  `ifdef RANDOMIZE_REG_INIT
  _RAND_1 = {1{`RANDOM}};
  ram_RW_0_addr_pipe_0 = _RAND_1[2:0];
  `endif // RANDOMIZE_REG_INIT
  `endif // RANDOMIZE
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

