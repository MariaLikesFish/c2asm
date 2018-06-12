section .data
section .bss
a resb 28
section .text
global main
main:
;Array
mov eax,5
mov [a+4*4],eax
;Return
mov eax,1
mov ebx,0
int 80h

