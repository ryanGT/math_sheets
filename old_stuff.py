new = 0
if new:
    ## myworksheet = worksheet_generator('addition_new.tex')
    ## myworksheet.generate_worksheet()
    ## myworksheet.run_latex()

    ## mypairs = {one_more_generator:'one_more_addition.tex', \
    ##            two_more_generator:'two_more_addition.tex', \
    ##            worksheet_generator:'addition_new.tex', \
    ##            subtraction_generator:'subtraction_new.tex', \
    ##            one_less_generator:'one_less_subtraction.tex', \
    ##            two_less_generator:'two_less_subtraction.tex', \
    ##            one_or_two_less_generator:'one_or_two_less_subtraction.tex', \
    ##            }

    #mypairs = {single_digit_addition:'addition_new.tex', \
    #           }
    import datetime
    now = datetime.datetime.now()
    datestr = now.strftime('%m_%d_%y')

    #mylist = [#(multiplication_generator,'multiplication.tex',{}), \
        #(multiplication_generator,'multiplication_level_2.tex',{'max_B':10, 'max_A':10}), \
        #(multiply_by_3, 'multiply_by_3.tex'), \
        #(multiply_by_B, 'multiply_by_2.tex', {'B':2}), \
        #(multiply_by_B, 'multiply_by_7.tex', {'B':7}), \
        #(multiply_by_2_or_3, 'multiply_by_2_or_3.tex'), \
        #(multiplication_intro_generator, 'multiply_by_2_intro.tex',{'B':2}), \
        #(multiplication_intro_generator, 'multiply_by_4_intro.tex', {'B':4}), \
        #(multiplication_intro_generator, 'multiply_by_5_intro.tex', {'B':5}), \
        #(multiplication_intro_generator, 'multiply_by_6_intro.tex', {'B':6}), \
        #(multiplication_intro_generator, 'multiply_by_8_intro.tex', {'B':8}), \
        #(multiplication_intro_generator, 'multiply_by_9_intro.tex', {'B':9}), \
        #(variable_add_subtract, 'mostly_add.tex', {'add_thresh':0.8}), \
        #(variable_add_subtract, 'mixed_add_subtract.tex', \
        #            {'add_thresh':0.6,'allow_neg':False}), \
        #(worksheet_generator,'addition_new.tex',{}), \
        #(addition_easy_to_medium,'addition_e_to_m_1.tex',{}), \
        #(addition_easy_to_medium,'addition_e_to_m_2.tex',{}), \
        #(addition_level_2,'addition_new_2B.tex',{}), \
        #(addition_level_2,'addition_new_3.tex',{'max_A':30, 'max_B':30}), \
        #(addition_two_digit_plus_single_digit,'addition_new_2C.tex',{}), \
        #(addition_two_digit_plus_single_digit,'addition_new_2D.tex',{}), \
        #(subtraction_generator,'subtraction_level_1_5.tex',{'mymax':15}), \
        #(mixed_add_subtract,'mixed_add_subtract.tex',{}), \
        ##!!!# Nov. 2020

    list1 = [#(multiplication_intro_generator, 'multiply_by_3_intro.tex'), \
             #(multiplication_intro_generator, 'multiply_by_4_intro.tex', {'B':4}), \
             #(multiply_range, 'multiply_by_2_thru_4_%s.tex' % datestr, {'B_list':[2,3,4]}), \
             (subtraction_force_negative, 'neg_subtract_1.tex', {}), \
             (add_big_to_little, 'add_big_to_little.tex', {}), \
             ]


    mylist = list1#+list2
    ## mypairs = {#one_more_generator:'one_more_addition.tex', \
    ##            #two_more_generator:'two_more_addition.tex', \
    ##            #worksheet_generator:'addition_new.tex', \
    ##            subtraction_generator:'subtraction_new.tex', \
    ##            #one_less_generator:'one_less_subtraction.tex', \
    ##            }

    run_print = 1

    for row in mylist:
        myclass = row[0]
        fn = row[1]
        if len(row) == 2:
            kwargs = {}
        else:
            kwargs = row[2]
        myworksheet = myclass(fn, **kwargs)
        myworksheet.generate_worksheet()
        myworksheet.run_latex()

        if run_print:
            fno, ext = os.path.splitext(fn)
            pdf_name = fno + '.pdf'
            #pcmd = "lpr %s" % pdf_name
            pcmd = "python3 -m webbrowser %s &" % pdf_name
            #pcmd = "okular %s" % pdf_name
            os.system(pcmd)


    ## for i in range(2):
    ##     generate_number_bonds(i+1)



    #sub2 = subtraction_generator('subtraction_level_1.tex', mymax=10)
    #sub2.generate_worksheet()
    #sub2.run_latex()
