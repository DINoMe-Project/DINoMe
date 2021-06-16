module AsyncResetRegVec_w2_i0( // @[:example.TestHarness.TinyBoomConfig8.fir@11787.2]
  input         clock, // @[:example.TestHarness.TinyBoomConfig8.fir@11788.4]
  input         reset, // @[:example.TestHarness.TinyBoomConfig8.fir@11789.4]
  input  [31:0] io_d, // @[:example.TestHarness.TinyBoomConfig8.fir@11790.4]
  output [31:0] io_q // @[:example.TestHarness.TinyBoomConfig8.fir@11790.4]
);
  wire  _T; // @[AsyncResetReg.scala 62:29:example.TestHarness.TinyBoomConfig8.fir@11795.4]
  reg [31:0] reg_; // @[AsyncResetReg.scala 62:50:example.TestHarness.TinyBoomConfig8.fir@11796.4]
  reg [31:0] _RAND_0;
  assign _T = reset; // @[AsyncResetReg.scala 62:29:example.TestHarness.TinyBoomConfig8.fir@11795.4]
  assign io_q = reg_; // @[AsyncResetReg.scala 66:8:example.TestHarness.TinyBoomConfig8.fir@11800.4]
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
  `ifdef RANDOMIZE_REG_INIT
  _RAND_0 = {1{`RANDOM}};
  reg_ = _RAND_0[31:0];
  `endif // RANDOMIZE_REG_INIT
  `endif // RANDOMIZE
    reg_ = 32'h0;
end
  always @(posedge clock) begin
    if (_T) begin
      reg_ <= 32'h0;
    end else begin
      reg_ <= io_d;
    end
  end
endmodule
