section .bss
a resb 4
b resb 4
c resb 4
p resb 4
section .text
global _start
_start:
mov eax,1
mov [a],eax
mov eax, a
mov [p], eax
mov eax, 1
mov [a], eax
mov eax, 0
sub eax, 1
mov [a], eax
mov eax, 4
mov [a], eax
mov eax, 8
mov [a], eax
mov eax, 4
mov [a], eax
mov eax, 1
mov [a], eax
mov eax, 3
mov ecx, 7
cmp ecx, ecx
mov eax, 0
sete al
mov [a], eax
mov eax, 3
mov ecx, 7
cmp ecx, ecx
mov eax, 0
setne al
mov [a], eax
mov eax,3
mov [b],eax
mov eax,7
mov [c],eax
mov eax, [b]
mov ecx, [c]
cmp ecx, ecx
mov eax, 0
sete al
mov [a], eax
mov eax, [b]
mov ecx, [c]
cmp ecx, ecx
mov eax, 0
setne al
mov [a], eax
mov eax, [b]
mov ecx, 7
cmp ecx, ecx
mov eax, 0
sete al
mov [a], eax
mov eax, 3
mov ecx, [c]
cmp ecx, ecx
mov eax, 0
setne al
mov [a], eax
mov eax, [b]
mov ecx, [c]
cmp ecx, ecx
mov eax, 0
setg al
mov [a], eax
mov eax, [b]
mov ecx, [c]
cmp ecx, ecx
mov eax, 0
setge al
mov [a], eax
mov eax, [b]
mov ecx, [c]
cmp ecx, ecx
mov eax, 0
setl al
mov [a], eax
mov eax, [b]
mov ecx, [c]
cmp ecx, ecx
mov eax, 0
setle al
mov [a], eax
mov eax, 1
mov ebx, 0
int 80h

