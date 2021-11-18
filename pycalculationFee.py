from typing import Mapping


def calculationfee(list):
    '''计算阶梯电费
    输入：[月份，电度数]
    '''
    month=list[0]
    summaryBox=float(list[1])
    if int(month) in (1,2,3,4,11,12):
        if summaryBox<=201:
            print("冬季第一档：剩余",201-summaryBox)
            sum=summaryBox*0.5886
        elif 201<summaryBox<=401:
            print("冬季第二档：剩余",401-summaryBox)
            sum=201*0.5886+(summaryBox-201)*0.6388
        elif summaryBox>401:
            print("冬季第三档")
            sum=201*0.5886+((401-201)*0.6388)+((summaryBox-401)*0.8888)
    elif int(month) in (5,6,7,8,9,10):
        if summaryBox<=261:
            print("夏季第一档")
            sum=summaryBox*0.5886
        elif 261<summaryBox<=601:
            print("夏季第二档")
            sum=261*0.5886+(summaryBox-261)*0.6388
        elif summaryBox>601:
            print("夏季第三档")
            sum=261*0.5886+(601-261)*0.6388+(summaryBox-601)*0.8888
    else:
        print("没数据")
        sum=0
    return sum


if __name__ == '__main__':
    print(calculationfee([11,112])) 
    #test