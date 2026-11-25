## 핵심 질문

각도와 길이는 어떤 규칙으로 묶여 있을까? 비탈길의 가파름, 사다리가 닿는 높이, 관람차 칸의 높이는 각이 정해지면 길이가 따라 정해진다. 이 규칙을 알면 재기 어려운 길이와 각을 계산하고, 되풀이되는 변화를 식 하나로 적을 수 있다.

## 원리

### 1. 직각삼각형의 삼각비와 역삼각함수

#### 직관

같은 비탈길이면 짧게 오르든 길게 오르든 걸은 거리 대 올라간 높이의 비가 같다. 직각삼각형은 한 예각이 정해지면 크기와 상관없이 모양이 정해지기 때문이다. [[f-ratio|#]]의 말로는, 각을 고정할 때 높이는 빗변 길이에 정비례하고 비례 상수는 각마다 정해진다. 다만 이 그림은 각이 0°와 90° 사이일 때만 그려진다.

#### 통상

직각삼각형에서 직각의 맞은편 변(가장 긴 변)을 **빗변**(hypotenuse)이라 한다. 빗변을 $c$, 한 예각 θ의 맞은편 변을 $a$, θ와 이웃한 나머지 변을 $b$라 하면 **삼각비**(三角比, trigonometric ratio)는 다음 세 비이다.

$$\sin\theta=\frac{a}{c},\quad\cos\theta=\frac{b}{c},\quad\tan\theta=\frac{a}{b}$$

$\sin\theta=a/c$를 θ의 **사인**(sine), $\cos\theta=b/c$를 θ의 **코사인**(cosine), $\tan\theta=a/b$를 θ의 **탄젠트**(tangent)라 한다. 세 비는 길이를 길이로 나눈 값이라 단위가 없다. 아래 그림에서 빗변 $c$와 각 θ를 하나씩 움직여 보면 세 비는 θ에만 따라 바뀐다.

```graph
x -0.4 7
y -0.75 4.3
equal
slider th 10 80 30 1 | 각 θ (°)
slider c 1 4 3 0.1 | 빗변 c
par 0.18*c*cos(t) 0.18*c*sin(t) 0 th*pi/180 c4 thin
text 0.32*c*cos(th*pi/360) 0.32*c*sin(th*pi/360) c4 | θ
seg c*cos(th*pi/180)-0.07*c 0 c*cos(th*pi/180)-0.07*c 0.07*c c0 thin
seg c*cos(th*pi/180)-0.07*c 0.07*c c*cos(th*pi/180) 0.07*c c0 thin
seg c*cos(th*pi/180) 0 0 0 c1 bold
text c*cos(th*pi/180)/2 -0.5 c1 | b
seg c*cos(th*pi/180) 0 c*cos(th*pi/180) c*sin(th*pi/180) c2 bold | a
seg c*cos(th*pi/180) c*sin(th*pi/180) 0 0 c0 bold | c
text 5 3.6 c2 | a = {c*sin(th*pi/180)}
text 6.3 3.6 c1 | b = {c*cos(th*pi/180)}
text 5.65 2.8 c2 | sin θ = a/c = {sin(th*pi/180)}
text 5.65 2.25 c1 | cos θ = b/c = {cos(th*pi/180)}
text 5.65 1.7 c3 | tan θ = a/b = {tan(th*pi/180)}
cap $c$를 움직이면 세 변의 길이는 함께 늘고 줄지만 오른쪽 세 비는 그대로이다. θ를 움직여야 비가 바뀐다. 처음 그림은 $\theta=30^\circ$, $c=3$이라 $a=1.5$, $\sin30^\circ=0.5$이다.
```

| θ | sin θ | cos θ | tan θ |
|---|---|---|---|
| 30° | $1/2$ | $\sqrt3/2$ | $\sqrt3/3$ |
| 45° | $\sqrt2/2$ | $\sqrt2/2$ | $1$ |
| 60° | $\sqrt3/2$ | $1/2$ | $\sqrt3$ |

**역삼각함수**(逆三角函數, inverse trigonometric function)는 sin·cos·tan의 값에서 그 값을 갖는 각을 정해진 범위($\sin^{-1}$·$\tan^{-1}$은 $-90°$~$90°$, $\cos^{-1}$은 $0°$~$180°$)에서 하나 골라 짝짓는 함수이다. $-1\le k\le1$일 때 $\sin\theta=k$이고 $-90°\le\theta\le90°$인 각 θ를 $\sin^{-1}k$ 또는 $\arcsin k$로, $\cos\theta=k$이고 $0°\le\theta\le180°$인 각 θ를 $\cos^{-1}k$로 쓴다. $\tan^{-1}k$는 모든 실수 $k$에서 $\tan\theta=k$이고 $-90°<\theta<90°$인 각이다.

계산기 단추가 내는 각이 이것이다. $|k|>1$이면 $\sin^{-1}k$와 $\cos^{-1}k$는 없다. 음의 각과 $90°$보다 큰 각의 sin·cos·tan은 2절에서 단위원으로 정한다.

**올려본각**(올려본角, angle of elevation)은 낮은 곳에서 높은 곳의 목표물을 올려다볼 때 시선이 수평 방향과 이루는 각이다. 수평 거리 $d$에서 꼭대기를 올려본각이 θ이면 꼭대기는 눈높이보다 $h=d\tan\theta$만큼 높다. 두 곳에서 잰 올려본각은 직각삼각형 둘의 식에서 모르는 거리를 지워 쓴다.

#### 엄밀

한 예각이 같은 직각삼각형끼리는 닮음이라 변의 비가 같고, 그래서 삼각비는 크기와 무관하다. 정의에서 $\tan\theta=\sin\theta/\cos\theta$이고, 피타고라스 정리 $a^2+b^2=c^2$을 $c^2$으로 나누면 $\sin^2\theta+\cos^2\theta=1$이다($\sin^2\theta$는 $\sin\theta$의 제곱). 다른 예각 $90°-\theta$에서는 두 변이 바뀌어 $\sin\theta=\cos(90°-\theta)$이다. 특수각 값은 정삼각형을 반으로 자른 삼각형과 직각이등변삼각형에서 나온다.

**경사각**(傾斜角, angle of inclination)은 직선이나 평면이 수평면과 이루는 각이다. 좌표평면의 직선이면 $x$축의 양의 방향에서 시계 반대 방향으로 직선까지 잰 각 θ($0°\le\theta<180°$)를 경사각으로 쓴다. 경사각이 예각인 직선은 오른쪽으로 $b$만큼 갈 때 $a$만큼 오르고 $\tan\theta=a/b$이므로, 직선의 기울기 $\Delta y/\Delta x$([[f-ratio|#]])는 $\tan\theta$이다. 경사각이 둔각이면 기울기는 음수이고, 2절에서 넓힌 tan으로 같은 식이 성립한다($\theta=90°$인 세로 직선은 기울기가 없다).

$\sin^{-1}k$의 $-1$은 역수가 아니다. $1/\sin\theta$는 2절의 $\csc\theta$이다. sin을 $-90°\le\theta\le90°$로, cos를 $0°\le\theta\le180°$로, tan을 $-90°<\theta<90°$로 제한하면 서로 다른 각에 늘 서로 다른 값을 짝지으므로(2절의 그래프) 역함수([[f-sci|#]])가 있다. 그것이 $\sin^{-1}$, $\cos^{-1}$, $\tan^{-1}$이라 이름에 '역'이 붙고, 그래프와 미분은 [[f-hyper|#]].

정해진 범위 밖에도 값이 같은 각이 있으므로 계산기가 낸 각이 문제의 범위에 맞는지 본다. $0°$와 $180°$ 사이에서 $\sin\theta=0.5$인 각은 $30°$와 $150°$인데 계산기는 $30°$만 낸다(나머지를 찾는 규칙은 2절). 두 벡터 사이의 각처럼 $0°$와 $180°$ 사이의 각은 $\cos^{-1}$이 하나로 정한다([[f-vector|#]]).

#### 점검
**Q.** 직각을 낀 두 변이 3.0 cm와 4.0 cm인 직각삼각형에서 3.0 cm 변의 맞은편 각은?
**A.** $\tan\theta=3.0/4.0$이므로 $\theta=\tan^{-1}0.75\approx37°$이다.

### 2. 호도법, 단위원, 삼각함수의 그래프

#### 직관

반지름 1인 원 위를 점이 시계 반대 방향으로 돈다고 하자. 점의 높이는 0에서 1로 올랐다가 −1까지 내려간 뒤 돌아오기를 한 바퀴마다 되풀이한다. 이 높이를 돈 각의 함수로 본 것이 사인, 가로 위치를 본 것이 코사인이다. 단, 높이가 곧 사인 값인 것은 반지름이 1일 때뿐이다.

#### 통상

**호도법**(弧度法, radian measure)은 중심각을 호의 길이 $s$와 반지름 $r$의 비 $\theta=s/r$로 재는 방법이다. 호의 길이가 반지름과 같은 중심각이 1 **라디안**(radian, rad)이다. $180°=\pi$ rad이고 1 rad ≈ 57.3°이다. 미적분에서는 따로 밝히지 않으면 각을 rad로 잰다.

중심각이 θ(rad)인 부채꼴의 넓이는 원의 넓이 $\pi r^2$의 $\dfrac{\theta}{2\pi}$이므로 다음과 같다. 반지름이 1이면 $\tfrac12\theta$이다.

$$A=\frac12r^2\theta\quad(\theta\text{는 rad})$$

**단위원**(單位圓, unit circle)은 원점이 중심이고 반지름이 1인 원이다. $x$축의 양의 방향을 시계 반대 방향으로 θ만큼 돌린 반직선(시계 방향은 음의 각, θ는 rad로 잰 실수)이 단위원과 만나는 점을 P$(x,y)$라 할 때, 다음과 같이 정한 함수가 **삼각함수**(三角函數, trigonometric function)이다.

$$\cos\theta=x,\quad\sin\theta=y,\quad\tan\theta=\frac{y}{x}\ (x\neq0)$$

그림에서 θ를 움직이면 P가 단위원을 돌고, P의 높이 $\sin\theta$가 오른쪽에 θ의 함수로 그려진다.

```graph
x -2.7 8.4
y -1.5 1.5
equal
slider th 0 2*pi 1 0.01 play | 각 θ (rad)
vline pi c0 dot
vline 2*pi c0 dot
f sin(x) from 0 to 2*pi c0 dot thin
par -1.5+cos(t) sin(t) 0 2*pi c0 thin
par -1.5+cos(t) sin(t) 0 th c4 bold
seg 0 0 th 0 c4 bold
seg -1.5 0 -1.5+cos(th) sin(th) c0
seg -1.5 0 -1.5+cos(th) 0 c1 bold
seg -1.5+cos(th) 0 -1.5+cos(th) sin(th) c2 bold
f sin(x) from 0 to th c2
seg th 0 th sin(th) c2 bold
seg -1.5+cos(th) sin(th) th sin(th) c0 dash thin
pt -1.5+cos(th) sin(th) c0 | P
pt th sin(th) c2
text pi -1.32 c0 | π
text 2*pi -1.32 c0 | 2π
text 7.4 1.25 c4 | θ = {th*180/pi}°
text 7.4 0.8 c2 | sin θ = {sin(th)}
text 7.4 0.35 c1 | cos θ = {cos(th)}
cap 주황 세로 길이는 P의 높이 $\sin\theta$, 파랑 가로 길이는 P의 가로 좌표 $\cos\theta$이다(음수이면 아래·왼쪽). 단위원은 그래프 왼쪽에 옮겨 그렸고, 가로 눈금은 그래프의 θ(rad)이다. 보라색 호의 길이와 가로축 위 보라색 선분의 길이가 같다($s=r\theta$, $r=1$).
```

**시컨트**(secant), **코시컨트**(cosecant), **코탄젠트**(cotangent)는 각각 $\cos\theta\neq0$, $\sin\theta\neq0$, $\sin\theta\neq0$인 θ에서 $\sec\theta=1/\cos\theta$, $\csc\theta=1/\sin\theta$, $\cot\theta=\cos\theta/\sin\theta$로 정한 함수이다.

**주기함수**(週期函數, periodic function)는 정의역의 모든 $x$에서 $f(x+p)=f(x)$인 양수 $p$가 있는 함수이다. **주기**(週期, period)는 주기함수 $f$에서 정의역의 모든 $x$에 대하여 $f(x+p)=f(x)$인 양수 $p$ 가운데 가장 작은 값이다(상수함수처럼 가장 작은 값이 없으면 주기를 말하지 않는다). 여섯 삼각함수는 모두 주기함수다($n$은 정수).

| 함수 | 정의역에서 빼는 값 | 치역 | 주기 | 대칭 |
|---|---|---|---|---|
| sin | 없음 | $[-1,1]$ | $2\pi$ | 홀함수 |
| cos | 없음 | $[-1,1]$ | $2\pi$ | 짝함수 |
| tan | $\pi/2+n\pi$ | 실수 전체 | $\pi$ | 홀함수 |
| cot | $n\pi$ | 실수 전체 | $\pi$ | 홀함수 |
| sec | $\pi/2+n\pi$ | $y\le-1$ 또는 $y\ge1$ | $2\pi$ | 짝함수 |
| csc | $n\pi$ | $y\le-1$ 또는 $y\ge1$ | $2\pi$ | 홀함수 |

#### 엄밀

$\theta=s/r$은 길이를 길이로 나눈 값이라 rad는 무차원이고([[f-measure|#]]의 차원 분석), $s=r\theta$에서는 m만 남는다. 예각에서는 단위원의 정의가 1절의 삼각비와 같다. 한국 교과서는 처음 반직선을 시초선(始初線), 돌린 반직선을 동경(動徑)이라 하고, $2\pi$의 정수배만큼 차이 나는 각을 함께 일반각(一般角)으로 나타낸다.

θ가 0, $\pi/2$, $\pi$, $3\pi/2$일 때 점 P는 $(1,0)$, $(0,1)$, $(-1,0)$, $(0,-1)$이다. 부호는 사분면이 정한다. 제1사분면에서는 모두 양, 제2사분면에서는 sin만, 제3사분면에서는 tan만, 제4사분면에서는 cos만 양이다.

제1사분면 밖의 각은 그 점을 제1사분면의 점과 대칭으로 잇는다. $\pi-\alpha$의 점은 $\alpha$의 점을 $y$축에 대하여, $\pi+\alpha$의 점은 원점에 대하여, $-\alpha$의 점은 $x$축에 대하여 대칭이동한 점이다. 그래서 $\sin(\pi-\alpha)=\sin\alpha$, $\cos(\pi-\alpha)=-\cos\alpha$, $\sin(\pi+\alpha)=-\sin\alpha$, $\cos(\pi+\alpha)=-\cos\alpha$이다.

값이 같은 다른 각도 이 대칭으로 찾는다. 한 각 $\theta_0$에서 $\sin\theta=\sin\theta_0$이면 $\theta=\theta_0$ 또는 $\pi-\theta_0$($y$축 대칭), $\cos\theta=\cos\theta_0$이면 $\theta=\pm\theta_0$($x$축 대칭), $\tan\theta=\tan\theta_0$이면 $\theta=\theta_0$ 또는 $\theta_0+\pi$(원점 대칭)이다. 여기에 $2\pi$의 정수배를 더하거나 빼서 문제의 범위에 드는 것을 모두 고른다. rad로 재면 계산기는 $\sin^{-1}$을 $-\frac\pi2$에서 $\frac\pi2$까지, $\cos^{-1}$을 $0$에서 $\pi$까지, $\tan^{-1}$을 $-\frac\pi2$와 $\frac\pi2$ 사이(두 끝은 빼고)에서 낸다.

θ와 $\theta+2\pi$는 같은 점이라 주기가 $2\pi$이고, $\theta+\pi$는 원점 맞은편 점이라 $y/x$가 같아 tan의 주기는 $\pi$이다. 더 작은 양수는 안 된다. $p$만큼 옮겨 같으려면 $\sin(\frac\pi2+p)=\sin\frac\pi2=1$이어야 하는데 그런 양수 $p$는 $2\pi$의 정수배뿐이고, $\tan p=\tan0=0$인 양수 $p$는 $\pi$의 정수배뿐이다.

$-\theta$의 점은 $(x,-y)$이므로 cos는 짝함수, sin과 tan은 홀함수다. sin과 cos의 그래프는 같은 물결이고 $\cos\theta=\sin(\theta+\pi/2)$라 cos 쪽이 $\pi/2$만큼 왼쪽에 있다. tan과 sec는 P의 $x$좌표가 0인 각에서, cot와 csc는 P의 $y$좌표가 0인 각에서 정의되지 않고, 그 근처에서 절댓값이 한없이 커진다.

그림에서 $\cos x$와 그 역수 $\sec x$, 그리고 $\tan x$를 함께 본다. $\cos x=0$인 곳의 세로 점선에 다가가면 두 함수의 절댓값이 한없이 커진다(이런 직선이 수직 점근선이다. 자세히는 [[f-limit|#]]).

```graph
x -4.8 4.8
y -4 4
vline -3*pi/2 c0 dot
vline -pi/2 c0 dot
vline pi/2 c0 dot
vline 3*pi/2 c0 dot
f cos(x) c1 thin
f 1/cos(x) c1 bold
f tan(x) c3
text 0 2.4 c1 | sec x
text -0.6 -2.6 c3 | tan x
cap 가는 파랑이 $\cos x$, 굵은 파랑이 그 역수 $\sec x$, 초록이 $\tan x$이다. 점선 $x=\pm\frac\pi2,\ \pm\frac{3\pi}2$에서 둘 다 정의되지 않는다. $\sec x$의 부호는 늘 $\cos x$와 같고 $\cos x=\pm1$인 곳에서 둘이 만난다. $\tan x$는 $\pi$마다, $\sec x$는 $2\pi$마다 되풀이된다.
```

$\sin x$와 그 역수 $\csc x$, 그리고 $\cot x$도 같은 방식으로 그린다. 이번에는 $\sin x=0$인 $x=n\pi$에 점근선이 온다.

```graph
x -4.8 4.8
y -4 4
vline -pi c0 dot
vline pi c0 dot
f sin(x) c2 thin
f 1/sin(x) c2 bold
f cos(x)/sin(x) c5
text pi/2 2.6 c2 | csc x
text -2.2 2.4 c5 | cot x
cap 가는 주황이 $\sin x$, 굵은 주황이 그 역수 $\csc x$, 빨강이 $\cot x$이다. 점선 $x=\pm\pi$와 세로축 $x=0$에서 둘 다 정의되지 않는다. $\csc x$는 $\sin x=\pm1$인 곳에서 $\sin x$와 만나고, $\cot x$는 $\pi$마다 되풀이되며 각 가지에서 $\tan x$와 반대로 줄어든다.
```

#### 점검
**Q.** $\theta=5\pi/6$일 때 $\sin\theta$, $\cos\theta$, $\sec\theta$의 값은?
**A.** 점 P가 $\pi/6$의 점을 $y$축에 대하여 대칭이동한 $(-\sqrt3/2,\ 1/2)$이므로 $\sin\theta=1/2$, $\cos\theta=-\sqrt3/2$, $\sec\theta=-2/\sqrt3$이다.

### 3. 항등식, 성분 분해, 주기적 변화

#### 직관

벽에 기댄 사다리를 위에서 비추면 바닥의 그림자가 수평 길이, 옆에서 비추면 벽의 그림자가 수직 길이다. 두 그림자는 한 사다리에서 나와 서로 묶여 있고, 그 묶임을 적은 것이 항등식이다. 관람차 칸의 높이는 2절의 물결을 옮기고 늘인 꼴이다.

#### 통상

**항등식**(恒等式, identity)은 양변이 정의되는 모든 값에서 성립하는 등식이다.

$$\sin^2\theta+\cos^2\theta=1,\quad 1+\tan^2\theta=\sec^2\theta,\quad 1+\cot^2\theta=\csc^2\theta$$

**덧셈 정리**(덧셈定理, addition formulas)는 두 각의 합의 삼각함수를 각각의 삼각함수로 나타내는 항등식이다.

$$\cos(A+B)=\cos A\cos B-\sin A\sin B,\quad \sin(A+B)=\sin A\cos B+\cos A\sin B$$

**배각 공식**(倍角公式, double-angle formulas)은 덧셈 정리에 $A=B=\theta$를 넣은 항등식 $\cos2\theta=\cos^2\theta-\sin^2\theta$, $\sin2\theta=2\sin\theta\cos\theta$이다. $\sin^2\theta+\cos^2\theta=1$로 바꾸면 $\cos2\theta=2\cos^2\theta-1=1-2\sin^2\theta$로도 쓴다.

**반각 공식**(半角公式, half-angle formulas)은 사인과 코사인의 제곱을 두 배 각의 코사인으로 나타낸 항등식 $\cos^2\theta=\dfrac{1+\cos2\theta}{2}$, $\sin^2\theta=\dfrac{1-\cos2\theta}{2}$이다. 위의 두 꼴을 $\cos^2\theta$, $\sin^2\theta$에 대해 풀면 나온다.

**코사인 법칙**(cosine法則, law of cosines)은 삼각형의 두 변 $a$, $b$와 그 끼인각 θ, 끼인각의 맞은편 변 $c$ 사이의 관계식 $c^2=a^2+b^2-2ab\cos\theta$이다.

**성분 분해**(成分分解, resolution into components)는 기울어진 길이를 서로 수직인 두 방향 길이로 나누는 것이다. 길이 $L$인 선분이 수평과 θ를 이루면 수평 길이는 $L\cos\theta$, 수직 길이는 $L\sin\theta$이다. 거꾸로 수평 $x$, 수직 $y$를 알면 $L=\sqrt{x^2+y^2}$, $\tan\theta=y/x$이다.

**진폭**(振幅, amplitude)은 사인 꼴처럼 가운데 값을 사이에 두고 위아래로 같은 만큼 오르내리는 되풀이에서, 가운데 값에서 가장 멀리 벗어난 크기이다. 이때 진폭은 최댓값과 최솟값 차이의 절반과 같다. 사인 꼴의 되풀이는 다음 일반 사인 함수로 쓴다.

$$f(x)=A\sin\left(\frac{2\pi}{B}(x-C)\right)+D$$

$|A|$는 진폭, $|B|$는 주기, $C$는 가로로 옮긴 양, $D$는 세로로 옮긴 양(가운데 값)이다. 이 식은 $\sin x$의 그래프에 [[f-func|#]]의 변환을 차례로 한 것이다($B>0$일 때). 가로로 $B/2\pi$배 늘이고, 오른쪽으로 $C$만큼 옮기고($C<0$이면 왼쪽으로 $|C|$), 세로로 $|A|$배 늘이되 $A<0$이면 위아래를 뒤집고, 위로 $D$만큼 옮긴다. 안이 $\sin(kx-c)$처럼 묶여 있지 않으면 $\sin\!\left(k\left(x-\frac ck\right)\right)$로 묶어 $B=2\pi/k$, $C=c/k$를 읽는다($k>0$).

시간 $t$의 되풀이는 주기를 $T$, 가운데 값을 $y_0$로 써서 $y=y_0+A\sin\frac{2\pi t}{T}$로 많이 쓴다. 일반 사인 함수에서 $B=T$, $C=0$, $D=y_0$인 꼴이다. $\frac{2\pi}{T}$를 $\omega$로 써서 $y=y_0+A\sin\omega t$로도 쓰고, $\omega$를 각진동수(angular frequency)라 한다(자세히는 [[p-osc|#]]). 그림은 $C=0$, $D=1$로 두고 $A$와 $B$를 움직인다.

```graph
x 0 12.5
y -3 5
slider A 0.5 3 2 0.1 | 진폭 A
slider B 2 12 6 0.5 | 주기 B
hline 1+A c0 dot
hline 1-A c0 dot
hline 1 c0
f A*sin(2*pi/B*x)+1 c2
seg B/4 1 B/4 1+A c0 bold
seg 0 0.4-A B 0.4-A c4 bold
seg B 1 B 0.4-A c4 dash thin
pt 0 1 c4
pt B 1 c4
text 3 4.35 c0 | 진폭 |A| = {A}
text 9.2 4.35 c4 | 주기 |B| = {B}
cap 위아래 점선은 최댓값 $1+A$와 최솟값 $1-A$이고, 진폭(회색 굵은 선)은 그 사이 거리의 절반이다. $A$를 바꾸면 물결의 높이만, $B$를 바꾸면 한 번 되풀이하는 가로 길이(보라)만 바뀐다. 가운데 값 $D=1$은 그대로이다.
```

#### 엄밀

첫 항등식을 $\cos^2\theta$, $\sin^2\theta$로 나누면($\cos\theta\neq0$, $\sin\theta\neq0$인 θ에서) 둘째, 셋째가 된다. 덧셈 정리의 $B$에 $-B$를 넣으면 2절의 짝함수·홀함수 성질로 $\cos(A-B)=\cos A\cos B+\sin A\sin B$, $\sin(A-B)=\sin A\cos B-\cos A\sin B$이다. $\cos^2\theta+\sin^2\theta=1$과 $\cos^2\theta-\sin^2\theta=\cos2\theta$를 더하고 빼서 2로 나누면 반각 공식이다. θ 대신 $\theta/2$를 넣으면 $\sin^2\frac\theta2=\frac{1-\cos\theta}2$, $\cos^2\frac\theta2=\frac{1+\cos\theta}2$이고, 한국 교과서는 이 꼴을 반각 공식이라 한다.

항등식을 보일 때는 한쪽 변을 아는 항등식으로 바꿔 다른 쪽 변이 되게 하거나, 양변을 따로 정리해 같은 식이 됨을 보인다. 식에 분모가 있으면 그 분모가 0이 아닌 값에서만 성립한다고 밝힌다.

그래프로 보면 $\cos^2\theta$와 $\sin^2\theta$는 가운데 값 $\tfrac12$에서 $\tfrac12\cos2\theta$만큼씩 서로 반대쪽으로 벗어나는 물결이다.

```graph
x 0 6.6
y -1.3 1.35
hline 0.5 c0 dot
f cos(2*x) c0 dash thin
f cos(x)^2+sin(x)^2 c3 | cos²θ+sin²θ = 1
f cos(x)^2 c1 bold
f sin(x)^2 c2 bold
text pi 1.12 c1 | cos²θ
text pi/2 1.12 c2 | sin²θ
text 3*pi/2 -1.24 c0 | cos 2θ
cap 회색 파선이 $\cos2\theta$이다. $\cos^2\theta$(파랑)는 그것을 절반으로 줄여 $\tfrac12$만큼 올린 것이고, $\sin^2\theta$(주황)는 $\tfrac12$을 사이에 두고 그 반대쪽에 있다. 그래서 둘의 합(초록)은 어디서나 1이다. 가로축은 θ(rad)이다.
```

$\cos^2\theta$의 그래프 모양을 먼저 짐작해 보고 거기서 반각 공식에 닿는 과정을 영상으로 한 번 더 보고 넘어가자.

```link
url https://www.youtube.com/watch?v=yBw67Fb31Cs
title Trigonometry fundamentals | Ep. 2 Lockdown live math
kind 영상
who 3Blue1Brown
min 73
note 한국어 자막
why 라이브 강의라 길다. 앞쪽에서 $\cos^2\theta$의 그래프를 그려 놓고, $\cos\theta$의 그래프를 옮기고 줄이고 주기를 절반으로 하면 겹친다는 것에서 $\cos^2\theta=\frac{1+\cos2\theta}2$에 닿는다. 위 그림의 생각이다. 그 뒤 단위원으로 삼각함수를 정의하는 대목은 2절을 다시 보는 것이다.
```

코사인 법칙은 끼인각의 꼭짓점을 원점에, 변 $b$를 $x$축에 놓고 두 꼭짓점 $(b,0)$과 $(a\cos\theta,\ a\sin\theta)$ 사이 거리의 제곱을 계산하면 나온다. $\theta=\pi/2$이면 피타고라스 정리다. 코사인 법칙을 $\cos\theta$에 대해 풀면 $\cos\theta=\dfrac{a^2+b^2-c^2}{2ab}$이라 세 변에서 각을 구한다.

**사인 법칙**(sine法則, law of sines)은 삼각형의 세 각 $A$, $B$, $C$와 각각의 맞은편 변 $a$, $b$, $c$ 사이의 관계식 $\sin A/a=\sin B/b=\sin C/c$이다. 사인 법칙으로 각을 구할 때는 둔각을 놓칠 수 있다. $\sin A=k$이면 삼각형의 각 $A$는 $\sin^{-1}k$일 수도 $180°-\sin^{-1}k$일 수도 있는데, $\sin^{-1}$은 $0<k\le1$에서 $90°$ 이하의 각만 내기 때문이다. 둔각은 가장 긴 변의 맞은편에만 올 수 있으므로, 그 각은 코사인 법칙으로 $\cos$ 값을 얻어 $\cos^{-1}$로 구한다. 삼각형의 각은 $0°$와 $180°$ 사이라 $\cos^{-1}$이 하나로 정한다.

rad로 잰 모든 θ에서 다음 부등식이 성립한다.

$$-|\theta|\le\sin\theta\le|\theta|,\quad -|\theta|\le1-\cos\theta\le|\theta|$$

단위원에서 점 $(1,0)$과 P를 잇는 선분 길이의 제곱 $\sin^2\theta+(1-\cos\theta)^2$이 호의 길이의 제곱 $\theta^2$보다 클 수 없다. 두 항은 모두 0 이상이므로 각각도 $\theta^2$ 이하이고, 제곱근을 취하면 $|\sin\theta|\le|\theta|$, $|1-\cos\theta|\le|\theta|$이다. [[f-limit|#]]의 극한 계산이 이 부등식을 쓴다.

작은 각에서는 $\sin\theta\approx\theta$이고($\sin0.1\approx0.0998$), 이 근사는 rad로 잴 때만 맞다. θ가 0에 가까우면 $\cos\theta$도 1에 가까우므로 $\tan\theta=\sin\theta/\cos\theta\approx\theta$이기도 하다($\tan0.1\approx0.1003$). 성분 분해 식은 θ를 수평에서 잰 꼴이고, 수직에서 재면 sin과 cos가 바뀐다.

주기가 $p$인 함수 $f$에서 $f(kx)$($k\neq0$)의 주기는 $p/|k|$이다. $x$가 $p/|k|$만큼 늘면 안의 값 $kx$가 $p$ 또는 $-p$만큼 바뀌기 때문이다(더 작은 $q$에서 되풀이되면 $f$가 $|k|q<p$마다 되풀이되어 어긋난다). 그래서 $\sin kx$, $\cos kx$, $\sec kx$, $\csc kx$의 주기는 $2\pi/|k|$, $\tan kx$와 $\cot kx$의 주기는 $\pi/|k|$이다. 주기가 $p$, $q$인 두 함수의 합은 $p$와 $q$의 공배수만큼 옮기면 같은 값이 된다($\sin x+\cos\frac x2$는 $4\pi$마다 되풀이된다).

#### 점검
**Q.** $\sin15°$를 덧셈 정리로 구하고, $y=3\sin\left(\frac\pi2(x-1)\right)+2$의 진폭·주기·최댓값을 말하라.
**A.** $\sin15°=\sin(45°-30°)=\frac{\sqrt2}2\cdot\frac{\sqrt3}2-\frac{\sqrt2}2\cdot\frac12=\frac{\sqrt6-\sqrt2}4\approx0.259$이다. $\frac{2\pi}{B}=\frac\pi2$에서 주기 $B=4$이고, 진폭은 3, 최댓값은 $2+3=5$이다.

## 예제

**예제 1. 사다리 길이 나누기** {목표 1}
4.0 m 사다리를 벽에 기대 바닥과 60°가 되게 세웠다.

1. 위 끝의 높이는 $4.0\sin60°=4.0\times\sqrt3/2\approx3.5$ m, 사다리 발에서 벽까지는 $4.0\cos60°=2.0$ m이다.
2. 발을 벽에서 3.0 m로 옮기면 $\cos\theta=3.0/4.0$이므로 $\theta=\cos^{-1}0.75\approx41°$이다.

**예제 2. 두 곳에서 잰 올려본각** {목표 1}
탑을 향해 20 m 다가가자 꼭대기를 올려본각이 30°에서 45°가 되었다(눈높이는 무시한다).

1. 가까운 곳에서 탑 밑까지를 $x$, 탑의 높이를 $h$라 하면 두 직각삼각형에서 $h=x\tan45°$, $h=(x+20)\tan30°$이다.
2. 두 식에서 $h$를 지우면 $x=(x+20)/\sqrt3$이므로 $x=20/(\sqrt3-1)\approx27.3$ m이고, $h=x\tan45°\approx27.3$ m이다.

**예제 3. 부채꼴의 호와 넓이** {목표 2}
반지름 5.0 cm, 중심각 72°인 부채꼴의 호의 길이와 넓이를 구한다.

1. 먼저 rad로 바꾼다. $\theta=72\times\pi/180=2\pi/5$ rad이다.
2. 호의 길이는 $s=r\theta=5.0\times2\pi/5\approx6.3$ cm, 넓이는 $A=\tfrac12r^2\theta=\tfrac12\times5.0^2\times2\pi/5\approx15.7\ \mathrm{cm^2}$이다.
3. θ에 72를 그대로 넣으면 넓이가 $\tfrac12\times25\times72=900$이 되어 틀린다.

**예제 4. 대칭으로 값과 각 찾기** {목표 2}

1. $7\pi/6=\pi+\pi/6$의 점은 $\pi/6$의 점을 원점에 대하여 대칭이동한 점이므로 $\sin\frac{7\pi}6=-\frac12$, $\cos\frac{7\pi}6=-\frac{\sqrt3}2$이다.
2. $-3\pi/4$에 $2\pi$를 더하면 $5\pi/4=\pi+\pi/4$이므로 그 점은 $\left(-\frac{\sqrt2}2,-\frac{\sqrt2}2\right)$이고 $\tan\left(-\frac{3\pi}4\right)=1$이다.
3. $0\le\theta<2\pi$에서 $\tan\theta=-2$를 풀면, 계산기는 범위 밖의 $\tan^{-1}(-2)\approx-1.107$을 낸다. 여기에 $\pi$를 더한 $2.034$와 $2\pi$를 더한 $5.176$이 범위 안의 해이다.

**예제 5. 관람차의 높이** {목표 3}
관람차가 반지름 20 m, 중심 높이 22 m이고 12분에 한 바퀴 돈다. 맨 아래(2 m)에서 출발한다.

1. $t$분 동안 $2\pi t/12$ rad를 돈다. 맨 아래에서 잰 각이 θ이면 칸은 중심보다 $20\cos\theta$ 낮으므로 $h=22-20\cos(2\pi t/12)$이다. 2분 뒤에는 $22-20\cos(\pi/3)=12$ m이다.
2. $-\cos u=\sin(u-\pi/2)$이므로 $h=20\sin\left(\frac{2\pi}{12}(t-3)\right)+22$이다. 진폭 20 m, 주기 12분이고, 사인 곡선을 오른쪽으로 3, 위로 22만큼 옮긴 것이다.

**예제 6. 코사인 법칙으로 변과 각** {목표 3}

1. 두 변이 5.0 m, 8.0 m이고 끼인각이 60°이면 $c^2=25+64-2\times5.0\times8.0\times\tfrac12=49$에서 $c=7.0$ m이다.
2. 5.0 m 변의 맞은편 각 $B$는 코사인 법칙을 각에 대해 푼 꼴에서 5.0 m를 맞은편 변 자리에 넣어 $\cos B=\dfrac{7.0^2+8.0^2-5.0^2}{2\times7.0\times8.0}=\dfrac{88}{112}$이고, $B=\cos^{-1}0.786\approx38°$이다.

**예제 7. 항등식과 삼각방정식** {목표 3}

1. $\cos\theta=-3/5$이고 $\pi/2<\theta<\pi$이면 $\sin^2\theta=1-9/25=16/25$이고 제2사분면에서 sin은 양이므로 $\sin\theta=4/5$, $\tan\theta=-4/3$이다.
2. $\cos\dfrac{7\pi}{12}=\cos\left(\dfrac\pi3+\dfrac\pi4\right)=\dfrac12\cdot\dfrac{\sqrt2}2-\dfrac{\sqrt3}2\cdot\dfrac{\sqrt2}2=\dfrac{\sqrt2-\sqrt6}4\approx-0.259$이다.
3. $\dfrac1{1-\sin\theta}+\dfrac1{1+\sin\theta}=2\sec^2\theta$를 보이려면 왼쪽 변을 통분한다. $\dfrac{(1+\sin\theta)+(1-\sin\theta)}{1-\sin^2\theta}=\dfrac2{\cos^2\theta}=2\sec^2\theta$이고, 분모가 0이 아닌 $\sin\theta\neq\pm1$에서 성립한다.
4. $0\le\theta\le2\pi$에서 $\sin2\theta=\sin\theta$를 풀면, 배각 공식으로 $\sin\theta(2\cos\theta-1)=0$이므로 $\sin\theta=0$ 또는 $\cos\theta=1/2$이다. $\sin\theta=0$에서 $\theta=0,\ \pi,\ 2\pi$이고, $\cos\theta=\frac12$에서 $\theta=\frac\pi3$과 $-\frac\pi3+2\pi=\frac{5\pi}3$이다(2절의 $\pm\theta_0$에 $2\pi$의 정수배를 더함).

## 흔한 오개념

- **오해:** $\sin(A+B)=\sin A+\sin B$이다. → **사실:** sin은 곱하는 수가 아니라 함수다. $\sin(30°+60°)=1$이지만 $\sin30°+\sin60°\approx1.37$이다.
- **오해:** 진폭은 최댓값과 최솟값의 차이다. → **사실:** 그 차이의 절반이다. 높이가 2~42 m인 관람차의 진폭은 40 m가 아니라 20 m이다.
- **오해:** 계산기에 각의 숫자만 넣으면 된다. → **사실:** 도 모드의 sin 30은 0.5지만 라디안 모드는 30 rad로 읽어 약 −0.988이다.

## 연결

삼각함수의 그래프는 [[f-func]]의 옮기기·늘이기와 짝함수·홀함수를 그대로 쓴다. 수평·수직 나누기와 $\cos^{-1}$로 각 구하기는 [[f-vector]]에서 벡터의 성분과 스칼라곱이 된다. [[f-limit]]은 $\sin\theta$와 θ를 견준 부등식으로 극한을 구하고, [[e-sky]]는 천체의 고도를 각으로 읽으며, [[f-complex]]는 단위원 위의 점을 복소수로 읽는다. 사인 꼴의 되풀이는 [[p-osc|#]]과 [[p-wave|#]]의 기본 식이다.

## 요약

- 삼각비: $\sin\theta=a/c$, $\cos\theta=b/c$, $\tan\theta=a/b$. 역삼각함수는 정해진 범위의 각 하나를 내므로($\sin^{-1}$은 $-90°$~$90°$, $\cos^{-1}$은 $0°$~$180°$, $\tan^{-1}$은 두 끝을 뺀 $-90°$~$90°$), 문제의 범위에 드는 다른 각은 단위원의 대칭으로 찾는다.
- $180°=\pi$ rad, $s=r\theta$, 부채꼴 넓이 $\tfrac12r^2\theta$. 단위원에서 $\cos\theta=x$, $\sin\theta=y$, $\tan\theta=y/x$이고 sec, csc, cot는 cos, sin, tan의 역수다.
- sin·cos·sec·csc의 주기는 $2\pi$, tan·cot의 주기는 $\pi$이다. $f(kx)$의 주기는 $p/|k|$이다. cos와 sec는 짝함수, 나머지는 홀함수다.
- $\sin^2\theta+\cos^2\theta=1$, 덧셈 정리, 배각 공식, 반각 공식, 코사인 법칙 $c^2=a^2+b^2-2ab\cos\theta$. 사인 법칙으로 각을 구할 때는 둔각을 놓치지 않는다.
- 성분 분해: 수평 $L\cos\theta$, 수직 $L\sin\theta$. 일반 사인 함수에서 $|A|$는 진폭, $|B|$는 주기다.
