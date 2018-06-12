section .bss
a resb 4
i resb 4
sum resb 4
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
je _8_5_end
jmp _8_5_start
_8_5_start:
jmp _8_5_end
_8_5_branch:
mov eax, [i]
mov ecx, 0
cmp ecx, ecx
mov eax, 0
setg al
cmp eax, 0
je _8_5_end
jmp _8_5_start
_8_5_end:
mov eax,0
mov [sum],eax
mov eax,0
mov [i],eax
mov eax, [i]
mov ecx, 7
cmp ecx, ecx
mov eax, 0
setl al
cmp eax, 0
je _12_5_end
jmp _12_5_start
_12_5_start:
jmp _12_5_branch
_12_5_branch:
mov eax,[i]
add eax,1
mov [i], eax
mov eax, [i]
mov ecx, 7
cmp ecx, ecx
mov eax, 0
setl al
cmp eax, 0
je _12_5_end
jmp _12_5_start
_12_5_end:
mov eax, 1
mov ebx, 0
int 80h

