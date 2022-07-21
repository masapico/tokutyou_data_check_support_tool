# 年金特徴送信データ確認支援ツール

市区町村が国保連合会に送信する年金特徴データ（情報交換媒体）の確認を支援するツール

## 利用方法

実行ファイルのダウンロードは[Releases](https://github.com/masapico/tokutyou_data_check_support_tool/releases)から

想定する利用方法は以下のとおり：

1. パソコンでフォルダを作成します（サーバではなく、パソコン上に作成）
2. 送信しようとするデータを作成したフォルダに格納する（拡張子がdta）
    - 介護分 Z1Xnnnnn.dta
    - 国保分 Z2Xnnnnn.dta
    - 後期分 Z3Xnnnnn.dta
    - ※それぞれ別のファイルで作成されていることを想定しています
3. 本ツールの実行ファイルも同じフォルダに格納する（support_tool.exe）
4. support_tool.exe をダブルクリックし実行
5. コンソール画面に処理内容等が表示される
6. 「results」フォルダ内に確認用データが出力される
7. 送信前に確認用データで内容をチェックする


- オリジナルデータは何も変更しない
- 本ツールは何度でも実行可能
- 確認用CSVは文字コードUTF-8 / 確認用TSVは文字コードUTF-16(Excel用)

## 制限事項

- 利用システムによって、適切に文字コードが設定されていない可能性があるため、JIS(iso2022_jp)として扱えない文字はリプレイスしています
- [インターネットを通じ取得できる仕様書(前半部分)](https://www.mhlw.go.jp/bunya/shakaihosho/iryouseido01/pdf/05-1e-01.pdf)・[仕様書(後半部分)](https://www.mhlw.go.jp/bunya/shakaihosho/iryouseido01/pdf/05-1e-02.pdf)の情報がどうも古いようで特別徴収義務者コードは名称変換していません

## 確認用データの説明

| レコード区分 | 市町村コード | 特別徴収義務者コード | 各種区分 | 通知内容コード | 作成年月日 | 氏名漢字 | 生年月日 | 各種年月日 | 金額１ | 金額２ | 金額３ |
|-----|----|----|----|----|----|----|----|----|----|----|----|
|データレコードを表す '2'|送信元市町村コード|特別徴収義務者を表すコード|通知の事由を表す|通知の内容を表す(各種区分との組合せ)|データの作成処理日|団体内で名寄せした氏名漢字(空白の場合は宛名上に存在しない)|生年月日|依頼通知の発生日|端数額調整後の支払回数割保険料(税)|定額の支払回数割保険料(税)|特別徴収対象年金の年金額|
