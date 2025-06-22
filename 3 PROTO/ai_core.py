import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from data_store import load_data
import settings

def load_model():
    try:
        with open("intent_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("vectorizer.pkl", "rb") as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    except FileNotFoundError:
        print("모델 파일 없음, 재학습 시작")
        retrain_model()
        with open("intent_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("vectorizer.pkl", "rb") as f:
            vectorizer = pickle.load(f)
        return model, vectorizer

def predict_intent(text, model, vectorizer):
    excluded = ["학습", "종료", "그만", "나가"]
    if text.strip().lower() in excluded:
        if settings.DEBUG:
            print("내부 명령어로 예측 제외됨")
        return "ignore"
    
    data = load_data()
    for sentence, intent in data:
        if sentence.strip().lower() == text.strip().lower():
            if settings.DEBUG:
                print(f"정확 매칭 의도: {intent}")
            return intent
        
    X_test = vectorizer.transform([text])
    pred = model.predict(X_test)
    if settings.DEBUG:
        print(f"예측 의도: {pred[0]}")
    return pred[0]

def retrain_model():
    data = load_data()
    if not data:
        print("학습 데이터 없음")
        return
    texts = [x[0] for x in data]
    labels = [x[1] for x in data]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    model = LogisticRegression()
    model.fit(X, labels)
    with open("intent_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    print("재학습 완료")

def add_training_example(sentence, intent):
    from data_store import load_data, save_data

    data = load_data()
    data.append([sentence, intent])
    save_data(data)
    retrain_model()
    print("재학습 완료")
