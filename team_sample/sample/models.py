from django.db import models

class Shouhin(models.Model):
    hontai_num=models.AutoField("本体No",primary_key=True)
    team=models.CharField("店舗",max_length=255,blank=True,null=True)
    shouhin_num=models.CharField("商品番号",max_length=255,blank=True,null=True)
    shouhin_name=models.CharField("商品名",max_length=255,blank=True,null=True)
    color=models.CharField("カラー",max_length=255,blank=True,null=True)
    size=models.CharField("サイズ",max_length=255,blank=True,null=True)
    size_num=models.IntegerField("サイズ値",default=0)
    tana=models.CharField("棚番号",max_length=255,blank=True,null=True)
    bikou=models.CharField("備考",max_length=255,blank=True,null=True)
    joutai=models.IntegerField("状態",default=0)
    rental_day=models.CharField("貸出日",max_length=255,blank=True,null=True)
    rental_tantou=models.CharField("担当",max_length=255,blank=True,null=True)
    rental_cus=models.CharField("顧客",max_length=255,blank=True,null=True)

    def __str__(self):
        return self.shouhin_name
    
    # joutai（状態）　0:在庫有り　1:貸出中


class Size(models.Model):
    size_num=models.IntegerField("順番",null=False)
    size=models.CharField("サイズ",max_length=255,blank=True)

    def __str__(self):
        return self.size