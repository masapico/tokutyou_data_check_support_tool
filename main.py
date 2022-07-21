# coding: utf-8

import os
import glob
import csv

APPNAME = '年金特徴送信データ確認支援ツール'
VERSION = '0.1'
DESCRIPTION = '国保連合会に送信するデータの確認支援ツール'
HOWTO = """
利用方法：
    1. パソコンでフォルダを作成します（サーバではなく、パソコン上に作成）
    2. 送信しようとするデータを作成したフォルダに格納する（拡張子がdta）
       介護分 Z1Xnnnnn.dta
       国保分 Z2Xnnnnn.dta
       後期分 Z3Xnnnnn.dta
       ※それぞれ別のファイルである前提
    3. 本ツールの実行ファイルも同じフォルダに格納する（support_tool.exe）
    4. suport_tool.exe をダブルクリックし実行
    5. 「results」フォルダ内に確認用データが出力される
    6. 送信前に確認用データで内容をチェックする
    ※オリジナルデータは何も変更しない
    ※本ツールは何度でも実行可能
    ※確認用CSVは文字コードUTF-8 / 確認用TSVは文字コードUTF-16(Excel用)
"""

OUTPUTDIR = 'results'

FILEDICT = {
    'Z11': '介護特別徴収対象者情報',
    'Z12': '介護特別徴収依頼情報',
    # 'Z13': '介護特別徴収依頼処理結果情報',
    'Z14': '介護特別徴収結果情報',
    'Z1A': '介護特別徴収各種異動情報',
    'Z21': '国保特別徴収対象者情報',
    'Z22': '国保特別徴収依頼情報',
    # 'Z23': '国保特別徴収依頼処理結果情報',
    'Z24': '国保特別徴収結果情報',
    'Z2A': '国保特別徴収各種異動情報',
    'Z31': '後期特別徴収対象者情報',
    'Z32': '後期特別徴収依頼情報',
    # 'Z33': '後期特別徴収依頼処理結果情報',
    'Z34': '後期特別徴収結果情報',
    'Z3A': '後期特別徴収各種異動情報',
}

TUTINAIYOU_CODE = {
    '00': '00_特別徴収対象者情報',
    '01': '01_特別徴収依頼通知',
    '02': '02_特別徴収依頼処理結果通知',
    '22': '22_特別徴収結果通知',
    '30': '30_特別徴収追加候補者情報',
    '31': '31_特別徴収追加依頼通知',
    '32': '32_特別徴収追加依頼処理結果通知',
    '41': '41_資格喪失等の通知',
    '42': '42_資格喪失等処理結果通知',
    '61': '61_仮徴収額変更通知',
    '62': '62_仮徴収額変更処理結果通知',
    '81': '81_住所地特例該当者通知',
    '82': '82_住所地特例該当者処理結果通知',
}

KUBUN_CODE_DETAIL ={
    '00-01': '01_新規者',
    '00-02': '02_前年度継続者',
    '00-70': '70_ダミーレコード',
    '01-01': '01_特別徴収対象者',
    '01-02': '02_特別徴収対象者（住所地特例該当）',
    '01-03': '03_特別徴収非対象者',
    '22-00': '00_正常',
    '22-01': '01_失権',
    '22-02': '02_差止',
    '22-03': '03_支払年金額不足',
    '22-05': '05_特別徴収該当（他制度による中止）',
    '22-10': '10_正常（75歳以上で国保特別徴収中）',
    '30-01': '01_新規者',
    '30-02': '02_住所変更者',
    '31-01': '01_特別徴収対象者',
    '31-02': '02_特別徴収対象者（住所地特例該当）',
    '31-03': '03_特別徴収非対象者',
    '41-01': '01_死亡',
    '41-02': '02_転出',
    '41-03': '03_特別事情',
    '41-04': '04_適用除外',
    '61-00': '00_初期値',
    '81-01': '01_住所地特例該当',
    '81-02': '02_住所地特例該当解除',
}

GENDER_CODE = {
    '1': '男',
    '2': '女',
}

# 入手できる仕様書に記述のないコード値が存在
# 名称変換は実装しない
#
# TOKUTYOU_GIMUSYA_CODE = {
#     '501': '501_国家公務員共済組合連合会',
#     '594': '594_地方職員共済組合',
#     '595': '595_地方職員共済組合団体共済部',
#     '596': '596_東京都職員共済組合',
#     '597': '597_札幌市職員共済組合',
#     '598': '598_川崎市職員共済組合',
#     '599': '599_横浜市職員共済組合',
#     '600': '600_名古屋市職員共済組合',
#     '601': '601_京都市職員共済組合',
#     '602': '602_大阪市職員共済組合',
#     '603': '603_神戸市職員共済組合',
#     '604': '604_広島市職員共済組合',
#     '605': '605_北九州市職員共済組合',
#     '606': '606_福岡市職員共済組合',
#     '700': '700_全国市町村共済組合連合会',
#     '686': '686_日本私立学校振興・共済事業団',
#     '687': '687_農林漁業団体職員共済組合',
#     '999': '999_社会保険庁',
# }

