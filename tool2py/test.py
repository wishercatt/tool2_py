def read_file(path):
    try:
        f = open(path, 'r', encoding='utf-8')
        list = []
        for line in f.readlines():
            list.append(line.strip())
    finally:
        if f:
            f.close()
    return list


def get_pi_from_str(string):
    result = []
    for i in range(0, len(string)):
        if string[i] == "<":
            for j in range(i + 1, len(string)):
                if string[j] == ">":
                    tmp = string[i + 1:j]
                    result.append(tmp)
                    break
                else:
                    continue
            i = j + 1;
        else:
            continue
    return result


def get_pi_from_list(file):
    result = []
    for string in file:
        pi_list = get_pi_from_str(string)
        result.extend(pi_list)
    return result


def verify(list1, list2, compliance, uncompliance):
    for string in list2:
        if string[0:2] == "您的":
            if string[2:len(string)] in list1:
                compliance.append(string)
            else:
                uncompliance.append(string)
        else:
            if string in list1:
                compliance.append(string)
            else:
                uncompliance.append(string)


def pretty_print(list_string):
    result = ""
    i = 0
    while i < len(list_string):
        string = list_string[i]
        length = len(string)
        j = i + 1
        while j < len(list_string):
            if length + len(list_string[j]) < 45:
                string = string + "、" + list_string[j]
                length = len(string)
            else:
                string = string + "、"
                break
            j = j + 1
        i = j
        string = string + "\n"
        result = result + string
    return result


def main():
    app = "淘宝"
    business = "网上购物"

    result = read_file("./resource/淘宝result.txt")
    answer = read_file("./resource/淘宝answer.txt")

    rule_pi = read_file("./rule/business/网上购物/pi.txt")
    answer_pi = get_pi_from_list(answer)
    result_pi = get_pi_from_list(result)

    answer_compliance = []
    answer_uncompliance = []
    verify(rule_pi, result_pi, answer_compliance, answer_uncompliance)

    true_pi = []
    for string in result_pi:
        if string in answer_pi:
            true_pi.append(string)
        else:
            continue

    result_compliance = []
    result_uncompliance = []
    verify(rule_pi, result_pi, result_compliance, result_uncompliance)

    output = open("./output/淘宝output.txt", 'w', encoding='gbk')

    if len(result_uncompliance) > 0:
        print(app + "隐私政策在" + business + "业务功能方面收集的个人信息违背了最少信息原则", file=output)
    else:
        print(app + "隐私政策在" + business + "业务功能方面收集的个人信息满足最少信息原则", file=output)
    print("\n<---------------------------------------------------------------------------------->\n", file=output)

    print("tool1标注结果分析：", file=output)
    num = str(len(true_pi))
    print("tool1正确提取的个人信息共" + num + "条，正确提取比例为" +
          str('{:.2%}'.format(len(true_pi) / len(answer_pi))), file=output)
    print("", file=output)

    print("tool1正确提取的个人信息中，满足最少信息原则的共" + str(len(result_compliance)) + "条\n如下所示：", file=output)
    print(pretty_print(result_compliance), file=output)
    print("", file=output)

    print("tool1正确提取的个人信息中，不满足最少信息原则的共" + str(len(result_uncompliance)) + "条\n如下所示：", file=output)
    print(pretty_print(result_uncompliance), file=output)
    print("", file=output)

    miss_list = [string for string in answer_pi if string not in true_pi]
    print("tool1产生的漏报共" + str(len(miss_list)) + "条\n如下所示：", file=output)
    print(pretty_print(miss_list), file=output)
    print("", file=output)

    extra_list = [string for string in result_pi if string not in answer_pi]
    print("tool1产生的误报共" + str(len(extra_list)) + "条\n如下所示：", file=output)
    print(pretty_print(extra_list), file=output)

    print("\n<---------------------------------------------------------------------------------->\n", file=output)

    print("手工标注结果分析：", file=output)
    print("隐私政策声明中，满足最少信息原则的信息收集共" + str(len(answer_compliance)) + "条\n如下所示:", file=output)
    print(pretty_print(answer_compliance), file=output)
    print("", file=output)

    print("隐私政策声明中，不满足最少信息原则的信息收集共" + str(len(answer_uncompliance)) + "条\n如下所示:", file=output)
    print(pretty_print(answer_uncompliance), file=output)
    print("", file=output)

    output.flush()
    output.close()


if __name__ == "__main__":
    print("main")
    main()
