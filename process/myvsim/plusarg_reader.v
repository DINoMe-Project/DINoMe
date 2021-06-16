// See LICENSE.SiFive for license details.

//VCS coverage exclude_file

// No default parameter values are intended, nor does IEEE 1800-2012 require them (clause A.2.4 param_assignment),
// but Incisive demands them. These default values should never be used.
module plusarg_reader #(parameter FORMAT="borked=%d", DEFAULT=0, WIDTH=1) (
   output [WIDTH-1:0] out
);
assign out = DEFAULT;

endmodule
