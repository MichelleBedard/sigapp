# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.proportion import proportions_chisquare_allpairs
import altair as alt
import copy

st.sidebar.title('Navigation')
st.sidebar.markdown("<a href='#linkto_nav0'>Top</a>", unsafe_allow_html=True)
st.sidebar.markdown("<a href='#linkto_nav1'>(1) Identify how many groups to compare</a>", unsafe_allow_html=True) 
st.sidebar.markdown("<a href='#linkto_nav2'>(2) Determine your success criteria</a>", unsafe_allow_html=True) 
st.sidebar.markdown("<a href='#linkto_nav3'>(3) Enter the data for your test</a>", unsafe_allow_html=True) 
st.sidebar.markdown("<a href='#linkto_nav4'>(4) Test if the difference between groups is statistically significant</a>", unsafe_allow_html=True) 

st.markdown("<div id='linkto_nav0'></div>", unsafe_allow_html=True)
st.title('Test for statistical significance tool')

st.header('Follow the steps below according to what you are testing')
st.write('  ') 
st.write('Note: This tool is only valid when each user is in only one group.')
st.write('__95% confidence interval__ is used during testing. This is the industry standard / best practice.')

st.markdown("<div id='linkto_nav1'></div>", unsafe_allow_html=True)
st.subheader('(1) Are you comparing two groups, or more than two groups?')
st.markdown('*__Example:__*<br /> __2 Groups:__ 2 email subject lines <br /> __More than 2 Groups:__ Day of the week testing (7 groups)', unsafe_allow_html=True)

def num_check(num):
    if int(str(float(num)).split('.')[1])==0 and num>=0:
        return True
    
def denom_check(num):
    if int(str(float(num)).split('.')[1])==0 and num>0:
        return True

def success_sample(s,n):
    if s<=n:
        return True

def try_data_tbl(names,nums,denoms):
    try:
        if all(num_check(nums[j]) for j in range(len(nums))) == True and all(denom_check(denoms[j]) for j in range(len(denoms))) == True and all(success_sample(nums[j],denoms[j]) for j in range(len(nums)))==True:
        #if all(num_check(g_2[j]) for j in range(len(g_2)))==True and all(denom_check(g_3[j]) for j in range(len(g_3)))==True and all(success_sample(g_2[j],g_3[j]) for j in range(len(g_2)))==True:
        #    multi_data().append([name_3,s3,n3,s3/n3*100])
            df=pd.DataFrame({'success':nums,'total':denoms})
            df.rename(lambda x: names[x], axis=0, inplace=True)
            dft=np.transpose(df)
            pct=pd.Series(dft.iloc[0]/dft.iloc[1]*100, name='success percentage')
            dft=dft.append(np.transpose(pct),ignore_index=False)
            result = dft
        else:
            result = 'Please enter valid inputs. Numbers must be positive whole numbers, and the number of successes cannot exceed the total number in the group.'
    except:
        result = 'Please enter valid inputs. Numbers must be positive whole numbers, and the number of successes cannot exceed the total number in the group.'
    return result

test_type = st.radio(
     "Choose if you are comparing two groups or more than two groups",
     ('Two groups', 'More than two groups'))

a=0.05

