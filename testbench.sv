`timescale 1ns/1ps

module tb;

  reg clk, rst, btn;
  wire red, green;

  top_module dut(clk, rst, btn, red, green);

  // Clock
  initial begin
    clk = 0;
    forever #5 clk = ~clk;
  end

  initial begin
    $dumpfile("reaction_timer.vcd");
    $dumpvars(0, tb);

    rst = 1;
    btn = 0;

    #10;
    rst = 0;

    // First counter cycle: button OFF
    btn = 0;
    repeat (8) begin
      @(posedge clk);
      #1;
      $display("Count=%b | Button=%b | Red=%b | Green=%b",
               dut.c.q, btn, red, green);
    end

    // Second counter cycle: button ON
    btn = 1;
    repeat (8) begin
      @(posedge clk);
      #1;
      $display("Count=%b | Button=%b | Red=%b | Green=%b",
               dut.c.q, btn, red, green);
    end

    $finish;
  end

endmodule
