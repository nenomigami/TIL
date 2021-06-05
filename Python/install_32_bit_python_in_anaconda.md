# Install 32bit python in anaconda
### 잘못된 예
```powershell
set CONDA_FORCE_32BIT=1
conda create -n py38_32 python=3.8
```

### 올바른 예
```powershell
conda create -n py38_32 python=3.8
conda activate py38_32

conda config --env --set subdir win-32
conda install python=3.8
```

### 비트 확인방법
```python
import platform
print(platform.architecture())
```

### terminal에서 파이썬 명령어 바로 실행
```powershell
$ python 
```