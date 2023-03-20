print("3주차 과제(프로그래머스 문제풀이)")

# 두 정수 사이의 합(12912) https://school.programmers.co.kr/learn/courses/30/lessons/12912

def solution(a, b):
    return sum(list(range(min(a,b), max(a,b)+1))) #list에 넣어도 되고 안 넣어도 됨 / min(a,b) == 둘 중에 작은 값, max(a,b) 둘 중에 큰 값


## 핸드폰 번호 가리기(12948) https://school.programmers.co.kr/learn/courses/30/lessons/12948

def solution(num):
    return "*" * (len(num) - 4) + num[-4:] #맨 끝자리가 -1부터 작아지므로 끝에서 네 번째 자리까지 하면 -4 (slicing)


## 없는 숫자 더하기(86051) https://school.programmers.co.kr/learn/courses/30/lessons/86051

def solution(numbers):
    num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    return sum(set(num) - set(numbers)) # 그냥 0~9까지 합이 45니까 return sum(45 - set(numbers))해도 됨


## 나누어 떨어지는 숫자 배열(12910) https://school.programmers.co.kr/learn/courses/30/lessons/12910

def solution(arr, divisor):
    return (sorted([n for n in arr if not (n%divisor)]) or [-1]) #논리연산자 && || ! 아니고 and or not임 / sorted는 정렬할 대상이 뒤에 바로 오고 .sort()는 메소드 / if (n%2) == 0 원래 의미


## 두 개 뽑아서 더하기(68644) https://school.programmers.co.kr/learn/courses/30/lessons/68644

import itertools # from itertools import combinations로 임포트하면 list 안에서 combinations만 써도 됨

def solution(numbers):
    answer = set()
    
    for i in list(itertools.combinations(numbers, 2)):
        answer.add(sum(i))
    
    return sorted(answer)


## 푸드 파이트 대회(134240) https://school.programmers.co.kr/learn/courses/30/lessons/134240

from itertools import chain

def solution(food):
    answer = ''
    
    for i in range(1, len(food)):
        answer += str(i)*(food[i]//2) # // --> 파이썬 몫 연산자
        
    return ''.join(map(str, chain(answer, [0], answer[::-1]))) #[::] - Extended Slices, [1::-1] 1번째 인덱스부터 끝까지 -1(역순)으로 정렬


## 모스부호 (1)(120838) https://school.programmers.co.kr/learn/courses/30/lessons/120838

def solution(letter):
    morse = { 
        '.-':'a','-...':'b','-.-.':'c','-..':'d','.':'e','..-.':'f',
        '--.':'g','....':'h','..':'i','.---':'j','-.-':'k','.-..':'l',
        '--':'m','-.':'n','---':'o','.--.':'p','--.-':'q','.-.':'r',
        '...':'s','-':'t','..-':'u','...-':'v','.--':'w','-..-':'x',
        '-.--':'y','--..':'z'
    } # 딕셔너리(dict)
    
    return ''.join(morse[i] for i in letter.split(' '))