from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Shouhin,Size
import datetime
from django.http import JsonResponse
import io
import csv
import json



@login_required
def index(request):
    if "team" not in request.session:
        request.session["team"]="全店舗"
    if "hinban_enter" not in request.session:
        request.session["hinban_enter"]=""
    if "hinban" not in request.session:
        request.session["hinban"]=""
    if "color" not in request.session:
        request.session["color"]=[]
    if "size" not in request.session:
        request.session["size"]=[]
    if "rental_now" not in request.session:
        request.session["rental_now"]="false"
    if "sample" not in request.session:
        request.session["sample"]=[]

    team=request.session["team"]
    hinban_enter=request.session["hinban_enter"]
    hinban=request.session["hinban"]
    color=request.session["color"]
    size=request.session["size"]
    rental_now=request.session["rental_now"]
    rental_count=len(list(request.session["sample"]))

    # フィルター
    fil={}
    if team != "全店舗":
        fil["team"]=team
    if hinban_enter != "":
        fil["shouhin_num__icontains"]=hinban_enter

    items=Shouhin.objects.filter(**fil)
    hinban_list=list(items.values_list("shouhin_num",flat=True).order_by("shouhin_num").distinct())
    if hinban_enter=="":
        hinban_list=[]

    shouhin_name=""
    color_list=[]
    size_list=[]
    color_dic={}
    size_dic={}
    
    if rental_now == "false":
        item_list=[]
        if hinban != "":
            fil["shouhin_num"]=hinban
            items=Shouhin.objects.filter(**fil)

            if len(items)>0:
                shouhin_name=items[0].shouhin_num + "　" + items[0].shouhin_name

                color_list=list(items.values_list("color",flat=True).order_by("color").distinct())
                for i in color_list:
                    if i in color:
                        color_dic[i]=1
                    else:
                        color_dic[i]=0

                size_list=list(items.values_list("size",flat=True).order_by("size_num").distinct())    
                for i in size_list:
                    if i in size:
                        size_dic[i]=1
                    else:
                        size_dic[i]=0

                if len(color) != 0:
                    fil["color__in"]=color
                if len(size) != 0:
                    fil["size__in"]=size

            item_list=Shouhin.objects.filter(**fil).order_by("color","size_num")

    else:
        if team == "全店舗":
            item_list=Shouhin.objects.filter(joutai=1).order_by("rental_day")
        else:
            item_list=Shouhin.objects.filter(team=team,joutai=1).order_by("rental_day")
  


    team_list=["全店舗","東京","大阪","高松","福岡"]
    params={
        "team":team,
        "team_list":team_list,
        "hinban_enter":hinban_enter or "",
        "hinban":hinban,
        "hinban_list":hinban_list,
        "shouhin_name":shouhin_name,
        "color":color,
        "color_dic":color_dic,
        "size":size,
        "size_dic":size_dic,
        "item_list":item_list,
        "rental_now":rental_now,
        "rental_count":rental_count,
    }
    return render(request,"sample/index.html",params)


# 品番検索に入力
def hinban_enter(request):
    team=request.POST.get("team")
    hinban_enter=request.POST.get("hinban_enter")
    if team=="全店舗":
        hinban_list=list(Shouhin.objects.filter(shouhin_num__icontains=hinban_enter).values_list("shouhin_num",flat=True).order_by("shouhin_num").distinct())
    else:
        hinban_list=list(Shouhin.objects.filter(team=team,shouhin_num__icontains=hinban_enter).values_list("shouhin_num",flat=True).order_by("shouhin_num").distinct())
    d={"hinban_list":hinban_list}
    return JsonResponse(d)


#品番リストをクリック
def hinban_click(request):
    request.session["team"]=request.POST.get("team")
    request.session["hinban_enter"]=request.POST.get("hinban_enter")
    request.session["hinban"]=request.POST.get("hinban")
    request.session["color"]=[]
    request.session["size"]=[]
    d={}
    return JsonResponse(d)


#店舗、カラー、サイズをクリック
def team_color_size_click(request):
    request.session["team"]=request.POST.get("team")
    request.session["hinban_enter"]=request.POST.get("hinban_enter")
    request.session["hinban"]=request.POST.get("hinban")
    color=request.POST.get("color")
    color=json.loads(color)
    size=request.POST.get("size")
    size=json.loads(size)
    request.session["color"]=color
    request.session["size"]=size
    d={}
    return JsonResponse(d)


# 貸出中のみ表示
def rental_now(request):
    request.session["hinban_enter"]=""
    request.session["hinban"]=""
    request.session["color"]=[]
    request.session["size"]=[]
    request.session["rental_now"]=request.POST.get("rental")
    d={}
    return JsonResponse(d)


