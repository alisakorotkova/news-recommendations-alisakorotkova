<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css">
    <style>
        .labeled { background-color: #f0f0f0; }
        .good { background-color: #e6f9e6; }
        .maybe { background-color: #fffae6; }
        .never { background-color: #ffe6e6; }
    </style>
</head>
<body>
<div class="ui container" style="padding-top: 20px;">
    <h2 class="ui header">Рекомендуемые новости</h2>
    
    %if not rows:
        <div class="ui warning message">Нет новостей для отображения</div>
    %else:
    <table class="ui celled table">
        <thead>
            <tr>
                <th>Заголовок</th>
                <th>Автор</th>
                <th>Сложность</th>
                <th>Предсказания</th>
            </tr>
        </thead>
        <tbody>
            %for news in rows:
            <tr>
                <td><a href="{{ news.url }}" target="_blank">{{ news.title }}</a></td>
                <td>{{ news.author }}</td>
                <td>{{ news.complexity }}</td>
                <td>
                    %if news.predicted_label == 'good':
                        <span class="ui green label">Рекомендуем</span>
                    %elif news.predicted_label == 'maybe':
                        <span class="ui yellow label">Возможно</span>
                    %else:
                        <span class="ui red label">Не интересно</span>
                    %end
                </td>
            </tr>
            %end
        </tbody>
    </table>
    %end
    
    <div class="ui segment">
        <a href="/update_news" class="ui primary button">Обновить новости</a>
        <a href="/news" class="ui button">Все новости</a>
    </div>
</div>
</body>
</html>