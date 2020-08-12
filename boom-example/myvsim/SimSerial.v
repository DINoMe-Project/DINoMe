module SimSerial (
    input         clock,
    input         reset,
    input         serial_out_valid,
    output        serial_out_ready,
    input  [31:0] serial_out_bits,

    output        serial_in_valid,
    input         serial_in_ready,
    output [31:0] serial_in_bits,

    output        exit
);

    assign serial_in_valid  = 0;
    assign serial_in_bits   = 0;
    assign serial_out_ready = 0;
    assign exit = 0;

endmodule
