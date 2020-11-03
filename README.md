# standardmotion
基于行为识别的人体运动姿态校准系统

#### 本地搭建

1. `git clone`到本地文件夹

2. `cd`到文件所在目录

3. 安装相关依赖

   ```
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
   ```

4. 更改路径 将`./src/main/python/main.py`中第26行与29中的路径替换为本地start.exe与json文件夹的路径。

5. `fbs run`测试环境

6. `fbs freeze`生成exe文件

7. 将release版本的`openpose`复制到生成的`./target/standardmotion`文件夹下

8. 运行exe文件