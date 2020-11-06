// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

    // s will hold the address of the word that will be turned into -1
    @SCREEN
    D=A
    @s
    M=D


(MAINLOOP)
    @KBD
    D=M

    // Initialize counter i
    @i
    M=0

    @PAINTBLACK
    D;JNE

    @PAINTWHITE
    0;JMP


(PAINTWHITE)
    // Check if i is 8192 - check if finished
    @8192
    D=A
    @i
    D=D-M
    @MAINLOOP
    D;JEQ

    // Fill black current word
    @i
    D=M
    @s
    A=D+M
    M=0

    // Add 1 to i
    @i
    M=M+1

    // Goto PAINTWHITE
    @PAINTWHITE
    0;JMP

(PAINTBLACK)
    // Check if i is 8192 - check if finished
    @8192
    D=A
    @i
    D=D-M
    @MAINLOOP
    D;JEQ

    // Fill black current word
    @i
    D=M
    @s
    A=D+M
    M=-1

    // Add 1 to i
    @i
    M=M+1

    // Goto PAINTBLACK
    @PAINTBLACK
    0;JMP
