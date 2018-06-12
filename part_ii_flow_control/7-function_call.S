section data
_9_5: db "Hello world!%d,%d,%d",0xa,0
section .bss
i resb 4
j resb 4
k resb 4
section .text
global main
main:
mov eax,1
mov [i],eax
mov eax,2
mov [j],eax
mov eax,3
mov [k],eax
push dword [k]
push dword [j]
push dword [i]
push dword _9_5
extern printf
call printf
add esp,byte 16
mov eax, 1
mov ebx, 0
int 80h

;printf --> 
;    http://blog.163.com/lixiangqiu_9202/blog/static/53575037201272611402815/
;Escape Character
