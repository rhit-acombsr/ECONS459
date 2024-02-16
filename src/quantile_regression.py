import numpy as np
import statsmodels.formula.api as smf
import pandas as pd



# # Example usage:
# # alphas = np.random.randn(124) * 0.03 - 0.03  # Generating some dummy alpha values for demonstration
# alphas = [-0.0012961334712643, -0.0026515923912585, -0.0019053278734480, -0.0010118721702770, -0.0044568389975975, -0.0057478957941918, -0.0084539032087319, -0.0064812349866509, -0.0053889085152327, -0.0034470324677369, -0.0050009839136477, -0.0039955860561227, -0.0057616400627252, -0.0137502669300543, -0.0233561972231696, -0.0109022007794174, -0.0332076483926323, 0.0024654386475955, -0.0000940426868093, -0.0085095785773083, -0.0075977598383462, -0.0112083033316054, -0.0075615855887342, -0.0059775059764067, 0.0012188796959472, -0.0076313492152929, -0.0204341111929440, -0.0217898330024630, -0.0207838241788166, -0.0126658558592215, 0.0050605264117713, -0.0169086649654390, -0.0017217575088467, -0.0122463202620833, -0.0239348862495412, -0.0139907108037993, -0.0160603713136605, -0.0337139007809824, -0.0144821027571457, -0.0076553691123992, -0.0190433545684730, -0.0166187320672385, -0.0226098704601307, -0.0081558232912415, -0.0208587492925720, -0.0300208870838878, -0.0196268710136884, -0.0260103106894554, -0.0276297728774715, -0.0204832785700618, -0.0182814064354875, -0.0222256896902085, -0.0258346979933552, -0.0280101796541412, -0.0317639135112288, -0.0384023828556795, -0.0452008614249020, -0.0191265780021669, -0.0251832489124778, -0.0207157439861150, -0.0114994983291531, -0.0129771155339489, -0.0128951049456062, -0.0272277825039774, -0.0380845374005673, -0.0084051682631718, -0.0210719010743912, -0.0157584880192367, -0.0145848288184592, -0.0267794738019181, -0.0204185963440637, -0.0286889271357492, -0.0336753890475585, -0.0218947395496203, -0.0123846322653549, -0.0221999535281763, -0.0413326219260290, -0.0130415725519425, -0.0429631350278777, -0.0489282658945486, -0.0111029262725042, -0.0109954686352354, -0.0337451799408381, -0.0301856031884612, -0.0057328918585619, -0.0399587613925634, -0.0585209715512969, -0.0301336369563050, -0.0254868590559461, -0.0293911464296153, -0.0146373859085300, -0.0251735493053936, -0.0182089277345611, -0.0219605016206065, -0.0305105894713281, -0.0130447273372611, -0.0249761051795496, -0.0322902854464773, -0.0147577901834689, -0.0141185724377732, -0.0406182930930071, -0.0103989223769909, -0.0181802723286234, -0.0257559087676496, -0.0370259826205881, -0.0156230125246003, -0.0237286206956635, -0.0412953788616880, -0.0353317583872803, -0.0032363866453234, -0.0268311330114025, -0.0152093070120470, -0.0268359041734152, -0.0418696246965185, -0.0568235949759133, -0.0366648035129179, -0.0211929730074283, -0.0329278497610145, -0.0441378995076583, 0.0166638110425532, 0.0365422709076982, -0.0542458343022556, -0.0111878723719392]
# results = quantile_regression_alpha(alphas)

# # To print the summary for each quantile regression model:
# for quantile, result in results.items():
#     print(f'{quantile} Regression Results:')
#     print(result.summary())


import numpy as np
import statsmodels.formula.api as smf
import pandas as pd
import random
import math

def unknown_function(k):
    constant_a = 5.415
    return constant_a*math.log(k)

def generate_data_point(k):
    upper_bound = 0
    lower_bound = 0-unknown_function(k)
    data_point = random.uniform(upper_bound,lower_bound)
    return data_point

data = []
for k in range(124):
    data.append(generate_data_point(k+1))

def quantile_regression_alpha(alphas, quantiles=[0.05, 0.95]):
    """
    Perform quantile regression on a list of alpha values over a range of k values.
    
    Parameters:
    - alphas: List of alpha values, assumed to be ordered from k=1 to k=124.
    - quantiles: List of quantiles to model (e.g., [0.05, 0.95] for 5th and 95th percentiles).
    
    Returns:
    - A dictionary containing regression results for each quantile.
    """
    # Ensure input is a pandas DataFrame
    df = pd.DataFrame({'alpha': alphas, 'k': range(1, len(alphas) + 1)})
    
    # Dictionary to store results
    results = {}
    
    # Perform quantile regression for specified quantiles
    for q in quantiles:
        model = smf.quantreg('alpha ~ k', df)
        res = model.fit(q=q)
        results[f'Quantile {q}'] = res
    
    return results

# # Example usage of "quantile_regression_alpha(data,quintiles)" function:
# quintiles = [0.04]
# results = quantile_regression_alpha(data,quintiles)

# Function to perform quantile regression and estimate the lower bound
def estimate_lower_bound(data, quantile=0.05):
    # Creating a DataFrame with data points and their corresponding k values
    df = pd.DataFrame(data, columns=['alpha'])
    df['k'] = range(1, len(data) + 1)

    # Perform quantile regression to estimate the lower bound
    model = smf.quantreg('alpha ~ k', df)
    res = model.fit(q=quantile)

    # Predict the lower bound using the quantile regression model
    df['lower_bound_estimate'] = res.predict(df[['k']])
    
    return df['lower_bound_estimate'].tolist()

print("data:")
print(data)
print("lower_bound:")
print(estimate_lower_bound(data, 0.05))

# def estimate_lower_bound(data):
#     bound_estimate = []
#     # TODO: Implement this function via quantile regression
#     return bound_estimate

# quintiles = [0.04]
# results = quantile_regression_alpha(data,quintiles)

# for quantile, result in results.items():
#     print(f'{quantile} Regression Results:')
#     print(result.summary())


# print(data)