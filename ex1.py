# while True:
#     from itertools import count

#     innum= int(input("enter your number:"))  

#     if innum>0:
#         for i in range(2, int(innum**0.5)+1):
#             if innum %i==0:
#                 print(" not prime number")
#             else:
#                 print("prime number")
                
#     else:
#         print("not prime")








# def add(a,b):
#     return a+b

# def dev(a,b):
#     if b!=0:
#         return a/b
#     else:
#         return "not exist"

# def mult(a,b):
#     return a*b

# def sub(a,b):
#     return a-b

# print("1.add\n1.sub\n3.mult\n4.dev")

# while True:
#     a=print(input("enter a:"))
#     b=print(input("enter b:"))
#     act=print(input("enter action number:"))
    
#     if act=="1":
#         res=add(a,b)
#         print(res)
#     elif act=="2":
#         res=sub(a,b)
#         print(res)
#     elif act=="3":
#         res=mult(a,b)
#         print(res)
#     elif act=="4":
#         res=dev(a,b)
#         print(res)
#     else:
#         print("enter corecct form")
     
        
        
        
        
        
        
        
# def fac(num):
#     if num==0 or num==1:
#         return 1
#     else:
#         return num*fac(num-1)
# print(fac(4))  
# m=int(input("enter your number: "))
# print(fac(m))






# user={"name":"dony","age":25,"lke":"foot"}
# user["adress"]=123
# del user['name']
# print(user)



# import re
# def tex(text):
#     text=re.sub(r"[^\w\s]","",text)
#     text=" ".join(text.split())
#     return text.lower()

# pr="heloo,,im hapyy?   ...."
# print(tex(pr))


# try:
#     with open("text.txt","r") as file:
#         text= file.readlines()
#         line_c= len(text)
#         word= sum(len(line.split()) for line in text)
#         print(f"line:{line_c} , word:{word}")
# except FileNotFoundError:
#     print("error file")
    
    
    
    
# def writer(name, items):
#     with open(name, "w") as file:
#         for item in items:
#             file.write(item + "\n")
            
            
# def reader(name):
#     with open(name, "r") as file:
#         file.readlines()
#     for item in items:
#         print(item.strip())
        
        
# forx=["do","so","du"]
# writer("text.txt", forx)
# print(reader("text.txt"))

# while file:
#     for 




# ۱. فراخوانی کتابخانه‌ها (مثل آوردن جعبه ابزار)
import numpy as np               # np یک نام مستعار کوتاه برای numpy است
import matplotlib.pyplot as plt  # plt ابزار رسم شکل ماست

print("--- فصل ۵: تبدیل سه‌بعدی ---")

# ۲. تعریف بردارهای پایه در فضای سه‌بعدی (مثل ۳ دیوار اتاق)
i_hat = np.array([1, 0, 0])  # یک واحد به راست
j_hat = np.array([0, 1, 0])  # یک واحد به جلو
k_hat = np.array([0, 0, 1])  # یک واحد به بالا

# ۳. ساخت یک ماتریس تبدیل ۳x۳ (مثلاً چرخش ۹۰ درجه حول محور Z)
# این ماتریس می‌گوید: i به جای j می‌رود، j به منفی i می‌رود، k ثابت می‌ماند
rotation_matrix = np.array([
    [0, -1,  0],
    [1,  0,  0],
    [0,  0,  1]
])

# ۴. اعمال تبدیل روی بردارها (ضرب ماتریس در بردار)
# علامت @ در پایتون یعنی "ضرب ماتریسی"
new_i = rotation_matrix @ i_hat
new_j = rotation_matrix @ j_hat
new_k = rotation_matrix @ k_hat

print(f"بردار i جدید: {new_i}")
print(f"بردار j جدید: {new_j}")
print(f"بردار k جدید: {new_k}")


print("\n--- فصل ۶: ضرب داخلی و دوگانگی ---")

# ۵. تعریف دو بردار دوبعدی برای مثال سایه و خورشید
v = np.array([3, 2])  # بردار چوب
w = np.array([1, 4])  # بردار جهت نور خورشید

# ۶. محاسبه ضرب داخلی به ۳ روش مختلف (همه یک جواب می‌دهند)
dot_product_1 = np.dot(v, w)  # روش کلاسیک کتابخانه
dot_product_2 = v @ w         # روش جدید و راحت پایتون (علامت @)
dot_product_3 = (v[0]*w[0]) + (v[1]*w[1]) # روش دستی (ضرب مؤلفه‌ها و جمع)

print(f"ضرب داخلی v و w برابر است با: {dot_product_1}")

# ۷. تفسیر هندسی: طول سایه
length_w = np.linalg.norm(w)           # طول بردار w (ریشه دوم مجموع مربعات)
projection_length = dot_product_1 / length_w # طول سایه v روی w
print(f"طول سایهٔ بردار v روی بردار w برابر است با: {projection_length:.2f}")


# ۸. رسم شکل برای درک بهتر ضرب داخلی
plt.figure(figsize=(6, 6))             # ساخت یک بوم نقاشی ۶ در ۶
plt.grid(True, linestyle='--', alpha=0.6) # کشیدن خطوط شطرنجی کمرنگ
plt.axhline(0, color='black', lw=1)    # خط محور افقی (x)
plt.axvline(0, color='black', lw=1)    # خط محور عمودی (y)

# رسم بردار v (زرد)
plt.arrow(0, 0, v[0], v[1], head_width=0.2, head_length=0.3, fc='yellow', ec='yellow', lw=2, label='v (چوب)')
# رسم بردار w (آبی)
plt.arrow(0, 0, w[0], w[1], head_width=0.2, head_length=0.3, fc='blue', ec='blue', lw=2, label='w (نور خورشید)')

# تنظیم محدوده شکل و نمایش راهنما
plt.xlim(-1, 5)
plt.ylim(-1, 5)
plt.legend()
plt.title("ضرب داخلی: سایه بردار v روی بردار w")
plt.show() # این دستور پنجره شکل را باز می‌کند