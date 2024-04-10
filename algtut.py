import numpy as np

import sympy as sp
from IPython.display import display

num_iters = 10
tot_score = 0

maxnum=int(input("\nEnter level of difficulty: "))
print("\n\n\n")
nums = np.arange(-maxnum,maxnum+1)
nums_nz=np.concatenate((np.arange(-maxnum,0),np.arange(1,maxnum+1)))

type = input("How many unknowns: [1 or 2]")
if type=="1":
    for i in range(num_iters):
        xval = np.random.choice(nums)
        [a1,a2] = np.random.choice(nums,2,replace=False)
        b1 = np.random.choice(nums)
        b2 = a1*xval+b1-a2*xval

        x = sp.symbols('x')
        print(f"\n\nProblem ({i+1}/{num_iters}):")
        eq = sp.Eq(a1*x+b1,a2*x+b2)
        display(eq)
        # print(sp.pretty(eq,use_unicode=True))
        # print(sp.print_latex(eq))

        x_ = int(input("\nx="))
        if xval==x_:
            print("Correct. \N{smiling face with sunglasses}")
            tot_score += 1
        else:
            print(f"Incorrect. \N{slightly frowning face}\nThe correct answer was x={xval}.")
elif type=="2":
    x,y = sp.symbols('x y')
    for i in range(num_iters):
        valid_soln=False
        while not valid_soln:
            xval = np.random.choice(nums)
            yval = np.random.choice(nums)
            [ax,ay] = np.random.choice(nums_nz,2,replace=True)
            [bx,by] = np.random.choice(nums_nz,2,replace=True)
            a = ax*xval+ay*yval
            b = bx*xval+by*yval
            eqA = sp.Eq(ax*x+ay*y,a)
            eqB = sp.Eq(bx*x+by*y,b)        
            if len(sp.solve((eqA,eqB),(x,y)))==2:
                valid_soln=True



        print(f"\n\nProblem ({i+1}/{num_iters}):")
        display(eqA)
        display(eqB)
        # print(sp.pretty(eq,use_unicode=True))
        # print(sp.print_latex(eq))

        x_ = int(input("\nx="))
        y_ = int(input("\ny="))
        if xval==x_ and yval==y_:
            print("Correct. \N{smiling face with sunglasses}")
            tot_score += 1
        else:
            print(f"Incorrect. \N{slightly frowning face}\nThe correct answer was x={xval} and y={yval}.")

print(f"\n\nYou solved {tot_score} out of {num_iters} problems correctly.")

if tot_score==num_iters:
    print("That's a perfect score! Well done! \N{Sparkling Heart}")
