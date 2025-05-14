# src\training\taining_results.py

from sklearn.metrics import classification_report

# Funkcija novērtēšanai
def evaluate_model(trainer, eval_dataset):
    predictions, labels, _ = trainer.predict(eval_dataset)
    predictions = predictions.argmax(axis=-1)

    # Izveido klasifikācijas pārskatu
    report = classification_report(labels.flatten(), predictions.flatten(), zero_division=0)
    print("Novērtēšanas rezultāti:")
    print(report)

    # Saglabā rezultātus failā
    with open("results/evaluation_report.txt", "w") as f:
        f.write(report)