section .bss
s resb 12
section .text
global _start
_start:
mov eax,72
mov [s+4*0],al
mov eax,101
mov [s+4*1],al
mov eax,108
mov [s+4*2],al
mov eax,108
mov [s+4*3],al
mov eax,111
mov [s+4*4],al
mov eax,32
mov [s+4*5],al
mov eax,119
mov [s+4*6],al
mov eax,111
mov [s+4*7],al
mov eax,114
mov [s+4*8],al
mov eax,108
mov [s+4*9],al
mov eax,100
mov [s+4*10],al
mov eax,33
mov [s+4*11],al
mov eax, 1
mov ebx, 0
int 80h

