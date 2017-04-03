Personalize News Recommendation sysytem by Tweet

Tweetを元にユーザの興味を反映したニュース記事を推薦するシステム


## 機能

- [NHK NEWS WEB](http://www3.nhk.or.jp/news/)から、ユーザの関心が高いと推測されるニュースを選定する


## 入力データ

- 認証したTwitterユーザのTweet


## 使ってるもの

- word2vec

- scikit-learn


## しくみ

ツイート中に頻出する名詞と[単語感情極性対応表](http://www.lr.pi.titech.ac.jp/~takamura/pndic_ja.html)に基づくツイートの感情極性から、言及する話題やポジティブな感情を持つ話題を分析することで、ユーザの興味関心を推定する
