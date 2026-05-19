# Blink detection metrics reference

> Use these definitions and formulas any time you need to turn TP/FP/FN/TN counts into actionable blink detection insights.

## Confusion matrix terms

| Term   | What it means for blink detection                | Example                            |
| ------ | ------------------------------------------------ | ---------------------------------- |
| **TP** | true blink correctly detected                    | actual blink detected as blink     |
| **FP** | noise or artifact incorrectly flagged as blink   | spike classified as blink          |
| **FN** | real blink that was missed                       | blink went undetected               |
| **TN** | non-blink that stayed unflagged                  | clean EEG segment left alone        |

## Sample breakdown (200 signal events)

| Category       | Count |
| -------------- | -----:|
| Real blinks    |    150 |
| Non-blinks     |     50 |

| Output         | Count |
| -------------- | -----:|
| **TP**         |    135 |
| **FP**         |     30 |
| **FN**         |     15 |
| **TN**         |     20 |

**What the numbers mean**

* **135** real blinks found → matches TP.
* **30** false blink alarms → FP.
* **15** missed blinks → FN.
* **20** correctly ignored non-blinks → TN.

## Confusion matrix layout

|                      | Predicted blink | Predicted non-blink |
| -------------------- | ---------------:| -------------------:|
| **Actual blink**     |              TP |                 FN  |
| **Actual non-blink** |              FP |                 TN  |

## Key metrics

### Precision
Precision answers: *of the detected blinks, how many were real?*

```math
Precision = \frac{TP}{TP + FP}
```

### Recall
Recall answers: *of the real blinks, how many were captured?*

```math
Recall = \frac{TP}{TP + FN}
```

### Accuracy
Accuracy reflects the overall hit rate across blink and non-blink events.

```math
Accuracy = \frac{TP + TN}{TP + FP + FN + TN}
```

### F1 score
F1 balances precision and recall for a single-number comparison.

```math
F1 = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}
```

## Practical guidance

* Prioritize **recall** when missing blinks is worse than having a few false alarms.
* Watch **precision** when you must avoid too many fake detections, such as for downstream quality metrics.
* **F1 score** is useful when both precision and recall matter and you need one number to compare models.

Give me your TP/FP/FN/TN counts if you want exact metrics computed for your detector.
 