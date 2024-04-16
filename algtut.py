import numpy as np

import sympy as sp
from IPython.display import display
import mailtrap as mt
from datetime import datetime

def save_dict(optdict, fname="options.txt", delim=":"):
    with open(fname, 'w') as file:
        file.writelines(str(x)+delim+str(y)+"\n" for x,y in optdict.items())

def load_dict(fname="options.txt", delim=":"):
    with open(fname, 'r') as file:
        lines = file.readlines() 
 
        optdict = {} 
        for line in lines: 
            key, value = line.strip().split(delim) 
            optdict[key] = value
        return optdict


def choose_number(max_enum, max_denom=1, is_pos=False):
    a = np.random.choice(max_enum+1)
    b = np.random.choice(np.arange(1,max_denom+1))
    s = np.random.choice([-1,1])
    return sp.sympify(f"{s}*{a}/{b}" if not is_pos else a/b)


opts = load_dict()

difficulty_def = int(opts['difficulty'])
unknowns_def = int(opts['unknowns'])
name = opts['name']


print(f"Hello {name}. Ready for some equations? Here we go...")

tot_score = 0

difficulty_inp = input(f"\nEnter level of difficulty: (1-5) [{difficulty_def}] ")
difficulty = difficulty_def if difficulty_inp.strip()=="" else int(difficulty_inp)
print("\n\n\n")


match difficulty:
    case 1:
        max_e =3 
        max_d =1 
    case 2:
        max_e =5 
        max_d =1 
    case 3:
        max_e =10 
        max_d =5 
    case 4:
        max_e =10 
        max_d =1 
    case 5:
        max_e =20 
        max_d =5 
        pass

nums = np.arange(-max_e,max_e+1)
nums_nz=np.concatenate((np.arange(-max_e,0),np.arange(1,max_e+1)))

num_iters = 10

unknowns_inp = input(f"How many unknowns: (1 or 2)  [{unknowns_def}] ")
unknowns = unknowns_def if unknowns_inp.strip()=="" else int(unknowns_inp)

save_dict({"difficulty":difficulty, "unknowns":unknowns, "name":name})

if unknowns==1:
    for i in range(num_iters):
        xval = choose_number(max_e, max_d)
        [a1,a2] = np.random.choice(nums,2,replace=False)
        b1 = np.random.choice(nums)
        b2 = a1*xval+b1-a2*xval
        b2_1,b2_2 = sp.fraction(b2)

        x = sp.symbols('x')
        print(f"\n\nProblem ({i+1}/{num_iters}):")
        eq = sp.Eq((a1*x+b1)*b2_2,(a2*x+b2)*b2_2)
        display(eq)
        # print(sp.pretty(eq,use_unicode=True))
        # print(sp.print_latex(eq))

        x_ = sp.sympify(input("\nx="))
        if xval==x_:
            print("Correct. \N{smiling face with sunglasses}")
            tot_score += 1
        else:
            print(f"Incorrect. \N{slightly frowning face}\nThe correct answer was x={xval}.")
elif unknowns==2:
    x,y = sp.symbols('x y')
    for i in range(num_iters):
        valid_soln=False
        while not valid_soln:
            xval = choose_number(max_e, max_d)
            yval = choose_number(max_e, max_d)
            [ax,ay] = np.random.choice(nums_nz,2,replace=True)
            [bx,by] = np.random.choice(nums_nz,2,replace=True)
            a_1,a_2 = sp.fraction(ax*xval+ay*yval)
            b_1,b_2 = sp.fraction(bx*xval+by*yval)
            eqA = sp.Eq((ax*x+ay*y)*a_2,a_1)
            eqB = sp.Eq((bx*x+by*y)*b_2,b_1)        
            if len(sp.solve((eqA,eqB),(x,y)))==2:
                valid_soln=True

        print(f"\n\nProblem ({i+1}/{num_iters}):")
        display(eqA)
        display(eqB)

        # display(sp.solve((eqA,eqB),(x,y)))

        x_ = sp.sympify(input("\nx="))
        y_ = sp.sympify(input("\ny="))
        if xval==x_ and yval==y_:
            print("Correct. \N{smiling face with sunglasses}")
            tot_score += 1
        else:
            print(f"Incorrect. \N{slightly frowning face}\nThe correct answer was x={xval} and y={yval}.")


s = f"\n\nYou solved {tot_score} out of {num_iters} problems correctly.\n"
if tot_score==num_iters:
    s += "That's a perfect score! Well done! \N{Sparkling Heart}"

print(s)
now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
mail = mt.Mail(
    sender=mt.Address(email="mailtrap@demomailtrap.com", name="Math test results"),
    to=[mt.Address(email="y_vog@yahoo.com")],
    subject=f"Math test ({name}): {tot_score}/{num_iters}",
    text=f"Test taken at {now}\n\n" + s
)

client = mt.MailtrapClient(token="504aeeabe79239741fecdcba8b988662")
client.send(mail)