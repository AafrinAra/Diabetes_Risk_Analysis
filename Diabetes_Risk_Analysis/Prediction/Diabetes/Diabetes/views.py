# code
from django.shortcuts import render
import pandas as pd

# Defer importing scikit-learn until the view runs so the dev server
# won't crash on startup when scikit-learn is not installed.

# for call home.html
def home(request):
    return render(request, 'home.html')

# for call predict.html
def predict(request):
    return render(request, 'predict.html')

# for display result on same page
def result(request):
    data = pd.read_csv(r"diabetes.csv")
    X = data.drop("Outcome", axis=1)
    Y = data["Outcome"]

    # Import scikit-learn here and show a helpful message if it's missing
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score
    except ImportError:
        return render(
            request,
            "predict.html",
            {
                "result2": (
                    "Server error: missing dependency 'scikit-learn'. "
                    "Install it in your environment with: pip install scikit-learn"
                )
            },
        )

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

    model = LogisticRegression()
    model.fit(X_train, Y_train)

    val1 = float(request.GET['n1'])
    val2 = float(request.GET['n2'])
    val3 = float(request.GET['n3'])
    val4 = float(request.GET['n4'])
    val5 = float(request.GET['n5'])
    val6 = float(request.GET['n6'])
    val7 = float(request.GET['n7'])
    val8 = float(request.GET['n8'])

    pred = model.predict([[val1, val2, val3,
                           val4, val5, val6, val7, val8]])

    result1 = ""
    if pred == [1]:
        result1 = "Diabetes risk detected. Medical advice is recommended."
    else:
        result1 = "No diabetes risk detected. Stay healthy."

    return render(request, "predict.html", {"result2": result1})