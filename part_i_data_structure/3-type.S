section .data
section .bss
i resb 1
j resb 4
k resb 8
section .text
global main
main:
mov eax,1
mov ebx,0
int 80h

