module tb_dut;

reg clk_i;
reg rst_i;
reg rx_i;
wire tx_o;
wire [3:0] anodos_o;
wire [7:0] segmentos_o;

initial begin
    $dumpfile("dut.vcd");
    $dumpvars(0, dut);
    $from_myhdl(
        clk_i,
        rst_i,
        rx_i
    );
    $to_myhdl(
        tx_o,
        anodos_o,
        segmentos_o
    );
end

dut dut(
    clk_i,
    rst_i,
    rx_i,
    tx_o,
    anodos_o,
    segmentos_o
);

endmodule
