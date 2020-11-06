    @sqrt
    M=0 // sqrt = 0
    @R0 // copy of sqrt
    M=0
    @R1 // copy of sqrt
    M=0

    @1000   // INGRESAR ACÁ EL VALOR DE X
    D=A
    @x
    M=D //x = R9 = x ingresado por usuario
    @R2
    M=0

(SQRT)
    // when sqrt 
    @R2
    D=M // D = actual sqrt
    @x
    D=D-M
    @FINISH
    D;JEQ
    @SQRTGREATER
    D;JGT

    @R0
    D=M
    @sqrt
    M=D
    M=M+1
    D=M
    @R0
    M=D
    @R1
    M=D
    

(MULT)
    @R2
    M=0

    // Save second factor in 'factor'
    @R1
    D=M
    @factor
    M=D
    @i
    M=0


(MULTLOOP)
    // Break when i==R1
    @i
    D=M
    @R1
    D=D-M
    @SQRT
    D;JEQ

    // Sum R0 again
    @R2
    D=M
    @R0
    D=D+M
    @R2
    M=D

    // Add 1 to i
    @i
    M=M+1

    @MULTLOOP
    0;JMP

(SQRTGREATER)
    @sqrt
    M=M-1

(FINISH)
    @sqrt
    D=M
    @3
    D=D-A
    @5
    M=D

(END)
    @END
    0;JMP
