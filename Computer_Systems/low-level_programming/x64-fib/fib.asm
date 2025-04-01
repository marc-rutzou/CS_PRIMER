section .text
global fib
fib:
    cmp rdi, 1
    jle .baseCase       ; n <= 1
    push rdi
    sub rdi, 1          
    call fib            ; f(n-1)
    ; stack: [2, 3] and rax = 1 and rdi = 1 (Still)
    mov rbx, rax        ; store return value
    pop rdi             ; pop 2 into rcx
    push rbx            ; store rbx, otherwise its overwritten
    sub rdi, 2          
    call fib            ; f(n-2)
    pop rbx
    ; stack: [3] and rax = 1
    add rax, rbx        ; f(n-2) + f(n-1)
    ret
.baseCase:
    mov rax, rdi       ; return n
    ret
