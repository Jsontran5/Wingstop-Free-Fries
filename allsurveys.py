# main.py
from blazefunction import blaze_pizza_survey
from pandafunction import panda_survey
from wingstopoptimizedfunction import wingstop_survey
from rubiosfunction import rubios_survey
from concurrent.futures import ThreadPoolExecutor

def main():
    email = input("Enter your email: ")

    # with ThreadPoolExecutor(max_workers=4) as executor:
    #     future_rubios = executor.submit(rubios_survey)
    #     future_blaze_pizza = executor.submit(blaze_pizza_survey, email)
    #     future_panda = executor.submit(panda_survey, email)
    #     future_wingstop = executor.submit(wingstop_survey, email)
        

    #     # Wait for both functions to complete
    #     future_rubios.result()
    #     future_blaze_pizza.result()
    #     future_panda.result()
    #     future_wingstop.result()
        
    rubios_survey()
    blaze_pizza_survey(email)
    panda_survey(email)
    wingstop_survey(email)
    

    return 0

if __name__ == "__main__":
    main()