def identify_files(files: list) -> dict:
    """
    どのファイルが格納されているかを示す
    """
    identified_dict = dict()
    for fl in files:
        basename = os.path.basename(fl)
        file_id = basename[0:3]
        if file_id in FILEDICT.keys():
            identified_dict[file_id] = '{0} : {1}'.format(FILEDICT[file_id], basename)
    return identified_dict


def data_record_extract(fpath: str) -> list:
    """
    データレコードを抽出

    fpath: インプットデータパス
    """
    meta_info = dict()
    data_records = []
    other_records = []
    with open(fpath, mode='r', encoding='iso2022_jp', errors='replace') as f:
        meta_info['市町村コード'] = f.read(5)
        dummy = f.read(1)
        meta_info['媒体連番'] = f.read(3)
        meta_info['作成年月日'] = f.read(8)
        dummy = f.read(31)
        meta_info['ファイル格納件数'] = int(f.read(6))
        dummy = f.read(42)
        current_offset = f.tell() # 管理レコード読み終わり時ファイル位置
        while True:
            record_top = f.read(6) # (1|2|3)NNNNN レコード区分&市町村コードで判定
            if record_top == '2{}'.format(meta_info['市町村コード']): # データレコード
                f.seek(current_offset)
                data_record = f.read(383)
                data_records.append(data_record)
                current_offset = f.tell()
            else: # ヘッダレコード、トレイラレコード
                f.seek(current_offset)
                dummy = f.read(500)
                current_offset = f.tell()
                if not dummy: # EOF
                    break
                else:
                    other_records.append(record_top)
    meta_info['データレコード件数'] = len(data_records)
    meta_info['その他レコード件数'] = len(other_records)
    print(os.path.basename(fpath))
    print(meta_info)
    return data_records


def data2file(fpath:str, data_records: list) -> None:
    """
    データレコードをCSVファイルに出力

    fpath: 出力ファイルパス
    data_records: 出力元となる固定長データのリスト
    """
    details = []
    details.append(['レコード区分','市町村コード','特別徴収義務者コード','各種区分','通知内容コード',
                    '作成年月日','氏名漢字', '生年月日', '性別', '各種年月日', '金額１', '金額２', '金額３'])
    for record in data_records:
        tmp = []
        tmp.append(record[0:1]) # レコード区分
        tmp.append(record[1:6]) # 市町村コード
        tmp.append(record[6:9]) # 特別徴収義務者コード
        tmp.append(TUTINAIYOU_CODE[record[9:11]]) # 通知内容コード
        code_detail = '{0}-{1}'.format(record[9:11], record[264:266])
        tmp.append(KUBUN_CODE_DETAIL[code_detail]) # コード詳細
        tmp.append('{0}/{1}/{2}'.format(record[13:17], record[17:19], record[19:21])) # 作成年月日
        tmp.append(record[72:97].strip()) # 氏名漢字
        tmp.append('{0}/{1}/{2}'.format(record[38:42], record[42:44], record[44:46])) # 生年月日
        tmp.append(GENDER_CODE[record[46:47]]) # 性別
        tmp.append('{0}/{1}/{2}'.format(record[269:273], record[273:275], record[275:277])) # 各種年月日
        tmp.append(str(int(record[278:288]))) # 金額１
        tmp.append(str(int(record[289:299]))) # 金額２
        tmp.append(str(int(record[300:310]))) # 金額３
        details.append(tmp)
    # utf-8のcsvデータ出力
    with open(fpath, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if len(details) > 1:
            writer.writerows(details)
            print('確認用CSVデータ: {}'.format(fpath))
    # utf-16のタブ区切りデータ出力（Excel向き）
    with open('{}.tsv'.format(fpath), mode='w', encoding='utf-16', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        if len(details) > 1:
            writer.writerows(details)
            print('確認用TSVデータ: {}.tsv'.format(fpath), '\n')
    return None


if __name__ == "__main__":
    print(APPNAME)
    print('--------------------------------------------------')
    print('バージョン情報: {}'.format(VERSION))
    print(DESCRIPTION)
    print('--------------------------------------------------')
    print(HOWTO)
    print('--------------------------------------------------')

    # 対象データの取得 ※datは大文字・小文字関係なし
    files = glob.glob('*.dta')

    # データが存在しない場合は終わる
    if len(files) == 0:
        print('年金特徴データが見つかりません')
        print('Enterキーを押すと終了します:')
        dummy = input()
        exit()
    
    # データが存在する場合は続く
    print('以下のファイルについて処理を行います:')
    for k, v in identify_files(files).items():
        print(k, v)
    print('--------------------------------------------------')

    # 出力フォルダの作成
    if not os.path.exists(OUTPUTDIR):
        os.mkdir(OUTPUTDIR)

    for f in files:
        data2file('{0}/{1}.csv'.format(OUTPUTDIR, os.path.basename(f)), data_record_extract(f))
    print('--------------------------------------------------')

    print('Enterを押すと、ツールを終了します:')
    dummy = input()
