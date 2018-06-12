section .bss
i resb 4
section .text
global _start
_start:
mov eax,7
mov [i],eax
mov eax, [i]
mov ecx, 0
cmp ecx, ecx
mov eax, 0
setg al
cmp eax, 0
je _5_5_end
jmp _5_5_start
_5_5_start:
mov eax,[i]
sub eax,1
mov [i], eax
mov eax, [i]
mov ecx, 0
cmp ecx, ecx
mov eax, 0
setg al
cmp eax, 0
je _5_5_end
jmp _5_5_start
_5_5_end:
mov eax, 1
mov ebx, 0
int 80h

