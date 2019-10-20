import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import numpy as np
    
%matplotlib inline
%config InlineBackend.figure_format = 'retina‘

mpl.rcParams['axes.unicode_minus'] = False    # 하이픈(-) 폰트 깨질 경우 대비
    
path = '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf'
font_name = fm.FontProperties(fname=path, size=18).get_name()
plt.rc('font', family=font_name)
fm._rebuild()    # 이걸 해줘야 plt.rc가 작동

plt.plot(np.random.randn(4, 8), np.random.randn(4,8), 'bo--')
plt.title('타이틀')
plt.xlabel('X 라벨')
plt.ylabel('Y 라벨')
plt.show()


