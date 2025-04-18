from bottle import route, run, template, request, redirect  # type: ignore

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    s.close()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    # PUT YOUR CODE HERE
    news_id = int(request.query.id)
    label = request.query.label
    s = session()
    news_item = s.query(News).get(news_id)
    if news_item:
        news_item.label = label
        s.commit()
    if __name__ == "__main__":
        redirect("/news")


@route("/update_news")
def update_news():
    # PUT YOUR CODE HERE
    news_list = get_news("https://habr.com/ru/all", n_pages=15)
    print(news_list)
    s = session()
    try:
        for news_data in news_list:
            existing_news = (
                s.query(News).filter(News.title == news_data["title"], News.author == news_data["author"]).first()
            )
            if not existing_news:
                new_news = News(
                    title=news_data["title"],
                    author=news_data["author"],
                    url=news_data["url"],
                    complexity=news_data.get("complexity", "-"),
                )
                s.add(new_news)
                s.commit()
    except Exception as e:
        print(f"Ошибка при обновлении новостей: {e}")
        s.rollback()
    finally:
        s.close()
    if __name__ == "__main__":
        redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    s = session()
    try:
        labeled_news = s.query(News).filter(News.label != None).all()

        X_train = [f"{news.title} {news.complexity}" for news in labeled_news]
        y_train = [news.label for news in labeled_news]

        classifier = NaiveBayesClassifier(alpha=1)
        classifier.fit(X_train, y_train)

        unlabeled_news = s.query(News).filter(News.label == None).all()

        X_new = [f"{news.title} {news.complexity}" for news in unlabeled_news]
        predictions = classifier.predict(X_new)

        for news, pred in zip(unlabeled_news, predictions):
            news.predicted_label = pred

        label_priority = {"good": 0, "maybe": 1, "never": 2}

        sorted_pairs = sorted(unlabeled_news, key=lambda x: label_priority[x.predicted_label])
        # X = [f"{news.title} {news.complexity}" for news in labeled_news]
        # y = [news.label for news in labeled_news]
        # num_of_test = int(len(labeled_news) * 0.25)
        # X_test = X[:num_of_test]
        # y_test = y[:num_of_test]
        # X_train = X[num_of_test:]
        # y_train = y[num_of_test:]
        # X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state=42)

        # classifier = NaiveBayesClassifier(alpha=1)
        # classifier.fit(X_train, y_train)
        # accuracy = classifier.score(X_test, y_test)
        # print(accuracy)

        # if __name__ != "__main__":
        return sorted_pairs

        # return template('news_template', rows=sorted_news)
    finally:
        s.close()


@route("/recommendations")
def recommendations():
    s = session()
    try:

        classified = classify_news()
        print(classified)

        return template("news_recommendations", rows=classified)
    finally:
        s.close()


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
