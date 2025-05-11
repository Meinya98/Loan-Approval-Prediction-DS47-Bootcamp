import streamlit as st
import streamlit.components.v1 as stc
import pickle

with open('Logistic_Regression_model.pkl', 'rb') as file:
    Logistic_Regression_Model = pickle.load(file)

html_temp = """<div style="background-color:#000;padding:10px;border-radius:10px">
                <h1 style="color:#fff;text-align:center">Loan Eligibility Prediction App</h1> 
                <h4 style="color:#fff;text-align:center">Made for: Credit Team</h4> 
                """

desc_temp = """ ### Loan Prediction App 
                This app is used by Credit team for deciding Loan Application
                
                #### Data Source
                Kaggle: Link https://raw.githubusercontent.com/frfusch21/Data-Science-Modul/master/Datasets/LoanApprovalPrediction.csv
                """

def main():
    stc.html(html_temp)
    menu = ["Home", "Machine Learning App"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.markdown(desc_temp, unsafe_allow_html=True)
    elif choice == "Machine Learning App":
        run_ml_app()

def run_ml_app():
    design = """<div style="padding:15px;">
                    <h1 style="color:#fff">Loan Eligibility Prediction</h1>
                </div
             """
    st.markdown(design, unsafe_allow_html=True)

    # Create form structure
    st.subheader("Please fill in the following details to check your loan eligibility")
    left,right = st.columns((2,2))
    gender = left.selectbox('Gender',('male','female'))
    married = right.selectbox('Married',('yes','no'))
    dependent = left.selectbox('Dependents',('0','1','2','3'))
    education = right.selectbox('Education',('Graduate','Not Graduate'))
    self_employed = left.selectbox('Self Employed',('yes','no'))
    applicant_income = right.number_input(label = 'Applicant Income', min_value=0)
    coApplicant_income = left.number_input(label = 'Co-Applicant Income', min_value=0)
    loan_amount = right.number_input(label = 'Loan Amount', min_value=0)
    loan_amount_term = left.number_input(label = 'Loan Amount Term', min_value=0, max_value=360)
    credit_history = right.selectbox('Credit History',('0.0','1.0'))
    property_area = st.selectbox('Property Area',('Rural','Semiurban','Urban'))
    button = st.button("Predict Loan Eligibility")
    #If button is clilcked
    if button:
        result = predict(gender, married, dependent, education, self_employed, applicant_income, coApplicant_income, loan_amount, loan_amount_term, credit_history, property_area)
        if result == 'Eligible':
            st.success(f"Congratulations! You are {result} for the loan.")
        else:
            st.warning(f"Sorry! You are {result} for the loan.")

def predict(gender, married, dependent, education, self_employed, applicant_income, coApplicant_income, loan_amount, loan_amount_term, credit_history, property_area):
    #Processing user input
    gen = 0 if gender == 'Male' else 1
    mar = 0 if married == 'Yes' else 1
    edu = 0 if education == 'Graduate' else 1
    sem = 0 if self_employed == 'Yes' else 1
    pro = 0 if property_area == 'Semiurban' else 1 if property_area == 'Urban' else 2

    #Making prediction
    prediction = Logistic_Regression_Model.predict(
        [[gen, mar, dependent, edu, sem, applicant_income, coApplicant_income, 
          loan_amount, loan_amount_term, credit_history, pro]])     
    result = 'Eligible' if prediction == 1 else 'Not Eligible'
    return result

if __name__ == "__main__":
    main()