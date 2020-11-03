# standardmotion
基于行为识别的人体运动姿态校准系统

#### 本地搭建

1. `git clone`到本地文件夹

2. `cd`到当前目录

3. 安装相关依赖

   ```
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
   ```

4. `fbs run`测试环境

5. `fbs freeze`生成exe文件

6. 将release版本的`openpose`复制到生成的`./target/standardmotion`文件夹下

7. 搭建完成