# Generated by Django 2.2.4 on 2019-10-16 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0010_remove_review_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmproduct',
            name='product_category',
            field=models.CharField(choices=[('杏', '杏'), ('いちご', 'いちご'), ('いちじく', 'いちじく'), ('梅', '梅'), ('柿', '柿'), ('オレンジ', 'オレンジ'), ('グレープフルーツ', 'グレープフルーツ'), ('ゆず', 'ゆず'), ('みかん', 'みかん'), ('レモン', 'レモン'), ('その他柑橘類', 'その他柑橘類'), ('キウイフルーツ', 'キウイフルーツ'), ('さくらんぼ', 'さくらんぼ'), ('スイカ', 'スイカ'), ('プラム', 'プラム'), ('洋梨', '洋梨'), ('梨', '梨'), ('パイナップル', 'パイナップル'), ('バナナ', 'バナナ'), ('パパイア', 'パパイア'), ('ビワ', 'ビワ'), ('ぶどう', 'ぶどう'), ('ブルーベリー', 'ブルーベリー'), ('クランベリー', 'クランベリー'), ('ラズベリー', 'ラズベリー'), ('マスカット', 'マスカット'), ('マンゴー', 'マンゴー'), ('メロン', 'メロン'), ('桃', '桃'), ('りんご', 'りんご'), ('プルーン', 'プルーン'), ('ネクタリン', 'ネクタリン'), ('その他', 'その他')], max_length=10, verbose_name='カテゴリー名'),
        ),
        migrations.AlterField(
            model_name='farmproduct',
            name='product_origin',
            field=models.CharField(choices=[('北海道産', '北海道'), ('青森県産', '青森県'), ('岩手県産', '岩手県'), ('宮城県産', '宮城県'), ('秋田県産', '秋田県'), ('山形県産', '山形県'), ('福島県産', '福島県'), ('茨城県産', '茨城県'), ('栃木県産', '栃木県'), ('群馬県産', '群馬県'), ('埼玉県産', '埼玉県'), ('千葉県産', '千葉県'), ('東京都産', '東京都'), ('神奈川県産', '神奈川県'), ('新潟県産', '新潟県'), ('富山県産', '富山県'), ('石川県産', '石川県'), ('福井県産', '福井県'), ('山梨県産', '山梨県'), ('長野県産', '長野県'), ('岐阜県産', '岐阜県'), ('静岡県産', '静岡県'), ('愛知県産', '愛知県'), ('三重県産', '三重県'), ('滋賀県産', '滋賀県'), ('京都府産', '京都府'), ('大阪府産', '大阪府'), ('兵庫県産', '兵庫県'), ('奈良県産', '奈良県'), ('和歌山県産', '和歌山県'), ('鳥取県産', '鳥取県'), ('島根県産', '島根県'), ('岡山県産', '岡山県'), ('広島県産', '広島県'), ('山口県産', '山口県'), ('徳島県産', '徳島県'), ('香川県産', '香川県'), ('愛媛県産', '愛媛県'), ('高知県産', '高知県'), ('福岡県産', '福岡県'), ('佐賀県産', '佐賀県'), ('長崎県産', '長崎県'), ('熊本県産', '熊本県'), ('大分県産', '大分県'), ('宮崎県産', '宮崎県'), ('鹿児島県産', '鹿児島県'), ('沖縄県産', '沖縄県')], max_length=5, verbose_name='産地名'),
        ),
    ]