# 貸出モーダル（貸出ボタン）
def rental_modal(request):
    hontai_num=request.POST.get("hontai_num")
    kubun=request.POST.get("kubun")
    ses=list(request.session["sample"])
    if kubun=="add":
        if hontai_num not in ses:
            ses.append(hontai_num)
    else:
        ses.remove(hontai_num)
    request.session["sample"]=ses
    ins=Shouhin.objects.filter(hontai_num__in=ses)
    rental_list=[]
    for i in ins:
        rental_list.append([i.hontai_num,i.team,i.shouhin_num,i.shouhin_name,i.color,i.size])

    d={"rental_list":rental_list}
    return JsonResponse(d)


# 貸出モーダル（買い物かご）
def rental_basket(request):
    ses=list(request.session["sample"])
    ins=Shouhin.objects.filter(hontai_num__in=ses)
    rental_list=[]
    for i in ins:
        rental_list.append([i.hontai_num,i.team,i.shouhin_num,i.shouhin_name,i.color,i.size])

    d={"rental_list":rental_list}
    return JsonResponse(d)


# 貸出処理
def rental_ok(request):
    tantou=request.POST.get("tantou")
    cus=request.POST.get("cus")
    today=datetime.date.today().strftime("%Y-%m-%d")
    ses=list(request.session["sample"])
    for i in ses:
        ins=Shouhin.objects.get(hontai_num=i)
        ins.joutai=1
        ins.rental_day=today
        ins.rental_tantou=tantou
        ins.rental_cus=cus
        ins.save()
    request.session["sample"]=[]
    d={}
    return JsonResponse(d)


# 返却モーダル
def return_modal(request):
    hontai_num=request.POST.get("hontai_num")
    ins=Shouhin.objects.get(hontai_num=hontai_num)
    shouhin=ins.shouhin_num + "　" + ins.shouhin_name + "　" + ins.color + "　" + ins.size
    d={"sample":[ins.team,shouhin]}
    return JsonResponse(d)


# 返却処理
def return_ok(request):
    hontai_num=request.POST.get("hontai_num")
    ins=Shouhin.objects.get(hontai_num=hontai_num)
    ins.joutai=0
    ins.rental_day=""
    ins.rental_tantou=""
    ins.rental_cus=""
    ins.save()
    d={}
    return JsonResponse(d)


@login_required
# 編集画面
def henshu_index(request):
    team=request.session["team"]
    team_list=["","東京","大阪","高松","福岡"]
    size_list=Size.objects.all()
    params={
        "team":team,
        "team_list":team_list,
        "size_list":size_list,
    }
    return render(request,"sample/henshu.html",params)


# 編集_品番クリック
def henshu_hinban_click(request):
    team=request.POST.get("team")
    hinban=request.POST.get("hinban")
    item_list=list(Shouhin.objects.filter(team=team,shouhin_num=hinban).order_by("color","size_num").values())
    d={"item_list":item_list}
    return JsonResponse(d)


# 編集_リストクリック
def henshu_list_click(request):
    hontai_num=request.POST.get("hontai_num")
    item=list(Shouhin.objects.filter(hontai_num=hontai_num).values())[0]
    d={"item":item}
    return JsonResponse(d)


# 編集_登録/更新
def henshu_up(request):
    hontai_num=request.POST.get("hontai_num")
    team=request.POST.get("team")
    shouhin_num=request.POST.get("shouhin_num")
    shouhin_name=request.POST.get("shouhin_name")
    color=request.POST.get("color")
    size=request.POST.get("size")
    size_num=Size.objects.get(size=size).size_num
    tana=request.POST.get("tana")
    joutai=request.POST.get("joutai")
    rental_day=request.POST.get("rental_day")
    rental_tantou=request.POST.get("rental_tantou")
    rental_cus=request.POST.get("rental_cus")
    bikou=request.POST.get("bikou")

    # 新規登録
    if hontai_num=="":
        Shouhin.objects.create(
            team=team,shouhin_num=shouhin_num,shouhin_name=shouhin_name,color=color,size=size,size_num=size_num,
            tana=tana,joutai=joutai,rental_day=rental_day,rental_tantou=rental_tantou,rental_cus=rental_cus,bikou=bikou,
        )
    # 内容更新
    else:
        ins=Shouhin.objects.get(hontai_num=hontai_num)
        ins.team=team
        ins.shouhin_num=shouhin_num
        ins.shouhin_name=shouhin_name
        ins.color=color
        ins.size=size
        ins.size_num=size_num
        ins.tana=tana
        ins.joutai=joutai
        ins.rental_day=rental_day
        ins.rental_tantou=rental_tantou
        ins.rental_cus=rental_cus
        ins.bikou=bikou
        ins.save()

    d={}
    return JsonResponse(d)