if test_type == 'Two groups':
    st.header('Comparing two groups')
    
    st.markdown("<div id='linkto_nav2'></div>", unsafe_allow_html=True)
    st.subheader('(2) What is your success criteria and total?')
    st.markdown('*__Example__ (Email Open Rate)__:__*<br /> __Success:__ # of Email Opens <br /> __Total:__ # of Email Sends <br /> __Group 1:__ Subject Line Variation A <br /> __Group 2:__ Subject Line Variation B', unsafe_allow_html=True)
    
    st.markdown("<div id='linkto_nav3'></div>", unsafe_allow_html=True)
    st.subheader('(3) Enter the number of successes and total number for each group you are testing')
    st.write('  ') 
    
    i_s1, i_n1 = st.beta_columns(2)
    with i_s1:
        s1=st.number_input('Number of successes in group 1', min_value=0, value=0)
    with i_n1:
        n1=st.number_input('Total number in group 1', min_value=0, value=0)
        
    i_s2, i_n2 = st.beta_columns(2)
    with i_s2:
        s2=st.number_input('Number of successes in group 2', min_value=0, value=0)
    with i_n2:
        n2=st.number_input('Total number in group 2', min_value=0, value=0)

    st.markdown("<div id='linkto_nav4'></div>", unsafe_allow_html=True)
    st.subheader('(4) Click "Calculate" to test if the difference between groups is statistically significant')
    st.write('  ') 

    if st.button("Calculate"): 
        if num_check(s1)==True and denom_check(n1)==True and num_check(s2)==True and denom_check(n2)==True and success_sample(s1,n1)==True and success_sample(s2,n2)==True:
            z=proportions_ztest(count=np.array([s1,s2]), nobs=np.array([n1,n2]),  alternative='two-sided')
            #st.write('Proportion test p-value: ', str(z[1]))
            p1=str((s1/n1)*100)
            p2=str((s2/n2)*100)
            if np.isnan(z[1]):
                st.write('Unable to calculate p-value.')
            elif z[1]<a:
                st.markdown(f"<span style='color:green'> __Statistically Significant at a 95% confidence interval__ </span> _(Groups are different)_ <br /> __Group 1:__ {p1}% <br /> __Group 2:__ {p2}%", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:red'> __Not Statistically Significant at a 95% confidence interval__ </span> _(We cannot determine if the groups are different)_ <br /> __Group 1:__ {p1}% <br /> __Group 2:__ {p2}%", unsafe_allow_html=True)
        else:
            st.write('Please enter valid inputs. Numbers must be positive whole numbers, and the number of successes cannot exceed the total number in the group')
 
elif test_type == 'More than two groups':
    st.header('Comparing more than two groups')
    
    st.markdown("<div id='linkto_nav2'></div>", unsafe_allow_html=True)
    st.subheader('(2) What is your success criteria and total?')
    st.markdown('*__Example__ (Email Open Rate)__:__*<br /> __Success:__ # of Email Opens <br /> __Total:__ # of Email Sends <br /> __Group 1:__ Sent on Monday <br /> __Group 2:__ Sent on Wednesday <br /> __Group 3:__ Sent on Friday', unsafe_allow_html=True)
    
    st.markdown("<div id='linkto_nav3'></div>", unsafe_allow_html=True)
    st.subheader('(3) For each group, enter the number of successes and total number. You may also edit the group name, if desired. Click "See Data" to view your input.')
    st.write('  ') 
    
    group_counter=st.number_input('How many groups are you comparing?', min_value=0, value=3)
    
    #for each group, we want to store inputs 1, 2, and 3 (for the name, success, and total)
    g_1=[]
    g_2=[]
    g_3=[]
    for i in range(group_counter):
        g_1.append(str(group_counter)+'_1')
        g_2.append(str(group_counter)+'_2')
        g_3.append(str(group_counter)+'_3')
    for i in range(group_counter):        
        i_name3, i_s3, i_n3 = st.beta_columns(3)
        with i_name3:
            g_1[i]=st.text_input(str(i+1)+') Group Name', value='Group '+str(i+1))
        with i_s3:
            g_2[i]=st.number_input(str(i+1)+') Number of successes in group', min_value=0, value=0)
        with i_n3:
            g_3[i]=st.number_input(str(i+1)+') Total number in group', min_value=0, value=0)
            
    st.write(' ')        
    
    if st.button ('See Data'):
        if type(try_data_tbl(g_1,g_2,g_3)) == type(pd.DataFrame()):
            st.write(try_data_tbl(g_1,g_2,g_3))
            plt_data=pd.DataFrame(list(zip(try_data_tbl(g_1,g_2,g_3).columns.values.tolist(),try_data_tbl(g_1,g_2,g_3).iloc[2].tolist())),columns=['groups','success percentage'])
            st.markdown('<br />', unsafe_allow_html=True)
            st.write(alt.Chart(plt_data, title='Proportions to test from above user input').mark_bar().encode(
                x=alt.X('groups', sort=None),
                y='success percentage',
                tooltip=['groups','success percentage']
                ).properties(width=700))  
        else:
            st.markdown(f"<span style='color:red'> {try_data_tbl(g_1,g_2,g_3)} </span>", unsafe_allow_html=True)
        
        
    st.markdown("<div id='linkto_nav4'></div>", unsafe_allow_html=True)
    st.subheader('(4) Choose the control group and click "Calculate" to test if the difference between groups is statistically significant')
    st.write('  ') 
    
    st.markdown('Select the control group for your experiment. <br /> _The control group will be compared to all variation groups while testing for significance._', unsafe_allow_html=True)
    control_lst=copy.deepcopy(g_1)
    control_lst.append('N/A - No control group (comparing every group against all other variants)')
    
    control_type = st.radio('Select Control Group',control_lst)
    
    
    st.markdown('*__Example:__*<br /> _In our weekday example, if Monday is the control group, you want to compare email open rate for:_ <br /> - Monday vs Wednesday <br /> - Monday vs Friday <br />', unsafe_allow_html=True)
    
    
    if st.button('Calculate '):        
        if type(try_data_tbl(g_1,g_2,g_3)) == type(pd.DataFrame()):
            st.write(try_data_tbl(g_1,g_2,g_3))
            st.text('The calculation uses the holm-sidak method to adjust p-values in multiple tests.')
            results=proportions_chisquare_allpairs(np.array(g_2), np.array(g_3))
            #st.write(results)
            p_values=results.pval_corrected()
            pair_names=results.all_pairs_names
            sig= ''
            nsig=''
            if control_type == 'N/A - No control group (comparing every group against all other variants)':
                for i in range(len(p_values)):
                    t=f'__{g_1[int(pair_names[i][1])]}__ ({str(round(g_2[int(pair_names[i][1])]/g_3[int(pair_names[i][1])]*100,4))}%) and __{g_1[int(pair_names[i][4])]}__ ({str(round(g_2[int(pair_names[i][4])]/g_3[int(pair_names[i][4])]*100,4))}%) are'
                    if float(p_values[i])<a:
                        sig=sig+('\n'+f'{t}'+' <span style="color:green">significantly different</span> <br />')
                    elif float(p_values[i])>=a:
                        nsig=nsig+('\n'+f'{t}'+' <span style="color:red">not significantly different</span> <br />')
                if len(sig)>len(''):
                    st.markdown('<span style="color:green">__Statistically Significant results (at a 95% confidence interval):__</span>', unsafe_allow_html=True)
                    st.markdown(sig, unsafe_allow_html=True)
                if len(nsig)>len(''):
                    st.markdown('<span style="color:red">__Not Statistically Significant results (at a 95% confidence interval):__</span>', unsafe_allow_html=True)
                    st.markdown(nsig, unsafe_allow_html=True)
                elif len(nsig)<=len('') and len(sig)<=len(''):
                    st.markdown('_Unable to calculate p-value._', unsafe_allow_html=True)
            else:
                list_number=g_1.index(control_type)
                control_items=[]
                p_items=[]
                control_names=[]
                for i in range(len(pair_names)):
                    if pair_names[i][1]==str(list_number):
                        control_items.append(pair_names[i])
                        p_items.append(p_values[i])
                    if pair_names[i][4]==str(list_number):
                        control_items.append(pair_names[i])    
                        p_items.append(p_values[i])
                for i in range(len(control_items)):
                    control_names.append('__'+str(g_1[int(control_items[i][1])])+'__ ('+ str(round(g_2[int(control_items[i][1])]/g_3[int(control_items[i][1])]*100,4)) +'%) and __'+str(g_1[int(control_items[i][4])])+'__ ('+ str(round(g_2[int(control_items[i][4])]/g_3[int(control_items[i][4])]*100,4))+ '%)')
                for i in range(len(p_items)): 
                    t=f'{control_names[i]} are'
                    if float(p_items[i])<a:
                        sig=sig+('\n'+f'{t}'+' <span style="color:green">significantly different</span> <br />')
                    elif float(p_items[i])>=a:
                        nsig=nsig+('\n'+f'{t}'+' <span style="color:red">not significantly different</span> <br />')
                if len(sig)>len(''):
                    st.markdown('<span style="color:green">__Statistically Significant results (at a 95% confidence interval):__</span>', unsafe_allow_html=True)
                    st.markdown(sig, unsafe_allow_html=True)
                if len(nsig)>len(''):
                    st.markdown('<span style="color:red">__Not Statistically Significant results (at a 95% confidence interval):__</span>', unsafe_allow_html=True)
                    st.markdown(nsig, unsafe_allow_html=True)
                elif len(nsig)<=len('') and len(sig)<=len(''):
                    st.markdown('_Unable to calculate p-value._', unsafe_allow_html=True)
        else: 
            st.markdown(f"<span style='color:red'> {try_data_tbl(g_1,g_2,g_3)} </span>", unsafe_allow_html=True)
            st.markdown('__Unable to calculate p-value.__', unsafe_allow_html=True)

st.title('')
st.title('')
st.title('')
st.title('')
st.title('')
st.title('')
st.title('')
st.title('')
st.title('')
st.title('')
st.title('')
st.title('')
st.title('')    
st.title('')
st.title('')          
