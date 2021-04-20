# Introducing

复现LDoS攻击
原始论文《[Low-rate TCP-targeted denial of service attacks: the shrew vs. the mice and elephants](https://github.com/ByeRose/reproducing_LDoS/blob/main/Low-rate%20TCP-targeted%20denial%20of%20service%20attacks%EF%BC%9Athe%20shrew%20vs.%20the%20mice%20and%20elephants..pdf)》

# Installation

    环境：ubuntu 16.04/18.04，python 2.7

## step 1 更新系统软件

    sudo apt update

## step 2 安装git

    sudo apt install git

## step 3 克隆repo到本地

    sudo git clone https://gitee.com/csodajet/reproducing-shrew-attack

## step 4 进入到repo路径

    sudo cd reproducing-shrew-attack

## step 5 授予脚本权限

    sudo chmod 777 installDependencies.sh

## step 6 安装mininet及其依赖

    sudo ./installDependencies.sh

## step 7 运行测试

    //sudo ./run.sh [tcp] [period]
    
    //tcp参数可选vegas,westwood,reno,bic,cubic,bbr
    
    //period参数可选0.5~2之间的数值
    
    //样例
      
    sudo ./run.sh vegas 1.0
    
    //结果

![输入图片说明](https://images.gitee.com/uploads/images/2020/1123/002007_51c651bf_5721796.png "屏幕截图.png")

![输入图片说明](https://images.gitee.com/uploads/images/2020/1123/002115_e1c2c01e_5721796.png "屏幕截图.png")