`timescale 1ns/1ps
module and_gate_tb;

    reg a, b;         // test inputs
    wire y;           // test output

    // Instantiate the AND gate
    and_gate uut (
        .a(a),
        .b(b),
        .y(y)
    );

    initial begin
        // Monitor values
        $monitor("Time=%0t | a=%b b=%b -> y=%b", $time, a, b, y);

        // Apply test values
        a = 0; b = 0; #10;
        a = 0; b = 1; #10;
        a = 1; b = 0; #10;
        a = 1; b = 1; #10;

        $finish; // stop simulation
    end

endmodule
