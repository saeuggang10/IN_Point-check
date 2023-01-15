# Degree
-------------------------------
### 설명
```
* 사각형(bbox>points)이 아니거나, 약속된 것과 다른 형식으로 좌표가 입력되어있는 데이터를 제거
* 많이 기울어진 데이터 제거
* 화질이 안 좋은 데이터 제거
```

-------------------------------
-------------------------------

### package
```
import math
import pandas as pd
import os
import json
import glob
from csv import DictWriter
import numpy as np
```

### def
```
삼각함수로 기울기를 구하기 위해 각 변의 길이를 구하는 함수
```

### input
```
dir_path = '주소를 입력해주세요'
```

### code
1. jpg_size
    * 저화질의 사진을 제거하기 위한 기능
    * 오름차순 정렬

2. nomal_data
    * 약속된 포맷과 다른 방식의 좌표값을 찾아내는 기능
    * 사각형 모양이 아닌 것 제거
    
3. seta_data
    * 사각형의 기울기를 구하는 기능
    
4. rank
    * 정상여부판단>기울기>화질 순으로 정렬해 순위가 높을수록 noisy data

-------------------------------
-------------------------------

# Plot
-------------------------------
### 설명
```
degree가 잘 작동되었는지 확인하기위해 시각화
```
-------------------------------
-------------------------------

### package
```
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from shapely.geometry.polygon import LinearRing, Polygon
```

### code
1. annotations
    * 약속된 포맷으로 들어갔는지 확인하기 위해 순서대로 좌표이름을 붙임

2. axhline / axvline
    * 기울어진 정도를 인지하기 편하도록 수직, 수평선을 그림

-------------------------------
-------------------------------

#### 첨부파일
1. AngleCheck.zip
    * 코드 테스팅을 위한 파일
    
#### 주의사항
* plot의 shapely패키지가 잘 실행되지 않을 수 있음으로 cmd에서 개별적인 설치가 필요함