# 編集_削除
def henshu_del(request):
    hontai_num=request.POST.get("hontai_num")
    Shouhin.objects.get(hontai_num=hontai_num).delete()
    d={}
    return JsonResponse(d)


@login_required
# サイズ画面
def size_index(request):
    sizes=Size.objects.all().order_by("size_num")
    return render(request,"sample/size.html",{"sizes":sizes})


# サイズ番号（順番）
def size_num(request):
    size_list=request.POST.get("size_list")
    size_list=json.loads(size_list)
    li=[]
    for key,value in size_list.items():
        li.append(value)
    # サイズ一覧
    for size in li:
        ins=Size.objects.get(size=size)
        if ins.size_num != li.index(size)+1:
            ins.size_num=li.index(size)+1
            ins.save()
    #商品一覧
    for size in li:
        ins=Shouhin.objects.filter(size=size)
        if ins.count() != 0:
            ins2=ins[0]
            if ins2.size_num != li.index(size)+1:
                for ins2 in ins:
                    ins2.size_num=li.index(size)+1
                    ins2.save()
    d={"":""}
    return JsonResponse(d)


# 新規サイズ追加
def size_new(request):
    size_new=request.POST.get("size_new")
    Size.objects.create(size_num=0, size=size_new)
    d={"":""}
    return JsonResponse(d)


# サイズ名称
def size_name(request):
    old_n=request.POST.get("size_name1")
    new_n=request.POST.get("size_name2")
    # サイズ一覧
    ins=Size.objects.get(size=old_n)
    ins.size=new_n
    ins.save()
    #商品一覧
    ins=Shouhin.objects.filter(size=old_n)
    if ins.count() != 0:
        for ins2 in ins:
            ins2.size=new_n
            ins2.save()
    d={"":""}
    return JsonResponse(d)


# サイズ削除
def size_del(request):
    size_name=request.POST.get("size_name")
    Size.objects.get(size=size_name).delete()
    # サイズ一覧
    ins=Size.objects.all()
    for i,h in enumerate(ins):
        h.size_num=i+1
        h.save()
    #商品一覧
    ins=Shouhin.objects.all()
    for i in ins:
        i.size_num=Size.objects.get(size=i.size).size_num
        i.save()
    d={"":""}
    return JsonResponse(d)


# 同サイズ使用サンプル
def size_sample(request):
    size_name=request.POST.get("size_name")
    size_sample=list(Shouhin.objects.filter(size=size_name).values())
    d={"size_sample":size_sample}
    return JsonResponse(d)


# CSVページ
def csv_index(request):
    return render(request,"sample/csv_imp.html")


# 初回CSVデータ取込
def csv_imp(request):

    # # サイズデータ
    # data = io.TextIOWrapper(request.FILES['csv1'].file, encoding="cp932")
    # csv_content = csv.reader(data)
    # csv_list=list(csv_content)
    # for i in csv_list:
    #     Size.objects.create(
    #         size_num=i[0],
    #         size=i[1],
    #     )

    # 商品データ
    data = io.TextIOWrapper(request.FILES['csv1'].file, encoding="cp932")
    csv_content = csv.reader(data)
    csv_list=list(csv_content)
    h=0
    for i in csv_list:
        if h!=0:
            Shouhin.objects.create(
                team=i[0],
                shouhin_num=i[1],
                shouhin_name=i[2],
                color=i[3],
                size=i[4],
                size_num=i[5],
                tana=i[6],
                bikou=i[7],
                joutai=i[8],
                rental_day=i[9],
                rental_tantou=i[10],
                rental_cus=i[11],
            )
        h+=1

    return render(request,"sample/csv_imp.html",{"ans":"yes"})



def free(request):
    #サンプルリスト初回取込
    data = io.TextIOWrapper(request.FILES['csv1'].file, encoding="cp932")
    csv_content = csv.reader(data)
    csv_list=list(csv_content)
    h=0
    for i in csv_list:
        if h!=0:
            Shouhin.objects.create(
                team=i[0],
                shouhin_num=i[1],
                shouhin_name=i[2],
                color=i[3],
                size=i[4],
                size_num=i[5],
                tana=i[6],
                bikou=i[7],
                joutai=i[8],
                rental_day=i[9],
                rental_tantou=i[10],
                rental_cus=i[11],
            )
        h+=1
    return redirect("sample:index")