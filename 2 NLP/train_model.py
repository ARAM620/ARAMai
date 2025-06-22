import pickle
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def train_model():
    if not os.path.exists("data.json"):
        initial_data = [
            ["메모장", "notepad"],
            ["웨일", "whale"],
            ["계산기", "calculator"]
        ]
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)
        print("data.json이 없어 기본 데이터를 생성했습니다.")
    
    with open("data.json", "r", encoding="utf-8") as f:
        training_data = json.load(f)

    texts = [x[0] for x in training_data]
    labels = [x[1] for x in training_data]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression()
    model.fit(X, labels)

    with open("intent_model.pkl", "wb") as f:
        pickle.dump(model, f)

    with open("vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    print("모델과 벡터라이저 저장 완료.")

if __name__ == "__main__":
    train_model()
