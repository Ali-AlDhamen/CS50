import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")



def load_data(filename):
    months = {
        'Jan': 0,
        'Feb': 1,
        'Mar': 2,
        'Apr': 3,
        'May': 4,
        'June': 5,
        'Jul': 6,
        'Aug': 7,
        'Sep': 8,
        'Oct': 9,
        'Nov': 10,
        'Dec': 11

    }
    evidence = []
    labels = []
    sample = [0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 1, 1, 1, 1, 1, 0]

    with open(filename, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
    # Iterate over each row in the csv using reader object
        for row in csv_reader:
            for index, value in enumerate(sample):
                if 'Administrative' in row:
                    continue

                if index == 10:
                    row[index] = months[row[10]]
                if index == 15:
                    if row[index] == 'Returning_Visitor':
                          row[index] = 1
                    else:
                          row[index] = 0
                if index == 16:
                    if row[index] == 'TRUE':
                          row[index] = 1
                    else:
                          row[index] = 0
                if index == 17:
                    if row[index] == 'TRUE':
                        row[index] = 1
                    else:
                        row[index] = 0
                if type(value) == float:
                    row[index] = float(row[index])
                elif type(value) == int:
                    row[index] = int(row[index])


            if row[-1] == 'TRUE':
                row[-1] = 1
            else:
                row[-1] = 0
            evidence.append(row[:-1])
            labels.append(row[-1])
    evidence.pop(0)
    labels.pop(0)
    return (evidence, labels)


def train_model(evidence, labels):
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model


def evaluate(labels, predictions):
    sensitivity = 0
    specificity = 0
    total =0
    for did , pre in zip(labels, predictions):
        total+=1
        if did == pre:
            sensitivity +=1
        else:
            specificity +=1
    sensitivity = sensitivity/total
    specificity = specificity/total
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
