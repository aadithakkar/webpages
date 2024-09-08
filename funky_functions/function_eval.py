def evaluate(expression, f=0, g=0):
    # if expression[1:-1].isdigit():
    #     return int(expression[1:-1])
    if "=" in expression:
        endi = expression.index("=")
        starti = 0
        inpar = 0
        for i in range(endi, -1, -1):
            if expression[i] in ")]":
                inpar += 1
            if expression[i] in "([":
                if inpar:
                    inpar -= 1
                else:
                    starti = i + 1
                    break
            if (not inpar and expression[i] in "+-*/^"):
                starti = i + 1
                break
        startoi = starti
        #print(expression[starti:endi])
        ex1 = expression[starti:endi]
        endi = 0
        starti = expression.index("=") + 1
        inpar = 0
        for i in range(starti, len(expression)):
            if expression[i] in "([":
                inpar += 1
            if expression[i] in ")]":
                if inpar:
                    inpar -= 1
                else:
                    endi = i
                    break
            if (not inpar and expression[i] in "+-*/^"):
                endi = i
                break
        #print(expression[starti:endi])
        ex2 = expression[starti:endi]
        if ex1[0] != "(":
            ex1 = "(" + ex1
        if ex1[-1] != ")":
            ex1 = ex1 + ")"
        if ex2[0] != "(":
            ex2 = "(" + ex2
        if ex2[-1] != ")":
            ex2 = ex2 + ")"
        #print(ex1, ex2, expression, startoi, endi)
        #print("HI", expression[:startoi] + str(int(int(evaluate(ex1) == evaluate(ex2)))) + expression[endi:])
        return evaluate(expression[:startoi] + str(int(evaluate(ex1, f, g) == evaluate(ex2, f, g))) + expression[endi:], f, g)
    if "[" in expression:
        starti = expression.index("[")+1
        brackets = 0
        endi = None
        for i in range(starti, len(expression)):
            if expression[i] == "[":
                brackets += 1
            if expression[i] == "]":
                if brackets == 0:
                    endi = i
                    break
                brackets -= 1
        #print(starti, endi)
        subexp = evaluate(expression[starti:endi], f, g)
        if subexp+0.5==int(subexp+0.5):
            subexp = subexp + 0.5
        else:
            subexp = round(subexp)
        return evaluate(expression[:starti-1] + str(subexp) + expression[endi+1:], f, g)
    if "{" in expression:
        starti = expression.index("{")+1
        brackets = 0
        endi = None
        for i in range(starti, len(expression)):
            if expression[i] == "{":
                brackets += 1
            if expression[i] == "}":
                if brackets == 0:
                    endi = i
                    break
                brackets -= 1
        #print(starti, endi)
        return evaluate(expression[:starti-1] + str(int(evaluate(expression[starti:endi], f, g))) + expression[endi+1:], f, g)
    if "<" in expression:
        starti = expression.index("<")+1
        brackets = 0
        endi = None
        for i in range(starti, len(expression)):
            if expression[i] == "<":
                brackets += 1
            if expression[i] == ">":
                if brackets == 0:
                    endi = i
                    break
                brackets -= 1
        #print(starti, endi)
        testexp = (evaluate(expression[starti:endi], f, g))
        return evaluate(expression[:starti-1] + str(int(round(testexp, 6) in [int(testexp), int(testexp)+1])) + expression[endi+1:], f, g)
    if "a" in expression:
        #print(expression)
        starti = expression.index("a")+1
        brackets = 0
        endi = None
        for i in range(starti, len(expression)):
            if expression[i] == "a":
                brackets += 1
            if expression[i] == "b":
                if brackets == 0:
                    endi = i
                    break
                brackets -= 1
        #print(starti, endi)
        testexp = (evaluate(expression[starti:endi], f, g))
        if testexp == 0:
            testexp = 0
        else:
            testexp = evaluate(f.replace("x", str(testexp)), f, g)
        #print(expression[:starti-1] + str(testexp) + expression[endi+1:])
        return evaluate(expression[:starti-1] + str(testexp) + expression[endi+1:], f, g)
    if "c" in expression:
        #print(expression)
        starti = expression.index("c")+1
        brackets = 0
        endi = None
        for i in range(starti, len(expression)):
            if expression[i] == "c":
                brackets += 1
            if expression[i] == "d":
                if brackets == 0:
                    endi = i
                    break
                brackets -= 1
        #print(starti, endi)
        testexp = (evaluate(expression[starti:endi], f, g))
        if testexp == 0:
            testexp = 0
        else:
            testexp = evaluate(g.replace("x", str(testexp)), f, g)
        #print(expression[:starti-1] + str(testexp) + expression[endi+1:])
        return evaluate(expression[:starti-1] + str(testexp) + expression[endi+1:], f, g)
    expression = expression.replace("^", "**")
    return eval(expression)


def modify(func):
    func = func.replace("==", "=")
    func = func.replace("**", "$")
    func = func.replace("//", "$")
    func = "(" + func + ")"
    while "f" in func:
        starti = func.index("f")
        parcount = 0
        for i in range(starti+1, len(func)):
            if func[i] == "(":
                parcount += 1
            if func[i] == ")":
                if parcount == 1:
                    endi = i
                    break
                else:
                    parcount -= 1
        func = func[:starti] + "a" + func[starti+2:endi] + "b" + func[endi+1:]
    while "g" in func:
        starti = func.index("g")
        parcount = 0
        for i in range(starti+1, len(func)):
            if func[i] == "(":
                parcount += 1
            if func[i] == ")":
                if parcount == 1:
                    endi = i
                    break
                else:
                    parcount -= 1
        func = func[:starti] +  "c" + func[starti+2:endi] + "d" + func[endi+1:]
    return func


def test(inp, out, func, g=0, hide=0):
    if func == "()":
        print("Empty Function Error!")
        return None
    try:
        actual_out = evaluate(func.replace("x", f"({inp})"), func, g)
    except SyntaxError:
        print("Syntax Error!")
        return None
    except RecursionError:
        print("Stack Overflow!")
        return None
    except OverflowError:
        print("Overflow Error!")
        return None
    except:
        print("Error")
        return None
    if float(actual_out) == float(out) or round(float(actual_out), 3) == float(out):
        return True
    else:
        if hide:
            print("Test Fail: Test Hidden")
        else:
            print(f"Test Fail: In = {inp}, Out = {actual_out}, Expected = {out}")
        return False
    

# func = modify(input("Function: "))
# g = modify(input("G: "))
# print(evaluate(func.replace("x", f"({826})"), func, g))


# while True:
#     f = modify(input("Function: "))
#     g = modify(input("G: "))
#     print(f)
#     if test(0, 0, f, g) and test(150, 51, f, g) and test(826, 628, f, g) and test(1023, 3201, f, g):
#         print("Success!")
#         break
