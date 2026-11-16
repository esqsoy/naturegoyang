## 핵심 질문

각도와 길이는 어떤 규칙으로 묶여 있을까? 비탈길의 가파름, 사다리가 닿는 높이, 관람차 칸의 높이는 각이 정해지면 길이가 따라 정해진다. 이 규칙을 알면 재기 어려운 길이와 각을 계산하고, 되풀이되는 변화를 식 하나로 적을 수 있다.

## 원리

### 1. 직각삼각형의 삼각비와 역삼각비

#### 직관

같은 비탈길이면 짧게 오르든 길게 오르든 걸은 거리 대 올라간 높이의 비가 같다. 직각삼각형은 한 예각이 정해지면 크기와 상관없이 모양이 정해지기 때문이다. [[f-ratio|#]]의 말로는, 각을 고정할 때 높이는 빗변 길이에 정비례하고 비례 상수는 각마다 정해진다. 다만 이 그림은 각이 0°와 90° 사이일 때만 그려진다.

#### 통상

직각삼각형에서 직각의 맞은편 변(가장 긴 변)을 **빗변**(hypotenuse)이라 한다. 빗변을 $c$, 한 예각 θ의 맞은편 변을 $a$, θ와 이웃한 나머지 변을 $b$라 하면 **삼각비**(三角比, trigonometric ratio)는 다음 세 비이다.

$$\sin\theta=\frac{a}{c},\quad\cos\theta=\frac{b}{c},\quad\tan\theta=\frac{a}{b}$$

각각 **사인**(sine), **코사인**(cosine), **탄젠트**(tangent)라 읽으며 단위가 없다. 아래 그림에서 빗변 $c$와 각 θ를 하나씩 움직여 보면, 세 비는 $c$가 아니라 θ에 따라 바뀐다.

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

**역삼각비**(逆三角比, inverse trigonometric ratio)는 삼각비의 값에서 각을 구하는 계산이다. $\sin\theta=k$인 각을 $\theta=\sin^{-1}k$ 또는 $\arcsin k$로 쓰고, $\cos^{-1}$, $\tan^{-1}$도 같다. 계산기는 각을 하나만 낸다. $\sin^{-1}$과 $\tan^{-1}$은 $-90°$에서 $90°$까지, $\cos^{-1}$은 $0°$에서 $180°$까지의 각을 낸다.

#### 엄밀

한 예각이 같은 직각삼각형끼리는 닮음이라 변의 비가 같고, 그래서 삼각비는 크기와 무관하다. 정의에서 $\tan\theta=\sin\theta/\cos\theta$이고, 피타고라스 정리 $a^2+b^2=c^2$을 $c^2$으로 나누면 $\sin^2\theta+\cos^2\theta=1$이다($\sin^2\theta$는 $\sin\theta$의 제곱). 다른 예각 $90°-\theta$에서는 두 변이 바뀌어 $\sin\theta=\cos(90°-\theta)$이다. 특수각 값은 정삼각형을 반으로 자른 삼각형과 직각이등변삼각형에서 나온다.

$\sin^{-1}k$의 $-1$은 역수가 아니다. $1/\sin\theta$는 2절의 $\csc\theta$이다. 2절처럼 각을 넓히면 삼각비 값이 같은 각이 여럿이므로, 계산기가 낸 각이 문제의 범위에 맞는지 본다. $0°$와 $180°$ 사이에서 $\sin\theta=0.5$인 각은 $30°$와 $150°$인데 계산기는 $30°$만 낸다. 두 벡터 사이의 각처럼 $0°$와 $180°$ 사이의 각은 $\cos^{-1}$이 하나로 정한다([[f-vector|#]]). 함수로서의 정의와 미분은 [[f-hyper|#]].

#### 점검
**Q.** 직각을 낀 두 변이 3.0 cm와 4.0 cm인 직각삼각형에서 3.0 cm 변의 맞은편 각은?
**A.** $\tan\theta=3.0/4.0$이므로 $\theta=\tan^{-1}0.75\approx37°$이다.

### 2. 호도법, 단위원, 삼각함수의 그래프

#### 직관

반지름 1인 원 위를 점이 시계 반대 방향으로 돈다고 하자. 점의 높이는 0에서 1로 올랐다가 −1까지 내려간 뒤 돌아오기를 한 바퀴마다 되풀이한다. 이 높이를 돈 각의 함수로 본 것이 사인, 가로 위치를 본 것이 코사인이다. 단, 높이가 곧 사인 값인 것은 반지름이 1일 때뿐이다.

#### 통상

**호도법**(弧度法, radian measure)은 중심각을 호의 길이 $s$와 반지름 $r$의 비 $\theta=s/r$로 재는 방법이다. 호의 길이가 반지름과 같은 중심각이 1 **라디안**(radian, rad)이다. $180°=\pi$ rad이고 1 rad ≈ 57.3°이다. 미적분에서는 따로 밝히지 않으면 각을 rad로 잰다.

**단위원**(單位圓, unit circle)은 원점이 중심이고 반지름이 1인 원이다. $x$축의 양의 방향을 시계 반대 방향으로 θ만큼 돌린 반직선(시계 방향은 음의 각)이 단위원과 만나는 점을 P$(x,y)$라 할 때, 다음과 같이 정한 함수가 **삼각함수**(三角函數, trigonometric function)이다.

$$\cos\theta=x,\quad\sin\theta=y,\quad\tan\theta=\frac{y}{x}$$

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

**시컨트**(secant)는 $\sec\theta=1/\cos\theta$로 정한 함수이다. **코시컨트**(cosecant)는 $\csc\theta=1/\sin\theta$로 정한 함수이다. **코탄젠트**(cotangent)는 $\cot\theta=\cos\theta/\sin\theta$로 정한 함수이다.

**주기함수**(週期函數, periodic function)는 정의역의 모든 $x$에서 $f(x+p)=f(x)$인 양수 $p$가 있는 함수이다. **주기**(週期, period)는 그런 양수 $p$ 가운데 가장 작은 값이다. 여섯 삼각함수는 모두 주기함수다($n$은 정수).

| 함수 | 정의역에서 빼는 값 | 치역 | 주기 | 대칭 |
|---|---|---|---|---|
| sin | 없음 | $[-1,1]$ | $2\pi$ | 홀함수 |
| cos | 없음 | $[-1,1]$ | $2\pi$ | 짝함수 |
| tan | $\pi/2+n\pi$ | 실수 전체 | $\pi$ | 홀함수 |
| cot | $n\pi$ | 실수 전체 | $\pi$ | 홀함수 |
| sec | $\pi/2+n\pi$ | $y\le-1$ 또는 $y\ge1$ | $2\pi$ | 짝함수 |
| csc | $n\pi$ | $y\le-1$ 또는 $y\ge1$ | $2\pi$ | 홀함수 |

#### 엄밀

$\theta=s/r$은 길이를 길이로 나눈 값이라 rad는 무차원이고([[f-measure|#]]의 차원 분석), $s=r\theta$에서는 m만 남는다. 예각에서는 단위원의 정의가 1절의 삼각비와 같다. θ가 0, $\pi/2$, $\pi$, $3\pi/2$일 때 점 P는 $(1,0)$, $(0,1)$, $(-1,0)$, $(0,-1)$이다. 부호는 사분면이 정한다. 제1사분면에서는 모두 양, 제2사분면에서는 sin만, 제3사분면에서는 tan만, 제4사분면에서는 cos만 양이다.

θ와 $\theta+2\pi$는 같은 점이라 주기가 $2\pi$이고, $\theta+\pi$는 원점 맞은편 점이라 $y/x$가 같아 tan의 주기는 $\pi$이다. $-\theta$의 점은 $(x,-y)$이므로 cos는 짝함수, sin과 tan은 홀함수다. sin과 cos의 그래프는 같은 물결이고 $\cos\theta=\sin(\theta+\pi/2)$라 cos 쪽이 $\pi/2$만큼 왼쪽에 있다. tan과 sec는 $x=0$인 각에서, cot와 csc는 $y=0$인 각에서 정의되지 않고, 그 근처에서 절댓값이 한없이 커진다.

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

**배각 공식**(倍角公式, double-angle formulas)은 덧셈 정리에 $A=B=\theta$를 넣은 항등식이다.

$$\cos2\theta=\cos^2\theta-\sin^2\theta,\quad \sin2\theta=2\sin\theta\cos\theta$$

**반각 공식**(半角公式, half-angle formulas)은 사인과 코사인의 제곱을 두 배 각의 코사인으로 나타내는 항등식이다.

$$\cos^2\theta=\frac{1+\cos2\theta}{2},\quad \sin^2\theta=\frac{1-\cos2\theta}{2}$$

**코사인 법칙**(cosine法則, law of cosines)은 삼각형의 두 변 $a$, $b$와 그 끼인각 θ, 끼인각의 맞은편 변 $c$ 사이의 관계식이다.

$$c^2=a^2+b^2-2ab\cos\theta$$

**성분 분해**(成分分解, resolution into components)는 기울어진 길이를 서로 수직인 두 방향 길이로 나누는 것이다. 길이 $L$인 선분이 수평과 θ를 이루면 수평 길이는 $L\cos\theta$, 수직 길이는 $L\sin\theta$이다. 거꾸로 수평 $x$, 수직 $y$를 알면 $L=\sqrt{x^2+y^2}$, $\tan\theta=y/x$이다.

**진폭**(振幅, amplitude)은 가운데 값에서 가장 멀리 벗어난 크기, 곧 최댓값과 최솟값 차이의 절반이다. 사인 꼴의 되풀이는 다음 일반 사인 함수로 쓴다.

$$f(x)=A\sin\left(\frac{2\pi}{B}(x-C)\right)+D$$

$|A|$는 진폭, $|B|$는 주기, $C$는 가로로 옮긴 양, $D$는 세로로 옮긴 양(가운데 값)이다. 그림은 $C=0$, $D=1$로 두고 $A$와 $B$를 움직인다.

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

첫 항등식을 $\cos^2\theta$, $\sin^2\theta$로 나누면 둘째, 셋째가 된다. 덧셈 정리의 $B$에 $-B$를 넣으면 $\cos(A-B)=\cos A\cos B+\sin A\sin B$, $\sin(A-B)=\sin A\cos B-\cos A\sin B$이다. $\cos^2\theta+\sin^2\theta=1$과 $\cos^2\theta-\sin^2\theta=\cos2\theta$를 더하고 빼면 반각 공식이다. 한국 교과서의 반각 공식은 θ 자리에 $\theta/2$를 쓴 같은 식이다.

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

코사인 법칙은 끼인각의 꼭짓점을 원점에, 변 $b$를 $x$축에 놓고 두 꼭짓점 $(b,0)$과 $(a\cos\theta,\ a\sin\theta)$ 사이 거리의 제곱을 계산하면 나온다. $\theta=\pi/2$이면 피타고라스 정리다. **사인 법칙**(sine法則, law of sines)은 삼각형의 세 각 $A$, $B$, $C$와 각각의 맞은편 변 $a$, $b$, $c$ 사이의 관계식 $\sin A/a=\sin B/b=\sin C/c$이다.

rad로 잰 모든 θ에서 다음 부등식이 성립한다.

$$-|\theta|\le\sin\theta\le|\theta|,\quad -|\theta|\le1-\cos\theta\le|\theta|$$

단위원에서 점 $(1,0)$과 P를 잇는 선분 길이의 제곱 $\sin^2\theta+(1-\cos\theta)^2$이 호의 길이의 제곱 $\theta^2$보다 클 수 없기 때문이다. [[f-limit|#]]의 극한 계산이 이 부등식을 쓴다. 작은 각에서는 $\sin\theta\approx\theta$이고($\sin0.1\approx0.0998$), 이 근사는 rad로 잴 때만 맞다. 성분 분해 식은 θ를 수평에서 잰 꼴이고, 수직에서 재면 sin과 cos가 바뀐다. $\sin kx$의 주기는 $2\pi/|k|$이다.

#### 점검
**Q.** $\cos\theta=-3/5$이고 $\pi/2<\theta<\pi$일 때 $\sin\theta$와 $\tan\theta$는?
**A.** $\sin^2\theta=1-9/25=16/25$이고 제2사분면에서 sin은 양이므로 $\sin\theta=4/5$, $\tan\theta=-4/3$이다.

## 예제

**예제 1. 사다리 길이 나누기**
4.0 m 사다리를 벽에 기대 바닥과 60°가 되게 세웠다.

1. 위 끝의 높이는 $4.0\sin60°=4.0\times\sqrt3/2\approx3.5$ m, 사다리 발에서 벽까지는 $4.0\cos60°=2.0$ m이다.
2. 발을 벽에서 3.0 m로 옮기면 $\cos\theta=3.0/4.0$이므로 $\theta=\cos^{-1}0.75\approx41°$이다.

**예제 2. 관람차의 높이**
관람차가 반지름 20 m, 중심 높이 22 m이고 12분에 한 바퀴 돈다. 맨 아래(2 m)에서 출발한다.

1. $t$분 동안 $2\pi t/12$ rad를 돈다. 맨 아래에서 잰 각이 θ이면 칸은 중심보다 $20\cos\theta$ 낮으므로 $h=22-20\cos(2\pi t/12)$이다. 2분 뒤에는 $22-20\cos(\pi/3)=12$ m이다.
2. $-\cos u=\sin(u-\pi/2)$이므로 $h=20\sin\left(\frac{2\pi}{12}(t-3)\right)+22$이다. 진폭 20 m, 주기 12분이고, 사인 곡선을 오른쪽으로 3, 위로 22만큼 옮긴 것이다.

**예제 3. 삼각형과 항등식**

1. 두 변이 5.0 m, 8.0 m이고 끼인각이 60°이면 $c^2=25+64-2\times5.0\times8.0\times\tfrac12=49$에서 $c=7.0$ m이다.
2. 5.0 m 변의 맞은편 각은 $\cos B=\dfrac{7.0^2+8.0^2-5.0^2}{2\times7.0\times8.0}=\dfrac{88}{112}$에서 $B=\cos^{-1}0.786\approx38°$이다.
3. $\cos\dfrac{7\pi}{12}=\cos\left(\dfrac\pi3+\dfrac\pi4\right)=\dfrac12\cdot\dfrac{\sqrt2}2-\dfrac{\sqrt3}2\cdot\dfrac{\sqrt2}2=\dfrac{\sqrt2-\sqrt6}4\approx-0.259$이다.
4. $0\le\theta\le2\pi$에서 $\sin2\theta=\sin\theta$를 풀면, 배각 공식으로 $\sin\theta(2\cos\theta-1)=0$이므로 $\sin\theta=0$ 또는 $\cos\theta=1/2$이고 $\theta=0,\ \pi/3,\ \pi,\ 5\pi/3,\ 2\pi$이다.

## 흔한 오개념

- **오해:** $\sin(A+B)=\sin A+\sin B$이다. → **사실:** sin은 곱하는 수가 아니라 함수다. $\sin(30°+60°)=1$이지만 $\sin30°+\sin60°\approx1.37$이다.
- **오해:** 진폭은 최댓값과 최솟값의 차이다. → **사실:** 그 차이의 절반이다. 높이가 2~42 m인 관람차의 진폭은 40 m가 아니라 20 m이다.
- **오해:** 계산기에 각의 숫자만 넣으면 된다. → **사실:** 도 모드의 sin 30은 0.5지만 라디안 모드는 30 rad로 읽어 약 −0.988이다.

## 연결

삼각함수의 그래프는 [[f-func]]의 옮기기·늘이기와 짝함수·홀함수를 그대로 쓴다. 수평·수직 나누기와 $\cos^{-1}$로 각 구하기는 [[f-vector]]에서 벡터의 성분과 스칼라곱이 된다. [[f-limit]]은 $\sin\theta$와 θ를 견준 부등식으로 극한을 구하고, [[e-sky]]는 천체의 고도를 각으로 읽으며, [[f-complex]]는 단위원 위의 점을 복소수로 읽는다. 사인 꼴의 되풀이는 [[p-osc|#]]과 [[p-wave|#]]의 기본 식이다.

## 요약

- 삼각비: $\sin\theta=a/c$, $\cos\theta=b/c$, $\tan\theta=a/b$. 역삼각비는 값에서 각을 구하며, 계산기가 낸 각의 범위를 확인한다.
- $180°=\pi$ rad, $s=r\theta$. 단위원에서 $\cos\theta=x$, $\sin\theta=y$, $\tan\theta=y/x$이고 sec, csc, cot는 cos, sin, tan의 역수다.
- sin·cos·sec·csc의 주기는 $2\pi$, tan·cot의 주기는 $\pi$이다. cos와 sec는 짝함수, 나머지는 홀함수다.
- $\sin^2\theta+\cos^2\theta=1$, 덧셈 정리, 배각 공식, 반각 공식, 코사인 법칙 $c^2=a^2+b^2-2ab\cos\theta$.
- 성분 분해: 수평 $L\cos\theta$, 수직 $L\sin\theta$. 일반 사인 함수에서 $|A|$는 진폭, $|B|$는 주기다.
