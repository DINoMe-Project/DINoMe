module AsyncResetRegVec_w1_i0( // @[:example.TestHarness.TinyBoomConfig8.fir@11817.2]
  input   clock, // @[:example.TestHarness.TinyBoomConfig8.fir@11818.4]
  input   reset, // @[:example.TestHarness.TinyBoomConfig8.fir@11819.4]
  input   io_d, // @[:example.TestHarness.TinyBoomConfig8.fir@11820.4]
  output  io_q // @[:example.TestHarness.TinyBoomConfig8.fir@11820.4]
);
  wire  _T; // @[AsyncResetReg.scala 62:29:example.TestHarness.TinyBoomConfig8.fir@11825.4]
  reg  reg_; // @[AsyncResetReg.scala 62:50:example.TestHarness.TinyBoomConfig8.fir@11826.4]
  reg [31:0] _RAND_0;
  assign _T = reset; // @[AsyncResetReg.scala 62:29:example.TestHarness.TinyBoomConfig8.fir@11825.4]
  assign io_q = reg_; // @[AsyncResetReg.scala 66:8:example.TestHarness.TinyBoomConfig8.fir@11830.4]
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
  reg_ = 1'h0;
  `endif // RANDOMIZE_REG_INIT
  `endif // RANDOMIZE

end
  always @(posedge clock) begin
    if (_T) begin
      reg_ <= 1'h0;
    end else begin
      reg_ <= io_d;
    end
  end
endmodule
